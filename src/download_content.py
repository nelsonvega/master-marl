"""
Read every *.txt file in outputs/, dedupe URLs across them, and download
fetchable content into downloads/<domain>/.

Resumable: re-runs read outputs/download_manifest.jsonl AND verify the
downloaded file still exists on disk before skipping. URLs missing from
disk are re-fetched even if the manifest says "ok".

Logs go to BOTH stdout (INFO+) and outputs/logs/download_<UTC>.log (DEBUG+).
The file log is the audit trail; stdout is the human view.

Usage:
    python src/download_content.py                  # full run
    python src/download_content.py --limit 50       # smoke test
    python src/download_content.py --domains arxiv.org github.com
    python src/download_content.py --workers 8 --timeout 20
    python src/download_content.py --retry-failed   # re-attempt prior failures
    python src/download_content.py --verbose        # per-URL stdout
    python src/download_content.py --refetch        # ignore manifest, redo all

Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import mimetypes
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

OUTPUTS = Path("outputs")
DOWNLOADS = Path("downloads")
LOGDIR = OUTPUTS / "logs"
MANIFEST = OUTPUTS / "download_manifest.jsonl"
STOP_FILE = Path("STOP")

USER_AGENT = (
    "Mozilla/5.0 (compatible; master-marl-research-fetcher/1.0; "
    "+https://github.com/nelsonvega/master-marl)"
)
DEFAULT_TIMEOUT = 25
MAX_BYTES = 25 * 1024 * 1024
DEFAULT_WORKERS = 32
DEFAULT_DOMAIN_DELAY = 0.75
ARXIV_DOMAIN_DELAY = 1.5
YOUTUBE_DOMAIN_DELAY = 2.0
DEFAULT_VIDEO_MAX_MB = 200

# Runtime-overridable copies (CLI flags mutate these)
_domain_delays = {
    "default": DEFAULT_DOMAIN_DELAY,
    "arxiv":   ARXIV_DOMAIN_DELAY,
    "youtube": YOUTUBE_DOMAIN_DELAY,
}
SKIP_EXTS = {".mov", ".avi", ".mkv", ".iso", ".dmg", ".exe"}  # mp4 stays -- some legit non-YT mp4s
URL_RE = re.compile(r"https?://[^\s)\]>\"'\\]+")
YOUTUBE_HOSTS = ("youtube.com", "youtu.be", "m.youtube.com", "music.youtube.com")

log = logging.getLogger("downloader")
_stop_event = threading.Event()
_active_procs: set[subprocess.Popen] = set()
_active_procs_lock = threading.Lock()


def setup_logging(verbose: bool) -> Path:
    LOGDIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    logfile = LOGDIR / f"download_{stamp}.log"

    log.setLevel(logging.DEBUG)
    log.handlers.clear()

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)-7s [%(threadName)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    ))
    log.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG if verbose else logging.INFO)
    sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s",
                                       datefmt="%H:%M:%S"))
    log.addHandler(sh)
    return logfile


def collect_urls() -> list[str]:
    urls: set[str] = set()
    if not OUTPUTS.exists():
        return []
    files = sorted(OUTPUTS.glob("*.txt"))
    for path in files:
        before = len(urls)
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith(("http://", "https://")):
                    urls.add(line)
                else:
                    for m in URL_RE.findall(line):
                        urls.add(m.rstrip(".,;:#\\"))
        log.info("Read %s: %d new unique URLs (running total %d)",
                 path.name, len(urls) - before, len(urls))
    return sorted(urls)


def safe_filename(url: str, content_type: str | None = None) -> Path:
    """Return a flat filename: <netloc>-<stem>_<hash><ext> (no subdirectory)."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace(":", "_") or "unknown"
    stem = unquote(parsed.path.strip("/")).replace("/", "_") or "index"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem)[:110]
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]

    ext = ""
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip().lower()) or ""
    if not ext:
        url_ext = os.path.splitext(parsed.path)[1].lower()
        if url_ext and len(url_ext) <= 6:
            ext = url_ext
    if not ext:
        ext = ".html"
    return Path(f"{domain}-{stem}_{digest}{ext}")


def migrate_flat_layout() -> None:
    """One-shot: move downloads/<domain>/<file> -> downloads/<domain>-<file>
    and rewrite manifest entries so resume still works."""
    if not DOWNLOADS.exists():
        return
    rename_map: dict[str, str] = {}  # old relative -> new relative (forward-slash)
    moved = 0
    skipped = 0
    for sub in list(DOWNLOADS.iterdir()):
        if not sub.is_dir():
            continue
        for f in list(sub.iterdir()):
            if not f.is_file():
                continue
            old_rel = f"{sub.name}/{f.name}"
            new_name = f"{sub.name}-{f.name}"
            new_path = DOWNLOADS / new_name
            if new_path.exists():
                skipped += 1
                continue
            try:
                f.rename(new_path)
                rename_map[old_rel] = new_name
                moved += 1
            except OSError as e:
                log.warning("migrate: failed to move %s: %s", old_rel, e)
        try:
            sub.rmdir()
        except OSError:
            pass
    if not moved and not skipped:
        return
    log.info("migrate: flattened %d files (%d already-existing skipped) "
             "into downloads/ root", moved, skipped)
    if MANIFEST.exists() and rename_map:
        out_lines: list[str] = []
        rewrites = 0
        with MANIFEST.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.rstrip("\n")
                if not stripped.strip():
                    continue
                try:
                    rec = json.loads(stripped)
                except json.JSONDecodeError:
                    out_lines.append(stripped)
                    continue
                changed = False
                for key in ("path", "transcript_path"):
                    if rec.get(key) in rename_map:
                        rec[key] = rename_map[rec[key]]
                        changed = True
                if changed:
                    rewrites += 1
                out_lines.append(json.dumps(rec))
        MANIFEST.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        log.info("migrate: rewrote %d manifest entries", rewrites)


_domain_locks: dict[str, threading.Lock] = defaultdict(threading.Lock)
_last_call: dict[str, float] = {}


def polite_wait(domain: str) -> float:
    if "arxiv" in domain:
        delay = _domain_delays["arxiv"]
    elif any(h in domain for h in YOUTUBE_HOSTS):
        delay = _domain_delays["youtube"]
    else:
        delay = _domain_delays["default"]
    with _domain_locks[domain]:
        now = time.time()
        prev = _last_call.get(domain, 0.0)
        wait = (prev + delay) - now
        if wait > 0:
            time.sleep(wait)
        _last_call[domain] = time.time()
    return max(wait, 0.0)


def interleave_by_domain(urls: list[str]) -> list[str]:
    """Round-robin URLs across domains so the executor naturally spreads
    across hosts instead of stalling on per-domain rate limits."""
    by_domain: dict[str, list[str]] = defaultdict(list)
    for u in urls:
        by_domain[urlparse(u).netloc.lower()].append(u)
    queues = list(by_domain.values())
    out: list[str] = []
    while queues:
        next_queues = []
        for q in queues:
            out.append(q.pop(0))
            if q:
                next_queues.append(q)
        queues = next_queues
    return out


def stop_requested() -> bool:
    if _stop_event.is_set():
        return True
    if STOP_FILE.exists():
        if not _stop_event.is_set():
            log.warning("STOP file detected at %s -- halting new work",
                        STOP_FILE.resolve())
        _stop_event.set()
        return True
    return False


def is_youtube(url: str) -> bool:
    netloc = urlparse(url).netloc.lower()
    return any(h in netloc for h in YOUTUBE_HOSTS)


def youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    if "youtu.be" in netloc:
        vid = parsed.path.strip("/").split("/")[0]
        return vid or None
    if "youtube.com" in netloc:
        if parsed.path.startswith(("/shorts/", "/embed/", "/v/")):
            return parsed.path.split("/")[2] if len(parsed.path.split("/")) > 2 else None
        qs = parse_qs(parsed.query)
        v = qs.get("v")
        return v[0] if v else None
    return None


def vtt_to_text(vtt_path: Path) -> str:
    """Best-effort VTT/SRT → plain text. Dedupes adjacent lines (YouTube auto-subs roll)."""
    out: list[str] = []
    last = ""
    try:
        raw = vtt_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if s == "WEBVTT" or s.startswith(("NOTE", "Kind:", "Language:", "STYLE")):
            continue
        if "-->" in s:
            continue
        if s.isdigit():
            continue
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"&nbsp;", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        if not s or s == last:
            continue
        out.append(s)
        last = s
    return "\n".join(out)


def _run_yt_dlp(args: list[str], timeout: int) -> tuple[int, str]:
    """Run yt-dlp, return (returncode, combined stdout/stderr)."""
    try:
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        with _active_procs_lock:
            _active_procs.add(proc)
        try:
            stdout, _ = proc.communicate(timeout=timeout)
            return proc.returncode, stdout or ""
        finally:
            with _active_procs_lock:
                _active_procs.discard(proc)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.communicate()
        except Exception:
            pass
        return 124, "TIMEOUT"
    except Exception as e:  # noqa: BLE001
        return 1, f"{type(e).__name__}: {e}"


def fetch_youtube(url: str, video_max_mb: int, timeout: int,
                  cookies_from_browser: str | None = None,
                  cookies_file: str | None = None) -> dict:
    """Two-pass yt-dlp: subs-only first (high success), video best-effort.
    Returns ok if EITHER subs or video succeed; transcript_source records which.

    YouTube's anti-bot blocks unauthenticated video streams (HTTP 403); pass
    `cookies_from_browser` (e.g. "firefox", "chrome") to use your logged-in
    session, which bypasses the gate."""
    yt_dlp = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    if not yt_dlp:
        log.error("yt-dlp not found on PATH -- cannot fetch %s", url)
        return {"url": url, "status": "error", "is_youtube": True,
                "error": "yt-dlp not installed"}

    vid = youtube_video_id(url)
    if not vid:
        log.warning("YT could not parse video id: %s", url)
        return {"url": url, "status": "error", "is_youtube": True,
                "error": "could not parse video id"}

    polite_wait("youtube.com")
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    yt_template = "youtube.com-%(id)s.%(ext)s"
    cookie_args: list[str] = []
    if cookies_file:
        cookie_args = ["--cookies", cookies_file]
    elif cookies_from_browser:
        cookie_args = ["--cookies-from-browser", cookies_from_browser]

    # Pass 1: subs only -- almost always succeeds even when video is gated
    sub_cmd = [
        yt_dlp, url,
        "--skip-download",
        "--write-auto-subs", "--write-subs",
        "--sub-langs", "en.*,en",
        "--convert-subs", "vtt",
        "--no-playlist", "--no-warnings", "--no-progress",
        "--restrict-filenames",
        "--retries", "2",
        "--socket-timeout", str(timeout),
        "-o", yt_template,
        "--paths", str(DOWNLOADS),
        "--extractor-args", "youtube:player_client=tv,web,android",
        *cookie_args,
    ]
    log.debug("YT subs cmd: %s", " ".join(sub_cmd))
    sub_rc, sub_out = _run_yt_dlp(sub_cmd, timeout=timeout * 6)
    if sub_rc != 0:
        log.debug("YT subs pass rc=%d tail=%s", sub_rc,
                  "\n  ".join(sub_out.splitlines()[-3:]))

    # Pass 2: video best-effort. Without authenticated cookies, anti-bot
    # currently 403s every public client. We try anyway with TLS
    # impersonation and multi-client fallback -- any of these may work
    # later as YouTube's anti-bot rules shift.
    video_cmd = [
        yt_dlp, url,
        "-f", "best[height<=360]/best[height<=480]/best",
        "--max-filesize", f"{video_max_mb}M",
        "--no-playlist", "--no-warnings", "--no-progress",
        "--restrict-filenames",
        "--retries", "2",
        "--socket-timeout", str(timeout),
        "--impersonate", "chrome",
        "-o", yt_template,
        "--paths", str(DOWNLOADS),
        "--extractor-args", "youtube:player_client=tv,web,android,ios,mweb",
        *cookie_args,
    ]
    log.debug("YT video cmd: %s", " ".join(video_cmd))
    vid_rc, vid_out = _run_yt_dlp(video_cmd, timeout=timeout * 20)
    if vid_rc != 0:
        log.debug("YT video pass rc=%d tail=%s", vid_rc,
                  "\n  ".join(vid_out.splitlines()[-3:]))

    elapsed = time.time() - t0

    # Inspect what landed on disk (flat layout: youtube.com-<vid>.*)
    candidates = list(DOWNLOADS.glob(f"youtube.com-{vid}.*"))
    video_files = [p for p in candidates
                   if p.suffix.lower() in (".mp4", ".webm", ".mkv", ".m4a", ".mp3")
                   and not p.name.endswith(".part")]
    sub_files = [p for p in candidates if p.suffix.lower() == ".vtt"]
    video_path = video_files[0] if video_files else None

    transcript_path = None
    transcript_source = "none"
    if sub_files:
        manual = [p for p in sub_files if ".auto" not in p.stem]
        chosen = manual[0] if manual else sub_files[0]
        text = vtt_to_text(chosen)
        if text:
            transcript_path = DOWNLOADS / f"youtube.com-{vid}.transcript.txt"
            transcript_path.write_text(text, encoding="utf-8")
            transcript_source = "youtube_manual" if manual else "youtube_auto"
            log.debug("YT transcript: %d chars from %s", len(text), chosen.name)

    have_video = video_path is not None
    have_transcript = transcript_path is not None

    if not (have_video or have_transcript):
        tail = "\n".join((vid_out or sub_out or "").splitlines()[-6:])
        log.warning("YT FAIL  %5.1fs  vid=%s  no video, no transcript",
                    elapsed, vid)
        if tail:
            log.debug("YT tail:\n  %s", tail.replace("\n", "\n  "))
        return {"url": url, "status": "error", "is_youtube": True,
                "video_id": vid,
                "error": f"sub_rc={sub_rc} video_rc={vid_rc}",
                "stderr_tail": tail[:500], "elapsed_s": round(elapsed, 3)}

    size = video_path.stat().st_size if video_path else 0
    if not have_video and have_transcript:
        # Distinct WARN line so it's grep-able. Anti-bot 403 is expected
        # without authenticated cookies; surface the fix in the log.
        log.warning("YT   transcript-only (video 403'd by anti-bot)  vid=%s  "
                    "fix: pass --yt-cookies-from <browser> or --yt-cookies-file",
                    vid)
    log.info("YT   ok %5.1fs  vid=%s  video=%s  transcript=%s  (%.1f MB)",
             elapsed, vid,
             video_path.name if video_path else "MISSING",
             transcript_source,
             size / (1024 * 1024))
    return {
        "url": url,
        "status": "ok",
        "is_youtube": True,
        "video_id": vid,
        "path": video_path.name if video_path else None,
        "video_status": "ok" if have_video else "failed",
        "transcript_path": transcript_path.name if transcript_path else None,
        "transcript_source": transcript_source,
        "size": size,
        "elapsed_s": round(elapsed, 3),
    }


def fetch(url: str, timeout: int, video_max_mb: int,
          yt_cookies_browser: str | None = None,
          yt_cookies_file: str | None = None) -> dict:
    if stop_requested():
        return {"url": url, "status": "stopped", "error": "stop requested"}

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if parsed.scheme not in ("http", "https"):
        log.debug("SKIP non-http: %s", url)
        return {"url": url, "status": "skipped", "error": "non-http scheme"}

    if is_youtube(url):
        return fetch_youtube(url, video_max_mb, timeout,
                             yt_cookies_browser, yt_cookies_file)

    if any(parsed.path.lower().endswith(e) for e in SKIP_EXTS):
        log.debug("SKIP media-ext: %s", url)
        return {"url": url, "status": "skipped", "error": "media extension"}

    waited = polite_wait(domain)
    if waited > 0.05:
        log.debug("rate-limited %s: waited %.2fs", domain, waited)

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/pdf,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            clen = resp.headers.get("Content-Length")
            if clen and clen.isdigit() and int(clen) > MAX_BYTES:
                log.warning("SKIP too-large (%s bytes): %s", clen, url)
                return {"url": url, "status": "skipped",
                        "error": f"too large ({clen} bytes)", "content_type": ctype}
            data = resp.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                log.warning("SKIP exceeded-cap: %s", url)
                return {"url": url, "status": "skipped", "error": "exceeded size cap"}
            rel = safe_filename(url, ctype)
            target = DOWNLOADS / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            elapsed = time.time() - t0
            log.info("OK   %d %7d B  %5.2fs  %s -> %s",
                     getattr(resp, "status", 200), len(data), elapsed,
                     url[:90], rel)
            return {
                "url": url,
                "status": "ok",
                "path": str(rel).replace("\\", "/"),
                "size": len(data),
                "content_type": ctype,
                "http_status": getattr(resp, "status", 200),
                "elapsed_s": round(elapsed, 3),
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        log.warning("HTTP %d  %5.2fs  %s  (%s)",
                    e.code, elapsed, url[:90], str(e)[:80])
        return {"url": url, "status": "http_error", "http_status": e.code,
                "error": str(e)[:200], "elapsed_s": round(elapsed, 3)}
    except urllib.error.URLError as e:
        elapsed = time.time() - t0
        log.warning("URL-ERR  %5.2fs  %s  (%s)",
                    elapsed, url[:90], str(e.reason)[:80])
        return {"url": url, "status": "url_error",
                "error": str(e.reason)[:200], "elapsed_s": round(elapsed, 3)}
    except (TimeoutError, OSError, ValueError) as e:
        elapsed = time.time() - t0
        log.warning("ERR  %5.2fs  %s  (%s: %s)",
                    elapsed, url[:90], type(e).__name__, str(e)[:80])
        return {"url": url, "status": "error",
                "error": f"{type(e).__name__}: {str(e)[:180]}",
                "elapsed_s": round(elapsed, 3)}


def load_manifest() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    if not MANIFEST.exists():
        return idx
    with MANIFEST.open("r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                idx[rec["url"]] = rec
            except json.JSONDecodeError as e:
                log.warning("manifest line %d: bad JSON, skipped (%s)", ln, e)
    return idx


def classify_resume(urls: list[str], manifest: dict[str, dict],
                    retry_failed: bool, refetch: bool
                    ) -> tuple[list[str], dict[str, int]]:
    """Return (todo, stats) where stats explain why each URL is or isn't skipped."""
    stats = Counter()
    todo = []
    for u in urls:
        if refetch:
            todo.append(u)
            stats["refetch_all"] += 1
            continue
        rec = manifest.get(u)
        if rec is None:
            todo.append(u)
            stats["new"] += 1
            continue
        if rec.get("status") == "ok":
            path = rec.get("path")
            on_disk = bool(path) and (DOWNLOADS / path).exists()
            # For YouTube: also require the transcript file if the manifest claims one
            if rec.get("is_youtube"):
                tpath = rec.get("transcript_path")
                if tpath and not (DOWNLOADS / tpath).exists():
                    on_disk = False
            if on_disk:
                stats["skip_ok_on_disk"] += 1
                continue
            stats["resume_missing_file"] += 1
            todo.append(u)
            continue
        # prior failure / stopped
        if retry_failed or rec.get("status") == "stopped":
            stats[f"retry_{rec.get('status','unknown')}"] += 1
            todo.append(u)
        else:
            stats[f"skip_prior_{rec.get('status', 'unknown')}"] += 1
    return todo, dict(stats)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--limit", type=int, default=0,
                   help="cap number of URLs (0 = no cap)")
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p.add_argument("--domains", nargs="*", default=None,
                   help="only fetch URLs whose netloc contains any of these")
    p.add_argument("--retry-failed", action="store_true",
                   help="re-attempt URLs whose prior status is not ok")
    p.add_argument("--refetch", action="store_true",
                   help="ignore manifest entirely; refetch every URL")
    p.add_argument("--verbose", action="store_true",
                   help="show DEBUG (per-URL) output on stdout too")
    p.add_argument("--video-max-mb", type=int, default=DEFAULT_VIDEO_MAX_MB,
                   help="cap YouTube video size (default %(default)s MB)")
    p.add_argument("--no-youtube", action="store_true",
                   help="skip YouTube URLs entirely")
    p.add_argument("--yt-cookies-from", choices=["firefox", "chrome", "edge",
                                                  "brave", "opera", "vivaldi", "safari"],
                   default=None,
                   help="use cookies from this browser for YouTube auth "
                        "(bypasses anti-bot 403 on video streams). Browser "
                        "must be CLOSED for Chromium-family browsers and "
                        "you must be signed into YouTube in that browser.")
    p.add_argument("--yt-cookies-file", default=None,
                   help="path to a cookies.txt file (Netscape format) for "
                        "YouTube auth -- use a browser extension like "
                        "'Get cookies.txt LOCALLY' to export from a "
                        "signed-in YouTube tab")
    p.add_argument("--domain-delay", type=float, default=DEFAULT_DOMAIN_DELAY,
                   help="seconds between requests to the same host "
                        "(default %(default)s)")
    p.add_argument("--arxiv-delay", type=float, default=ARXIV_DOMAIN_DELAY,
                   help="seconds between arxiv.org requests (default %(default)s)")
    p.add_argument("--youtube-delay", type=float, default=YOUTUBE_DOMAIN_DELAY,
                   help="seconds between youtube requests (default %(default)s)")
    args = p.parse_args()

    _domain_delays["default"] = args.domain_delay
    _domain_delays["arxiv"] = args.arxiv_delay
    _domain_delays["youtube"] = args.youtube_delay

    # Clear any leftover STOP file at startup so it doesn't auto-halt the run
    if STOP_FILE.exists():
        try:
            STOP_FILE.unlink()
        except OSError:
            pass

    DOWNLOADS.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    logfile = setup_logging(args.verbose)
    migrate_flat_layout()

    log.info("=" * 70)
    log.info("master-marl downloader starting")
    log.info("repo root:  %s", REPO_ROOT)
    log.info("outputs:    %s", OUTPUTS.resolve())
    log.info("downloads:  %s", DOWNLOADS.resolve())
    log.info("manifest:   %s", MANIFEST.resolve())
    log.info("logfile:    %s", logfile.resolve())
    log.info("config:     workers=%d timeout=%ds max_bytes=%dMB "
             "domain_delay=%.2fs (arxiv=%.2fs, youtube=%.2fs)",
             args.workers, args.timeout, MAX_BYTES // (1024*1024),
             _domain_delays["default"], _domain_delays["arxiv"],
             _domain_delays["youtube"])
    log.info("flags:      limit=%s domains=%s retry_failed=%s refetch=%s "
             "verbose=%s no_youtube=%s video_max_mb=%d",
             args.limit or "none", args.domains, args.retry_failed,
             args.refetch, args.verbose, args.no_youtube, args.video_max_mb)
    yt_path = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    log.info("yt-dlp:     %s", yt_path or "NOT FOUND (YouTube URLs will fail)")
    if args.yt_cookies_file:
        log.info("yt cookies: file=%s", args.yt_cookies_file)
    elif args.yt_cookies_from:
        log.info("yt cookies: browser=%s", args.yt_cookies_from)
    else:
        log.info("yt cookies: NONE (YouTube videos will likely 403; "
                 "transcripts will still work)")
    log.info("stop file:  create %s to halt cleanly between tasks",
             STOP_FILE.resolve())
    log.info("=" * 70)

    urls = collect_urls()
    log.info("Total unique URLs across outputs/*.txt: %d", len(urls))
    if not urls:
        log.error("No URLs found. Run extract_urls.py first.")
        return 1

    if args.domains:
        before = len(urls)
        urls = [u for u in urls
                if any(d.lower() in urlparse(u).netloc.lower()
                       for d in args.domains)]
        log.info("Domain filter %s: %d -> %d URLs",
                 args.domains, before, len(urls))

    if args.no_youtube:
        before = len(urls)
        urls = [u for u in urls if not is_youtube(u)]
        log.info("--no-youtube: %d -> %d URLs", before, len(urls))

    manifest = load_manifest()
    log.info("Manifest entries loaded: %d", len(manifest))

    todo, resume_stats = classify_resume(
        urls, manifest, args.retry_failed, args.refetch)
    log.info("Resume breakdown:")
    for k, v in sorted(resume_stats.items()):
        log.info("  %-25s %6d", k, v)
    log.info("URLs to fetch this run: %d", len(todo))

    if args.limit:
        todo = todo[: args.limit]
        log.info("--limit %d -> trimmed to %d URLs", args.limit, len(todo))

    if not todo:
        log.info("Nothing to do. Exiting.")
        return 0

    # Per-domain forecast (for ETA awareness)
    by_domain = Counter(urlparse(u).netloc.lower() for u in todo)
    log.info("Distinct domains in this run: %d", len(by_domain))
    log.info("Top 10 domains in this run:")
    for d, c in by_domain.most_common(10):
        if "arxiv" in d:
            delay = _domain_delays["arxiv"]
        elif any(h in d for h in YOUTUBE_HOSTS):
            delay = _domain_delays["youtube"]
        else:
            delay = _domain_delays["default"]
        log.info("  %-35s %5d urls  (~%.0fs serialized at %.2fs/req)",
                 d, c, c * delay, delay)

    # Round-robin interleave so the worker pool spreads across domains
    # instead of stalling on per-domain rate-limit locks.
    todo_ordered = interleave_by_domain(todo)
    # Estimate ETA: parallel-bound by the slowest domain queue, since the
    # interleaver lets every domain make progress concurrently.
    serial_per_domain = max(
        c * (_domain_delays["arxiv"] if "arxiv" in d
             else _domain_delays["youtube"] if any(h in d for h in YOUTUBE_HOSTS)
             else _domain_delays["default"])
        for d, c in by_domain.items()
    )
    log.info("Interleaved %d URLs across %d domains.", len(todo_ordered), len(by_domain))
    log.info("ETA lower bound (slowest-domain queue): ~%.1f min",
             serial_per_domain / 60)

    counts: Counter[str] = Counter()
    domain_counts: dict[str, Counter[str]] = defaultdict(Counter)
    error_reasons: Counter[str] = Counter()
    bytes_total = 0
    start = time.time()

    def _signal_handler(signum, _frame):
        log.warning("Signal %s received -- requesting stop", signum)
        _stop_event.set()
        # also try to terminate any in-flight subprocesses (yt-dlp)
        with _active_procs_lock:
            for p in list(_active_procs):
                try:
                    p.terminate()
                except Exception:
                    pass

    signal.signal(signal.SIGINT, _signal_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _signal_handler)
    if hasattr(signal, "SIGBREAK"):  # Windows Ctrl+Break
        signal.signal(signal.SIGBREAK, _signal_handler)

    with MANIFEST.open("a", encoding="utf-8") as mfile:
        with ThreadPoolExecutor(max_workers=args.workers,
                                thread_name_prefix="dl") as ex:
            futures = {ex.submit(fetch, u, args.timeout, args.video_max_mb,
                                 args.yt_cookies_from, args.yt_cookies_file): u
                       for u in todo_ordered}
            try:
                for i, fut in enumerate(as_completed(futures), 1):
                    rec = fut.result()
                    mfile.write(json.dumps(rec) + "\n")
                    mfile.flush()
                    s = rec["status"]
                    counts[s] += 1
                    domain_counts[urlparse(rec["url"]).netloc.lower()][s] += 1
                    if s == "ok":
                        bytes_total += rec.get("size", 0)
                    elif s != "stopped":
                        error_reasons[str(rec.get("error", "unknown"))[:80]] += 1
                    if i % 10 == 0 or i == len(todo):
                        elapsed = time.time() - start
                        rate = i / elapsed if elapsed > 0 else 0
                        eta = (len(todo) - i) / rate if rate > 0 else 0
                        log.info("[progress %d/%d] ok=%d http=%d url=%d "
                                 "skip=%d err=%d stop=%d | %.1f/s ETA=%.1fmin "
                                 "| %.1f MB",
                                 i, len(todo), counts["ok"],
                                 counts.get("http_error", 0),
                                 counts.get("url_error", 0),
                                 counts.get("skipped", 0),
                                 counts.get("error", 0),
                                 counts.get("stopped", 0),
                                 rate, eta / 60, bytes_total / (1024*1024))
                    if stop_requested():
                        log.warning("Stop signal active -- cancelling pending tasks")
                        for f in futures:
                            if not f.done():
                                f.cancel()
                        break
            except KeyboardInterrupt:
                _stop_event.set()
                log.warning("KeyboardInterrupt -- cancelling pending tasks "
                            "(in-flight subprocesses will be terminated)")
                with _active_procs_lock:
                    for p in list(_active_procs):
                        try:
                            p.terminate()
                        except Exception:
                            pass
                for f in futures:
                    if not f.done():
                        f.cancel()

    # Clean up STOP sentinel after a clean run so the next run isn't blocked.
    if STOP_FILE.exists() and not _stop_event.is_set():
        try:
            STOP_FILE.unlink()
        except OSError:
            pass

    elapsed = time.time() - start
    log.info("=" * 70)
    log.info("Run complete in %.1f min  (%.1f MB downloaded)",
             elapsed / 60, bytes_total / (1024 * 1024))
    log.info("Final counts: %s", dict(counts))
    log.info("Top 10 domains by outcome:")
    for d, sub in sorted(domain_counts.items(),
                         key=lambda kv: -sum(kv[1].values()))[:10]:
        total = sum(sub.values())
        log.info("  %-35s total=%4d  ok=%4d  fail=%4d",
                 d, total, sub.get("ok", 0), total - sub.get("ok", 0))
    if error_reasons:
        log.info("Top 10 error reasons:")
        for reason, n in error_reasons.most_common(10):
            log.info("  %4d  %s", n, reason)
    log.info("Manifest: %s  (%d total entries after run)",
             MANIFEST, len(load_manifest()))
    log.info("Logfile:  %s", logfile)
    log.info("Re-run safe: this script is idempotent. "
             "Use --retry-failed to retry errors, --refetch to redo everything.")
    log.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

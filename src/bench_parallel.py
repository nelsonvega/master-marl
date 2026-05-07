"""
A/B benchmark: parallel speedup of the downloader on a multi-domain slice.

Picks N URLs spread across distinct domains (to defeat alphabetical clustering)
and runs the downloader twice -- with --workers 1 and with --workers WORKERS --
both with --refetch so manifest doesn't short-circuit. Reports wall-clock for
each run.
"""
from __future__ import annotations
import os, sys, time, subprocess, random
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

PUBLIC = Path("outputs/public_urls.txt")
SAMPLE = Path("outputs/_bench_sample.txt")

N_PER_DOMAIN = 1
N_TOTAL = 30
WORKERS = 16

def main():
    urls = [u.strip() for u in PUBLIC.read_text(encoding="utf-8").splitlines()
            if u.strip().startswith(("http://", "https://"))]
    by_domain = defaultdict(list)
    for u in urls:
        nl = urlparse(u).netloc.lower()
        # avoid arxiv (one giant cluster) and youtube (yt-dlp path is different)
        if "arxiv" in nl or any(h in nl for h in ("youtube", "youtu.be")):
            continue
        by_domain[nl].append(u)

    random.seed(42)
    sample = []
    for nl, lst in sorted(by_domain.items(), key=lambda kv: -len(kv[1])):
        random.shuffle(lst)
        sample.extend(lst[:N_PER_DOMAIN])
        if len(sample) >= N_TOTAL:
            break
    sample = sample[:N_TOTAL]
    print(f"Bench sample: {len(sample)} URLs across "
          f"{len(set(urlparse(u).netloc for u in sample))} domains")
    SAMPLE.write_text("\n".join(sample), encoding="utf-8")

    def run(workers: int) -> float:
        # Override outputs/*.txt: copy sample into a temp outputs dir trick
        # is overkill -- just point downloader at the file via a tmp outputs/.
        # Simpler: temporarily rename other outputs, restore after.
        bak = {}
        for f in Path("outputs").glob("*.txt"):
            if f.name == SAMPLE.name:
                continue
            tmp = f.with_suffix(".txt.bak")
            f.rename(tmp)
            bak[tmp] = f
        try:
            t0 = time.time()
            subprocess.run(
                [sys.executable, "src/download_content.py",
                 "--refetch", f"--workers={workers}",
                 "--no-youtube"],
                check=False,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            elapsed = time.time() - t0
        finally:
            for tmp, orig in bak.items():
                tmp.rename(orig)
            SAMPLE.unlink(missing_ok=True)
        return elapsed

    print("Running serial (workers=1)...")
    t1 = run(1)
    print(f"  serial:   {t1:.1f}s  ({len(sample)/t1:.2f} URL/s)")

    print(f"Running parallel (workers={WORKERS})...")
    tn = run(WORKERS)
    print(f"  parallel: {tn:.1f}s  ({len(sample)/tn:.2f} URL/s)")

    print(f"\nSpeedup: {t1/tn:.2f}x  (ideal would be ~{WORKERS}x)")

if __name__ == "__main__":
    main()

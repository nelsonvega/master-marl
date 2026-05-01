import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)
DOCS = "docs"
URL_RE = re.compile(r"https?://[^\s)\]>\"'\\]+")

counts = Counter()
for fn in sorted(os.listdir(DOCS)):
    if not fn.endswith(".md"):
        continue
    p = os.path.join(DOCS, fn)
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    urls = URL_RE.findall(text)
    for u in urls:
        u = u.rstrip(".,;:#\\")
        u = u.replace("\\#", "#").replace("\\&", "&").replace("\\_", "_")
        # Normalize arxiv/abs vs pdf to same id
        if "arxiv.org" in u:
            m = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9.]+)", u)
            if m:
                u = f"https://arxiv.org/abs/{m.group(1)}"
        counts[u] += 1

print(f"Unique normalized URLs: {len(counts)}")
print("\nTop 60 most-cited URLs (signal of importance):")
for u, c in counts.most_common(60):
    print(f"  {c:3d}  {u}")

# Also: top 40 arxiv papers
arxiv = Counter({u: c for u, c in counts.items() if "arxiv.org/abs" in u})
print(f"\nTop 30 most-cited arxiv papers ({len(arxiv)} total):")
for u, c in arxiv.most_common(30):
    print(f"  {c:3d}  {u}")

# Top github repos
gh = Counter({u: c for u, c in counts.items() if "github.com" in u and "/settings" not in u})
print(f"\nTop 25 most-cited GitHub URLs ({len(gh)} total):")
for u, c in gh.most_common(25):
    print(f"  {c:3d}  {u}")

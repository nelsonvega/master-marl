import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)
DOCS = "docs"
URL_RE = re.compile(r"https?://[^\s)\]>\"'\\]+")

all_urls = []
per_file = {}
for fn in sorted(os.listdir(DOCS)):
    if not fn.endswith(".md"):
        continue
    p = os.path.join(DOCS, fn)
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    urls = URL_RE.findall(text)
    cleaned = []
    for u in urls:
        # strip trailing punctuation/escapes
        u = u.rstrip(".,;:#\\")
        # markdown often emits \# or \&; remove backslash escapes
        u = u.replace("\\#", "#").replace("\\&", "&").replace("\\_", "_")
        cleaned.append(u)
    per_file[fn] = len(cleaned)
    all_urls.extend(cleaned)

print("Total URL hits:", len(all_urls))
unique = sorted(set(all_urls))
print("Unique URLs:", len(unique))

domains = Counter()
for u in unique:
    try:
        d = urlparse(u).netloc.lower()
        domains[d] += 1
    except Exception:
        pass

print("Top 40 domains:")
for d, c in domains.most_common(40):
    print(f"  {c:4d}  {d}")

os.makedirs("outputs", exist_ok=True)
with open("outputs/all_unique_urls.txt", "w", encoding="utf-8") as f:
    for u in unique:
        f.write(u + "\n")

# Categorize by likely-public vs auth-walled
AUTH_DOMAINS = {
    "portal.azure.com", "ai.azure.com", "github.com",  # github mostly public but settings/etc not
    "discord.com", "www.linkedin.com", "linkedin.com",
    "learning.oreilly.com", "www.udemy.com", "udemy.com",
    "learn.mit.edu", "www.perplexity.ai", "perplexity.ai",
    "www.google.com", "www.youtube.com", "youtube.com",
}
public = []
walled = []
for u in unique:
    netloc = urlparse(u).netloc.lower()
    if netloc in AUTH_DOMAINS or netloc.endswith(".microsoft.com") or u.startswith("chrome"):
        walled.append(u)
    else:
        public.append(u)

with open("outputs/public_urls.txt", "w", encoding="utf-8") as f:
    for u in public:
        f.write(u + "\n")
with open("outputs/walled_urls.txt", "w", encoding="utf-8") as f:
    for u in walled:
        f.write(u + "\n")

print(f"\nPublic-fetchable: {len(public)}")
print(f"Likely-walled / interactive: {len(walled)}")

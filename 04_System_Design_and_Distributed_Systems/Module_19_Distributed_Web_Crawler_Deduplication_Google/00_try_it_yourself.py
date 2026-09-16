"""Beginner playground for Module 19 - Distributed Web Crawler and Deduplication.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib
import re

# ---------------------------------------------- 1. Politeness is not optional
MIN_DELAY_SECONDS = 1.0
last_fetch = {}


def may_fetch(host, now):
    if now - last_fetch.get(host, -999) < MIN_DELAY_SECONDS:
        return False
    last_fetch[host] = now
    return True


print("t=0.0  a.com:", may_fetch("a.com", 0.0))
print("t=0.5  a.com:", may_fetch("a.com", 0.5))
print("t=0.5  b.com:", may_fetch("b.com", 0.5))
assert may_fetch("a.com", 0.6) is False, "too soon for this host"
assert may_fetch("c.com", 0.6) is True, "a different host is unaffected"
print("Parallelism comes from breadth across hosts, not depth into one.")


# -------------------------------- 2. Canonicalise before you do anything else
TRACKING = {"utm_source", "utm_medium", "utm_campaign", "fbclid", "gclid"}


def canonicalise(url):
    url = url.split("#")[0]
    scheme, _, rest = url.partition("://")
    host, _, path = rest.partition("/")
    host = host.lower().replace(":80", "").replace(":443", "")
    path, _, query = path.partition("?")
    path = "/" + path.strip("/")
    kept = sorted(p for p in query.split("&")
                  if p and p.split("=")[0] not in TRACKING)
    return f"{scheme.lower()}://{host}{path}" + ("?" + "&".join(kept) if kept else "")


spellings = [
    "https://EXAMPLE.com/page",
    "https://example.com/page/",
    "https://example.com:443/page",
    "https://example.com/page?utm_source=twitter",
    "https://example.com/page#section-2",
]
canonical = {canonicalise(u) for u in spellings}
for url in spellings:
    print(f"  {url:<44} -> {canonicalise(url)}")
assert len(canonical) == 1, "five spellings, one page"


# -------------------------------------- 3. Exact duplicates: hash the content
pages = {
    "https://a.com/story": "Breaking news: the thing happened today.",
    "https://b.com/story": "Breaking news: the thing happened today.",
    "https://c.com/other": "Something completely different.",
}
seen_hashes = set()
indexed = []
for url, body in pages.items():
    digest = hashlib.sha256(body.encode()).hexdigest()
    if digest in seen_hashes:
        print(f"  skipped {url} - byte-identical to a page already indexed")
        continue
    seen_hashes.add(digest)
    indexed.append(url)

print("indexed:", indexed)
assert len(indexed) == 2, "the mirror was dropped"


# ----------------------------------- 4. Near-duplicates need a different tool
def shingles(text, size=3):
    words = re.findall(r"[a-z]+", text.lower())
    return {" ".join(words[i:i + size]) for i in range(len(words) - size + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


original = "the quick brown fox jumps over the lazy dog every single morning"
near_dupe = "the quick brown fox jumps over the lazy dog every single evening"
unrelated = "database indexes make lookups fast by avoiding a full table scan"

print(f"original vs near-duplicate: {jaccard(shingles(original), shingles(near_dupe)):.2f}")
print(f"original vs unrelated:      {jaccard(shingles(original), shingles(unrelated)):.2f}")
assert jaccard(shingles(original), shingles(near_dupe)) > 0.7
assert jaccard(shingles(original), shingles(unrelated)) < 0.05


# ------------------------------------------- 5. The trap: the web is infinite
MAX_DEPTH = 3
PER_HOST_BUDGET = 5


def crawl(seed, depth=0, fetched=None):
    fetched = fetched if fetched is not None else []
    if depth >= MAX_DEPTH or len(fetched) >= PER_HOST_BUDGET:
        return fetched
    fetched.append(seed)
    return crawl(f"{seed}/next", depth + 1, fetched)


trapped = crawl("https://cal.com/2026-01")
print("pages fetched before the limits stopped it:", len(trapped))
print(" ", trapped[-1])
assert len(trapped) == MAX_DEPTH, "bounded, despite an infinite URL space"


print()
print("All checks passed.")

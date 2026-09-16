# Beginner Playground - Distributed Web Crawler and Deduplication

> *"A polite visitor knocks once, waits, and does not photograph the same room from four doorways and file it four times."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
import re
```

---

## 1. Politeness is not optional

A crawler that fetches as fast as it can is indistinguishable from a denial of
service attack, and gets your address blocked.

So the frontier is organised **per host**: each host has its own queue and its own
minimum delay between requests. Parallelism comes from crawling many hosts at
once, never from hammering one.

```python
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
```

---

## 2. Canonicalise before you do anything else

The same page is reachable by many spellings. Normalise the URL - lowercase the
host, strip the default port, drop the fragment, remove tracking parameters, sort
what remains - and the duplicates collapse before they ever enter the frontier.

```python
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
```

---

## 3. Exact duplicates: hash the content

Different URLs can still serve identical bytes - mirrors, syndicated articles,
printer-friendly versions. Hash the body and keep a set of hashes.

A fixed-size digest per page is cheap enough to hold for billions of pages, which
a set of page bodies obviously is not.

```python
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
```

---

## 4. Near-duplicates need a different tool

Change one word and the hash changes completely - that is what a hash is for. But
a page with one extra advert is still the same page.

**Shingling** compares overlapping word groups: two documents that share most of
their shingles are near-duplicates. Production crawlers use SimHash or MinHash,
which give the same answer without comparing every pair.

```python
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
```

---

## 5. The trap: the web is infinite

A calendar page with a "next month" link generates URLs forever. So does any
search box with a page parameter. A crawler that follows every link it finds will
crawl one site until the heat death of the universe.

Defences: a depth limit, a per-host page budget, and a hard look at URLs that grow
a parameter each hop. Every real crawler has been caught by this once.

```python
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
```

---

## 6. Predict before you run

`example.com/page`, `example.com/page/`, `EXAMPLE.com/page` and
`example.com/page?utm_source=x` are four URLs. How many pages are they? What
does your crawler store if it does not know that?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Roughly a third of the web is duplicate content. A crawler that does not
deduplicate spends a third of its bandwidth, storage and index on copies -
and then serves a search results page with the same article four times.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

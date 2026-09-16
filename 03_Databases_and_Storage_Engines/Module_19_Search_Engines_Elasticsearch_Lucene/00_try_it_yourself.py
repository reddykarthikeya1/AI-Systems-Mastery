"""Beginner playground for Module 19 - Search Engines - Elasticsearch and Lucene.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import re

# ------------------------------------------- 1. Scanning versus looking it up
documents = {
    1: "The Database stores rows on disk",
    2: "Running a database is running a service",
    3: "Disk seeks are slow",
    4: "A search index avoids scanning the disk",
}


def tokenize(text):
    return re.findall(r"[a-z]+", text.lower())


docs_scanned = {"count": 0}


def scan_search(word):
    hits = []
    for doc_id, text in documents.items():
        docs_scanned["count"] += 1
        if word in tokenize(text):
            hits.append(doc_id)
    return hits


print("scan for 'disk':", scan_search("disk"), f"({docs_scanned['count']} docs read)")
assert scan_search("disk") == [1, 3, 4]


# --------------------------------- 2. Build the index at the back of the book
inverted = {}
for doc_id, text in documents.items():
    for word in set(tokenize(text)):
        inverted.setdefault(word, set()).add(doc_id)

print("entry for 'disk':    ", sorted(inverted["disk"]))
print("entry for 'database':", sorted(inverted["database"]))
assert sorted(inverted["disk"]) == [1, 3, 4], "same answer as the scan"
assert inverted["database"] == {1, 2}, "and it never touched documents 3 or 4"


# -------------------------------------- 3. Boolean queries are just set maths
both = inverted["disk"] & inverted["database"]
either = inverted["disk"] | inverted["database"]
print("disk AND database:", sorted(both))
print("disk OR  database:", sorted(either))
assert both == {1}, "only document 1 mentions both"
assert either == {1, 2, 3, 4}


# --------------------------------------- 4. The bug that returns zero results
def stem(word):
    for suffix in ("ning", "ing", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    return word


stemmed_index = {}
for doc_id, text in documents.items():
    for word in set(tokenize(text)):
        stemmed_index.setdefault(stem(word), set()).add(doc_id)

wrong = stemmed_index.get("Running".lower(), set())
right = stemmed_index.get(stem("Running".lower()), set())
print("searching the stemmed index with the RAW word  ->", sorted(wrong))
print("searching it with the SAME analysis as indexing ->", sorted(right))
assert wrong == set(), "zero results, no error, documents definitely present"
assert right == {2}, "matching analysis finds it immediately"
print("Index-time and query-time analysis must agree. This is THE search bug.")


print()
print("All checks passed.")

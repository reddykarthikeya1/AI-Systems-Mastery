# Beginner Playground - Search Engines - Elasticsearch and Lucene

> *"The index at the back of a book. Nobody finds 'photosynthesis' by reading every page - you look it up and it tells you which pages to open."*


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
import re
```

---

## 1. Scanning versus looking it up

The slow way to find every document containing "database" is to read all of them.
That is a `LIKE '%database%'` query, and its cost grows with the size of your
corpus whether or not anything matches.

An **inverted index** flips it around: for each word, keep the list of documents
containing it. Searching becomes a dictionary lookup.

```python
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
```

---

## 2. Build the index at the back of the book

One pass over the corpus builds a map from word to document ids. After that, a
search reads exactly one entry no matter how large the corpus grows.

```python
inverted = {}
for doc_id, text in documents.items():
    for word in set(tokenize(text)):
        inverted.setdefault(word, set()).add(doc_id)

print("entry for 'disk':    ", sorted(inverted["disk"]))
print("entry for 'database':", sorted(inverted["database"]))
assert sorted(inverted["disk"]) == [1, 3, 4], "same answer as the scan"
assert inverted["database"] == {1, 2}, "and it never touched documents 3 or 4"
```

---

## 3. Boolean queries are just set maths

`disk AND database` is an intersection. `OR` is a union. `NOT` is a difference.
The posting lists are kept sorted precisely so these operations are fast.

```python
both = inverted["disk"] & inverted["database"]
either = inverted["disk"] | inverted["database"]
print("disk AND database:", sorted(both))
print("disk OR  database:", sorted(either))
assert both == {1}, "only document 1 mentions both"
assert either == {1, 2, 3, 4}
```

---

## 4. The bug that returns zero results

"Analysis" is what turns raw text into the tokens that go in the index:
lowercasing, splitting, and often **stemming** - reducing `running` and `runs` to
`run`.

The rule that matters: **the query must be analysed the same way the document
was.** Store stemmed tokens and search with an unstemmed one and you match
nothing, with no error to tell you why.

```python
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
```

---

## 5. Predict before you run

Your index stores lowercase words. A user searches for "Running". Do they
get a hit? What if the index applied stemming but the search box did not?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

The single most common Elasticsearch bug in production is an analyzer
mismatch: text processed one way when stored and a different way when searched.
It fails silently, returning zero results for documents that are definitely
there.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

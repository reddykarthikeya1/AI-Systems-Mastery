# Beginner Playground - Vector Databases - pgvector and Qdrant

> *"An embedding is a map reference for meaning. Things that mean similar things get put near each other, and 'find me something like this' becomes 'what is nearby'."*

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
import math
```

---

## 1. Meaning as coordinates

A model turns text into a list of numbers - a **vector** - positioned so that
similar meanings end up close together. The numbers themselves mean nothing to a
human. Only the distances matter.

Real embeddings have hundreds or thousands of dimensions. Three is enough to see
the idea, and you can check these by eye.

```python
vectors = {
    "king":    [0.90, 0.80, 0.10],
    "queen":   [0.88, 0.75, 0.15],
    "monarch": [0.85, 0.82, 0.12],
    "banana":  [0.10, 0.15, 0.95],
    "mango":   [0.12, 0.10, 0.92],
}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm


print(f"king vs queen : {cosine(vectors['king'], vectors['queen']):.3f}")
print(f"king vs banana: {cosine(vectors['king'], vectors['banana']):.3f}")
assert cosine(vectors["king"], vectors["queen"]) > 0.99
assert cosine(vectors["king"], vectors["banana"]) < 0.5
print("Nothing was told that kings and queens are related. The geometry says so.")
```

---

## 2. Search means 'what is nearest'

No keywords, no matching text. You embed the query and return whatever is closest.
Which is why a vector search for "royalty" can return a document that never
contains the word.

```python
def nearest(query_vector, k=2):
    scored = [(cosine(query_vector, v), name) for name, v in vectors.items()]
    scored.sort(reverse=True)
    return [name for _, name in scored[:k]]


print("nearest to 'king':  ", nearest(vectors["king"]))
print("nearest to 'banana':", nearest(vectors["banana"]))
assert set(nearest(vectors["king"])) <= {"king", "queen", "monarch"}
assert set(nearest(vectors["banana"])) <= {"banana", "mango"}
```

---

## 3. Exact search does not scale, and here is the arithmetic

`nearest` above compares the query against *every* vector. That is fine for five.
For ten million vectors at a hundred queries a second it is a billion comparisons
a second, and each one is arithmetic across hundreds of dimensions.

This is why vector databases exist as a separate category. Not for the similarity
function - for everything done to avoid running it ten million times.

```python
corpus_size = 10_000_000
queries_per_second = 100
dimensions = 768

comparisons = corpus_size * queries_per_second
print(f"exact search: {comparisons:,} comparisons/second")
print(f"             x {dimensions} dimensions = {comparisons * dimensions:,} "
      f"multiply-adds/second")
assert comparisons == 1_000_000_000
print("That is not a tuning problem. It is the wrong algorithm.")
```

---

## 4. Approximate search: trade a little recall for a lot of speed

**ANN** - approximate nearest neighbour - organises vectors so a search can skip
most of them. Group similar vectors together, find the nearest group, search only
inside it.

You give up exactness. Occasionally the true nearest neighbour sits just over a
group boundary and gets missed. The measure of that loss is **recall**, and for
"related products" trading 2% recall for a 50x speed-up is obviously right.

The honest question is never "is it exact" - it is "what recall do I get, and can
my product live with it".

```python
groups = {
    "royalty": ["king", "queen", "monarch"],
    "fruit": ["banana", "mango"],
}
centroids = {
    name: [sum(vectors[m][d] for m in members) / len(members) for d in range(3)]
    for name, members in groups.items()
}

comparison_count = {"n": 0}


def approximate_nearest(query_vector, k=2):
    best_group = max(centroids, key=lambda g: cosine(query_vector, centroids[g]))
    comparison_count["n"] += len(centroids)
    candidates = groups[best_group]
    comparison_count["n"] += len(candidates)
    scored = sorted(((cosine(query_vector, vectors[m]), m) for m in candidates),
                    reverse=True)
    return [name for _, name in scored[:k]]


comparison_count["n"] = 0
approx = approximate_nearest(vectors["king"])
exact = nearest(vectors["king"])
print("approximate result:", approx, f"({comparison_count['n']} comparisons)")
print("exact result:      ", exact, f"({len(vectors)} comparisons)")
assert approx == exact, "same answer here - and it looked at fewer vectors"
assert comparison_count["n"] <= len(vectors), "and the gap widens with scale"
```

---

## 5. Predict before you run

Exact nearest-neighbour search compares your query against every vector in
the database. With 10 million vectors and 100 queries a second, how many
comparisons per second is that? Is that a search you can afford?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every 'related products', 'similar images' and retrieval-augmented chatbot is
this. The interesting engineering is not similarity - it is avoiding the
comparison with all ten million.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

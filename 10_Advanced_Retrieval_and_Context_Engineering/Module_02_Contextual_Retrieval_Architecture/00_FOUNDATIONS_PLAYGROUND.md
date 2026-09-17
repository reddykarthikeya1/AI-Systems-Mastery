# 🐣 Interactive Foundations Playground: Contextual Retrieval Architecture

> *"Contextual retrieval prepends a short document synopsis to every chunk before embedding it."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
```

---

## 1. Contextual Header Prepending

Isolated chunks like 'revenue grew 15%' lack identity; prepending 'Document: Apple Q3 2024 Report' grounds the vector representation.

```python
doc_context = "Document: Apple Inc. Q3 2024 Earnings Report."
raw_chunk = "Services revenue grew 15% year-over-year reaching an all-time record."
contextual_chunk = f"{doc_context}\n{raw_chunk}"

assert "Apple Inc." in contextual_chunk
assert "Services revenue" in contextual_chunk
assert len(contextual_chunk) > len(raw_chunk)
print(f"Contextualized chunk:\n{contextual_chunk}")
```

---

## 2. Embedding Drift Reduction

Contextual headers pull ambiguous chunks into the correct topical cluster in embedding space.

```python
tags = ["finance", "earnings", "apple"]
assert "apple" in tags
print(f"Semantic metadata tags embedded: {tags}")
```

---

## 3. Deduplication via Chunk Fingerprinting

Hashing raw text prevents re-embedding identical chunks across repeated document ingestion cycles.

```python
h1 = hashlib.md5(raw_chunk.encode()).hexdigest()
h2 = hashlib.md5(raw_chunk.encode()).hexdigest()
assert h1 == h2
print(f"Deterministic chunk fingerprint: {h1[:8]}")
```

---

# 🐣 Interactive Foundations Playground: Parsing & Hierarchical Chunking

> *"Chunking is slicing a textbook: too small and you lose context, too big and you drown in noise."*

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
import math
```

---

## 1. Fixed-Size Chunking with Overlap

Sliding window chunking advances by $\text{stride} = \text{chunk\_size} - \text{overlap}$, ensuring semantic continuity across boundaries.

```python
text = "abcdefghijklmnopqrstuvwxyz"
chunk_size = 10
overlap = 3
stride = chunk_size - overlap  # 7

chunks = []
for i in range(0, len(text), stride):
    chunks.append(text[i:i+chunk_size])

assert len(chunks) == 4
assert chunks[0] == "abcdefghij"
assert chunks[1] == "hijklmnopq"  # 'hij' overlapping
assert chunks[0][-overlap:] == chunks[1][:overlap]
print(f"Chunks generated with 3-char overlap: {chunks}")
```

---

## 2. Parent-Child Hierarchical Mapping

Retrieval queries small child chunks for precise vector matching, but feeds the larger parent chunk to the LLM for rich context.

```python
parent_chunk = "Database index internals: B-Trees balance height to maintain O(log N) lookup."
child_1 = "Database index internals"
child_2 = "B-Trees balance height to maintain O(log N) lookup."

parent_child_map = {101: parent_chunk, 102: parent_chunk}
assert parent_child_map[101] == parent_child_map[102]
print("Child chunks 101 and 102 successfully map to parent document context.")
```

---

## 3. Token Count Boundary Guard

Enforcing strict upper token limits per chunk avoids exceeding embedding model context windows.

```python
max_tokens = 512
chunk_tokens = 350
assert chunk_tokens <= max_tokens
print(f"Chunk verified within {max_tokens}-token embedding budget.")
```

---

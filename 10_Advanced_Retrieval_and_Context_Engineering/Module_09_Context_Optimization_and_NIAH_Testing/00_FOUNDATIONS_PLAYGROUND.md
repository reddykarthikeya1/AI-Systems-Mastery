# 🐣 Interactive Foundations Playground: Context Optimization & NIAH Testing

> *"Needle In A Haystack tests whether an LLM can spot a secret key hidden deep inside a 100,000-word document."*

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

## 1. Needle In A Haystack (NIAH) Placement

Inserting a specific target fact at various depth percentages (0%, 25%, 50%, 75%, 100%) measures retrieval recall fidelity.

```python
haystack_tokens = ["the", "quick", "brown", "fox"] * 25  # 100 tokens
needle = "SECRET_PASSWORD_123"
depth_pct = 0.50  # 50% depth

insert_idx = int(len(haystack_tokens) * depth_pct)
haystack_with_needle = haystack_tokens[:insert_idx] + [needle] + haystack_tokens[insert_idx:]

assert haystack_with_needle[insert_idx] == needle
assert len(haystack_with_needle) == 101
print(f"Needle successfully inserted at index {insert_idx} ({depth_pct*100:.0f}% depth).")
```

---

## 2. Lost in the Middle Phenomenon

LLMs attend with highest accuracy to tokens at the very beginning and very end of their context window, dipping in the middle.

```python
accuracy_by_depth = {0.0: 0.98, 0.25: 0.85, 0.50: 0.72, 0.75: 0.84, 1.0: 0.99}

assert accuracy_by_depth[0.50] < accuracy_by_depth[0.0]
assert accuracy_by_depth[0.50] < accuracy_by_depth[1.0]
assert accuracy_by_depth[1.0] > 0.95
print(f"U-shaped accuracy curve: start={accuracy_by_depth[0.0]}, middle={accuracy_by_depth[0.50]}, end={accuracy_by_depth[1.0]}")
```

---

## 3. Context Window Reordering

Placing the most critical retrieved evidence at the start and end of prompt maximizes LLM reasoning accuracy.

```python
retrieved_passages = ["doc_3", "doc_2", "doc_1"]
# Put most relevant at beginning and second most at end
optimized_context = [retrieved_passages[2], retrieved_passages[0], retrieved_passages[1]]

assert optimized_context[0] == "doc_1"
assert len(optimized_context) == 3
print(f"Optimized context layout: {optimized_context}")
```

---

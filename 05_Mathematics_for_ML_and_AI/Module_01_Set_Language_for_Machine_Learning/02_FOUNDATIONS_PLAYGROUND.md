# 🐣 Interactive Foundations Playground: Set Language for Machine Learning

> *"Think of a Set like a VIP guest list: no duplicates allowed, and order does not matter."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python

```

---

## 1. Set Operations and Deduplication

Sets discard duplicate items instantly, modeling unique token vocabularies and distinct entities.

```python
vocab = {"apple", "banana", "apple", "cherry"}
assert len(vocab) == 3
assert "apple" in vocab
print(f"Deduplicated vocabulary ({len(vocab)} items): {sorted(vocab)}")
```

---

## 2. Union, Intersection and Difference

Set union combines features, intersection finds overlapping signals, and difference identifies out-of-vocabulary terms.

```python
alice_skills = {"python", "sql", "docker"}
bob_skills = {"sql", "pytorch", "rust"}

union = alice_skills | bob_skills
intersect = alice_skills & bob_skills
diff = alice_skills - bob_skills

assert len(union) == 5
assert intersect == {"sql"}
assert diff == {"python", "docker"}
print(f"Union: {union}, Intersect: {intersect}, Diff: {diff}")
```

---

## 3. Train/Val/Test Disjoint Partition Verification

The golden rule of ML dataset preparation: training, validation, and test splits must have strictly empty pairwise intersections to prevent data leakage.

```python
train_ids = {101, 102, 103, 104}
val_ids = {105, 106}
test_ids = {107, 108, 109}

leak1 = train_ids & val_ids
leak2 = train_ids & test_ids
leak3 = val_ids & test_ids

assert len(leak1) == 0, "Train and Val must be disjoint"
assert len(leak2) == 0, "Train and Test must be disjoint"
assert len(leak3) == 0, "Val and Test must be disjoint"
print("Clean dataset partition confirmed: zero data leakage.")
```

---

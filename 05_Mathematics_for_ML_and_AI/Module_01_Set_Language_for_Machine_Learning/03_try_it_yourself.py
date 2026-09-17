"""Beginner playground for Module 01 - Set Language for Machine Learning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. Set Operations and Deduplication
vocab = {"apple", "banana", "apple", "cherry"}
assert len(vocab) == 3
assert "apple" in vocab
print(f"Deduplicated vocabulary ({len(vocab)} items): {sorted(vocab)}")

# -------------------------------------------- 2. Union, Intersection and Difference
alice_skills = {"python", "sql", "docker"}
bob_skills = {"sql", "pytorch", "rust"}

union = alice_skills | bob_skills
intersect = alice_skills & bob_skills
diff = alice_skills - bob_skills

assert len(union) == 5
assert intersect == {"sql"}
assert diff == {"python", "docker"}
print(f"Union: {union}, Intersect: {intersect}, Diff: {diff}")

# -------------------------------------------- 3. Train/Val/Test Disjoint Partition Verification
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

print()
print("All checks passed.")

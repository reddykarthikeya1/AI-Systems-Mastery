"""Beginner playground for Module 09 - Research Paper Implementation & Metrics.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Precision, Recall, and F1 Score
tp, fp, fn = 80, 20, 10
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * (precision * recall) / (precision + recall)

assert precision == 0.8
assert abs(recall - 80 / 90) < 1e-6
assert 0.8 < f1 < 0.9
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.4f}")

# -------------------------------------------- 2. BLEU Score N-gram Precision
candidate = "the cat sat on the mat".split()
reference = "the cat is on the mat".split()

cand_bigrams = [tuple(candidate[i:i+2]) for i in range(len(candidate)-1)]
ref_bigrams = set(tuple(reference[i:i+2]) for i in range(len(reference)-1))

matches = sum(1 for bg in cand_bigrams if bg in ref_bigrams)
p2 = matches / len(cand_bigrams)

assert len(cand_bigrams) == 5
assert matches == 3  # ('the', 'cat'), ('on', 'the'), ('the', 'mat')
assert p2 == 0.6
print(f"Bigram precision: {p2:.2f} ({matches}/{len(cand_bigrams)})")

# -------------------------------------------- 3. Perplexity Calculation from Cross-Entropy
cross_entropy_loss = 1.386  # ln(4)
perplexity = math.exp(cross_entropy_loss)

assert abs(perplexity - 4.0) < 0.01
assert perplexity > 1.0
print(f"Cross-entropy {cross_entropy_loss} corresponds to perplexity ~{perplexity:.2f}")

print()
print("All checks passed.")

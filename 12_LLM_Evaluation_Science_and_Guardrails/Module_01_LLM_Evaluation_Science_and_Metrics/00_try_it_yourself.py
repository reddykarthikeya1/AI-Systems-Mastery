"""Beginner playground for Module 01 - LLM Evaluation Science & Metrics.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Exact Match (EM) Binary Metric
def exact_match(pred, ref):
    return 1.0 if pred.strip().lower() == ref.strip().lower() else 0.0

assert exact_match("Paris", "paris") == 1.0
assert exact_match("Paris.", "paris") == 0.0
assert exact_match("Rome", "Paris") == 0.0
print("Exact match evaluation metric confirmed.")

# -------------------------------------------- 2. ROUGE-L Longest Common Subsequence Metric
def lcs_len(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = 1 + dp[i-1][j-1] if s1[i-1] == s2[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

pred_tokens = ["the", "quick", "brown", "fox"]
ref_tokens = ["the", "fast", "brown", "fox"]
lcs = lcs_len(pred_tokens, ref_tokens)
rouge_l_recall = lcs / len(ref_tokens)

assert lcs == 3  # "the", "brown", "fox"
assert rouge_l_recall == 0.75
print(f"ROUGE-L Recall: {rouge_l_recall:.2%}")

# -------------------------------------------- 3. Token Perplexity from Cross-Entropy Loss
neg_log_probs = [0.5, 0.8, 0.2, 1.1]
mean_loss = sum(neg_log_probs) / len(neg_log_probs)
ppl = math.exp(mean_loss)

assert abs(mean_loss - 0.65) < 1e-6
assert ppl > 1.0
print(f"Evaluation Perplexity: {ppl:.2f} (from mean loss {mean_loss:.2f})")

print()
print("All checks passed.")

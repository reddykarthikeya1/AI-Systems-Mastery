"""Reference Solution — Problem 01: Exact Match F1 Score

Topic: 01 LLM Evaluation Science and Metrics
"""

from __future__ import annotations


def exact_match_f1_score(prediction: str, ground_truth: str) -> tuple[int, float]:
    from collections import Counter
    p_tokens = prediction.strip().lower().split()
    g_tokens = ground_truth.strip().lower().split()
    em = 1 if p_tokens == g_tokens else 0
    if not p_tokens or not g_tokens:
        return (em, 1.0 if p_tokens == g_tokens else 0.0)
    common = Counter(p_tokens) & Counter(g_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return (em, 0.0)
    precision = num_same / float(len(p_tokens))
    recall = num_same / float(len(g_tokens))
    f1 = (2.0 * precision * recall) / (precision + recall)
    return (em, round(f1, 4))

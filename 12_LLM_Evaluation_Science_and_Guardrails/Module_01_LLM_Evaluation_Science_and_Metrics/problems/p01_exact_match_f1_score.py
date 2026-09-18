"""Problem 01 — Exact Match F1 Score

Topic: 01 LLM Evaluation Science and Metrics
Target: Production-grade implementation

Compute Exact Match (EM) and token-level F1 score for QA evaluation.

Example:
    >>> exact_match_f1_score('The Eiffel Tower', 'eiffel tower')
    (0, 0.8)
    >>> exact_match_f1_score('Paris', 'Paris')
    (1, 1.0)

Hints:
    Hint 1: Exact match and F1 grade at different granularities — EM cares
        whether the whole normalized string matches, while F1 cares about
        the multiset of tokens the two strings share, regardless of order
        or extra words.
    Hint 2: Normalize by lowercasing and splitting on whitespace, then use
        a Counter intersection (Counter(pred) & Counter(gt)) to count
        overlapping tokens, from which you derive precision (overlap /
        len(pred_tokens)) and recall (overlap / len(gt_tokens)) and
        combine them into the F1 formula.
    Hint 3: "The Eiffel Tower" vs "eiffel tower" scores EM=0 (the extra
        token "The" breaks exact equality) but F1 should still reward the
        two shared tokens — and when either token list is empty, guard
        against dividing by zero: F1 is 1.0 only if both are empty,
        otherwise 0.0.
"""

from __future__ import annotations


def exact_match_f1_score(prediction: str, ground_truth: str) -> tuple[int, float]:
    """Exact Match is 1 if normalized strings match exactly else 0.
    Token-level F1 = 2 * P * R / (P + R) where P = overlap / len(pred), R = overlap / len(gt).
    Normalize by lowercasing and splitting into whitespace tokens.
    Returns (em, f1 rounded to 4 decimals).
    """
    raise NotImplementedError("Implement exact_match_f1_score")

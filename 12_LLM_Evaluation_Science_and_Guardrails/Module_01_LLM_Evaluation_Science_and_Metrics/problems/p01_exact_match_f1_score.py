"""Problem 01 — Exact Match F1 Score

Topic: 01 LLM Evaluation Science and Metrics
Target: Production-grade implementation

Compute Exact Match (EM) and token-level F1 score for QA evaluation.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def exact_match_f1_score(prediction: str, ground_truth: str) -> tuple[int, float]:
    """Exact Match is 1 if normalized strings match exactly else 0.
    Token-level F1 = 2 * P * R / (P + R) where P = overlap / len(pred), R = overlap / len(gt).
    Normalize by lowercasing and splitting into whitespace tokens.
    Returns (em, f1 rounded to 4 decimals).
    """
    raise NotImplementedError("Implement exact_match_f1_score")

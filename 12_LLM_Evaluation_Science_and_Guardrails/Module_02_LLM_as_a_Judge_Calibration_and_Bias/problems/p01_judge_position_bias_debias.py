"""Problem 01 — Judge Position Bias Debias

Topic: 02 LLM as a Judge Calibration and Bias
Target: Production-grade implementation

Average pairwise judge evaluations across swapped candidate orders to neutralize position bias.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def judge_position_bias_debias(score_ab: tuple[float, float], score_ba: tuple[float, float]) -> tuple[float, float]:
    """score_ab: (score_A, score_B) when model A presented first.
    score_ba: (score_B, score_A) when model B presented first.
    Returns debiased (final_A, final_B) by averaging score_A and score_B across both trials, rounded to 2 decimals.
    """
    raise NotImplementedError("Implement judge_position_bias_debias")

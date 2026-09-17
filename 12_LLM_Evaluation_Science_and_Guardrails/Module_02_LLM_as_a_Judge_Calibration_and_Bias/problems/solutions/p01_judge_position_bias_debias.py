"""Reference Solution — Problem 01: Judge Position Bias Debias

Topic: 02 LLM as a Judge Calibration and Bias
"""

from __future__ import annotations


def judge_position_bias_debias(score_ab: tuple[float, float], score_ba: tuple[float, float]) -> tuple[float, float]:
    a1, b1 = score_ab
    b2, a2 = score_ba
    final_a = (a1 + a2) / 2.0
    final_b = (b1 + b2) / 2.0
    return (round(final_a, 2), round(final_b, 2))

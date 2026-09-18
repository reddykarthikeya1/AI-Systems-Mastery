"""Problem 01 — Judge Position Bias Debias

Topic: 02 LLM as a Judge Calibration and Bias
Target: Production-grade implementation

Average pairwise judge evaluations across swapped candidate orders to neutralize position bias.

Example:
    >>> judge_position_bias_debias((9.0, 6.0), (8.0, 7.0))
    (8.0, 7.0)

Hints:
    Hint 1: Position bias means the same model can score differently
        depending on whether it's shown first or second — debiasing means
        averaging each model's two scores across both trials, not
        favoring either presentation order.
    Hint 2: Unpack score_ab as (a_when_first, b_when_second) and score_ba
        as (b_when_first, a_when_second), then average the two scores
        that belong to model A and, separately, the two that belong to
        model B.
    Hint 3: The two tuples are not in matching (A, B) order — score_ba is
        (score_B, score_A) because B was shown first in that trial — so
        pairing them up means unpacking score_ba's first element as B's
        score and its second element as A's, not zipping the tuples
        positionally.
"""

from __future__ import annotations


def judge_position_bias_debias(score_ab: tuple[float, float], score_ba: tuple[float, float]) -> tuple[float, float]:
    """score_ab: (score_A, score_B) when model A presented first.
    score_ba: (score_B, score_A) when model B presented first.
    Returns debiased (final_A, final_B) by averaging score_A and score_B across both trials, rounded to 2 decimals.
    """
    raise NotImplementedError("Implement judge_position_bias_debias")

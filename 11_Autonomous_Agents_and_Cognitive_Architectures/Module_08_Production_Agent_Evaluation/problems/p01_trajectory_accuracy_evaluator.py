"""Problem 01 — Trajectory Accuracy Evaluator

Topic: 08 Production Agent Evaluation
Target: Production-grade implementation

Score agent tool invocation sequence against expected golden trajectory.

Example:
    >>> trajectory_accuracy_evaluator(['search', 'scrape', 'summarize'], ['search', 'scrape', 'summarize'])
    1.0
    >>> trajectory_accuracy_evaluator(['search', 'summarize'], ['search', 'scrape', 'summarize'])
    0.3333

Hints:
    Hint 1: This scores position-by-position agreement, not set overlap —
        a correct tool call used at the wrong step still counts as a
        mismatch for that step.
    Hint 2: Use zip(agent_trajectory, golden_trajectory) to compare
        same-index pairs and count matches, then divide by the length of
        the LONGER trajectory (not the shorter one, and not the sum) so
        length mismatches are penalized too.
    Hint 3: zip() stops at the shorter sequence, so any extra steps in the
        longer trajectory are dropped from the numerator but must still
        count in the denominator (max of the two lengths) — and both
        trajectories empty is a special case that returns 1.0 instead of
        dividing by zero.
"""

from __future__ import annotations


def trajectory_accuracy_evaluator(agent_trajectory: list[str], golden_trajectory: list[str]) -> float:
    """Compute step-by-step match score:
    matches = sum(1 for a, g in zip(agent_trajectory, golden_trajectory) if a == g)
    accuracy = matches / max(len(agent_trajectory), len(golden_trajectory))
    Returns float rounded to 4 decimals (1.0 if both empty).
    """
    raise NotImplementedError("Implement trajectory_accuracy_evaluator")

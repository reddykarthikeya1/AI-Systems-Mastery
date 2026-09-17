"""Problem 01 — Trajectory Accuracy Evaluator

Topic: 08 Production Agent Evaluation
Target: Production-grade implementation

Score agent tool invocation sequence against expected golden trajectory.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def trajectory_accuracy_evaluator(agent_trajectory: list[str], golden_trajectory: list[str]) -> float:
    """Compute step-by-step match score:
    matches = sum(1 for a, g in zip(agent_trajectory, golden_trajectory) if a == g)
    accuracy = matches / max(len(agent_trajectory), len(golden_trajectory))
    Returns float rounded to 4 decimals (1.0 if both empty).
    """
    raise NotImplementedError("Implement trajectory_accuracy_evaluator")

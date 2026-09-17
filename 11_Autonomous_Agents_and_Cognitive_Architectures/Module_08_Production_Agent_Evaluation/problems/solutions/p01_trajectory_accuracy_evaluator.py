"""Reference Solution — Problem 01: Trajectory Accuracy Evaluator

Topic: 08 Production Agent Evaluation
"""

from __future__ import annotations


def trajectory_accuracy_evaluator(agent_trajectory: list[str], golden_trajectory: list[str]) -> float:
    if not agent_trajectory and not golden_trajectory:
        return 1.0
    denom = max(len(agent_trajectory), len(golden_trajectory))
    if denom == 0:
        return 1.0
    matches = sum(1 for a, g in zip(agent_trajectory, golden_trajectory) if a == g)
    return round(matches / float(denom), 4)

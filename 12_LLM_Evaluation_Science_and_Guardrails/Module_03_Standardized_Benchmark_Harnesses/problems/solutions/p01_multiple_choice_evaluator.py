"""Reference Solution — Problem 01: Multiple Choice Evaluator

Topic: 03 Standardized Benchmark Harnesses
"""

from __future__ import annotations


def multiple_choice_evaluator(predictions: list[str], ground_truths: list[str]) -> float:
    if not predictions or len(predictions) != len(ground_truths):
        return 0.0
    correct = sum(1 for p, g in zip(predictions, ground_truths) if p.strip().upper() == g.strip().upper())
    return round((correct / float(len(predictions))) * 100.0, 2)

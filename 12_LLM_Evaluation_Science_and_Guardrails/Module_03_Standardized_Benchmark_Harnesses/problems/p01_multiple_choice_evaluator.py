"""Problem 01 — Multiple Choice Evaluator

Topic: 03 Standardized Benchmark Harnesses
Target: Production-grade implementation

Calculate overall accuracy across multiple choice questions (MMLU / ARC).

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def multiple_choice_evaluator(predictions: list[str], ground_truths: list[str]) -> float:
    """Compute percentage of correct predictions (0.0 to 100.0).
    Normalize by uppercase stripping.
    Returns accuracy percentage rounded to 2 decimals.
    """
    raise NotImplementedError("Implement multiple_choice_evaluator")

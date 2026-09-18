"""Problem 01 — Multiple Choice Evaluator

Topic: 03 Standardized Benchmark Harnesses
Target: Production-grade implementation

Calculate overall accuracy across multiple choice questions (MMLU / ARC).

Example:
    >>> multiple_choice_evaluator(['A', 'b ', 'C', 'd'], ['A', 'B', 'C', 'A'])
    75.0

Hints:
    Hint 1: This is a plain per-item accuracy count, but the raw strings
        can't be compared directly — trailing whitespace and letter-case
        differences shouldn't count as wrong answers.
    Hint 2: Normalize each prediction/ground-truth pair with
        .strip().upper() before comparing with ==, count the matches, then
        divide by the total count and multiply by 100.
    Hint 3: A length mismatch between predictions and ground_truths (or an
        empty predictions list) can't be zipped safely — guard for that
        case and return 0.0 rather than raising or silently truncating to
        the shorter list.
"""

from __future__ import annotations


def multiple_choice_evaluator(predictions: list[str], ground_truths: list[str]) -> float:
    """Compute percentage of correct predictions (0.0 to 100.0).
    Normalize by uppercase stripping.
    Returns accuracy percentage rounded to 2 decimals.
    """
    raise NotImplementedError("Implement multiple_choice_evaluator")

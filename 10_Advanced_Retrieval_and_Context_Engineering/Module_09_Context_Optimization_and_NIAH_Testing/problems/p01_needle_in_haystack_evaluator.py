"""Problem 01 — Needle In Haystack Evaluator

Topic: 09 Context Optimization and NIAH Testing
Target: Production-grade implementation

Evaluate retrieval accuracy across context window depth percentages.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def needle_in_haystack_evaluator(needle: str, retrieved_contexts: list[tuple[float, str]]) -> dict[str, float]:
    """retrieved_contexts: list of (depth_percent, retrieved_text).
    For each test, check if needle in retrieved_text.
    Returns dict with 'overall_accuracy_pct' and 'min_depth_failure'.
    """
    raise NotImplementedError("Implement needle_in_haystack_evaluator")

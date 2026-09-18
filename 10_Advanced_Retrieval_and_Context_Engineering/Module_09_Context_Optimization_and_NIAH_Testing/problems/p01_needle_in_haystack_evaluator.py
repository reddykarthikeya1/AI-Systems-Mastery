"""Problem 01 — Needle In Haystack Evaluator

Topic: 09 Context Optimization and NIAH Testing
Target: Production-grade implementation

Evaluate retrieval accuracy across context window depth percentages.

Example:
    >>> needle_in_haystack_evaluator("42", [(10.0, "secret key is 42"), (50.0, "nothing here"), (90.0, "secret key is 42")])
    {'overall_accuracy_pct': 66.67, 'min_depth_failure': 50.0}

Hints:
    Hint 1: `min_depth_failure` cares about the SHALLOWEST position where
        retrieval broke down, not how many tests failed or the deepest
        failure — you need the minimum depth among only the failing tests.
    Hint 2: Make a single pass over `retrieved_contexts`: count how many
        entries contain `needle` as a substring for the accuracy figure,
        while separately tracking the running minimum `depth_percent` among
        entries where it was NOT found.
    Hint 3: An empty `retrieved_contexts` must short-circuit to
        `{'overall_accuracy_pct': 0.0, 'min_depth_failure': -1.0}` instead of
        dividing by zero; `min_depth_failure` stays `-1.0` (a sentinel for
        "no failures") when every test passes; and accuracy is a percentage
        (`passed / total * 100`) rounded to 2 decimals, not a raw fraction.
"""

from __future__ import annotations


def needle_in_haystack_evaluator(needle: str, retrieved_contexts: list[tuple[float, str]]) -> dict[str, float]:
    """retrieved_contexts: list of (depth_percent, retrieved_text).
    For each test, check if needle in retrieved_text.
    Returns dict with 'overall_accuracy_pct' and 'min_depth_failure'.
    """
    raise NotImplementedError("Implement needle_in_haystack_evaluator")

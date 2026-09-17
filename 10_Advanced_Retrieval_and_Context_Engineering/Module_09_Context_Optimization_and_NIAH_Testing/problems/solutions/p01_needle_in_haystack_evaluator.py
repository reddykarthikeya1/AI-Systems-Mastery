"""Reference Solution — Problem 01: Needle In Haystack Evaluator

Topic: 09 Context Optimization and NIAH Testing
"""

from __future__ import annotations


def needle_in_haystack_evaluator(needle: str, retrieved_contexts: list[tuple[float, str]]) -> dict[str, float]:
    if not retrieved_contexts:
        return {'overall_accuracy_pct': 0.0, 'min_depth_failure': -1.0}
    passed = 0
    min_fail = -1.0
    for depth, text in retrieved_contexts:
        if needle in text:
            passed += 1
        else:
            if min_fail < 0 or depth < min_fail:
                min_fail = depth
    acc = (passed / float(len(retrieved_contexts))) * 100.0
    return {
        'overall_accuracy_pct': round(acc, 2),
        'min_depth_failure': min_fail
    }

"""Reference solution — Problem 05: Does This Complexity Fit The Constraint?

Pattern:    Complexity analysis
Complexity: Time O(1) amortised, Space O(1)
"""

from __future__ import annotations


def fits_budget(n: int, complexity: str, budget: int = 10**8) -> bool:
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")

    log_n = max(1, n.bit_length() - 1)   # floor(log2 n), at least 1

    if complexity == "O(1)":
        ops = 1
    elif complexity == "O(log n)":
        ops = log_n
    elif complexity == "O(n)":
        ops = n
    elif complexity == "O(n log n)":
        ops = n * log_n
    elif complexity == "O(n^2)":
        ops = n * n
    elif complexity == "O(n^3)":
        ops = n * n * n
    elif complexity == "O(2^n)":
        # Short-circuit before building an astronomically large integer: if the
        # exponent alone exceeds the budget's bit length, it cannot possibly fit.
        if n > budget.bit_length() + 1:
            return False
        ops = 1 << n
    elif complexity == "O(n!)":
        if n > 25:            # 25! already dwarfs any realistic budget
            return False
        ops = 1
        for k in range(2, n + 1):
            ops *= k
            if ops > budget:
                return False
    else:
        raise ValueError(f"unsupported complexity class: {complexity!r}")

    return ops <= budget

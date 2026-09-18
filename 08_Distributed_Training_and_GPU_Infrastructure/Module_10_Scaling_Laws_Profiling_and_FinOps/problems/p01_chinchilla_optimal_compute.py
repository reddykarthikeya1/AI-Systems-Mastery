"""Problem 01 — Chinchilla Optimal Compute

Topic: 10 Scaling Laws Profiling and FinOps
Target: Production-grade implementation

Compute Chinchilla compute-optimal parameter count N and token count D for FLOP budget C.

Example:
    >>> chinchilla_optimal_compute(6.0e18)
    (1000000000.0, 1000000000.0)

Hints:
    Hint 1: Chinchilla's key finding is that compute-optimal training splits
        a fixed FLOP budget *evenly* between model size and data size — N
        and D end up equal, not one dominating the other.
    Hint 2: Since `C ~= 6*N*D` and the optimum sets `N == D`, both reduce to
        the same closed-form expression: `N = D = sqrt(flop_budget / 6.0)`.
    Hint 3: A non-positive `flop_budget` must return `(0.0, 0.0)` rather
        than calling `math.sqrt` on a negative or zero value (which would
        raise or silently return 0 in a way that hides the guard). Round
        both outputs to 2 decimals.
"""

from __future__ import annotations


def chinchilla_optimal_compute(flop_budget: float) -> tuple[float, float]:
    """Chinchilla scaling law: C ~= 6 * N * D.
    Optimal allocation: N ~= sqrt(C / 6), D ~= sqrt(C / 6).
    Returns (N_parameters, D_tokens) rounded to 2 decimals.
    """
    raise NotImplementedError("Implement chinchilla_optimal_compute")

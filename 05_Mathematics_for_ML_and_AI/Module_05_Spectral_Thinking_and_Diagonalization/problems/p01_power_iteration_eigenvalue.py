"""Problem 01 — Power Iteration Eigenvalue

Topic: 05 Spectral Thinking and Diagonalization
Target: Production-grade implementation

Compute dominant eigenvalue and eigenvector of symmetric matrix.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def power_iteration_eigenvalue(A: list[list[float]], iterations: int = 15) -> tuple[float, list[float]]:
    """Compute dominant eigenvalue lambda and normalized eigenvector v using power iteration.
    Returns (lambda_val, eigenvector) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement power_iteration_eigenvalue")

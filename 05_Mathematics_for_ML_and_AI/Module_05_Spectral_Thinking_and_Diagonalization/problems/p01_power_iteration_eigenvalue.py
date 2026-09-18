"""Problem 01 — Power Iteration Eigenvalue

Topic: 05 Spectral Thinking and Diagonalization
Target: Production-grade implementation

Compute dominant eigenvalue and eigenvector of symmetric matrix.

Example:
    >>> power_iteration_eigenvalue([[2.0, 1.0], [1.0, 2.0]], 20)
    (3.0, [0.7071, 0.7071])

Hints:
    Hint 1: Repeatedly multiplying almost any starting vector by A stretches
        it toward the direction of the dominant eigenvector, because that
        component grows fastest relative to the others with each pass.
    Hint 2: Start from a normalized vector, loop `iterations` times applying
        `A @ b` and renormalizing, then recover the eigenvalue with the
        Rayleigh quotient `b . (A @ b)` on the final (unit-length) vector.
    Hint 3: Renormalizing requires dividing by the vector's norm each pass —
        guard against a near-zero norm (e.g. A is the zero matrix) so you
        don't divide by ~0, and round the eigenvalue and each eigenvector
        component to 4 decimal places.
"""

from __future__ import annotations


def power_iteration_eigenvalue(A: list[list[float]], iterations: int = 15) -> tuple[float, list[float]]:
    """Compute dominant eigenvalue lambda and normalized eigenvector v using power iteration.
    Returns (lambda_val, eigenvector) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement power_iteration_eigenvalue")

"""Reference Solution — Problem 01: Power Iteration Eigenvalue

Topic: 05 Spectral Thinking and Diagonalization
"""

from __future__ import annotations


def power_iteration_eigenvalue(A: list[list[float]], iterations: int = 15) -> tuple[float, list[float]]:
    import math
    n = len(A)
    b_k = [1.0 / math.sqrt(n)] * n
    for _ in range(iterations):
        # A * b_k
        A_b = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x * x for x in A_b))
        if norm < 1e-9:
            break
        b_k = [x / norm for x in A_b]
    # Rayleigh quotient
    A_b = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
    eigenval = sum(b_k[i] * A_b[i] for i in range(n))
    return (round(eigenval, 4), [round(x, 4) for x in b_k])

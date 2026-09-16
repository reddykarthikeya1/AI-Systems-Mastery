"""Power iteration with three planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations

import math


def matvec(matrix, v):
    return [sum(matrix[i][j] * v[j] for j in range(len(v))) for i in range(len(matrix))]


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def power_iteration(matrix, iterations=200):
    """Dominant eigenvector by repeated multiplication."""
    v = [1.0] * len(matrix)
    for _ in range(iterations):
        v = matvec(matrix, v)
    return v


def rayleigh(matrix, v):
    """Eigenvalue estimate for an eigenvector v."""
    av = matvec(matrix, v)
    return sum(a * b for a, b in zip(av, v))


def converged(previous, current, tol=1e-10):
    return max(abs(a - b) for a, b in zip(previous, current)) < tol


def main():
    print("=" * 66)
    print("POWER ITERATION - dominant eigenpair report")
    print("=" * 66)

    print()
    print("[1] A small symmetric matrix")
    m = [[2.0, 1.0], [1.0, 2.0]]
    v = power_iteration(m, iterations=60)
    print(f"    raw vector after 60 iterations: {[f'{x:.3e}' for x in v]}")
    length = norm(v)
    unit = [x / length for x in v] if length else v
    print(f"    normalised: {[round(x, 6) for x in unit]}")
    print(f"    eigenvalue estimate: {rayleigh(m, unit):.6f}   (true value 3.0)")

    print()
    print("[2] More iterations on the same matrix")
    for n in (200, 400, 700):
        vn = power_iteration(m, iterations=n)
        print(f"    after {n:>3} iterations, first component = {vn[0]:.6e}")

    print()
    print("[3] Convergence test on an oscillating eigenvector")
    osc = [[0.0, 1.0], [1.0, 0.0]]
    a = [1.0, -1.0]
    b = [-1.0, 1.0]
    print(f"    v        = {a}")
    print(f"    A @ v    = {matvec(osc, a)}   (same direction, opposite sign)")
    print(f"    converged(v, A@v) reports: {converged(a, matvec(osc, a))}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

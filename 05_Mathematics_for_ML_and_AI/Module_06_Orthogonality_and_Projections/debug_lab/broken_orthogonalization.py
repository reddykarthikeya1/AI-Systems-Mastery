"""A Gram-Schmidt implementation with three planted defects.

It runs to completion, raises nothing and exits 0. Every number it prints is
plausible. Three of them are wrong.
"""
from __future__ import annotations

import math


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def norm(v):
    return math.sqrt(dot(v, v))


def scale(v, k):
    return [a * k for a in v]


def subtract(u, v):
    return [a - b for a, b in zip(u, v)]


def project(v, onto):
    """The component of v along `onto`."""
    return scale(onto, dot(v, onto))


def classical_gram_schmidt(vectors):
    basis = []
    for v in vectors:
        w = v[:]
        for b in basis:
            w = subtract(w, project(v, b))
        length = norm(w)
        if length > 0:
            basis.append(scale(w, 1.0 / length))
    return basis


def max_off_diagonal(basis):
    worst = 0.0
    for i, u in enumerate(basis):
        for j, v in enumerate(basis):
            if i != j:
                worst = max(worst, abs(dot(u, v)))
    return worst


def main():
    print("=" * 66)
    print("ORTHOGONALIZER - basis quality report")
    print("=" * 66)

    print()
    print("[1] Three well-separated vectors")
    easy = [[1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]]
    basis = classical_gram_schmidt(easy)
    print(f"    vectors in: {len(easy)}, basis out: {len(basis)}")
    print(f"    worst |dot| between distinct basis vectors: {max_off_diagonal(basis):.2e}")
    print(f"    norms: {[round(norm(b), 12) for b in basis]}")

    print()
    print("[2] Nearly parallel vectors")
    eps = 1e-8
    hard = [[1.0, eps, 0.0], [1.0, 0.0, eps], [1.0, 0.0, 0.0]]
    basis2 = classical_gram_schmidt(hard)
    print(f"    vectors in: {len(hard)}, basis out: {len(basis2)}")
    print(f"    worst |dot| between distinct basis vectors: {max_off_diagonal(basis2):.2e}")

    print()
    print("[3] A linearly dependent input")
    dependent = [[1.0, 0.0], [2.0, 0.0], [0.0, 1.0]]
    basis3 = classical_gram_schmidt(dependent)
    print(f"    vectors in: {len(dependent)} (rank is 2)")
    print(f"    basis out: {len(basis3)}")
    print(f"    worst |dot|: {max_off_diagonal(basis3):.2e}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

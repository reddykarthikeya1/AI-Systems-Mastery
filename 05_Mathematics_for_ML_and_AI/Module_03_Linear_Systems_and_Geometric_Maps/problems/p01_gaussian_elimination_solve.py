"""Problem 01 — Gaussian Elimination Solve

Topic: 03 Linear Systems and Geometric Maps
Target: Production-grade implementation

Solve 2x2 or 3x3 system of linear equations Ax = b using Gaussian elimination.

Example:
    >>> gaussian_elimination_solve([[2.0, 1.0], [1.0, 3.0]], [5.0, 5.0])
    [2.0, 1.0]

Hints:
    Hint 1: Row operations (swapping rows, subtracting a multiple of one row
        from another) don't change the solution set, so you can freely
        reshape A and b together as long as you treat each row as one unit.
    Hint 2: Build the augmented matrix [A | b], eliminate downward column by
        column to reach upper-triangular form, then solve for x from the
        bottom row upward via back substitution.
    Hint 3: If a pivot is (near) zero, dividing by it blows up or raises a
        ZeroDivisionError — swap in a row below with a larger entry in that
        column first (partial pivoting) instead of dividing by the tiny
        value, and round each solved component to 4 decimal places.
"""

from __future__ import annotations


def gaussian_elimination_solve(A: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b for square matrix A and vector b.
    Returns solution vector x.
    """
    raise NotImplementedError("Implement gaussian_elimination_solve")

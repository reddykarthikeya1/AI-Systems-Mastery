"""A Gaussian elimination solver with three planted defects.

It runs to completion, raises nothing and exits 0. Every number it prints is
plausible. Three of them are wrong.
"""
from __future__ import annotations


def solve(matrix, rhs):
    """Gaussian elimination with back substitution."""
    n = len(matrix)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]

    for col in range(n):
        pivot_row = col
        for row in range(col, n):
            if a[row][col] != 0:
                pivot_row = row
                break
        a[col], a[pivot_row] = a[pivot_row], a[col]

        for row in range(col + 1, n):
            factor = a[row][col] / a[col][col]
            for k in range(col, n + 1):
                a[row][k] -= factor * a[col][k]

    x = [0.0] * n
    for row in range(n - 1, -1, -1):
        total = sum(a[row][k] * x[k] for k in range(row + 1, n))
        x[row] = (a[row][n] - total) / a[row][row]
    return x


def is_singular(matrix):
    """True if the system has no unique solution."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    for col in range(n):
        for row in range(col + 1, n):
            if a[col][col] == 0:
                continue
            factor = a[row][col] / a[col][col]
            for k in range(n):
                a[row][k] -= factor * a[col][k]
    return any(a[i][i] == 0 for i in range(n))


def residual(matrix, x, rhs):
    return max(abs(sum(matrix[i][j] * x[j] for j in range(len(x))) - rhs[i])
               for i in range(len(rhs)))


def main():
    print("=" * 66)
    print("LINEAR SOLVER - accuracy report")
    print("=" * 66)

    print()
    print("[1] A well-conditioned 3x3 system")
    m = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
    b = [8.0, -11.0, -3.0]
    x = solve(m, b)
    print(f"    solution: {[round(v, 6) for v in x]}")
    print(f"    expected: [2.0, 3.0, -1.0]")
    print(f"    residual: {residual(m, x, b):.2e}")

    print()
    print("[2] The same system with a tiny leading pivot")
    m2 = [[1e-18, 1.0], [1.0, 1.0]]
    b2 = [1.0, 2.0]
    x2 = solve(m2, b2)
    print(f"    solution: {[round(v, 8) for v in x2]}")
    print(f"    exact answer is approximately [1.0, 1.0]")
    print(f"    residual: {residual(m2, x2, b2):.2e}")

    print()
    print("[3] Detecting a singular system")
    almost = [[1.0, 2.0], [1.0, 2.0000000001]]
    exact = [[1.0, 2.0], [2.0, 4.0]]
    print(f"    rows [1,2] and [2,4]              -> singular? {is_singular(exact)}")
    print(f"    rows [1,2] and [1,2.0000000001]   -> singular? {is_singular(almost)}")
    xs = solve(almost, [3.0, 3.0])
    print(f"    solving it with b=[3, 3]           -> {[round(v, 2) for v in xs]}")
    xs2 = solve(almost, [3.0, 3.000000001])
    print(f"    nudging b by 1e-9                  -> {[round(v, 2) for v in xs2]}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

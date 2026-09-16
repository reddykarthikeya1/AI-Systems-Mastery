"""A rank analyser with two planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations


def row_echelon(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        target = None
        for r in range(pivot_row, rows):
            if a[r][col] != 0:
                target = r
                break
        if target is None:
            continue
        a[pivot_row], a[target] = a[target], a[pivot_row]
        for r in range(pivot_row + 1, rows):
            factor = a[r][col] / a[pivot_row][col]
            for k in range(cols):
                a[r][k] -= factor * a[pivot_row][k]
        pivot_row += 1
    return a


def rank(matrix):
    """Number of non-zero rows after elimination."""
    return sum(1 for row in row_echelon(matrix) if any(v != 0 for v in row))


def nullity(matrix):
    """dim(null space) = number of columns - rank."""
    return len(matrix) - rank(matrix)


def main():
    print("=" * 66)
    print("RANK ANALYSER - feature matrix report")
    print("=" * 66)

    print()
    print("[1] An obviously rank-deficient matrix")
    m = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0]]
    print(f"    rows: {m}")
    print(f"    rank reported: {rank(m)}   (row 2 is exactly 2x row 1)")

    print()
    print("[2] The same structure, with rounding")
    m2 = [[0.1, 0.2, 0.3], [0.3, 0.6, 0.9], [1.0, 1.0, 1.0]]
    print(f"    rows: {m2}")
    print(f"    rank reported: {rank(m2)}   (row 2 is exactly 3x row 1)")
    reduced = row_echelon(m2)
    print(f"    last row after elimination: {[f'{v:.3e}' for v in reduced[-1]]}")

    print()
    print("[3] Rank-nullity on a wide matrix")
    wide = [[1.0, 0.0, 2.0, 3.0], [0.0, 1.0, 1.0, 1.0]]
    print(f"    shape: {len(wide)} rows x {len(wide[0])} columns")
    print(f"    rank: {rank(wide)}")
    print(f"    nullity reported: {nullity(wide)}")
    print(f"    rank + nullity = {rank(wide) + nullity(wide)}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

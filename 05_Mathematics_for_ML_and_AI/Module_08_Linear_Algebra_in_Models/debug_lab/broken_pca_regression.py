"""PCA and normal-equation regression with two planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations


def column_means(x):
    n = len(x)
    return [sum(row[j] for row in x) / n for j in range(len(x[0]))]


def covariance(x):
    """Sample covariance of the columns of x."""
    n = len(x)
    cols = len(x[0])
    out = [[0.0] * cols for _ in range(cols)]
    for i in range(cols):
        for j in range(cols):
            out[i][j] = sum(row[i] * row[j] for row in x) / (n - 1)
    return out


def transpose(m):
    return [list(col) for col in zip(*m)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def solve_2x2(a, b):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        return [0.0, 0.0]
    return [(b[0] * a[1][1] - b[1] * a[0][1]) / det,
            (b[1] * a[0][0] - b[0] * a[1][0]) / det]


def fit_normal_equation(x, y):
    """Least squares via (X^T X) beta = X^T y."""
    xt = transpose(x)
    xtx = matmul(xt, x)
    xty = [sum(xt[i][k] * y[k] for k in range(len(y))) for i in range(len(xt))]
    return solve_2x2(xtx, xty)


def main():
    print("=" * 66)
    print("PCA + REGRESSION - model fitting report")
    print("=" * 66)

    data = [[10.0, 20.1], [10.2, 20.5], [9.8, 19.6], [10.1, 20.3], [9.9, 19.9]]

    print()
    print("[1] The data")
    print(f"    rows: {len(data)}")
    print(f"    column means: {[round(v, 3) for v in column_means(data)]}")
    print(f"    the two columns are near-perfectly correlated (col2 ~ 2 x col1)")

    print()
    print("[2] Covariance matrix used for PCA")
    cov = covariance(data)
    for row in cov:
        print(f"    {[round(v, 4) for v in row]}")
    print(f"    off-diagonal (should be a small covariance): {cov[0][1]:.4f}")

    print()
    print("[3] Least squares on near-collinear features")
    x = [[1.0, 2.0], [2.0, 4.001], [3.0, 6.0], [4.0, 8.002]]
    y = [1.0, 2.0, 3.0, 4.0]
    beta = fit_normal_equation(x, y)
    print(f"    fitted coefficients: {[round(b, 4) for b in beta]}")
    fitted = [sum(xi[j] * beta[j] for j in range(2)) for xi in x]
    print(f"    predictions: {[round(v, 4) for v in fitted]}")
    print(f"    targets    : {y}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

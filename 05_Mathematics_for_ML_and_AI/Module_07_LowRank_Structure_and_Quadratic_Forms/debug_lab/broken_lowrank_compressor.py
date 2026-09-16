"""A low-rank truncation with two planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations


def fake_svd(matrix):
    """Stand-in for an SVD: returns singular values in DESCENDING order.

    Hard-coded so the lab has no dependencies. The ordering convention is the
    real one: numpy.linalg.svd also returns descending singular values.
    """
    singular_values = [50.0, 12.0, 3.0, 0.4, 0.05]
    return singular_values


def energy_kept(singular_values, k):
    """Fraction of the total 'energy' retained by keeping k components."""
    total = sum(s * s for s in singular_values)
    kept = sum(s * s for s in singular_values[-k:])
    return kept / total


def choose_rank(singular_values, target=0.99):
    """Smallest k whose retained energy reaches the target."""
    for k in range(1, len(singular_values) + 1):
        if energy_kept(singular_values, k) >= target:
            return k
    return len(singular_values)


def compression_ratio(rows, cols, k):
    """Parameters in the factored form versus the dense form."""
    return (rows * cols) / (k * (rows + cols))


def main():
    print("=" * 66)
    print("LOW-RANK COMPRESSOR - truncation report")
    print("=" * 66)

    values = fake_svd(None)

    print()
    print("[1] The singular values")
    print(f"    {values}")
    print(f"    total energy: {sum(s * s for s in values):.2f}")

    print()
    print("[2] Energy retained by keeping k components")
    for k in (1, 2, 3, 4, 5):
        print(f"    k={k}: {energy_kept(values, k):.6f}")

    print()
    print("[3] Choosing a rank and the compression it buys")
    k = choose_rank(values, target=0.99)
    print(f"    rank chosen for 99% energy: {k}")
    print(f"    a 1000x1000 weight matrix at that rank:")
    print(f"      dense parameters  : {1000 * 1000:,}")
    print(f"      factored parameters: {k * (1000 + 1000):,}")
    print(f"      compression ratio : {compression_ratio(1000, 1000, k):.1f}x")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()

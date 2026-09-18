# Debug Lab: Tiled Matmul Only Keeps the Last K-Tile's Contribution
# Course 07 - Module 05 Tiled Matrix Multiplication (GEMM)

def reference_matmul(a, b):
    n, k, m = len(a), len(b), len(b[0])
    return [[sum(a[i][t] * b[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def tiled_matmul(a, b, tile_size):
    n, k, m = len(a), len(b), len(b[0])
    c = [[0.0] * m for _ in range(n)]
    for i0 in range(0, n, tile_size):
        for j0 in range(0, m, tile_size):
            for t0 in range(0, k, tile_size):
                for i in range(i0, i0 + tile_size):
                    for j in range(j0, j0 + tile_size):
                        acc = 0.0
                        for t in range(t0, t0 + tile_size):
                            acc += a[i][t] * b[t][j]
                        c[i][j] = acc
    return c


if __name__ == "__main__":
    n = 4  # evenly divisible by tile_size, so tile boundaries line up cleanly
    a = [[float(i + j) for j in range(n)] for i in range(n)]
    b = [[float(i - j + 1) for j in range(n)] for i in range(n)]

    expected = reference_matmul(a, b)
    actual = tiled_matmul(a, b, tile_size=2)
    mismatches = sum(
        1 for i in range(n) for j in range(n) if abs(actual[i][j] - expected[i][j]) > 1e-9
    )

    print(f"Tiled matmul (tile_size=2) vs triple-loop reference on a {n}x{n} x {n}x{n} product:")
    for i in range(n):
        print(f"  row {i}: reference={[round(v, 1) for v in expected[i]]}  tiled={[round(v, 1) for v in actual[i]]}")
    print(f"Mismatched entries: {mismatches} of {n * n}")

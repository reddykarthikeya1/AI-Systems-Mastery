"""Chapter 18 - High-performance computing with NumPy (needs numpy; the runner skips this chapter without it).

1. pairwise_distances: Euclidean distance matrix with broadcasting and no Python loops.
2. moving_average: sliding mean via cumulative sums.
3. normalize_columns (debugging): crashes or corrupts its input for integer arrays.
"""
import numpy as np

BUGGY = {
    "normalize_columns": '''def normalize_columns(a):
    """Return a NEW float array where every column has mean 0 and standard deviation 1 (constant columns become all 0).
    The input array must not be modified."""
    a -= a.mean(axis=0)
    std = a.std(axis=0)
    a /= np.where(std == 0, 1, std)
    return a''',
}


def pairwise_distances(points):
    """`points` is an (n, d) array. Return the (n, n) matrix of Euclidean distances. No Python-level loops over rows."""
    p = np.asarray(points, dtype=float)
    diff = p[:, None, :] - p[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def moving_average(x, w):
    """Mean of every window of w consecutive values: a float array of length len(x) - w + 1.
    w < 1 or w > len(x) raises ValueError. Must be O(n), not O(n*w)."""
    x = np.asarray(x, dtype=float)
    if w < 1 or w > len(x):
        raise ValueError("bad window")
    c = np.concatenate(([0.0], np.cumsum(x)))
    return (c[w:] - c[:-w]) / w


def normalize_columns(a):
    """Return a NEW float array where every column has mean 0 and standard deviation 1 (constant columns become all 0).
    The input array must not be modified."""
    a = np.asarray(a, dtype=float)
    centered = a - a.mean(axis=0)
    std = centered.std(axis=0)
    return centered / np.where(std == 0, 1, std)


def t_pairwise_matches_loops(m):
    rng = np.random.default_rng(0)
    pts = rng.random((30, 4))
    ref = np.array([[np.linalg.norm(a - b) for b in pts] for a in pts])
    assert np.allclose(m.pairwise_distances(pts), ref)
    assert np.allclose(m.pairwise_distances([[0, 0], [3, 4]]), [[0, 5], [5, 0]])


def t_pairwise_is_vectorised(m):
    import time
    pts = np.random.default_rng(1).random((600, 3))
    t0 = time.perf_counter()
    d = m.pairwise_distances(pts)
    assert d.shape == (600, 600) and time.perf_counter() - t0 < 1.0


def t_moving_average_values_and_errors(m):
    assert np.allclose(m.moving_average([1, 2, 3, 4, 5], 2), [1.5, 2.5, 3.5, 4.5])
    assert np.allclose(m.moving_average([5, 5, 5], 3), [5])
    for w in (0, 4):
        try:
            m.moving_average([1, 2, 3], w)
        except ValueError:
            continue
        raise AssertionError("bad window must raise")


def t_moving_average_is_linear_time(m):
    import time
    x = np.random.default_rng(2).random(2_000_000)
    t0 = time.perf_counter()
    out = m.moving_average(x, 1000)
    assert len(out) == len(x) - 999 and time.perf_counter() - t0 < 1.0


def t_normalize_columns_new_array_and_ints(m):
    a = np.array([[1, 10, 5], [2, 20, 5], [3, 30, 5]])
    orig = a.copy()
    out = m.normalize_columns(a)
    assert (a == orig).all() and out is not a
    assert np.allclose(out.mean(axis=0), 0) and np.allclose(out.std(axis=0), [1, 1, 0])

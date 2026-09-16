"""Tests for Module 22 - the native Rust accelerator.

Three distinct kinds of test live here, and the distinction matters:

1. **Correctness** of the pure-Python reference (always runs).
2. **Equivalence** - the Rust backend must agree with the Python oracle bit for
   bit. Skipped when the extension is not built.
3. **Performance** (``@pytest.mark.perf``) - the native path must actually BE
   faster. These fail loudly if an "optimisation" is a regression, which is how
   the old ctypes implementation slipped through unnoticed.

Run everything:            pytest test_native_accelerator.py -v
Skip the slow perf tests:  pytest test_native_accelerator.py -m "not perf"
"""

from __future__ import annotations

import time

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from native_accelerator import (
    PyAccelerator,
    PyRollingStats,
    benchmark,
    load_backend,
    rust_available,
)

# Marks every Rust test as skipped-with-a-reason instead of failing on a fresh clone.
requires_rust = pytest.mark.skipif(
    not rust_available(),
    reason="Rust extension not built - run: cd rust_accelerator && maturin develop --release",
)

PY = PyAccelerator()


# ===========================================================================
# 1. CORRECTNESS OF THE PYTHON REFERENCE
# ===========================================================================


def test_fnv1a_known_vector() -> None:
    """FNV-1a has published test vectors; verify against one."""
    # The empty string must hash to the offset basis itself.
    assert PY.fnv1a_64(b"") == 0xCBF29CE484222325
    # "a" -> published FNV-1a 64 value.
    assert PY.fnv1a_64(b"a") == 0xAF63DC4C8601EC8C


def test_fnv1a_is_deterministic_and_sensitive() -> None:
    assert PY.fnv1a_64(b"payload") == PY.fnv1a_64(b"payload")
    assert PY.fnv1a_64(b"payload") != PY.fnv1a_64(b"payloaD")


def test_fnv1a_stays_in_64_bits() -> None:
    """A wrap bug here is invisible until it silently truncates. Pin it."""
    for data in (b"", b"x", b"x" * 1000, bytes(range(256))):
        assert 0 <= PY.fnv1a_64(data) <= 0xFFFFFFFFFFFFFFFF


def test_dot_product_basic() -> None:
    assert PY.dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == 32.0


def test_dot_product_empty_is_zero() -> None:
    assert PY.dot_product([], []) == 0


def test_dot_product_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError, match="equal length"):
        PY.dot_product([1.0, 2.0], [1.0])


def test_count_primes_known_values() -> None:
    # pi(10)=4, pi(100)=25, pi(1000)=168 - standard prime-counting values.
    assert PY.count_primes(10) == 4
    assert PY.count_primes(100) == 25
    assert PY.count_primes(1000) == 168


def test_count_primes_degenerate_limits() -> None:
    assert PY.count_primes(0) == 0
    assert PY.count_primes(2) == 0
    assert PY.count_primes(3) == 1


def test_sum_of_squares() -> None:
    # 0+1+4+9+16 = 30
    assert PY.sum_of_squares(5) == 30
    assert PY.sum_of_squares(0) == 0


# ===========================================================================
# 2. ROLLING STATISTICS (Welford)
# ===========================================================================


def test_rolling_stats_matches_textbook_variance() -> None:
    stats = PyRollingStats()
    stats.extend([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    assert stats.count == 8
    assert stats.mean == pytest.approx(5.0)
    # Bessel-corrected sample variance of that classic dataset is 32/7.
    assert stats.variance == pytest.approx(32 / 7)


def test_rolling_stats_variance_undefined_below_two_samples() -> None:
    stats = PyRollingStats()
    assert stats.variance is None
    stats.push(1.0)
    assert stats.variance is None
    stats.push(3.0)
    assert stats.variance == pytest.approx(2.0)


@given(st.lists(st.floats(min_value=-1e6, max_value=1e6, allow_nan=False), min_size=2, max_size=200))
@settings(max_examples=50, deadline=None)
def test_rolling_mean_matches_naive_mean(xs: list[float]) -> None:
    """Property: Welford's streaming mean equals the naive mean."""
    stats = PyRollingStats()
    stats.extend(xs)
    assert stats.mean == pytest.approx(sum(xs) / len(xs), rel=1e-9, abs=1e-6)


# ===========================================================================
# 3. EQUIVALENCE: Rust must agree with the Python oracle
# ===========================================================================


@requires_rust
def test_backend_selection_prefers_rust_when_built() -> None:
    assert load_backend().name == "rust"
    assert load_backend(prefer_rust=False).name == "python"


@requires_rust
@pytest.mark.parametrize(
    "payload",
    [b"", b"a", b"hello world", bytes(range(256)), b"\x00" * 64, b"\xff" * 64],
)
def test_rust_fnv1a_matches_python(payload: bytes) -> None:
    assert load_backend().fnv1a_64(payload) == PY.fnv1a_64(payload)


@requires_rust
@given(st.binary(max_size=512))
@settings(max_examples=60, deadline=None)
def test_rust_fnv1a_matches_python_property(payload: bytes) -> None:
    """Property-based equivalence - the strongest guarantee available here."""
    assert load_backend().fnv1a_64(payload) == PY.fnv1a_64(payload)


@requires_rust
@pytest.mark.parametrize("limit", [0, 2, 3, 10, 100, 1000, 5000])
def test_rust_count_primes_matches_python(limit: int) -> None:
    assert load_backend().count_primes(limit) == PY.count_primes(limit)


@requires_rust
def test_rust_dot_product_matches_python() -> None:
    a = [1.5, -2.0, 3.25, 0.0, 7.125]
    b = [2.0, 1.5, -2.0, 100.0, 0.5]
    assert load_backend().dot_product(a, b) == pytest.approx(PY.dot_product(a, b))


@requires_rust
def test_rust_dot_product_raises_valueerror_like_python() -> None:
    """Rust `Err` must surface as a real Python ValueError, not a panic."""
    with pytest.raises(ValueError, match="equal length"):
        load_backend().dot_product([1.0, 2.0], [1.0])


@requires_rust
def test_rust_rolling_stats_matches_python() -> None:
    import rust_accelerator

    samples = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    rs = rust_accelerator.RollingStats()
    rs.extend(samples)
    py = PyRollingStats()
    py.extend(samples)
    assert rs.count == py.count
    assert rs.mean == pytest.approx(py.mean)
    assert rs.variance == pytest.approx(py.variance)


# ===========================================================================
# 4. PERFORMANCE ASSERTIONS - these catch a fake "optimisation"
# ===========================================================================


@requires_rust
@pytest.mark.perf
@pytest.mark.slow
def test_rust_is_substantially_faster_on_cpu_bound_work() -> None:
    """The whole point of Module 22. If this fails, the native path is a lie.

    The threshold is deliberately conservative (5x). Measured speedup on a
    typical dev machine is 25-40x; anything under 5x means the FFI overhead is
    dominating or the Rust build was made in debug mode (forgot --release).
    """
    res = benchmark(limit=120_000, repeats=3)
    assert "rust_ms" in res, "Rust backend reported as available but did not benchmark"
    assert res["speedup"] > 5.0, (
        f"native backend only {res['speedup']:.2f}x faster "
        f"(python={res['python_ms']:.1f}ms rust={res['rust_ms']:.1f}ms). "
        "Did you build with --release?"
    )


@requires_rust
@pytest.mark.perf
@pytest.mark.slow
def test_gil_is_actually_released() -> None:
    """Two threads running `count_primes` must overlap in wall-clock time.

    Pure-Python CPU work cannot do this: the GIL serialises it. If this test
    fails, `py.allow_threads()` was dropped from lib.rs and the extension is
    holding the interpreter hostage.
    """
    import threading

    backend = load_backend()
    limit = 500_000

    t0 = time.perf_counter()
    backend.count_primes(limit)
    serial_one = time.perf_counter() - t0

    threads = [threading.Thread(target=backend.count_primes, args=(limit,)) for _ in range(4)]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    parallel_four = time.perf_counter() - t0

    # With the GIL released, 4 threads on a multicore box finish in well under
    # 4x the single-run time. Allow 3.5x to tolerate thread creation overhead on Windows and 2-core CI runners.
    assert parallel_four < serial_one * 3.5, (
        f"4 threads took {parallel_four * 1000:.0f}ms vs {serial_one * 1000:.0f}ms for one - "
        "the GIL does not appear to be released (check py.allow_threads in lib.rs)"
    )

#!/usr/bin/env python3
"""Module 22 - Native Acceleration: Pure-Python reference vs. real Rust extension.

This file deliberately contains NO fake acceleration. It holds two things:

1. ``PyAccelerator`` - a correct, idiomatic **pure-Python** implementation. This is
   the baseline you are trying to beat, and the oracle that proves the Rust
   version is correct.
2. ``load_backend()`` - imports the compiled Rust extension when it is available
   and transparently falls back to ``PyAccelerator`` when it is not.

Why no ctypes here?
-------------------
A previous version of this project used ``ctypes.c_double * n`` arrays and then
looped over them **in Python**::

    c_a = (ctypes.c_double * size)(*vec_a)
    for i in range(size):
        total += c_a[i] * c_b[i]      # <-- allocates a Python float per access

That is *slower* than plain Python lists, because every ``c_a[i]`` boxes a fresh
Python object. Wrapping data in a C type does not make Python code native. Real
acceleration requires the **loop itself** to run in compiled code - which is
exactly what ``rust_accelerator/src/lib.rs`` does. See ``01_ctypes_honest_demo.py``
for what ctypes is genuinely good at (calling existing C libraries).

Build the Rust backend
----------------------
::

    cd rust_accelerator
    maturin develop --release

On Windows + OneDrive, first redirect the build dir out of the synced folder::

    $env:CARGO_TARGET_DIR = "$env:LOCALAPPDATA\\cargo-target"

(see TROUBLESHOOTING_AND_EDGE_CASES.md - OneDrive locks the linker output).
"""

from __future__ import annotations

import time
from typing import Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# The contract both backends satisfy (Module 23 teaches Protocols in depth).
# ---------------------------------------------------------------------------


@runtime_checkable
class AcceleratorBackend(Protocol):
    """Structural type implemented by both the Python and Rust backends."""

    name: str

    def fnv1a_64(self, data: bytes) -> int: ...
    def dot_product(self, a: list[float], b: list[float]) -> float: ...
    def count_primes(self, limit: int) -> int: ...
    def sum_of_squares(self, n: int) -> int: ...


# ---------------------------------------------------------------------------
# 1. PURE-PYTHON REFERENCE IMPLEMENTATION
# ---------------------------------------------------------------------------

_FNV_OFFSET_BASIS = 0xCBF29CE484222325
_FNV_PRIME = 0x100000001B3
_U64_MASK = 0xFFFFFFFFFFFFFFFF


class PyAccelerator:
    """Correct, idiomatic pure-Python implementation: the baseline and the oracle."""

    name = "python"

    @staticmethod
    def fnv1a_64(data: bytes) -> int:
        """FNV-1a 64-bit hash. Iterates ``bytes`` directly - no ctypes theatre."""
        h = _FNV_OFFSET_BASIS
        for byte in data:
            h = ((h ^ byte) * _FNV_PRIME) & _U64_MASK
        return h

    @staticmethod
    def dot_product(a: list[float], b: list[float]) -> float:
        """Dot product of two equal-length vectors."""
        if len(a) != len(b):
            raise ValueError(f"vectors must be equal length (got {len(a)} and {len(b)})")
        # zip+sum is the fastest pure-Python form: the iteration runs in C, but
        # every multiply still allocates. Compare with Rust to see what is left.
        return sum(x * y for x, y in zip(a, b, strict=True))

    @staticmethod
    def count_primes(limit: int) -> int:
        """Trial division - deliberately CPU-bound, and holds the GIL throughout."""
        count = 0
        for n in range(2, limit):
            if n < 4:
                count += 1
                continue
            if n % 2 == 0:
                continue
            d = 3
            while d * d <= n:
                if n % d == 0:
                    break
                d += 2
            else:
                count += 1
        return count

    @staticmethod
    def sum_of_squares(n: int) -> int:
        """Sum of i*i for i in range(n), wrapped to 64 bits."""
        total = 0
        for i in range(n):
            total = (total + (i * i)) & _U64_MASK
        return total


class PyRollingStats:
    """Welford's online algorithm in Python - mirrors the Rust ``#[pyclass]``."""

    def __init__(self) -> None:
        self._count = 0
        self._mean = 0.0
        self._m2 = 0.0

    def push(self, x: float) -> None:
        """Feed one sample into the accumulator."""
        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        self._m2 += delta * (x - self._mean)

    def extend(self, xs: list[float]) -> None:
        """Feed a whole batch of samples."""
        for x in xs:
            self.push(x)

    @property
    def count(self) -> int:
        return self._count

    @property
    def mean(self) -> float:
        return self._mean

    @property
    def variance(self) -> float | None:
        """Bessel-corrected sample variance; None until 2 samples exist."""
        return None if self._count < 2 else self._m2 / (self._count - 1)

    def __repr__(self) -> str:
        return f"PyRollingStats(count={self._count}, mean={self._mean:.6f})"


# ---------------------------------------------------------------------------
# 2. BACKEND LOADING
# ---------------------------------------------------------------------------


class _RustAdapter:
    """Adapts the flat Rust module to the ``AcceleratorBackend`` Protocol."""

    name = "rust"

    def __init__(self, mod: object) -> None:
        self._m = mod

    def fnv1a_64(self, data: bytes) -> int:
        return int(self._m.fnv1a_64(data))  # type: ignore[attr-defined]

    def dot_product(self, a: list[float], b: list[float]) -> float:
        return float(self._m.dot_product(a, b))  # type: ignore[attr-defined]

    def count_primes(self, limit: int) -> int:
        return int(self._m.count_primes(limit))  # type: ignore[attr-defined]

    def sum_of_squares(self, n: int) -> int:
        return int(self._m.sum_of_squares(n))  # type: ignore[attr-defined]

    @property
    def RollingStats(self) -> type:
        return self._m.RollingStats  # type: ignore[attr-defined]


def rust_available() -> bool:
    """True when the compiled extension can be imported."""
    try:
        import rust_accelerator  # noqa: F401
    except ImportError:
        return False
    return True


def load_backend(*, prefer_rust: bool = True) -> AcceleratorBackend:
    """Return the Rust backend if built, else the pure-Python fallback.

    This is the production pattern: ship a native fast path, but never make it a
    hard requirement. Users on a platform without a prebuilt wheel still get a
    working library - just slower.
    """
    if prefer_rust:
        try:
            import rust_accelerator

            return _RustAdapter(rust_accelerator)
        except ImportError:
            pass
    return PyAccelerator()


# ---------------------------------------------------------------------------
# 3. HONEST BENCHMARKING
# ---------------------------------------------------------------------------


def _time_once(fn, *args) -> float:  # type: ignore[no-untyped-def]
    t0 = time.perf_counter()
    fn(*args)
    return time.perf_counter() - t0


def benchmark(limit: int = 150_000, repeats: int = 3) -> dict[str, float]:
    """Time both backends on the same CPU-bound workload.

    Uses ``perf_counter`` and takes the **minimum** of N runs - the standard way
    to suppress scheduler noise (Module 20 covers this in depth).
    """
    py = PyAccelerator()
    results: dict[str, float] = {}

    best_py = min(_time_once(py.count_primes, limit) for _ in range(repeats))
    results["python_ms"] = best_py * 1000

    if rust_available():
        rs = load_backend()
        best_rs = min(_time_once(rs.count_primes, limit) for _ in range(repeats))
        results["rust_ms"] = best_rs * 1000
        results["speedup"] = best_py / best_rs
    return results


def main() -> None:
    print("=" * 68)
    print("   MODULE 22 - NATIVE RUST ACCELERATOR vs PURE PYTHON")
    print("=" * 68)

    backend = load_backend()
    print(f"\nActive backend : {backend.name}")
    print(f"Rust built     : {rust_available()}")
    if not rust_available():
        print("\n  -> Build it:  cd rust_accelerator && maturin develop --release")

    payload = b"Modern CPython Internals and Native Extensions"
    print(f"\nFNV-1a hash    : 0x{backend.fnv1a_64(payload):016X}")
    print(f"Dot product    : {backend.dot_product([1.5, 2.0, 3.5], [2.0, 1.5, 2.0])}")

    print("\n--- Benchmark: count_primes (CPU-bound) ---")
    res = benchmark()
    print(f"  pure Python : {res['python_ms']:8.1f} ms")
    if "rust_ms" in res:
        print(f"  native Rust : {res['rust_ms']:8.1f} ms")
        print(f"  speedup     : {res['speedup']:8.1f}x")
    else:
        print("  native Rust : not built - nothing to compare")

    print("\n--- Streaming statistics (Rust #[pyclass] vs Python) ---")
    samples = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    ps = PyRollingStats()
    ps.extend(samples)
    variance = ps.variance
    assert variance is not None
    print(f"  python : {ps}  variance={variance:.4f}")
    if rust_available():
        import rust_accelerator

        rs_stats = rust_accelerator.RollingStats()
        rs_stats.extend(samples)
        print(f"  rust   : {rs_stats}  variance={rs_stats.variance:.4f}")


if __name__ == "__main__":
    main()

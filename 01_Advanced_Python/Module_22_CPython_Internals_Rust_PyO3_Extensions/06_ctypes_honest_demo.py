#!/usr/bin/env python3
"""Module 22, Demo 1 - What ctypes is ACTUALLY for (and what it is not).

ctypes has one job: **call functions that already exist in a compiled library**
without writing any C yourself. It is a bridge, not an accelerator.

The trap this demo exists to kill
---------------------------------
It is tempting to write::

    buf = (ctypes.c_double * n)(*values)
    total = 0.0
    for i in range(n):
        total += buf[i] * buf[i]     # "native math", right?

This is *slower* than plain Python. Every ``buf[i]`` constructs a brand-new
Python float object; you added marshalling cost and removed nothing. The loop
still runs in the interpreter. Section 3 below measures exactly that, so you
can see the regression rather than take it on faith.

Rule of thumb
-------------
* Need to call an existing C library (libm, libz, a vendor SDK)?  -> ctypes.
* Need YOUR OWN hot loop to run at machine speed?                 -> Rust/PyO3
  (see ``project_solution/rust_accelerator/src/lib.rs``) or C, Cython, numpy.

Run:  python 01_ctypes_honest_demo.py
"""

from __future__ import annotations

import ctypes
import ctypes.util
import math
import platform
import time


# ===========================================================================
# 1. THE LEGITIMATE USE: bind to a real system library
# ===========================================================================
def load_libm() -> ctypes.CDLL | None:
    """Load the platform C runtime that exposes the math functions.

    This is genuinely useful: no compiler, no build step, no wrapper code -
    just address-of-symbol plus a type signature.
    """
    system = platform.system()
    candidates: list[str] = []
    if system == "Windows":
        # The UCRT hosts the math functions on modern Windows.
        candidates = ["ucrtbase", "msvcrt"]
    elif system == "Darwin":
        candidates = ["libSystem.dylib", "libm.dylib"]
    else:
        found = ctypes.util.find_library("m")
        candidates = [found] if found else ["libm.so.6"]

    for name in candidates:
        try:
            return ctypes.CDLL(name)
        except OSError:
            continue
    return None


def demo_real_ffi() -> None:
    print("=" * 68)
    print(" 1. LEGITIMATE ctypes: calling C's libm directly")
    print("=" * 68)

    libm = load_libm()
    if libm is None:
        print("  Could not locate the platform C math library; skipping.")
        return

    # ---- THE CRITICAL STEP: declare the signature -------------------------
    # Without argtypes/restype, ctypes assumes every argument is an int and the
    # return value is an int. On a float function that yields silent garbage -
    # not a crash, not an exception. Garbage. This is the #1 ctypes bug.
    try:
        cbrt = libm.cbrt
    except AttributeError:
        print("  This C runtime does not export 'cbrt'; skipping.")
        return

    print("\n  (a) WITHOUT argtypes/restype - undefined behaviour:")
    raw = libm.cbrt
    raw.argtypes = None
    raw.restype = ctypes.c_int  # deliberately wrong
    try:
        print(f"      cbrt(27.0) mis-declared -> {raw(27.0)!r}   <-- meaningless")
    except (ctypes.ArgumentError, TypeError) as exc:
        print(f"      raised {type(exc).__name__}: {exc}")

    print("\n  (b) WITH the correct signature:")
    cbrt.argtypes = [ctypes.c_double]
    cbrt.restype = ctypes.c_double
    for value in (27.0, 64.0, 1000.0):
        native = cbrt(value)
        pythonic = value ** (1 / 3)
        print(f"      cbrt({value:7.1f}) = {native:.10f}   (Python: {pythonic:.10f})")

    # Struct marshalling: another thing ctypes is genuinely good at.
    print("\n  (c) Passing a by-reference out-parameter (modf splits a float):")
    try:
        modf = libm.modf
        modf.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
        modf.restype = ctypes.c_double
        int_part = ctypes.c_double()
        frac = modf(3.75, ctypes.byref(int_part))
        print(f"      modf(3.75) -> frac={frac:.4f}, int={int_part.value:.1f}")
    except AttributeError:
        print("      'modf' not exported here; skipping.")


# ===========================================================================
# 2. STRUCTS: describing a C memory layout from Python
# ===========================================================================
class Point3D(ctypes.Structure):
    """A C struct laid out exactly as a compiler would lay it out."""

    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double),
    ]

    def __repr__(self) -> str:
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"


def demo_structs() -> None:
    print("\n" + "=" * 68)
    print(" 2. ctypes.Structure: exact control over memory layout")
    print("=" * 68)

    p = Point3D(1.0, 2.0, 3.0)
    print(f"\n  value      : {p}")
    print(f"  sizeof     : {ctypes.sizeof(p)} bytes  (3 x 8-byte doubles)")
    print(f"  alignment  : {ctypes.alignment(p)} bytes")
    print(f"  raw memory : {bytes(p)[:16].hex(' ')} ...")

    # Zero-copy reinterpretation: the bytes ARE the struct.
    blob = bytes(p)
    revived = Point3D.from_buffer_copy(blob)
    print(f"  round-trip : {revived}")

    # This is what a real native call receives: a pointer to 24 bytes.
    print(f"  byref()    : {ctypes.byref(p)!r}")


# ===========================================================================
# 3. THE MEASURED TRUTH: ctypes arrays do NOT accelerate Python loops
# ===========================================================================
def dot_pure_python(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def dot_ctypes_wrapped(a: list[float], b: list[float]) -> float:
    """The anti-pattern: C storage, Python loop. Looks native. Is not."""
    n = len(a)
    array_type = ctypes.c_double * n
    ca, cb = array_type(*a), array_type(*b)
    total = 0.0
    for i in range(n):
        total += ca[i] * cb[i]  # boxes a Python float on every single access
    return total


def demo_the_regression() -> None:
    print("\n" + "=" * 68)
    print(" 3. MEASURED: wrapping data in C types makes Python SLOWER")
    print("=" * 68)

    n = 200_000
    a = [float(i) * 0.5 for i in range(n)]
    b = [float(i) * 1.5 for i in range(n)]

    def timed(fn) -> tuple[float, float]:  # type: ignore[no-untyped-def]
        best = float("inf")
        result = 0.0
        for _ in range(3):
            t0 = time.perf_counter()
            result = fn(a, b)
            best = min(best, time.perf_counter() - t0)
        return best, result

    t_py, r_py = timed(dot_pure_python)
    t_ct, r_ct = timed(dot_ctypes_wrapped)

    print(f"\n  vector length          : {n:,}")
    print(f"  pure Python (zip+sum)  : {t_py * 1000:8.2f} ms")
    print(f"  ctypes-wrapped loop    : {t_ct * 1000:8.2f} ms")
    print(f"  results agree          : {math.isclose(r_py, r_ct, rel_tol=1e-9)}")

    ratio = t_ct / t_py
    verdict = "SLOWER" if ratio > 1 else "faster"
    print(f"\n  -> the 'native' version is {ratio:.2f}x {verdict} than plain Python.")
    print("     Storage type is not execution speed. The loop must leave Python.")

    print("\n  For a loop that genuinely leaves Python, see:")
    print("     project_solution/rust_accelerator/src/lib.rs   (25-40x faster)")
    print("     cd project_solution/rust_accelerator && maturin develop --release")


def main() -> None:
    demo_real_ffi()
    demo_structs()
    demo_the_regression()
    print("\n" + "=" * 68)
    print(" Takeaway: ctypes = call existing native code.")
    print("           PyO3/Rust = make YOUR code native.")
    print("=" * 68)


if __name__ == "__main__":
    main()

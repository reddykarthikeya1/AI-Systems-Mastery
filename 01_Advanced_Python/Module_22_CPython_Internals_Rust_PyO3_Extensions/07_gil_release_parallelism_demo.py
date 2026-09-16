#!/usr/bin/env python3
"""Module 22, Demo 2 - The real reason to write a native extension: GIL release.

Module 09 taught you the hard rule: **Python threads cannot run CPU-bound code
in parallel.** One interpreter lock, one thread executing bytecode at a time.
Adding threads to CPU work adds overhead and nothing else.

A native extension can break that rule. Inside ``py.allow_threads(|| ...)`` a
Rust function holds no GIL, so N threads occupy N cores for real. This is the
single most valuable thing PyO3 buys you - more valuable than raw single-thread
speed, because it is a capability Python simply does not have.

This demo measures three things on the same workload:

    1. Pure Python, 1 thread      - the baseline
    2. Pure Python, 4 threads     - should be NO faster (GIL-bound)
    3. Rust,        4 threads     - should scale with your core count

Run:  python 02_gil_release_parallelism_demo.py

Requires the extension. Build it first:
    cd project_solution/rust_accelerator && maturin develop --release
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

# Make the project_solution package importable when run from the module root.
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from native_accelerator import PyAccelerator, load_backend, rust_available

WORKLOAD = 150_000  # primes ceiling - big enough to dominate thread overhead
THREADS = 4


def run_parallel(fn, n_threads: int, arg: int) -> float:  # type: ignore[no-untyped-def]
    """Run `fn(arg)` on `n_threads` OS threads; return wall-clock seconds."""
    threads = [threading.Thread(target=fn, args=(arg,)) for _ in range(n_threads)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def bar(seconds: float, scale: float, width: int = 44) -> str:
    """A tiny ASCII bar so the numbers are visible at a glance."""
    filled = max(1, min(width, round(width * seconds / scale)))
    return "#" * filled


def main() -> None:
    cores = os.cpu_count() or 1
    print("=" * 72)
    print("  MODULE 22 - GIL RELEASE: WHERE NATIVE EXTENSIONS EARN THEIR KEEP")
    print("=" * 72)
    print(f"\n  CPU cores detected : {cores}")
    print(f"  Threads per test   : {THREADS}")
    print(f"  Workload           : count_primes({WORKLOAD:,})")

    py = PyAccelerator()

    # ---- 1. Pure Python, single thread -----------------------------------
    t0 = time.perf_counter()
    py.count_primes(WORKLOAD)
    py_serial = time.perf_counter() - t0

    # ---- 2. Pure Python, N threads ---------------------------------------
    py_parallel = run_parallel(py.count_primes, THREADS, WORKLOAD)

    scale = max(py_serial, py_parallel)

    print("\n" + "-" * 72)
    print("  PURE PYTHON")
    print("-" * 72)
    print(f"  1 thread   {py_serial * 1000:8.0f} ms  {bar(py_serial, scale)}")
    print(f"  {THREADS} threads  {py_parallel * 1000:8.0f} ms  {bar(py_parallel, scale)}")
    py_scaling = py_serial * THREADS / py_parallel
    print(f"\n  Ideal scaling would be {THREADS:.1f}x. Measured: {py_scaling:.2f}x")
    print("  -> The GIL serialises the work. Threads bought you nothing.")

    if not rust_available():
        print("\n" + "-" * 72)
        print("  RUST BACKEND NOT BUILT - the interesting half of this demo is")
        print("  unavailable. Build it and re-run:")
        print("      cd project_solution/rust_accelerator")
        print("      maturin develop --release")
        print("-" * 72)
        return

    # ---- 3. Rust, single thread and N threads ----------------------------
    rs = load_backend()
    t0 = time.perf_counter()
    rs.count_primes(WORKLOAD)
    rs_serial = time.perf_counter() - t0
    rs_parallel = run_parallel(rs.count_primes, THREADS, WORKLOAD)

    rs_scale = max(rs_serial, rs_parallel)
    print("\n" + "-" * 72)
    print("  NATIVE RUST (py.allow_threads)")
    print("-" * 72)
    print(f"  1 thread   {rs_serial * 1000:8.1f} ms  {bar(rs_serial, rs_scale)}")
    print(f"  {THREADS} threads  {rs_parallel * 1000:8.1f} ms  {bar(rs_parallel, rs_scale)}")
    rs_scaling = rs_serial * THREADS / rs_parallel
    print(f"\n  Ideal scaling would be {THREADS:.1f}x. Measured: {rs_scaling:.2f}x")
    if rs_scaling > 1.5:
        print("  -> The GIL is released. Those threads ran on separate cores.")
    else:
        print("  -> Scaling is flat. On a 1-2 core machine this is expected;")
        print("     on a multicore box, check py.allow_threads() in lib.rs.")

    # ---- Summary ---------------------------------------------------------
    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  single-thread speedup (rust vs python) : {py_serial / rs_serial:6.1f}x")
    print(f"  {THREADS}-thread    speedup (rust vs python) : {py_parallel / rs_parallel:6.1f}x")
    print(f"  python thread scaling                  : {py_scaling:6.2f}x  (GIL-bound)")
    print(f"  rust   thread scaling                  : {rs_scaling:6.2f}x  (GIL released)")
    print("\n  Two independent wins compound:")
    print("    (1) compiled code is faster per core, and")
    print("    (2) it can use every core at once.")
    print("\n  Next: Module 23 packages an extension like this into a typed,")
    print("        publishable wheel with a pure-Python fallback.")


if __name__ == "__main__":
    main()

"""Benchmarks behind the performance numbers quoted in the chapters.

    python labs/05_benchmarks.py          # prints a table; add --quick for a smaller run

Numbers depend on hardware, Python and library versions. The chapters quote *ranges and ratios*
from this script, never absolute times. Optional libraries (numpy, pandas, polars) are skipped
when missing.
"""
from __future__ import annotations

import platform
import sys
import time
from statistics import median

QUICK = "--quick" in sys.argv


def best_of(fn, repeat: int = 5) -> float:
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return median(times)


def concat_vs_join(n: int):
    def concat():
        s = ""
        for i in range(n):
            s += str(i)
        return s

    def join():
        return "".join(str(i) for i in range(n))

    return best_of(concat), best_of(join)


def loop_vs_numpy(n: int):
    import numpy as np

    arr = np.random.random(n)
    lst = arr.tolist()

    def py():
        total = 0.0
        for x in lst:
            total += x
        return total

    return best_of(py, 3), best_of(lambda: arr.sum(), 20)


def pandas_vs_polars(n: int):
    import numpy as np
    import pandas as pd
    import polars as pl

    rng = np.random.default_rng(0)
    data = {"k": rng.integers(0, 1000, n), "v": rng.random(n)}
    pdf, pldf = pd.DataFrame(data), pl.DataFrame(data)
    return best_of(lambda: pdf.groupby("k")["v"].sum()), best_of(lambda: pldf.group_by("k").agg(pl.col("v").sum()))


def main() -> None:
    n = 20_000 if QUICK else 200_000
    print(f"Python {platform.python_version()} on {platform.system()} {platform.machine()}  (n={n:,})\n")
    print(f"{'benchmark':<34}{'baseline s':>12}{'improved s':>12}{'ratio':>9}")
    rows = [("str += vs ''.join", concat_vs_join, n)]
    try:
        import numpy  # noqa: F401
        rows.append(("python float loop vs numpy.sum", loop_vs_numpy, n * 5))
    except ImportError:
        print("numpy missing: skipping loop-vs-numpy")
    try:
        import pandas, polars  # noqa: F401, E401
        rows.append(("pandas vs polars group-by sum", pandas_vs_polars, n * 5))
    except ImportError:
        print("pandas/polars missing: skipping group-by")
    for name, fn, size in rows:
        a, b = fn(size)
        print(f"{name:<34}{a:>12.4f}{b:>12.4f}{a / b:>8.1f}x")
    print("\nRatios are the only portable output. Re-run on your own machine before quoting them.")


if __name__ == "__main__":
    main()

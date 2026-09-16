"""Worker functions for the Module 09 notebook.

Why this file exists
--------------------
``ProcessPoolExecutor`` cannot run a function defined in a *notebook cell* on any
platform that uses the ``spawn`` start method — Windows, and macOS since Python
3.8. ``spawn`` pickles the target **by qualified name**, then the fresh child
process imports that name. A notebook cell lives in the kernel's ``__main__``,
which the child does not have, so you get::

    AttributeError: Can't get attribute 'cpu_task' on <module '__main__'>

Putting the worker in an importable module is the fix, and it is also what you do
in production. Keep this file next to the notebook and ``import nb_workers``.
"""

from __future__ import annotations

import math


def cpu_task(n: int) -> int:
    """Deliberately CPU-bound work: integer square roots over a range.

    Pure computation, no I/O, so it holds the GIL for its entire duration. That
    is what makes it a fair test of threads (which cannot parallelise it) versus
    processes (which can).
    """
    return sum(int(math.sqrt(i)) for i in range(n))


def io_task(seconds: float = 0.1) -> str:
    """Deliberately I/O-bound work, for the opposite comparison.

    ``time.sleep`` releases the GIL, so threads *do* overlap here — which is why
    threading is the right tool for I/O and the wrong tool for CPU work.
    """
    import time

    time.sleep(seconds)
    return f"slept {seconds}s"

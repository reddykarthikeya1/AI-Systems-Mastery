"""Chapter 10 - Production debugging and profiling.

1. peak_alloc_kb: measure the peak memory a call allocates (tracemalloc).
2. growth_by_line: find the source line responsible for memory growth.
3. render (debugging): a cache that eventually eats all the memory.
"""
import functools
import time
import tracemalloc

BUGGY = {
    "render": '''@functools.lru_cache(maxsize=None)
def render(user_id):
    """Expensive pure function of user_id, cached. The cache must stay bounded at 128 entries."""
    return "x" * 1000 + str(user_id)''',
}

_LEAK = []


def _leaky():
    _LEAK.append(bytearray(10_000))      # the leaking line


def peak_alloc_kb(fn):
    """Run fn() under tracemalloc and return the peak traced memory in KiB (a float). Leave tracemalloc stopped afterwards."""
    tracemalloc.start()
    try:
        fn()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return peak / 1024


def growth_by_line(fn, rounds=50):
    """Call fn() `rounds` times between two tracemalloc snapshots and return (lineno, bytes_added) for the line INSIDE fn's
    own file that grew the most. Return None if nothing grew. Leave tracemalloc stopped afterwards."""
    fname = fn.__code__.co_filename
    tracemalloc.start()
    try:
        before = tracemalloc.take_snapshot()
        for _ in range(rounds):
            fn()
        after = tracemalloc.take_snapshot()
    finally:
        tracemalloc.stop()
    stats = [s for s in after.compare_to(before, "lineno") if s.traceback[0].filename == fname and s.size_diff > 0]
    if not stats:
        return None
    top = max(stats, key=lambda s: s.size_diff)
    return top.traceback[0].lineno, top.size_diff


@functools.lru_cache(maxsize=128)
def render(user_id):
    """Expensive pure function of user_id, cached. The cache must stay bounded at 128 entries."""
    return "x" * 1000 + str(user_id)


def t_peak_alloc_scales(m):
    small = m.peak_alloc_kb(lambda: [0] * 10)
    big = m.peak_alloc_kb(lambda: [0] * 200_000)
    assert big > 1000 and big > 20 * small
    assert not tracemalloc.is_tracing()


def t_growth_by_line_finds_leak(m):
    import inspect
    lines, start = inspect.getsourcelines(_leaky)
    leak_line = start + next(i for i, l in enumerate(lines) if "the leaking line" in l)
    res = m.growth_by_line(_leaky, rounds=40)
    assert res is not None and res[0] == leak_line and res[1] >= 40 * 10_000
    assert not tracemalloc.is_tracing()


def t_growth_by_line_no_growth(m):
    assert m.growth_by_line(lambda: sum(range(100)), rounds=20) is None


def t_render_cache_bounded(m):
    for i in range(1000):
        m.render(i)
    info = m.render.cache_info()
    assert info.currsize <= 128 and info.maxsize == 128

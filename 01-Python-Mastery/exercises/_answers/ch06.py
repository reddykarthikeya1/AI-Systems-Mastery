"""Chapter 06 - Concurrency: asyncio, threads.

1. run_bounded: run async tasks with a concurrency limit, results in input order.
2. first_completed: return the result of whichever thread finishes first.
3. fetch_all (debugging): ten "requests" take ten times as long as one. Why?
"""
import asyncio
import concurrent.futures
import time

BUGGY = {
    "fetch_all": '''async def fetch_all(n):
    """Simulate n concurrent 50 ms requests and return their ids in order. Total time must stay near 50 ms, not n * 50 ms."""
    async def fetch(i):
        time.sleep(0.05)
        return i
    return await asyncio.gather(*(fetch(i) for i in range(n)))''',
}


async def run_bounded(factories, limit):
    """`factories` is a list of zero-argument async callables. Run them with at most `limit` running at once and
    return their results in input order. If one raises, the exception propagates. limit < 1 raises ValueError."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    sem = asyncio.Semaphore(limit)

    async def guarded(f):
        async with sem:
            return await f()

    return await asyncio.gather(*(guarded(f) for f in factories))


def first_completed(funcs, timeout):
    """Run the zero-argument callables in separate threads and return the result of the first to finish.
    Raise TimeoutError if none finishes within `timeout` seconds. Do not wait for the slower ones before returning."""
    ex = concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(funcs)))
    try:
        futs = [ex.submit(f) for f in funcs]
        done, _ = concurrent.futures.wait(futs, timeout=timeout, return_when=concurrent.futures.FIRST_COMPLETED)
        if not done:
            raise TimeoutError("no task finished in time")
        return next(iter(done)).result()
    finally:
        ex.shutdown(wait=False, cancel_futures=True)


async def fetch_all(n):
    """Simulate n concurrent 50 ms requests and return their ids in order. Total time must stay near 50 ms, not n * 50 ms."""
    async def fetch(i):
        await asyncio.sleep(0.05)
        return i
    return await asyncio.gather(*(fetch(i) for i in range(n)))


def t_run_bounded_limits_concurrency(m):
    state = {"now": 0, "peak": 0}

    def make(i):
        async def job():
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
            await asyncio.sleep(0.01)
            state["now"] -= 1
            return i * i
        return job

    res = asyncio.run(m.run_bounded([make(i) for i in range(10)], 3))
    assert res == [i * i for i in range(10)] and state["peak"] == 3


def t_run_bounded_errors(m):
    async def boom():
        raise RuntimeError("x")
    try:
        asyncio.run(m.run_bounded([boom], 2))
    except RuntimeError:
        pass
    else:
        raise AssertionError("exception must propagate")
    try:
        asyncio.run(m.run_bounded([], 0))
    except ValueError:
        return
    raise AssertionError("limit 0 must raise ValueError")


def t_first_completed_is_fast(m):
    t0 = time.perf_counter()
    assert m.first_completed([lambda: (time.sleep(0.5), "slow")[1], lambda: (time.sleep(0.02), "fast")[1]], 2) == "fast"
    assert time.perf_counter() - t0 < 0.4


def t_first_completed_timeout(m):
    try:
        m.first_completed([lambda: time.sleep(0.3)], 0.05)
    except TimeoutError:
        return
    raise AssertionError("expected TimeoutError")


def t_fetch_all_is_concurrent(m):
    t0 = time.perf_counter()
    assert asyncio.run(m.fetch_all(10)) == list(range(10))
    assert time.perf_counter() - t0 < 0.3

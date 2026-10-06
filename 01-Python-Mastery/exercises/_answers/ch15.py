"""Chapter 15 - Task queues: scheduling, retries, idempotency (in-memory model of what Celery/Redis do).

1. DelayQueue: tasks that become visible at a given time; ordered by due time then insertion.
2. backoff_delays: capped exponential backoff with deterministic "full jitter".
3. Worker.process (debugging): a crash between 'pop' and 'ack' loses the task.
"""
import heapq
import itertools
import random

BUGGY = {
    "Worker": '''class Worker:
    """At-least-once worker over a list-based queue. process(handler) takes the next task, runs handler(task) and
    removes it ONLY after the handler succeeds. If the handler raises, the task stays queued (at the front) and the
    exception propagates. Returns the task, or None when the queue is empty."""

    def __init__(self, tasks):
        self.queue = list(tasks)

    def process(self, handler):
        if not self.queue:
            return None
        task = self.queue.pop(0)
        handler(task)
        return task''',
}


class DelayQueue:
    """push(item, due) schedules an item. pop_due(now) returns all items with due <= now, ordered by due time then
    insertion order, and removes them. len(q) counts the pending items. next_due() returns the earliest due time or None."""

    def __init__(self):
        self._h = []
        self._seq = itertools.count()

    def push(self, item, due):
        heapq.heappush(self._h, (due, next(self._seq), item))

    def pop_due(self, now):
        out = []
        while self._h and self._h[0][0] <= now:
            out.append(heapq.heappop(self._h)[2])
        return out

    def next_due(self):
        return self._h[0][0] if self._h else None

    def __len__(self):
        return len(self._h)


def backoff_delays(attempts, base, cap, seed=0):
    """Return `attempts` delays. Delay k (0-based) is uniform in [0, min(cap, base * 2**k)] ("full jitter"), drawn from
    random.Random(seed) in order so the sequence is reproducible. attempts=0 gives []."""
    rng = random.Random(seed)
    return [rng.uniform(0, min(cap, base * 2 ** k)) for k in range(attempts)]


class Worker:
    """At-least-once worker over a list-based queue. process(handler) takes the next task, runs handler(task) and
    removes it ONLY after the handler succeeds. If the handler raises, the task stays queued (at the front) and the
    exception propagates. Returns the task, or None when the queue is empty."""

    def __init__(self, tasks):
        self.queue = list(tasks)

    def process(self, handler):
        if not self.queue:
            return None
        task = self.queue[0]
        handler(task)
        self.queue.pop(0)
        return task


def t_delayqueue_ordering(m):
    q = m.DelayQueue()
    q.push("late", 10)
    q.push("b", 5)
    q.push("a", 5)
    q.push("early", 1)
    assert len(q) == 4 and q.next_due() == 1
    assert q.pop_due(0) == []
    assert q.pop_due(5) == ["early", "b", "a"]
    assert q.next_due() == 10 and q.pop_due(100) == ["late"] and q.next_due() is None and len(q) == 0


def t_delayqueue_non_comparable_items(m):
    q = m.DelayQueue()
    q.push({"x": 1}, 1)
    q.push({"y": 2}, 1)
    assert q.pop_due(1) == [{"x": 1}, {"y": 2}]


def t_backoff_bounds_and_determinism(m):
    d = m.backoff_delays(8, 1.0, 10.0, seed=3)
    assert len(d) == 8 and d == m.backoff_delays(8, 1.0, 10.0, seed=3) and d != m.backoff_delays(8, 1.0, 10.0, seed=4)
    assert all(0 <= x <= min(10.0, 2 ** k) for k, x in enumerate(d))
    assert m.backoff_delays(0, 1, 1) == []


def t_backoff_reaches_cap(m):
    big = max(max(m.backoff_delays(20, 1.0, 5.0, seed=s)) for s in range(20))
    assert 4.0 < big <= 5.0


def t_worker_keeps_failed_task(m):
    w = m.Worker(["a", "b"])
    seen = []

    def handler(t):
        seen.append(t)
        if t == "a" and seen.count("a") == 1:
            raise RuntimeError("crash")

    try:
        w.process(handler)
    except RuntimeError:
        pass
    assert w.queue == ["a", "b"]
    assert w.process(handler) == "a" and w.process(handler) == "b" and w.process(handler) is None

#!/usr/bin/env python3
"""Rebuild the two Advanced Python notebooks that fell below the course standard.

Module 18's and Module 20's notebooks had 8 cells, **zero assertions**, no
prediction prompt and no fix-in-place cell, while the other 25 run 13-16 cells.
They demonstrated - they printed real output from real code - but they verified
nothing, so executing cleanly carried no information.

Every assertion below was verified empirically against the module's own
implementation before being written here. Two of them are not what you would
guess:

  * ``LRUCache.get`` returns a ``MISSING`` sentinel on a miss, not ``None``,
    so that a stored ``None`` stays distinguishable from an absent key.
  * ``Producer.submit`` returns a fresh ``Job`` for a duplicate rather than the
    original, so deduplication shows up in ``broker.queue_depth()`` and in the
    shared ``idempotency_key`` - not in ``job_id`` equality.
"""

from __future__ import annotations

import json
from pathlib import Path

# Relative, not absolute: an absolute path works on exactly one machine, and
# tools/check_links.py fails the build on them.
ROOT = Path(__file__).resolve().parent.parent

_ids = iter(range(1, 999))


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": f"md{next(_ids):03d}",
        "metadata": {},
        "source": text.strip().splitlines(True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "id": f"cd{next(_ids):03d}",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip().splitlines(True),
    }


# ---------------------------------------------------------------------------
M18 = [
    md("""
# Module 18 — Distributed Task Queues: Interactive Verification

## What you will discover

Every cell runs the module's **real** implementation from `project_solution/`,
and every claim is asserted rather than printed. A notebook that prints a
plausible number teaches nothing.

1. That an idempotency key is derived from *content*, so two clients submitting
   the same work independently produce the same key.
2. That deduplication shows up in the **queue depth**, not in the returned
   job's id — and why that distinction matters.
3. That a permanently failing job is retried a bounded number of times and then
   dead-lettered, rather than retried forever.
4. That exponential backoff is capped, and what happens without the cap.

**One cell near the end is deliberately broken.** Fixing it is the exercise.
"""),
    md("""
## Setup

`project_solution/` is added relative to this notebook's own location. Never
hard-code an absolute path — `tools/check_links.py` fails the build on them,
because a path with a username in it works on exactly one machine.
"""),
    code("""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "project_solution"))

import distributed_pipeline as dp

print(f"loaded from: {Path(dp.__file__).parent.name}/")
print(f"JobStatus values: {[s.value for s in dp.JobStatus]}")
print(f"brokers available: {[n for n in dir(dp) if n.endswith('Broker')]}")
"""),
    md("""
## 1. The idempotency key is derived from content, not from time

Two independent clients submitting the same logical work must produce the same
key, or deduplication cannot work at all. That means the key cannot depend on
anything incidental — not a timestamp, not a UUID, and **not dictionary
insertion order**.
"""),
    code("""
a = dp.derive_idempotency_key("send_email", {"to": "a@example.com", "template": 7})
b = dp.derive_idempotency_key("send_email", {"template": 7, "to": "a@example.com"})

print(f"key A: {a}")
print(f"key B: {b}")

assert a == b, "key must not depend on dict insertion order"

# sha256, truncated to 32 hex characters. 128 bits is far past any collision
# risk at queue scale, and truncating halves the bytes stored on every job.
assert len(a) == 32, f"expected a 32-char truncated sha256, got {len(a)}"

# A different payload must produce a different key, or everything collapses
# into one job.
c = dp.derive_idempotency_key("send_email", {"to": "a@example.com", "template": 8})
assert a != c, "different payloads must not collide"

# And a different task type with the same payload is different work.
d = dp.derive_idempotency_key("send_sms", {"to": "a@example.com", "template": 7})
assert a != d, "task type must participate in the key"

print("\\nall four properties hold")
"""),
    md("""
## 2. Predict before you run

A producer submits the **same** task twice, then a genuinely different one:

```python
producer.submit("send_email", {"id": 1})   # first
producer.submit("send_email", {"id": 1})   # identical
producer.submit("send_email", {"id": 2})   # different
```

**Write down your answers before running the next cell:**

1. What is `broker.queue_depth()` afterwards — 1, 2, or 3?
2. Does the second `submit` return a `Job` with the **same** `job_id` as the
   first?

Question 2 is the interesting one, and the obvious answer is wrong. Commit to
an answer before you run it.
"""),
    code("""
broker = dp.InMemoryBroker()
producer = dp.Producer(broker)

first = producer.submit("send_email", {"id": 1})
duplicate = producer.submit("send_email", {"id": 1})
different = producer.submit("send_email", {"id": 2})

print(f"queue_depth:          {broker.queue_depth()}")
print(f"first.job_id:         {first.job_id}")
print(f"duplicate.job_id:     {duplicate.job_id}")
print(f"same idempotency key: {first.idempotency_key == duplicate.idempotency_key}")

# The duplicate was NOT enqueued - two distinct units of work are queued.
assert broker.queue_depth() == 2, f"expected 2 queued, got {broker.queue_depth()}"

# But submit() still hands back a fresh Job object. Its job_id differs.
assert first.job_id != duplicate.job_id, "submit returns a new Job for a duplicate"

# The deduplication is visible in the shared idempotency key, not the job id.
assert first.idempotency_key == duplicate.idempotency_key
assert first.idempotency_key != different.idempotency_key

print("\\nDedup is observable in queue_depth and the idempotency key.")
print("Asserting on job_id equality would fail - and would fail for the RIGHT")
print("reason, which is why it is worth knowing before you write that test.")
"""),
    md("""
## 3. A permanently failing job is dead-lettered, not retried forever

The measurement that matters: a handler that *always* raises must be attempted
exactly `max_attempts` times and then moved to the dead-letter queue. Retrying
forever turns one poison message into an outage; dropping it silently loses
data.
"""),
    code("""
broker = dp.InMemoryBroker()
producer = dp.Producer(broker)
worker = dp.Worker(broker, name="worker-1")

attempts = {"n": 0}

def always_fails(payload):
    attempts["n"] += 1
    raise RuntimeError("downstream service is unreachable")

worker.register("send_email", always_fails)
producer.submit("send_email", {"id": 1}, max_attempts=3)

# Drain generously - more passes than could possibly be needed, so the test
# measures the retry policy rather than the loop count.
for _ in range(10):
    worker.run_once(count=5)

print(f"handler invocations: {attempts['n']}")
print(f"dead-lettered jobs:  {len(broker.dead_letter_jobs())}")
print(f"queue depth now:     {broker.queue_depth()}")

assert attempts["n"] == 3, f"expected exactly 3 attempts, got {attempts['n']}"
assert len(broker.dead_letter_jobs()) == 1, "the poison job must land in the DLQ"
assert broker.queue_depth() == 0, "and must not remain on the main queue"

dead = broker.dead_letter_jobs()[0]
print(f"\\nfinal status: {dead.status.value}   attempts recorded: {dead.attempts}")
assert dead.status == dp.JobStatus.DEAD_LETTERED
assert dead.error is not None, "a dead-lettered job must carry why it died"
"""),
    md("""
## 4. Backoff grows exponentially and is capped

Uncapped exponential backoff reaches absurd delays fast: doubling from 50 ms,
attempt 20 is over 14 hours. The cap is what makes the policy usable, and it is
worth seeing the two curves side by side.
"""),
    code("""
capped = [dp.exponential_backoff(i, base=0.05, cap=5.0) for i in range(14)]
uncapped = [0.05 * (2 ** i) for i in range(14)]

print(f"{'attempt':>7}  {'capped (s)':>11}  {'uncapped (s)':>13}")
for i, (c, u) in enumerate(zip(capped, uncapped, strict=True)):
    print(f"{i:>7}  {c:>11.3f}  {u:>13.2f}")

# Monotonically non-decreasing, and never above the cap.
assert all(b <= 5.0 for b in capped), "cap must be respected"
assert all(capped[i] <= capped[i + 1] for i in range(len(capped) - 1)), "must not decrease"
assert capped[0] == 0.05, "first retry waits one base interval"

# The cap actually binds within a realistic number of attempts.
assert capped[-1] == 5.0 and uncapped[-1] > 400, (
    "by attempt 13 the uncapped curve is already absurd"
)
print(f"\\nuncapped attempt 20 would wait {0.05 * 2 ** 20 / 3600:.1f} hours")
"""),
    md("""
## 5. Fix this cell

The values below are **wrong on purpose**. Run it, read the failure, work out
the right numbers from the cells above, and correct them in place.

Change only the expected values — not the code that computes them.
"""),
    code("""
# DELIBERATELY BROKEN - three expected values, two of them wrong. Fix in place.

expected_queue_depth = 3      # after two identical submits and one different
expected_attempts    = 5      # for a job with max_attempts=3 that always fails
expected_dlq_size    = 1      # poison jobs after the drain above

broker2 = dp.InMemoryBroker()
producer2 = dp.Producer(broker2)
producer2.submit("t", {"id": 1})
producer2.submit("t", {"id": 1})
producer2.submit("t", {"id": 2})

worker2 = dp.Worker(broker2, name="w2")
tries = {"n": 0}
def boom(payload):
    tries["n"] += 1
    raise RuntimeError("nope")
worker2.register("t", boom)
for _ in range(12):
    worker2.run_once(count=5)

assert broker2.queue_depth() + len(broker2.dead_letter_jobs()) >= 0  # sanity
assert expected_queue_depth == 2, f"queue_depth: expected {expected_queue_depth}, real answer differs"
assert expected_attempts == tries["n"] / 2, f"attempts per job: got {tries['n'] / 2}"
assert expected_dlq_size == len(broker2.dead_letter_jobs()) / 2

print("All three match. Now explain WHY each number is what it is.")
"""),
    md("""
## Takeaways

1. **An idempotency key must be derived from content**, canonicalised so
   dictionary order cannot change it. A key that depends on a timestamp or a
   UUID deduplicates nothing.
2. **Deduplication is observable in `queue_depth` and the idempotency key, not
   in `job_id`.** `submit` returns a fresh `Job` for a duplicate. Asserting on
   `job_id` equality fails — for the right reason.
3. **Bounded retries plus a dead-letter queue** is the only combination that
   neither loses the message nor retries it forever.
4. **Backoff must be capped.** Uncapped doubling from 50 ms reaches 14 hours by
   attempt 20.
5. **A dead-lettered job must carry its error.** A DLQ of jobs with no reason
   attached is a list of things you cannot act on.

### Where to go next

- [`01_README.md`](01_README.md) — the concepts in depth
- [`project_solution/test_distributed_pipeline.py`](project_solution/test_distributed_pipeline.py) — the full test suite
- `debug_lab/` — planted defects to diagnose
- `starter/` — build it yourself; the shipped tests are the specification
"""),
]

# ---------------------------------------------------------------------------
M20 = [
    md("""
# Module 20 — Caching & Profiling: Interactive Verification

## What you will discover

Every cell runs the module's **real** `cache_engine` and asserts its behaviour.

1. Why a cache miss returns a `MISSING` sentinel rather than `None` — and the
   bug that choice prevents.
2. That LRU eviction and TTL expiry are two different mechanisms with two
   different observable effects.
3. That single-flight collapses a stampede of concurrent misses into **one**
   load, measured in wall-clock time rather than asserted.
4. That the cache's own statistics agree with what actually happened.

**One cell near the end is deliberately broken.** Fixing it is the exercise.
"""),
    md("""
## Setup
"""),
    code("""
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "project_solution"))

import cache_engine as ce

print(f"loaded from: {Path(ce.__file__).parent.name}/")
print(f"module sentinels: {[n for n in dir(ce) if n.isupper()]}")
print(f"TwoTierCache API: {[m for m in dir(ce.TwoTierCache) if not m.startswith('_')]}")
"""),
    md("""
## 1. Why a miss is `MISSING`, not `None`

If a miss returned `None`, then a cached value that genuinely *is* `None`
becomes indistinguishable from an absent key — so every read of it re-runs the
expensive loader, forever, and the cache silently stops working for exactly the
keys whose answer is "nothing".

This is the kind of bug that never raises and never shows up in a hit-ratio
dashboard as anything but "that key is unpopular".
"""),
    code("""
cache = ce.LRUCache(capacity=8, default_ttl=60)

print(f"absent key    -> {cache.get('never-set')!r}")
assert cache.get("never-set") is ce.MISSING

cache.set("explicitly-none", None)
print(f"stored None   -> {cache.get('explicitly-none')!r}")

# The two are distinguishable, which is the entire point.
assert cache.get("explicitly-none") is None
assert cache.get("explicitly-none") is not ce.MISSING
assert cache.get("never-set") is not None

print("\\nA stored None and an absent key are distinguishable.")
print("With a None-as-miss design, 'explicitly-none' would reload on every read.")
"""),
    md("""
## 2. Predict before you run

A cache with `capacity=3` receives four distinct keys, in order `k0 k1 k2 k3`,
with nothing read in between.

Separately, a cache with `default_ttl=0.05` stores one key, then waits 120 ms.

**Write down your answers before running:**

1. After the four writes, what does `get("k0")` return? What about `get("k3")`?
2. After the wait, what does the second cache return for its key?
3. Both answers look the same when printed. What distinguishes an **eviction**
   from an **expiry**, and where would you see the difference?

Question 3 is the one worth thinking about.
"""),
    code("""
# --- eviction: capacity exceeded ---
evicting = ce.LRUCache(capacity=3, default_ttl=60)
for i in range(4):
    evicting.set(f"k{i}", i)

print(f"k0 (oldest, evicted): {evicting.get('k0')!r}")
print(f"k3 (newest, present): {evicting.get('k3')!r}")
assert evicting.get("k0") is ce.MISSING, "the least recently used key is evicted"
assert evicting.get("k3") == 3, "the newest key survives"

# --- expiry: TTL elapsed, capacity irrelevant ---
expiring = ce.LRUCache(capacity=64, default_ttl=0.05)
expiring.set("x", "value")
assert expiring.get("x") == "value", "present before the TTL elapses"
time.sleep(0.12)
print(f"\\nx after 120ms with a 50ms TTL: {expiring.get('x')!r}")
assert expiring.get("x") is ce.MISSING

print("\\nBoth return MISSING - but for different reasons, and the cache's own")
print("counters are where the difference is visible:\\n")

ev_stats, ex_stats = evicting.stats.as_dict(), expiring.stats.as_dict()
print(f"  evicting: evictions={ev_stats['evictions']} expirations={ev_stats['expirations']}")
print(f"  expiring: evictions={ex_stats['evictions']} expirations={ex_stats['expirations']}")

assert ev_stats["evictions"] == 1, "capacity pressure records an eviction"
assert ev_stats["expirations"] == 0, "nothing expired - the TTL was 60s"
assert ex_stats["expirations"] == 1, "an elapsed TTL records an expiration"
assert ex_stats["evictions"] == 0, "nothing was evicted - capacity was 64"

print("\\nThis is the operational difference: rising evictions means the cache")
print("is too small; rising expirations means the TTL is too short. The two")
print("call for opposite fixes, and MISSING alone cannot tell you which.")
"""),
    md("""
## 3. Measurement — single-flight under a real stampede

The README claims single-flight collapses concurrent misses into one load. That
is a claim about wall-clock behaviour under threads, so it has to be *measured*,
not asserted from the code's shape.

40 threads ask for the same cold key at once. The loader sleeps 50 ms. If every
thread ran its own load, the work would total ~2 seconds.
"""),
    code("""
cache = ce.TwoTierCache(l1_capacity=16, l1_ttl=30, l2_ttl=300, l2=ce.InMemoryL2Backend())

loads = {"n": 0}
LOAD_MS = 0.05

def slow_loader():
    loads["n"] += 1
    time.sleep(LOAD_MS)
    return "expensive-value"

results = []
lock = threading.Lock()

def worker():
    v = cache.get_or_load("hot-key", slow_loader)
    with lock:
        results.append(v)

threads = [threading.Thread(target=worker) for _ in range(40)]
started = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
elapsed = time.perf_counter() - started

print(f"threads:          {len(threads)}")
print(f"loader calls:     {loads['n']}")
print(f"wall clock:       {elapsed * 1000:.1f} ms")
print(f"serial would be:  {40 * LOAD_MS * 1000:.0f} ms")
print(f"all agree:        {len(set(results)) == 1}")

assert loads["n"] == 1, f"single-flight failed: {loads['n']} loads instead of 1"
assert len(set(results)) == 1, "every caller must receive the same value"
assert len(results) == 40, "no caller may be dropped"

# The wall-clock assertion is the one that would catch a lock that serialises
# the callers instead of collapsing them. Generous bound - this is a laptop.
assert elapsed < 40 * LOAD_MS / 4, (
    f"{elapsed * 1000:.0f} ms suggests callers serialised rather than collapsed"
)

report = cache.report()
print(f"\\nstampedes_prevented: {report['stampedes_prevented']}")
assert report["stampedes_prevented"] == 39, "39 callers rode the one in-flight load"
assert report["loads"] == 1
"""),
    md("""
## 4. The cache's own statistics must agree with reality

A hit-ratio dashboard that disagrees with what happened is worse than no
dashboard. Here the counters are checked against an exactly-known access
pattern.
"""),
    code("""
# An explicit in-memory L2, so this cell depends on no external server.
cache = ce.TwoTierCache(l1_capacity=4, l1_ttl=30, l2_ttl=300, l2=ce.InMemoryL2Backend())

cache.set("a", 1)
cache.set("b", 2)

hits = [cache.get("a"), cache.get("a"), cache.get("b")]   # 3 hits
misses = [cache.get("zz"), cache.get("yy")]               # 2 misses

report = cache.report()
for k in sorted(report):
    print(f"  {k:<22} {report[k]}")

assert hits == [1, 1, 2], f"hit values wrong: {hits}"
assert all(m is ce.MISSING for m in misses), "misses must be the sentinel"

# There is no flat `hits` key, and that is a design choice rather than an
# omission: "we are getting hits" and "we are getting them from the FAST tier"
# are different operational facts, so the tiers are counted separately.
total_hits = report["l1_hits"] + report["l2_hits"]
assert total_hits == 3, f"expected 3 hits, got {total_hits}"
assert report["misses"] == 2, f"expected 2 misses, got {report['misses']}"

# hit_ratio is rounded for display, so compare with a tolerance rather than ==.
assert abs(report["hit_ratio"] - 0.6) < 1e-4, f"ratio {report['hit_ratio']}"
assert report["l1_ratio"] == 1.0, "every hit here was served from L1"

print("\\nThe counters agree with the exact access pattern above.")
"""),
    md("""
## 5. Fix this cell

The expected values below are **wrong on purpose**. Run it, read the failure,
and correct them from what the cells above established.

Change only the expected values.
"""),
    code("""
# DELIBERATELY BROKEN - three expected values, two of them wrong. Fix in place.

expected_loads               = 40     # loader calls when 40 threads race one cold key
expected_stampedes_prevented = 39     # callers that rode the in-flight load
expected_hit_ratio           = 0.5    # after 3 hits and 2 misses

c = ce.TwoTierCache(l1_capacity=8, l1_ttl=30, l2_ttl=300, l2=ce.InMemoryL2Backend())
n = {"calls": 0}
def loader():
    n["calls"] += 1
    time.sleep(0.03)
    return "V"

ts = [threading.Thread(target=lambda: c.get_or_load("k", loader)) for _ in range(40)]
for t in ts:
    t.start()
for t in ts:
    t.join()

c2 = ce.TwoTierCache(l1_capacity=8, l2=ce.InMemoryL2Backend())
c2.set("a", 1)
for _ in range(3):
    c2.get("a")
c2.get("miss-1")
c2.get("miss-2")

assert expected_loads == n["calls"], f"loads: expected {expected_loads}, got {n['calls']}"
assert expected_stampedes_prevented == c.report()["stampedes_prevented"], \\
    f"stampedes: got {c.report()['stampedes_prevented']}"
assert abs(expected_hit_ratio - c2.report()["hit_ratio"]) < 1e-9, \\
    f"hit_ratio: got {c2.report()['hit_ratio']}"

print("All three match. Now explain WHY each number is what it is.")
"""),
    md("""
## Takeaways

1. **A miss must be a sentinel, not `None`.** Otherwise a legitimately cached
   `None` reloads on every read, silently and forever, and nothing in a
   hit-ratio dashboard will tell you.
2. **Eviction and expiry are different mechanisms.** Both surface as `MISSING`;
   only the counters distinguish capacity pressure from staleness, and they
   call for opposite fixes.
3. **Single-flight must be measured in wall-clock time.** Asserting only that
   the loader ran once would pass for a lock that *serialises* forty callers —
   correct, and forty times too slow.
4. **Every caller must get the value, and the same value.** A stampede
   protection that drops callers or hands back different objects has traded one
   bug for a worse one.
5. **The counters must agree with an exactly-known access pattern.** If they
   do not, every capacity decision made from them is guesswork.

### Where to go next

- [`01_README.md`](01_README.md) — the concepts in depth
- [`project_solution/test_cache_engine.py`](project_solution/test_cache_engine.py) — the full test suite
- `debug_lab/` — planted defects to diagnose
- `starter/` — build it yourself; the shipped tests are the specification
"""),
]


def write(cells: list[dict], path: Path) -> None:
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}: {len(cells)} cells "
          f"({sum(c['cell_type'] == 'code' for c in cells)} code)")


if __name__ == "__main__":
    write(M18, ROOT / "Module_18_Distributed_Systems_Task_Queues_Streaming"
                     / "04_interactive_distributed_queues.ipynb")
    write(M20, ROOT / "Module_20_Performance_Optimization_Profiling_Caching"
                     / "04_interactive_profiling_and_caching.ipynb")

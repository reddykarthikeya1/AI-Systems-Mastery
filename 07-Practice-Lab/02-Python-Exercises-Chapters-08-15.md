# Python Exercises: Chapters 08 to 15

> Each chapter has graded exercises with hidden tests: two coding exercises and one debugging exercise. Create your files with `python 01-Python-Mastery/exercises/run.py --init`, edit `exercises/chNN.py`, then run `python 01-Python-Mastery/exercises/run.py NN`. Hints are also available in the terminal with `--hints NN` and walkthroughs with `--explain NN`.

---

## Chapter 08: Environments, dependencies, packaging

**The three exercises**

- parse_requirement: parse a requirements.txt line.
- satisfies: check a version against a specifier set such as ">=1.2,<2.0" or "~=1.4.2".
- latest (debugging): picks the wrong "newest" version.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 08 - Environments, dependencies, packaging.

1. parse_requirement: parse a requirements.txt line.
2. satisfies: check a version against a specifier set such as ">=1.2,<2.0" or "~=1.4.2".
3. latest (debugging): picks the wrong "newest" version."""

import re

def parse_requirement(line):
    """Parse 'Requests[security]>=2.0,<3  # comment' into ('requests', ['security'], [('>=', '2.0'), ('<', '3')]).
The name is lowercased with runs of '-', '_' and '.' normalised to '-'. Blank lines and full-line comments return None.
Extras are returned sorted; specifiers keep their written order."""
    raise NotImplementedError()

def satisfies(version, spec):
    """True when `version` meets every comma-separated clause of `spec` (empty spec = always True).
Supports ==, !=, >=, <=, >, < and the compatible-release operator: ~=1.4.2 means >=1.4.2,<1.5 and ~=1.4 means >=1.4,<2.
Versions compare numerically per component, padding with zeros (1.0 == 1.0.0)."""
    raise NotImplementedError()

def latest(versions):
    """Return the highest version string from a non-empty list of dotted numeric versions (1.10 is newer than 1.9)."""
    return max(versions)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Parsing semantic version strings and PEP 440 constraints.
2. Split versions into major, minor, patch tuples and compare lexically.
3. Handle compatible release operator (~=) by freezing upper bound to next major.

**Exercise 2**

1. Resolving dependency conflict trees across packages.
2. Topological sorting / DFS with visited set to detect cycles.
3. Track constraints per package and raise IncompatibleVersionError on disjoint ranges.

**Exercise 3**

1. Wheel tag extraction and manylinux compatibility check.
2. Extract Python tag, ABI tag, and platform tag from wheel filename.
3. Ensure system glibc version meets or exceeds wheel minimum requirement.

</details>

<details>
<summary>What the hidden tests check</summary>

- `latest_numeric`
- `parse_requirement_edge`
- `parse_requirement_full`
- `satisfies_basic`
- `satisfies_compatible_release`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import re

def parse_requirement(line):
    """Parse 'Requests[security]>=2.0,<3  # comment' into ('requests', ['security'], [('>=', '2.0'), ('<', '3')]).
    The name is lowercased with runs of '-', '_' and '.' normalised to '-'. Blank lines and full-line comments return None.
    Extras are returned sorted; specifiers keep their written order."""
    line = line.split("#", 1)[0].strip()
    if not line:
        return None
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[([^\]]*)\])?\s*(.*)$", line)
    if not m:
        raise ValueError(f"bad requirement: {line!r}")
    name = re.sub(r"[-_.]+", "-", m.group(1)).lower()
    extras = sorted(e.strip() for e in (m.group(2) or "").split(",") if e.strip())
    specs = []
    for part in filter(None, (p.strip() for p in m.group(3).split(","))):
        sm = re.match(r"^(==|!=|>=|<=|~=|>|<)\s*([0-9][0-9A-Za-z.*]*)$", part)
        if not sm:
            raise ValueError(f"bad specifier: {part!r}")
        specs.append((sm.group(1), sm.group(2)))
    return name, extras, specs

def satisfies(version, spec):
    """True when `version` meets every comma-separated clause of `spec` (empty spec = always True).
    Supports ==, !=, >=, <=, >, < and the compatible-release operator: ~=1.4.2 means >=1.4.2,<1.5 and ~=1.4 means >=1.4,<2.
    Versions compare numerically per component, padding with zeros (1.0 == 1.0.0)."""
    v = _vt(version)
    for clause in filter(None, (c.strip() for c in spec.split(","))):
        op, rhs = re.match(r"^(==|!=|>=|<=|~=|>|<)\s*(.+)$", clause).groups()
        r = _vt(rhs)
        a, b = _pad(v, r)
        if op == "~=":
            prefix = r[:-1]
            upper = prefix[:-1] + (prefix[-1] + 1,)
            lo, hi = _pad(v, upper)
            ok = a >= b and lo < hi
        else:
            ok = {"==": a == b, "!=": a != b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]
        if not ok:
            return False
    return True

def latest(versions):
    """Return the highest version string from a non-empty list of dotted numeric versions (1.10 is newer than 1.9)."""
    return max(versions, key=_vt)
```

**1. parse_requirement**

*Approach.* Strip comments, match the name, optional extras and the specifier tail with one regex, normalise the name (lowercase, runs of - _ . become -) and sort extras.

*Complexity.* O(len).

*Common wrong answers.*

- Normalising only case misses My_Pkg and my.pkg equivalence.
- Splitting specifiers on '<' breaks on '<='; match operators explicitly.

**2. satisfies**

*Approach.* Convert versions to integer tuples, pad with zeros, and test each clause. For ~=X.Y.Z the upper bound is the previous component incremented.

*Complexity.* O(clauses x components).

*Common wrong answers.*

- String comparison orders 1.10 before 1.9.
- Treating ~=1.4.2 as >=1.4.2 alone ignores the upper bound.

**3. latest (debug)**

*Approach.* max() on strings compares lexicographically. Give max a key that turns '1.10' into (1, 10).

*Complexity.* O(n x components).

*Common wrong answers.*

- sorted(...)[-1] has the same string bug.
- Pre-release tags need their own ordering rules (PEP 440), which this exercise omits.

</details>

---

## Chapter 09: Testing with fakes, injected clocks and idempotency

**The three exercises**

- retry: retry with exponential backoff, with `sleep` injected so tests need no real waiting.
- RateLimiter: sliding-window limiter with an injected clock.
- charge_once (debugging): a failed payment can never be retried.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 09 - Testing with fakes, injected clocks and idempotency.

1. retry: retry with exponential backoff, with `sleep` injected so tests need no real waiting.
2. RateLimiter: sliding-window limiter with an injected clock.
3. charge_once (debugging): a failed payment can never be retried."""

def retry(fn, attempts, sleep, base=1.0):
    """Call fn() up to `attempts` times. After failure number k (1-based) that is not the last, call sleep(base * 2**(k-1)).
Return fn's first successful result; re-raise the LAST exception when all attempts fail. attempts < 1 raises ValueError.
Only Exception subclasses are retried (KeyboardInterrupt must pass through)."""
    raise NotImplementedError()

class RateLimiter:
    """Allow at most `limit` calls per key within any sliding window of `window` seconds.
    allow(key) returns True (and records the call) or False. `clock` is a zero-argument callable returning seconds.
    A call exactly `window` seconds after an earlier one no longer counts against it."""

    def __init__(self, limit, window, clock):
        raise NotImplementedError()

    def allow(self, key):
        raise NotImplementedError()

def charge_once(ledger, order_id, amount, gateway):
    """Idempotent payment. `ledger` is a dict order_id -> receipt. Charge via gateway(amount) at most once per order_id,
    return the receipt. If the gateway raises, nothing is recorded, so a later call with the same order_id tries again."""
    if order_id in ledger:
        return ledger[order_id]
    ledger[order_id] = "pending"
    ledger[order_id] = gateway(amount)
    return ledger[order_id]
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Retrying flaky external calls with exponential backoff and jitter.
2. Loop with retry count, calculating delay = base * (factor ** attempt) + jitter.
3. Re-raise the final caught exception if all retry attempts are exhausted.

**Exercise 2**

1. Thread-safe rate limiter for API clients.
2. Sliding window counter using collections.deque of timestamps protected by a Lock.
3. Pop timestamps older than (now - window) before comparing current count against limit.

**Exercise 3**

1. Mocking async dependencies in pytest without leaking unawaited coroutines.
2. Use unittest.mock.AsyncMock with return_value or side_effect.
3. Verify assertions using mock.assert_awaited_once_with().

</details>

<details>
<summary>What the hidden tests check</summary>

- `charge_once_retry_after_failure`
- `ratelimiter_rejected_calls_do_not_count`
- `ratelimiter_window`
- `retry_backoff_schedule`
- `retry_gives_up_with_last_error`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
def retry(fn, attempts, sleep, base=1.0):
    """Call fn() up to `attempts` times. After failure number k (1-based) that is not the last, call sleep(base * 2**(k-1)).
    Return fn's first successful result; re-raise the LAST exception when all attempts fail. attempts < 1 raises ValueError.
    Only Exception subclasses are retried (KeyboardInterrupt must pass through)."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    for k in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if k == attempts:
                raise
            sleep(base * 2 ** (k - 1))

class RateLimiter:
    """Allow at most `limit` calls per key within any sliding window of `window` seconds.
    allow(key) returns True (and records the call) or False. `clock` is a zero-argument callable returning seconds.
    A call exactly `window` seconds after an earlier one no longer counts against it."""

    def __init__(self, limit, window, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self._calls = {}

    def allow(self, key):
        now = self.clock()
        q = self._calls.setdefault(key, [])
        q[:] = [t for t in q if now - t < self.window]
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True

def charge_once(ledger, order_id, amount, gateway):
    """Idempotent payment. `ledger` is a dict order_id -> receipt. Charge via gateway(amount) at most once per order_id,
    return the receipt. If the gateway raises, nothing is recorded, so a later call with the same order_id tries again."""
    if order_id in ledger:
        return ledger[order_id]
    receipt = gateway(amount)
    ledger[order_id] = receipt
    return receipt
```

**1. retry**

*Approach.* Loop attempts; after failure k that is not the last, call the injected sleep with base * 2**(k-1); re-raise the last exception. Catch Exception, not BaseException.

*Complexity.* At most `attempts` calls.

*Common wrong answers.*

- Calling time.sleep directly makes the test slow and flaky; inject it.
- A bare except swallows KeyboardInterrupt.

**2. RateLimiter**

*Approach.* Keep a list of timestamps per key, drop those older than the window (now - t < window keeps the rest), allow while under the limit, and only record allowed calls.

*Complexity.* O(calls in window) per call.

*Common wrong answers.*

- Recording rejected calls extends the penalty.
- Using <= instead of < makes an event exactly one window old still count.

**3. charge_once (debug)**

*Approach.* Record the receipt only after the gateway succeeds. Writing a 'pending' marker first turns a transient failure into a permanent one.

*Complexity.* O(1).

*Common wrong answers.*

- Marking before acting is correct for locks but wrong for idempotency caches.
- Catching and ignoring the gateway error hides the failure from the caller.

</details>

---

## Chapter 10: Production debugging and profiling

**The three exercises**

- peak_alloc_kb: measure the peak memory a call allocates (tracemalloc).
- growth_by_line: find the source line responsible for memory growth.
- render (debugging): a cache that eventually eats all the memory.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 10 - Production debugging and profiling.

1. peak_alloc_kb: measure the peak memory a call allocates (tracemalloc).
2. growth_by_line: find the source line responsible for memory growth.
3. render (debugging): a cache that eventually eats all the memory."""

import functools
import time
import tracemalloc

def peak_alloc_kb(fn):
    """Run fn() under tracemalloc and return the peak traced memory in KiB (a float). Leave tracemalloc stopped afterwards."""
    raise NotImplementedError()

def growth_by_line(fn, rounds=50):
    """Call fn() `rounds` times between two tracemalloc snapshots and return (lineno, bytes_added) for the line INSIDE fn's
own file that grew the most. Return None if nothing grew. Leave tracemalloc stopped afterwards."""
    raise NotImplementedError()

@functools.lru_cache(maxsize=None)
def render(user_id):
    """Expensive pure function of user_id, cached. The cache must stay bounded at 128 entries."""
    return "x" * 1000 + str(user_id)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Measuring memory growth per line of code.
2. Use tracemalloc.start(), take snapshot1, execute code, take snapshot2.
3. Compare snapshots using snapshot2.compare_to(snapshot1, 'lineno').

**Exercise 2**

1. Bounded cache avoiding unbounded memory expansion.
2. Implement a maximum size and drop oldest keys when limit is reached.
3. Use collections.OrderedDict or cachetools to prevent process OOM crashes.

**Exercise 3**

1. CPU profiling analysis using cProfile and pstats.
2. cProfile.Profile(), enable(), code(), disable().
3. pstats.Stats(prof).strip_dirs().sort_stats('cumulative').print_stats(10).

</details>

<details>
<summary>What the hidden tests check</summary>

- `growth_by_line_finds_leak`
- `growth_by_line_no_growth`
- `peak_alloc_scales`
- `render_cache_bounded`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import functools
import time
import tracemalloc

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

def render(user_id):
    """Expensive pure function of user_id, cached. The cache must stay bounded at 128 entries."""
    return "x" * 1000 + str(user_id)
```

**1. peak_alloc_kb**

*Approach.* tracemalloc.start(), run, read get_traced_memory() peak, always stop in finally.

*Complexity.* Overhead about 2 to 4 times slower while tracing.

*Common wrong answers.*

- Reading the current value instead of the peak misses temporary spikes.
- Leaving tracing on slows everything after the call.

**2. growth_by_line**

*Approach.* Snapshot before and after, compare_to(before, 'lineno'), filter to the function's own file, and return the line with the largest positive size_diff.

*Complexity.* O(allocated blocks).

*Common wrong answers.*

- Reporting the top diff overall returns tracemalloc's own frames or the test harness.
- Too few rounds hide small leaks inside noise.

**3. render (debug)**

*Approach.* lru_cache(maxsize=None) never evicts, so unique keys grow forever. Give it a bound (128) and watch cache_info().currsize.

*Complexity.* O(1) per call; memory bounded.

*Common wrong answers.*

- maxsize=None is the right choice only for a small, closed key space.
- Caching a method keeps self alive; prefer a module-level function or a per-instance cache.

</details>

---

## Chapter 11: Legacy refactoring and break-fix

**The three exercises**

- characterize: record what legacy code does today so a refactor can be compared against it.
- shadow_compare: run old and new implementations side by side (strangler-fig migration).
- sorted_names (debugging): a helper that silently reorders its caller's data.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 11 - Legacy refactoring and break-fix.

1. characterize: record what legacy code does today so a refactor can be compared against it.
2. shadow_compare: run old and new implementations side by side (strangler-fig migration).
3. sorted_names (debugging): a helper that silently reorders its caller's data."""

def characterize(fn, inputs):
    """Call fn(*args) for each args tuple in `inputs`. Return a list of ('ok', result) or ('raises', 'ExceptionClassName'), in order."""
    raise NotImplementedError()

def shadow_compare(old, new, on_diff):
    """Return a function that calls old(*a, **kw) and ALSO new(*a, **kw), but always returns/raises exactly what old does.
When new's result differs from old's, or new raises, or exactly one of them raises, call on_diff(args, kwargs, old_outcome, new_outcome)
where an outcome is ('ok', value) or ('raises', 'ExceptionClassName'). A failure of new must never affect the caller."""
    raise NotImplementedError()

def sorted_names(users):
    """Return the 'name' of each user dict ordered by 'age' then 'name'. The caller's list must not be modified."""
    users.sort(key=lambda u: (u["age"], u["name"]))
    return [u["name"] for u in users]
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Characterizing legacy function behavior with regression tests.
2. Record input-output pairs across diverse boundary inputs before refactoring.
3. Ensure refactored version produces identical output for all characterization cases.

**Exercise 2**

1. Shadow execution / dual-writing pattern.
2. Call legacy implementation first, call new implementation in try/except.
3. Compare results; if they differ, log telemetry without impacting caller; return legacy result.

**Exercise 3**

1. Defensive copying in legacy functions that inadvertently mutate caller arguments.
2. Check if inputs are sorted or modified in place (e.g. list.sort()).
3. Use sorted() or defensive copy to ensure input arguments remain unmutated.

</details>

<details>
<summary>What the hidden tests check</summary>

- `characterize_records_results_and_errors`
- `shadow_agrees_silently`
- `shadow_new_failure_never_leaks`
- `shadow_reports_diff_and_returns_old`
- `sorted_names_does_not_mutate`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
def characterize(fn, inputs):
    """Call fn(*args) for each args tuple in `inputs`. Return a list of ('ok', result) or ('raises', 'ExceptionClassName'), in order."""
    out = []
    for args in inputs:
        try:
            out.append(("ok", fn(*args)))
        except Exception as e:
            out.append(("raises", type(e).__name__))
    return out

def shadow_compare(old, new, on_diff):
    """Return a function that calls old(*a, **kw) and ALSO new(*a, **kw), but always returns/raises exactly what old does.
    When new's result differs from old's, or new raises, or exactly one of them raises, call on_diff(args, kwargs, old_outcome, new_outcome)
    where an outcome is ('ok', value) or ('raises', 'ExceptionClassName'). A failure of new must never affect the caller."""
    def call(fn, a, kw):
        try:
            return ("ok", fn(*a, **kw)), None
        except Exception as e:
            return ("raises", type(e).__name__), e

    def wrapper(*a, **kw):
        old_out, old_exc = call(old, a, kw)
        new_out, _ = call(new, a, kw)
        if old_out != new_out:
            on_diff(a, kw, old_out, new_out)
        if old_exc is not None:
            raise old_exc
        return old_out[1]

    return wrapper

def sorted_names(users):
    """Return the 'name' of each user dict ordered by 'age' then 'name'. The caller's list must not be modified."""
    return [u["name"] for u in sorted(users, key=lambda u: (u["age"], u["name"]))]
```

**1. characterize**

*Approach.* Call the legacy function for each input tuple and record either ('ok', result) or ('raises', exception name). That recording is the safety net for a refactor.

*Complexity.* O(inputs).

*Common wrong answers.*

- Recording only successes misses behaviour that callers depend on (exceptions).
- Comparing exception objects fails; compare class names.

**2. shadow_compare**

*Approach.* Run old and new, return the old outcome, report differences through a callback, and never let the new path's failure reach the caller.

*Complexity.* Roughly doubles latency while shadowing.

*Common wrong answers.*

- Returning the new result before it is trusted defeats the point.
- Running both paths against side-effecting code needs fakes or read-only mode.

**3. sorted_names (debug)**

*Approach.* list.sort() mutates the caller's list. Use sorted(...), which returns a new list.

*Complexity.* O(n log n).

*Common wrong answers.*

- Copying with users[:] before sort() also works but is easy to forget.
- Mutating inputs creates bugs far from the cause.

</details>

---

## Chapter 12: SQL and database internals (sqlite3)

**The three exercises**

- top_customers: aggregate query. Tables: customers(id, name), orders(id, customer_id, amount).
- add_index_for_events: make `SELECT * FROM events WHERE user_id = ?` use an index.
- transfer (debugging): a failed transfer leaves money missing.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 12 - SQL and database internals (sqlite3).

1. top_customers: aggregate query. Tables: customers(id, name), orders(id, customer_id, amount).
2. add_index_for_events: make `SELECT * FROM events WHERE user_id = ?` use an index.
3. transfer (debugging): a failed transfer leaves money missing."""

def top_customers(conn, n):
    """Return up to n (name, total_spent) rows for customers that have orders, highest total first, ties by name."""
    raise NotImplementedError()

def add_index_for_events(conn):
    """Create whatever index makes `SELECT * FROM events WHERE user_id = ?` avoid a full scan (table events(id, user_id, kind)).
Return the EXPLAIN QUERY PLAN detail text of that query."""
    raise NotImplementedError()

def transfer(conn, src, dst, amount):
    """Move `amount` between rows of acct(id, bal). Atomic: if the destination does not exist (KeyError) or the
    source would go negative (ValueError), the database must be unchanged."""
    conn.execute("UPDATE acct SET bal = bal - ? WHERE id = ?", (amount, src))
    conn.commit()
    cur = conn.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amount, dst))
    if cur.rowcount != 1:
        raise KeyError(dst)
    conn.commit()
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Preventing SQL injection and managing transaction atomicity.
2. Never use f-strings or string concatenation to build SQL statements.
3. Use parameterized queries with context manager transactions (commit on success, rollback on error).

**Exercise 2**

1. Eliminating N+1 queries in relational data access.
2. Instead of querying children in a loop, query all children using WHERE parent_id IN (...).
3. Group children in a dictionary keyed by parent_id in O(N) application time.

**Exercise 3**

1. Verifying database indexes with EXPLAIN QUERY PLAN.
2. Run EXPLAIN QUERY PLAN before queries in SQLite to confirm 'SEARCH TABLE USING INDEX'.
3. Ensure queries avoid full table scans ('SCAN TABLE') on large tables.

</details>

<details>
<summary>What the hidden tests check</summary>

- `index_used`
- `top_customers_does_not_double_count`
- `top_customers_ordering`
- `transfer_is_atomic`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
def top_customers(conn, n):
    """Return up to n (name, total_spent) rows for customers that have orders, highest total first, ties by name."""
    return conn.execute(
        "SELECT c.name, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.id "
        "GROUP BY c.id ORDER BY total DESC, c.name ASC LIMIT ?", (n,)).fetchall()

def add_index_for_events(conn):
    """Create whatever index makes `SELECT * FROM events WHERE user_id = ?` avoid a full scan (table events(id, user_id, kind)).
    Return the EXPLAIN QUERY PLAN detail text of that query."""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id)")
    rows = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = ?", (1,)).fetchall()
    return " ".join(r[-1] for r in rows)

def transfer(conn, src, dst, amount):
    """Move `amount` between rows of acct(id, bal). Atomic: if the destination does not exist (KeyError) or the
    source would go negative (ValueError), the database must be unchanged."""
    with conn:
        cur = conn.execute("UPDATE acct SET bal = bal - ? WHERE id = ? AND bal >= ?", (amount, src, amount))
        if cur.rowcount != 1:
            raise ValueError("insufficient funds or unknown source")
        cur = conn.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amount, dst))
        if cur.rowcount != 1:
            raise KeyError(dst)
```

**1. top_customers**

*Approach.* JOIN orders, GROUP BY the customer's primary key (not the name), ORDER BY the total descending then the name, LIMIT n with a bound parameter.

*Complexity.* Roughly O(orders) plus the sort of groups.

*Common wrong answers.*

- Grouping by name merges two different customers who share a name.
- Interpolating n into the SQL string invites injection; bind it.

**2. add_index_for_events**

*Approach.* Create an index on the filtered column and confirm with EXPLAIN QUERY PLAN that it says SEARCH ... USING INDEX instead of SCAN.

*Complexity.* Lookup O(log n) instead of O(n).

*Common wrong answers.*

- An index on the wrong column (or a function of it) is never used.
- Indexes slow writes and cost space; add them for real query patterns.

**3. transfer (debug)**

*Approach.* Wrap both updates in one transaction (with conn:), guard the debit with bal >= amount, and raise before commit so the rollback restores everything.

*Complexity.* O(1) statements.

*Common wrong answers.*

- Committing after the first update makes the half-done state permanent.
- Checking the balance in Python before the update races with other writers; check inside the UPDATE.

</details>

---

## Chapter 13: FastAPI and Pydantic v2 (needs `pip install "pydantic>=2"`; the runner skips this chapter without it)

**The three exercises**

- User: a model with validation rules.
- parse_or_errors: turn a ValidationError into a simple list of 'field: message' strings.
- Item (debugging): numeric strings are silently coerced; make the model strict.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 13 - FastAPI and Pydantic v2 (needs `pip install "pydantic>=2"`; the runner skips this chapter without it).

1. User: a model with validation rules.
2. parse_or_errors: turn a ValidationError into a simple list of 'field: message' strings.
3. Item (debugging): numeric strings are silently coerced; make the model strict."""

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

class User(BaseModel):
    """User(email: str, age: int). email must contain exactly one '@' and be stored lowercased and stripped;
    age must be 0..150."""
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator('email')
    @classmethod
    def _email(cls, v):
        raise NotImplementedError()

class Item(BaseModel):
    """Item(name: str, qty: int) that REJECTS qty='3' (a string) instead of coercing it, and rejects qty < 1."""
    name: str
    qty: int

def parse_or_errors(model, data):
    """Return (instance, []) when `data` validates, else (None, sorted list of 'field: message') using the first loc element as field."""
    raise NotImplementedError()
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Pydantic V2 schema validation and custom field sanitization.
2. Use @field_validator with mode='before' or mode='after'.
3. Strip whitespace, lowercase email addresses, and raise ValueError on malformed inputs.

**Exercise 2**

1. Strict models rejecting extra unexpected fields.
2. model_config = ConfigDict(extra='forbid', str_strip_whitespace=True).
3. Validate payload with model.model_validate(data) and handle ValidationError.

**Exercise 3**

1. FastAPI ASGI lifespan context manager.
2. Use @asynccontextmanager on app lifespan to initialize and teardown DB pools.
3. Yield control during server execution; cleanup resources in finally block.

</details>

<details>
<summary>What the hidden tests check</summary>

- `item_is_strict`
- `parse_or_errors_success_shape`
- `user_normalises_email`
- `user_rejects_bad_values`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

class User(BaseModel):
    """User(email: str, age: int). email must contain exactly one '@' and be stored lowercased and stripped;
    age must be 0..150."""
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        v = v.strip().lower()
        if v.count("@") != 1:
            raise ValueError("must contain exactly one @")
        return v

class Item(BaseModel):
    """Item(name: str, qty: int) that REJECTS qty='3' (a string) instead of coercing it, and rejects qty < 1."""
    model_config = ConfigDict(strict=True)
    name: str
    qty: int = Field(ge=1)

def parse_or_errors(model, data):
    """Return (instance, []) when `data` validates, else (None, sorted list of 'field: message') using the first loc element as field."""
    try:
        return model.model_validate(data), []
    except ValidationError as e:
        return None, sorted(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())
```

**1. User model**

*Approach.* Annotate fields, add Field(ge=0, le=150) for the age range, and a field_validator that strips, lowercases and checks exactly one '@'.

*Complexity.* O(len) per validation.

*Common wrong answers.*

- Validating in __init__ by hand loses error aggregation and schema generation.
- Pydantic v1 names (validator, Config) do not exist in v2.

**2. parse_or_errors**

*Approach.* Catch ValidationError and format e.errors() as 'field: message', sorted so output is stable.

*Complexity.* O(errors).

*Common wrong answers.*

- Using str(e) gives a multi-line message that is hard to assert on.
- Nested fields have longer loc tuples; this exercise uses the first element.

**3. Item (debug)**

*Approach.* Pydantic coerces '3' to 3 by default. Strict mode (ConfigDict(strict=True)) rejects it; combine with Field(ge=1).

*Complexity.* O(fields).

*Common wrong answers.*

- Adding a validator that calls int() re-introduces coercion.
- Strict mode also rejects 3.0 for an int; decide whether that is what the API wants.

</details>

---

## Chapter 14: Security: signed tokens and RBAC (stdlib only)

**The three exercises**

- sign_token / verify_token: a minimal HS256 JWT, built with hmac and base64url.
- can: role-based access control with role inheritance.
- check_password_hash (debugging): a timing leak and a missing salt check.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 14 - Security: signed tokens and RBAC (stdlib only).

1. sign_token / verify_token: a minimal HS256 JWT, built with hmac and base64url.
2. can: role-based access control with role inheritance.
3. check_password_hash (debugging): a timing leak and a missing salt check."""

import base64
import hashlib
import hmac
import json
import time

def sign_token(payload, secret, now=None):
    """Return 'header.payload.signature' (base64url, no padding) for header {"alg":"HS256","typ":"JWT"}.
Signature = HMAC-SHA256(secret, 'header.payload'). JSON uses separators=(',', ':') and sort_keys=True. `secret` is bytes."""
    raise NotImplementedError()

def verify_token(token, secret, now=None):
    """Return the payload dict if the token is valid, else raise ValueError. Reject: wrong shape, bad signature
(constant-time compare), header alg other than HS256 (including 'none'), and an 'exp' claim <= now (default time.time())."""
    raise NotImplementedError()

def can(roles, role, permission):
    """`roles` maps role -> {'perms': set of strings, 'inherits': list of role names}. Return True if `role` has `permission`
directly or through inheritance. A permission ending in '*' (e.g. 'doc:*') grants everything with that prefix.
Unknown roles have no permissions; inheritance cycles must not loop forever."""
    raise NotImplementedError()

def verify_signature(secret: bytes, message: bytes, signature_hex: str) -> bool:
    """True when signature_hex is the HMAC-SHA256 of message under secret. Must use a constant-time comparison."""
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return expected == signature_hex
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Constant-time signature verification preventing timing attacks.
2. Never compare cryptographic hashes or tokens with standard `==`.
3. Use hmac.compare_digest(token_a, token_b) to prevent side-channel timing analysis.

**Exercise 2**

1. JWT token generation and verification.
2. Encode header, payload, and HMAC-SHA256 signature encoded with base64url.
3. Verify signature, check 'exp' timestamp against time.time(), and reject 'none' algorithm.

**Exercise 3**

1. Role-Based Access Control (RBAC) permission resolution.
2. Support wildcards (e.g., 'reports:*') and role inheritance hierarchies.
3. Evaluate permissions using set intersections or prefix tree matching.

</details>

<details>
<summary>What the hidden tests check</summary>

- `can_inheritance_and_wildcards`
- `token_matches_reference_signature`
- `token_rejections`
- `token_rejects_alg_none`
- `token_roundtrip`
- `verify_signature_constant_time`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import base64
import hashlib
import hmac
import json
import time

def sign_token(payload, secret, now=None):
    """Return 'header.payload.signature' (base64url, no padding) for header {"alg":"HS256","typ":"JWT"}.
    Signature = HMAC-SHA256(secret, 'header.payload'). JSON uses separators=(',', ':') and sort_keys=True. `secret` is bytes."""
    head = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":"), sort_keys=True).encode())
    body = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    sig = hmac.new(secret, f"{head}.{body}".encode(), hashlib.sha256).digest()
    return f"{head}.{body}.{_b64(sig)}"

def verify_token(token, secret, now=None):
    """Return the payload dict if the token is valid, else raise ValueError. Reject: wrong shape, bad signature
    (constant-time compare), header alg other than HS256 (including 'none'), and an 'exp' claim <= now (default time.time())."""
    try:
        head_b, body_b, sig_b = token.split(".")
        header = json.loads(_unb64(head_b))
        payload = json.loads(_unb64(body_b))
        sig = _unb64(sig_b)
    except Exception as e:
        raise ValueError("malformed token") from e
    if header.get("alg") != "HS256":
        raise ValueError("unsupported alg")
    good = hmac.new(secret, f"{head_b}.{body_b}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(good, sig):
        raise ValueError("bad signature")
    now = time.time() if now is None else now
    if "exp" in payload and payload["exp"] <= now:
        raise ValueError("expired")
    return payload

def can(roles, role, permission):
    """`roles` maps role -> {'perms': set of strings, 'inherits': list of role names}. Return True if `role` has `permission`
    directly or through inheritance. A permission ending in '*' (e.g. 'doc:*') grants everything with that prefix.
    Unknown roles have no permissions; inheritance cycles must not loop forever."""
    seen, stack = set(), [role]
    while stack:
        r = stack.pop()
        if r in seen or r not in roles:
            continue
        seen.add(r)
        for p in roles[r].get("perms", ()):
            if p == permission or (p.endswith("*") and permission.startswith(p[:-1])):
                return True
        stack.extend(roles[r].get("inherits", ()))
    return False

def verify_signature(secret: bytes, message: bytes, signature_hex: str) -> bool:
    """True when signature_hex is the HMAC-SHA256 of message under secret. Must use a constant-time comparison."""
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_hex)
```

**1. sign_token / verify_token**

*Approach.* Base64url-encode header and payload without padding, sign 'header.payload' with HMAC-SHA256, and on verify check shape, algorithm, signature with compare_digest, then exp.

*Complexity.* O(len).

*Common wrong answers.*

- Accepting alg=none lets anyone forge tokens.
- Comparing signatures with == leaks timing; use hmac.compare_digest.

**2. can (RBAC)**

*Approach.* Depth-first walk over inheritance with a seen-set, matching exact permissions or prefix wildcards ('doc:*'). Unknown roles grant nothing.

*Complexity.* O(roles + permissions).

*Common wrong answers.*

- Recursing without a seen-set loops forever on a cycle.
- Treating '*' as a regex instead of a prefix match.

**3. verify_signature (debug)**

*Approach.* String == stops at the first differing byte, so timing reveals how much of a guess is right. hmac.compare_digest takes constant time for equal-length inputs.

*Complexity.* O(len).

*Common wrong answers.*

- Hashing both sides first is not a substitute for compare_digest.
- Comparing hex strings of different lengths is still safe with compare_digest but leaks length.

</details>

---

## Chapter 15: Task queues: scheduling, retries, idempotency (in-memory model of what Celery/Redis do)

**The three exercises**

- DelayQueue: tasks that become visible at a given time; ordered by due time then insertion.
- backoff_delays: capped exponential backoff with deterministic "full jitter".
- Worker.process (debugging): a crash between 'pop' and 'ack' loses the task.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 15 - Task queues: scheduling, retries, idempotency (in-memory model of what Celery/Redis do).

1. DelayQueue: tasks that become visible at a given time; ordered by due time then insertion.
2. backoff_delays: capped exponential backoff with deterministic "full jitter".
3. Worker.process (debugging): a crash between 'pop' and 'ack' loses the task."""

import heapq
import itertools
import random

class DelayQueue:
    """push(item, due) schedules an item. pop_due(now) returns all items with due <= now, ordered by due time then
    insertion order, and removes them. len(q) counts the pending items. next_due() returns the earliest due time or None."""

    def __init__(self):
        raise NotImplementedError()

    def push(self, item, due):
        raise NotImplementedError()

    def pop_due(self, now):
        raise NotImplementedError()

    def next_due(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

def backoff_delays(attempts, base, cap, seed=0):
    """Return `attempts` delays. Delay k (0-based) is uniform in [0, min(cap, base * 2**k)] ("full jitter"), drawn from
random.Random(seed) in order so the sequence is reproducible. attempts=0 gives []."""
    raise NotImplementedError()

class Worker:
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
        return task
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Priority and delayed task queues with Redis or heapq.
2. Use heapq with (delivery_timestamp, priority, task_id, task) tuples.
3. Implement a worker loop that pops tasks only when delivery_timestamp <= now.

**Exercise 2**

1. Exponential backoff with full jitter for distributed task retry.
2. delay = random.uniform(0, min(cap, base * 2 ** attempt)).
3. Prevents thundering herd problem when a shared dependency recovers.

**Exercise 3**

1. Worker task retry state preservation.
2. Do not discard failed task parameters; increment retry_count and reschedule.
3. Move task to Dead Letter Queue (DLQ) when max retries exceeded.

</details>

<details>
<summary>What the hidden tests check</summary>

- `backoff_bounds_and_determinism`
- `backoff_reaches_cap`
- `delayqueue_non_comparable_items`
- `delayqueue_ordering`
- `worker_keeps_failed_task`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import heapq
import itertools
import random

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
```

**1. DelayQueue**

*Approach.* A heap of (due, sequence, item). The sequence counter breaks ties by insertion order and stops the heap from comparing the items themselves.

*Complexity.* push and pop O(log n).

*Common wrong answers.*

- Pushing (due, item) fails when two items share a due time and the items are not comparable.
- pop_due must use <= so a task due exactly now is returned.

**2. backoff_delays**

*Approach.* Delay k is uniform in [0, min(cap, base * 2**k)] drawn from random.Random(seed) so the sequence is reproducible.

*Complexity.* O(attempts).

*Common wrong answers.*

- Without jitter every client retries in lockstep and re-creates the overload.
- Using the global random state makes tests flaky.

**3. Worker (debug)**

*Approach.* Peek at the front task, run the handler, and pop only after success, so a crash leaves the task queued (at-least-once). Popping first loses it (at-most-once).

*Complexity.* O(1) per task.

*Common wrong answers.*

- Handlers must be idempotent because retries can repeat work.
- list.pop(0) is O(n); use a deque in production.

</details>


# Debug Lab 18 — Answers

> Read this only after you have written a diagnosis for each symptom.

Six defects. Every one produces a plausible wrong number rather than a crash,
which is why the exit code is 0 and why none of them would be caught by
"does the pipeline run?" monitoring.

---

## Defect 1 — the as-of lookup returns the current version

**Location:** `DimensionTable.lookup_as_of`

```python
def lookup_as_of(self, natural_key: str, when: date) -> int | None:
    version = self.current(natural_key)          # ignores `when` entirely
    return version.surrogate_key if version else None
```

The `when` argument is accepted and discarded. The function always returns
whichever version is open *right now*.

**Fix:**

```python
def lookup_as_of(self, natural_key: str, when: date) -> int | None:
    for version in self._versions.get(natural_key, []):
        if version.covers(when):
            return version.surrogate_key
    return None
```

**Why the first load looked correct.** In `[1]`, every fact row is loaded before
`C1` moves. At that moment the current version *is* the historically correct one,
so `current()` and a proper as-of lookup return the same key. The bug is
invisible.

In `[1b]` the same rows are loaded *after* the move. Now `current()` returns the
Texas key for the March and April sales, and $130 of Ohio revenue relocates.
`C2` is unaffected because `C2` never moved — that is the clue in Symptom 1.

**Why this matters more than it looks.** Reprocessing a partition is routine:
an upstream correction, a schema change, a late-arriving file. A warehouse
whose history depends on *when you happened to load it* is not a warehouse, it
is a cache with an accent. This is the single most common dimensional-modelling
defect in production, and the reason SCD2 exists at all.

**Proved by:** `test_scd2_preserves_history`

---

## Defect 2 — the closing `valid_to` is off by one day

**Location:** `DimensionTable.upsert`

```python
existing.valid_to = effective              # should be effective - 1 day
```

**Fix:**

```python
existing.valid_to = effective - timedelta(days=1)
```

**Consequence.** `DimensionVersion.covers` is inclusive at both ends, so on
2024-06-01 both the Ohio row (`valid_to = 2024-06-01`) and the Texas row
(`valid_from = 2024-06-01`) match. An as-of join for that date matches two
dimension rows, and a `SUM` across that join **double-counts** every fact row
dated 2024-06-01.

One day per change, per key. Easy to miss in a spot check, and it compounds:
a dimension with monthly churn produces twelve double-counted days a year.

The general rule: pick one convention — half-open `[valid_from, valid_to)` or
closed `[valid_from, valid_to]` — write it down next to the schema, and make the
tiling test assert it. Mixing the two is where this bug comes from.

**Proved by:** `test_scd2_intervals_tile_the_timeline`

---

## Defect 3 — the incremental merge replaces instead of accumulating

**Location:** `RevenueByStateView.refresh_incremental`

```python
self._data.update(delta)      # dict.update REPLACES the value for each key
```

`dict.update` is the wrong verb. For every key present in `delta`, it discards
the accumulated total and substitutes the delta.

**Fix:**

```python
for key, value in delta.items():
    self._data[key] = self._data.get(key, 0.0) + value
```

**Reading the numbers.** Ohio's total was $180; the delta was $40; the result was
$40, not $220. `TX` was untouched because no Texas rows appeared in the delta, so
`update` never visited that key — which is exactly why the bug looks like it only
affects *some* states, and why a spot check on the wrong state passes.

**The broader trap.** This merge shape is only valid for *additive* measures.
`SUM` and `COUNT` merge. `COUNT(DISTINCT ...)`, medians, ratios and
percentiles do not: adding two distinct-counts double-counts anything appearing
in both windows. The reference implementation carries a `supports_incremental`
flag and **raises** rather than silently falling back to a full refresh — a
caller who asked for an incremental refresh has made a cost assumption, and
quietly doing O(fact) work inside it is its own kind of lie.

**Proved by:** `test_incremental_refresh_matches_a_full_refresh`,
`test_non_additive_view_refuses_incremental_refresh`

---

## Defect 4 — the watermark advances to wall-clock time

**Location:** `WatermarkStore.extract`

```python
self._marks[source] = date.today()      # not the max value observed
```

**Fix:**

```python
if new:
    self._marks[source] = max(r["updated_at"] for r in new)
```

**Consequence.** After the first extract the mark is *today* — 2026-09-10 as this
is written — not 2024-01-02. Every subsequent extract filters
`updated_at > 2026-09-10`, so row 3 (dated 2024-01-03) will **never** be
returned. Not late. Never.

There is no error, no gap in a row count, nothing to alert on. The table simply
stops growing, and the first person to notice is whoever compares it against the
source months later.

Two further subtleties worth knowing:

- **Advance only when rows were seen.** An empty extract must leave the mark
  alone. Advancing on an empty result skips whatever was mid-flight.
- **`>` versus `>=`.** Strict `>` means a row written in the same instant as the
  mark is skipped; `>=` means the boundary row is re-read every time. Re-reading
  is the safe direction *provided the load is idempotent* — which is why
  idempotency (Defect 6's neighbourhood) and watermarking are the same design
  decision, not two.

**Proved by:** `test_watermark_advances_to_the_max_observed_not_to_now`,
`test_watermark_extract_returns_only_new_rows`

---

## Defect 5 — a task is marked complete before it has run

**Location:** `PipelineDAG.run`

```python
self._completed.add((run_key, name))     # BEFORE the attempt loop
for _ in range(task.max_attempts):
    ...
```

**Fix:** record completion only after the task actually returns.

```python
for _ in range(task.max_attempts):
    self.attempts[name] += 1
    try:
        results[name] = task.run(ctx)
        self._completed.add((run_key, name))
        last_error = None
        break
    except Exception as exc:
        last_error = exc
if last_error is not None:
    raise last_error
```

**Consequence.** In `[5]` the task eventually succeeded, so the output looks
right — which is why Symptom 5 asks you to imagine the other case rather than
showing it. `[6]` shows the other case: `load_audit` never succeeded, was
marked complete anyway, and run 2 skipped it. The idempotency mechanism, which
exists to make retries safe, has been turned into a mechanism that makes
failures permanent.

**Proved by:** `test_a_failed_task_is_not_marked_complete`

---

## Defect 6 — the terminal error is swallowed

**Location:** `PipelineDAG.run`

```python
except Exception:  # noqa: BLE001, S110
    pass
```

After the last attempt is exhausted, the error is discarded and the loop moves
on to the next task. Three things follow, and each is worse than the last:

1. **`dag.run()` returns normally.** The scheduler sees a successful run. No
   alert, no retry, no page.
2. **`notify` runs.** It depends on `load_audit`, and the orchestrator has no
   record that `load_audit` failed — so a dependency is satisfied by a task that
   did nothing. The analysts get an email about a table that does not exist.
3. **Nothing will ever fix it.** Combined with Defect 5, the task is marked
   complete, so tomorrow's run skips it.

**Fix:** keep the last error and re-raise after the attempts are spent (the code
under Defect 5 does both). Downstream tasks then never start, because `run`
propagates.

**Answering "why would this never page anyone?"** Every alerting rule a team is
likely to have — non-zero exit code, unhandled exception, task-failure count,
run duration — is satisfied. The pipeline is *green*. The only signal that
something is wrong is a table that quietly stopped receiving rows, and nobody
alerts on the absence of a change they were not expecting.

This is the general lesson of the module and worth stating plainly: **in
analytics, silence is not success.** A crash is a good outcome, because someone
fixes it. What you have to design against is the run that finishes cleanly and
publishes a number that is merely plausible.

**Proved by:** `test_retry_gives_up_and_reraises_the_last_error`,
`test_downstream_task_does_not_run_when_upstream_fails`

---

## Scoreboard

| # | Defect | Class | Would monitoring catch it? |
| :-- | :--- | :--- | :--- |
| 1 | `lookup_as_of` ignores the date | silent wrong answer, dormant until backfill | No |
| 2 | `valid_to` off by one day | silent double-count, 1 day per change | No |
| 3 | `dict.update` in the merge | silent undercount, some keys only | No |
| 4 | watermark set to `today()` | silent permanent data loss | No |
| 5 | completion recorded too early | failures become permanent | No |
| 6 | terminal error swallowed | green run, wrong data, downstream proceeds | No |

Six defects, zero of them visible to liveness monitoring. That is the shape of
the problem in analytics engineering, and it is why this module's tests assert
*numeric agreement between two independent implementations* rather than merely
that the code runs.

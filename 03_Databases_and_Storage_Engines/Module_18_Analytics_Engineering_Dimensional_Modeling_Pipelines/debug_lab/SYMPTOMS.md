# Debug Lab 18 — Symptoms

> A nightly warehouse load. It runs to completion, raises nothing, and exits 0.
> The numbers it publishes are wrong.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written down
> a diagnosis for each symptom — the reasoning is the skill, and reading the
> answer first skips it entirely.

```bash
cd debug_lab
python broken_warehouse_pipeline.py
```

There are **six** distinct defects in `broken_warehouse_pipeline.py`. Five of
them are visible in the output below. One is visible only in what the output
*fails* to say.

---

## Symptom 1 — the same sales produce different totals on a re-run

```
[1] Revenue by state, full refresh
      OH:   180.00
      TX:    25.00

[1b] Revenue by state after reprocessing the March partition
      OH:    50.00
      TX:   155.00
```

Section `[1b]` loads the **identical four sales** as `[1]`. Nothing about the
sales changed. The only thing that happened in between is that customer `C1`
relocated from Ohio to Texas in June.

$130 of revenue earned in March and April — while `C1` was demonstrably in Ohio —
is now reported as Texas revenue.

**Why this one is dangerous:** the first load was correct. It stays dormant
until a partition is reprocessed, which is an ordinary weekly operation. So it
ships, passes review, produces correct numbers for months, and then silently
rewrites history the first time someone backfills.

**Questions to answer:**
- Which of the four sales moved, and which stayed put? What do the moved ones
  have in common?
- What is different about the *order* of operations between `[1]` and `[1b]`?
- Which single function is consulted in both cases, and what does it actually
  return?

---

## Symptom 2 — a customer is in two states on the same day

```
[2] dim_customer validity ranges
      sk=1 C1 OH  2024-01-01 -> 2024-06-01
      sk=3 C1 TX  2024-06-01 -> open
      overlapping version pairs: 1
```

Read the two ranges for `C1`. Ask what the warehouse believes about
**2024-06-01** specifically.

**Questions to answer:**
- How many rows does an as-of join for `C1` on 2024-06-01 match?
- What does a `SUM` do when a fact row matches two dimension rows?
- The ranges in this model are inclusive at both ends. Given that, what should
  the closing `valid_to` have been?

---

## Symptom 3 — incremental and full refresh disagree

```
[3] Incremental refresh vs full refresh
      incremental: {'OH': 40.0, 'TX': 25.0}
      full:        {'OH': 220.0, 'TX': 25.0}
      agree: False
```

One new $40 sale arrived for an Ohio customer. Ohio's total before the new sale
was $180.

**Questions to answer:**
- $220 is the right answer. Where did $40 come from instead?
- The delta was computed correctly — verify that for yourself before going
  further. So which step corrupts it?
- Why does `TX` survive unharmed while `OH` does not? What is different about
  the two keys in this particular run?

---

## Symptom 4 — a new source row is never extracted

```
[4] Incremental extraction from the source system
      first  extract: [1, 2]
      second extract: []
```

Row `3` was appended to the source with `updated_at = 2024-01-03` before the
second extract. The second extract returned nothing.

**Questions to answer:**
- What value does the high-water mark hold after the first extract? Print it.
- Compare that value to `2024-01-03`. Now compare it to what the mark *should*
  hold after observing rows dated 2024-01-01 and 2024-01-02.
- This row is not delayed. Under what circumstances would it ever arrive?

---

## Symptom 5 — a retried task is skipped instead of retried

```
[5] Retry behaviour on a transient failure
      run 1 results: {'extract': 'extracted', 'load': 'loaded'}
      attempts:      {'extract': 1, 'load': 3}
      run 2 results: {}
      run 2 skipped: ['extract', 'load']
```

Run 1 is correct — `load` failed twice, succeeded on the third attempt.
Run 2 skipping both tasks is also correct: they genuinely completed.

So this section looks fine. Hold that thought and read Symptom 6, then come
back and ask what run 2 would have done if `load` had **not** eventually
succeeded.

---

## Symptom 6 — a failed load reports success, and the failure is permanent

```
[6] A task whose target table does not exist
      run 1 results: {'notify': 'emailed the analysts'}
      run 1 attempts: {'load_audit': 2, 'notify': 1}
      run 2 results: {}
      run 2 skipped: ['load_audit', 'notify']
```

`load_audit` raised `RuntimeError: relation 'audit_log' does not exist` on both
of its attempts. It never succeeded.

Three things happened anyway:

1. `dag.run()` returned normally. No exception reached the caller, so the
   scheduler recorded a successful run and no alert fired.
2. `notify` — which depends on `load_audit` — ran, and emailed the analysts
   about a table that was never loaded.
3. Run 2 **skipped** `load_audit`. The retry that would have fixed it once the
   table existed will never happen.

**Questions to answer:**
- Find the line that decides a task has completed. What has to be true at that
  point for the decision to be correct? Is it?
- Find the `except` clause. What does it do with the error after the final
  attempt is exhausted?
- Why did `notify` run? Trace what the orchestrator knows about `load_audit`'s
  outcome at the moment it decides to start `notify`.
- Of the six defects in this file, this is the one that would page you at 3am —
  except that it will not page anyone, ever. Why not?

---

## How to verify a fix

The reference implementation in `../project_solution/` and its 59 tests encode
every property broken here. After each fix, the corresponding test should go
from red to green:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_scd2_preserves_history` |
| 2 | `test_scd2_intervals_tile_the_timeline` |
| 3 | `test_incremental_refresh_matches_a_full_refresh` |
| 4 | `test_watermark_advances_to_the_max_observed_not_to_now` |
| 5 | `test_a_failed_task_is_not_marked_complete` |
| 6 | `test_retry_gives_up_and_reraises_the_last_error`, `test_downstream_task_does_not_run_when_upstream_fails` |

```bash
cd ../project_solution
python -m pytest test_dimensional_engine.py -q
```

Fix the file in place. When the printed output matches what you reasoned it
should be, and all six tests above pass against your corrected logic, you are
done.

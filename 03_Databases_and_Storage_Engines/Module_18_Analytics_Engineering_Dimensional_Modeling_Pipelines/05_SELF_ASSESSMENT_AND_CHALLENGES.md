# Module 18 Analytics Engineering: Self-Assessment & Mastery Challenges

Work through Part 1 without looking anything up. Part 4 is the part that matters
most — those are the questions an on-call engineer actually faces.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. A star schema deliberately denormalises dimensions, which Module 01 taught you
   to avoid. State the workload characteristic that makes the trade-off correct
   here, and name one workload where it would be wrong.

2. `customer_id` uniquely identifies a customer in the source system. Give the
   specific reason it cannot serve as the primary key of an SCD Type 2 dimension.

3. A dimension uses closed intervals (`valid_from` and `valid_to` both
   inclusive). A customer changes state effective 2024-06-01. What exactly must
   `valid_to` on the outgoing row be set to, and what happens to fact rows dated
   2024-06-01 if you set it to 2024-06-01?

4. Why is the open-ended `valid_to` stored as `9999-12-31` rather than `NULL`?
   Answer in terms of the query you would otherwise have to write.

5. Your `dim_customer` is Type 2 and tracks `state`. The source system sends a
   corrected phone number. How many rows should the dimension have afterwards,
   and why?

6. A nightly full extract re-sends all 2 million customer rows every night. Your
   Type 2 dimension grows by 2 million rows per night. What is the defect?

7. `mv_daily_revenue` aggregates `SUM(revenue)`. `mv_daily_active_users`
   aggregates `COUNT(DISTINCT user_id)`. One can be incrementally refreshed and
   one cannot. Which, and what specifically goes wrong with the other?

8. An extract runs `WHERE updated_at > watermark` and then sets the watermark to
   `now()`. Describe the class of rows that will never be extracted, and explain
   why no row count or error will reveal it.

9. A pipeline task fails on all three attempts. The orchestrator records it as
   complete and `run()` returns normally. Name the two separate defects, and say
   which one makes the failure *permanent*.

10. Your nightly pipeline is green for six months. What single piece of evidence
    would actually justify trusting the numbers it publishes, that "the run
    succeeded" does not provide?

---

## Part 2: Answer Key & Detailed Explanations

**1.** Analytics is read-dominated with batched, append-only writes, so the cost
3NF avoids (update anomalies across redundant copies) barely arises, while the
cost it imposes (deep multi-table joins on every read) is paid on every query
over billions of rows. It would be wrong for an OLTP system where a single
customer attribute is updated thousands of times a second and must be
transactionally consistent — there, redundancy is a correctness hazard.

**2.** Because a Type 2 dimension stores *several rows per natural key* — one per
historical version. Once `C1` has three versions, `customer_id = 'C1'` matches
three rows, so it is not unique and cannot be a primary key. You need a surrogate
key that identifies *a version*, not an entity.

**3.** `valid_to` must be `2024-05-31` — the day before. If you set it to
`2024-06-01`, both the outgoing and incoming rows satisfy
`'2024-06-01' BETWEEN valid_from AND valid_to`, so an as-of join matches two
dimension rows and every fact row dated 2024-06-01 is **double-counted** in any
`SUM`. One day per change, per key, compounding silently.

**4.** So that `valid_to` stays `NOT NULL` and a range predicate is a plain
`WHEN BETWEEN valid_from AND valid_to`. With `NULL` you need
`(? >= valid_from AND (valid_to IS NULL OR ? <= valid_to))` at every call site,
and the first time someone forgets the `IS NULL` branch the current version stops
matching entirely.

**5.** One row. `phone` is not a tracked attribute, so it is corrected in place —
Type 1 behaviour inside a Type 2 dimension. Versioning on it would create history
that answers no question anyone will ask, while making every as-of join scan more
rows.

**6.** The dimension is versioning on rows that did not change. A Type 2 upsert
must compare tracked attributes against the current version and be a **no-op**
when nothing differs. Without that check a full extract produces 365 identical
versions per key per year, and the as-of lookup gets progressively slower for no
information gained.

**7.** `SUM` can be merged from deltas because addition is associative;
`COUNT(DISTINCT user_id)` cannot, because a user active in both the existing
window and the delta window is counted once in each and twice in the sum. The
merged number is wrong and plausible — which is worse than an error, so the
implementation should refuse rather than approximate.

**8.** Any row whose `updated_at` is earlier than wall-clock time but which had
not yet been committed when the extract ran — including every row that arrives
with a backdated timestamp. Because the mark has jumped far into the future
relative to the data, those rows fail `updated_at > watermark` **forever**. There
is no error and no gap in a count of *extracted* rows; the only symptom is a
table that stopped growing, and nobody alerts on the absence of a change they
were not expecting.

**9.** (a) The task is recorded as complete despite never succeeding. (b) The
terminal exception is swallowed instead of re-raised. (b) makes the run look
green and lets downstream tasks proceed; **(a) is what makes it permanent**,
because tomorrow's run sees the task as done and skips the retry.

**10.** Agreement between two independent computations of the same number — for
example, the reconciliation test in this module comparing the hand-built model
against DuckDB, or in production a daily control-total check comparing warehouse
`SUM(revenue)` against the source system's own ledger. "The run succeeded" is a
statement about the pipeline's liveness; it contains no information about whether
the numbers are right.

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation

Implement all of `starter/dimensional_engine.py` until the 39 shipped Track A
tests pass. Then, without modifying the tests, add:

1. **SCD Type 3** (`previous_state` column alongside `state`) as a third
   strategy. Write two tests: one showing what it answers that Type 1 cannot, and
   one showing the question it *cannot* answer that Type 2 can.
2. **A late-arriving-fact path.** Currently a fact dated before a dimension's
   first version resolves to `None`. Implement an explicit
   `UNKNOWN_MEMBER` surrogate key (conventionally `-1`) so those rows are
   *countable* rather than dropped, and write the test that proves revenue is
   conserved.

### 🚀 Challenge 2: Architect Stretch Problem

**A.** `fact_sales` has 4 billion rows. `mv_revenue_by_state` must be no more
than 15 minutes stale, and a full refresh takes 50 minutes. Design the refresh
strategy. Your answer must address: what the watermark is keyed on, what happens
to a row whose `event_date` is in the past but which arrives now, and how you
detect that the incremental chain has drifted from the true total. State the
control-total query you would run and how often.

**B.** A dimension change arrives **retroactively**: on 2024-09-01 you learn that
`C1` actually moved to Texas on 2024-06-01, and three months of facts were loaded
against the Ohio version. Write the correction procedure. Your answer must
address: which fact rows must be re-keyed, whether you mutate the existing
dimension rows or insert a correcting version, what any already-published report
for July should say after the correction, and how you would make the correction
itself auditable.

There is no single right answer to either. There are wrong answers, and both
hinge on the same question: *what did we tell people, and are we allowed to
change it?*

---

## Verification Criteria

- [ ] 59 tests pass from `project_solution/`.
- [ ] `test_model_and_duckdb_agree_on_revenue_by_state` passes.
- [ ] An untouched `starter/` fails all 39 Track A tests.
- [ ] Challenge 1's Type 3 tests state, in the test name, which question the
      strategy cannot answer.
- [ ] Challenge 1's unknown-member test asserts **conservation** — total revenue
      before equals total revenue after, with nothing silently dropped.
- [ ] Your Challenge 2A answer names a control total and a cadence.
- [ ] Your Challenge 2B answer takes a position on restating published reports.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

### D1. Last Year's Revenue Changed Overnight, With No Deploy

A finance analyst reports that Q1 revenue by state changed between Friday and
Monday. No code was deployed. No Q1 source data changed. The pipeline was green
all weekend.

The only thing that ran was a routine reprocess of the Q1 partition after an
upstream vendor re-sent a corrected file.

```sql
-- the aggregation, unchanged for a year
SELECT c.state, SUM(f.revenue)
FROM fact_sales f
JOIN dim_customer c ON f.customer_sk = c.customer_sk
WHERE f.event_date BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY c.state;
```

**Q:** The SQL is correct. Where is the defect, and why did it stay hidden for a
year?

**A:** The defect is in the *load*, not the query — specifically in how
`customer_sk` was resolved when the facts were written. The loader resolved the
customer's **current** dimension version rather than the version in effect on
`event_date`. On the original load the two coincided, because the facts were
written before any of those customers changed. On the reprocess they no longer
coincide: every customer who has changed state since Q1 now writes the new
version's key, and their Q1 revenue moves with them.

It stayed hidden for a year because the bug is **dormant until a backfill**. The
first load of any partition is always correct. Only a reprocess — an ordinary
weekly operation — exposes it.

Fix: resolve `customer_sk` with an as-of lookup against `event_date`. Then verify
by reprocessing a partition twice and asserting byte-identical output; that
assertion is the regression test.

### D2. A Dashboard Total Is 0.3% Low, But Only On Some Days

```python
def refresh_incremental(self, watermark):
    delta = self._compute(rows_after(watermark))
    self._data.update(delta)          # merge the delta in
    return self._data
```

Totals are correct for most states. For a handful they are low, and the affected
set changes day to day.

**Q:** Explain the pattern — why *some* keys and not others?

**A:** `dict.update` **replaces** the value for every key present in `delta`
rather than adding to it. So any key appearing in the delta window loses its
accumulated history and is left holding only the delta; any key *absent* from the
delta window is untouched and stays correct.

That is exactly the observed pattern: the affected set is "whichever states had
sales in the last window," which changes daily. A spot check on a quiet state
passes.

Fix: `self._data[k] = self._data.get(k, 0.0) + v`. And add the invariant test —
incremental refresh must equal a full refresh — because that is the assertion
that would have caught it on day one.

### D3. A Table Silently Stopped Growing In March

`fact_orders` received rows daily until 2024-03-14 and nothing since. The
pipeline has run green every night for five months. No errors, no failed tasks,
no alerts.

```python
def extract(self, source, rows):
    mark = self.get(source)
    new = [r for r in rows if mark is None or r["updated_at"] > mark]
    self._marks[source] = date.today()
    return new
```

**Q:** What happened on 2024-03-14, and why did five months of monitoring miss
it?

**A:** The watermark was set to `date.today()` instead of the maximum
`updated_at` actually observed. Once the mark jumped ahead of the data's own
timestamps, `updated_at > mark` stopped matching anything, permanently.
2024-03-14 was simply the last day the source happened to produce a row with a
timestamp beyond the already-inflated mark.

Monitoring missed it because every signal was healthy: the task ran, returned
zero rows, and exited 0. "Extracted 0 rows" is indistinguishable from a quiet
night. Nobody alerts on the absence of an expected change.

Fix: `if new: self._marks[source] = max(r["updated_at"] for r in new)` — advance
to the max *observed*, and not at all when nothing was seen. Then add a freshness
alert: `MAX(updated_at)` in the target must be within N hours of now. That alert,
not the pipeline's exit code, is what detects this class of failure.

### D4. A Fixed Pipeline Never Recovers

An engineer creates the missing `audit_log` table at 09:00 and waits for the
night's run to backfill it. The run is green. The table is still empty.

```python
task = self._tasks[name]
self._completed.add((run_key, name))
for _ in range(task.max_attempts):
    try:
        results[name] = task.run(ctx)
        break
    except Exception:
        pass
```

**Q:** Two defects. Name both, and say which one the engineer's fix was defeated
by.

**A:** (1) Completion is recorded **before** the task runs, so a task that never
succeeds is nonetheless marked done for that `run_key`. (2) The terminal
exception is swallowed, so `run()` returns normally and downstream tasks proceed
against data that was never loaded.

The engineer was defeated by (1): the task had already been marked complete for
that run key, so the retry was *skipped*, not attempted. Creating the table
changed nothing, because the pipeline never tried again.

Fix: record completion only inside the `try`, after `task.run` returns; keep the
last exception and re-raise it once attempts are exhausted. Then assert both
properties — a failed task is not marked complete, and a downstream task does not
run after an upstream failure.

### D5. Revenue Double-Counts On Exactly One Day Per Customer Move

Monthly revenue is 0.1–0.4% high. Drilling in, the excess always lands on the
date a customer changed a tracked attribute.

```sql
SELECT COUNT(*) FROM dim_customer
WHERE customer_id = 'C1' AND DATE '2024-06-01' BETWEEN valid_from AND valid_to;
-- 2
```

**Q:** What is the off-by-one, and what should the tiling assertion be?

**A:** The outgoing version's `valid_to` was set to the change date rather than
the day before it. With closed intervals both versions cover 2024-06-01, so the
as-of join fans out to two dimension rows and every fact row on that date is
summed twice.

Fix: `valid_to = effective - INTERVAL 1 DAY`. The assertion that catches it:

```sql
SELECT COUNT(*) FROM (
    SELECT valid_to,
           LEAD(valid_from) OVER (PARTITION BY customer_id ORDER BY valid_from) AS next_from
    FROM dim_customer
) t
WHERE next_from IS NOT NULL AND next_from <> valid_to + INTERVAL 1 DAY;
-- must be 0
```

That query asserts no gaps *and* no overlaps in one pass, and belongs in the
nightly data-quality suite rather than in a code review.

---

### Scoring

| Score | Interpretation |
| :--- | :--- |
| **9–10 quiz + all 5 diagnostics** | Tier 3. Attempt both stretch problems; you are ready to own a warehouse. |
| **7–8 quiz + 3–4 diagnostics** | Tier 2 complete. Re-read §2 and §3 of the README, then work the debug lab. |
| **5–6 quiz + 1–2 diagnostics** | Tier 1 solid. Implement `MaterializedView` and `PipelineDAG` before moving on. |
| **Below 5** | Re-read the README's §2 (SCD) and re-run `03_scd2_and_pipeline_demo.py`, reading each printed number against the code that produced it. |

The diagnostics are weighted more heavily than the quiz on purpose. Every one of
them is a real defect that produces a green pipeline and a wrong number, and
recognising that pattern is the actual skill this module teaches.

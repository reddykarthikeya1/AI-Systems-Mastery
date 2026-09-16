# Module 18: Analytics Engineering — Dimensional Modelling, Materialised Aggregates & Pipelines

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

> **Prerequisite:** [Module 17 — Columnar OLAP, DuckDB & ClickHouse](../Module_17_Columnar_OLAP_DuckDB_ClickHouse/01_README.md).
> Module 17 taught you how an analytical *engine* stores and scans data. This
> module is about what you put in it, and how the data gets there every night.

---

## 🧭 Why This Module Exists

Modules 01–17 build engines. This one builds the thing engines are *for*.

A columnar engine will happily scan a badly-modelled table at 10 GB/s and
return a wrong answer very quickly. The defects in this module do not look like
crashes — they look like a revenue figure that is 4% off, or a dashboard that
silently stopped updating in March. Every one of them is a **silent wrong
answer**, and that is a different discipline from the one the previous modules
taught.

The central problem, stated once:

> A fact row must join to the dimension version that was current **when the
> event happened**, not to the version that is current now.

Get it wrong and every historical report restates itself whenever a dimension
changes. A customer who moves from Ohio to Texas retroactively takes last
year's revenue with them — and the numbers stay *plausible*, so nobody notices
until someone reconciles a quarterly report by hand.

---

## 📊 1. Why Dimensional Modelling, and Not Just Normalising

Modules 01 and 02 taught third normal form: eliminate redundancy, one fact in
one place. That is the right shape for an OLTP system where writes dominate and
every write must be atomic and consistent.

Analytics inverts the workload. Writes are batched and append-only; reads are
enormous aggregations across billions of rows. Under that workload, 3NF's virtue
becomes its cost:

| | 3NF (OLTP) | Star schema (OLAP) |
| :--- | :--- | :--- |
| Optimised for | write integrity | read throughput |
| Tables in a typical query | 8–15 | 2–4 |
| Redundancy | eliminated | deliberate, in dimensions |
| Join depth | deep, chained | one hop, fact → dimension |
| Grain | implicit | **declared and enforced** |

A star schema is a deliberate denormalisation with a specific shape:

```
              dim_date            dim_customer
                  │                     │
                  └────────┐   ┌────────┘
                           ▼   ▼
                      ┌──────────────┐
        dim_product ─▶│  fact_sales  │◀─ dim_store
                      └──────────────┘
                         narrow rows:
                         only keys, a date, and measures
```

The fact table stays **narrow** — surrogate keys, an event date, and numeric
measures, nothing else. Dimensions stay **wide** — every attribute you might
group by, denormalised flat. On columnar storage this is the whole economic
argument: a `SUM(revenue) GROUP BY state` touches the revenue column and one
narrow key column, and reads nothing else off disk.

### Grain, and why it is enforced in code here

A fact table's **grain** is the precise meaning of one row: *one row per order
line per shipment*. It sounds like documentation. It is the most important
declaration in the schema, because an undeclared grain is how a table ends up
holding a mixture of per-order and per-line rows — at which point every `SUM`
is wrong, no query errors, and there is nothing to find.

`FactTable` in this module rejects any row that does not carry exactly the
declared grain keys. That is not how a real warehouse enforces it (you would use
a composite key or a `dbt` uniqueness test), but building the check by hand once
makes the concept concrete.

---

## 🕰️ 2. Slowly Changing Dimensions

Source systems overwrite. `UPDATE customers SET state = 'TX' WHERE id = 1`
destroys the fact that the customer was ever in Ohio. A warehouse's job is to
remember.

### Type 1 — overwrite

Correct the row, keep no history.

```
customer_sk | customer_id | state
     1      |     C1      |  TX      ← was OH, now just TX
```

Right choice for **corrections**: a misspelled name was never true, so there is
no history worth keeping. Wrong choice for anything you will report on over
time.

### Type 2 — versioned rows

Close the old row, open a new one.

```
customer_sk | customer_id | state | valid_from | valid_to   | is_current
     1      |     C1      |  OH   | 2024-01-01 | 2024-05-31 |   false
     3      |     C1      |  TX   | 2024-06-01 | 9999-12-31 |   true
```

Three details that all cause production bugs when missed:

1. **The surrogate key.** `customer_id` is no longer unique once history
   accumulates, so it cannot be the primary key. You need a key that is yours,
   narrow, and never moves — see `SurrogateKeyAllocator`.
2. **`9999-12-31`, not `NULL`.** Keeping `valid_to` NOT NULL means a range
   predicate is a plain `BETWEEN` with no special case for the open interval.
3. **The interval convention.** These ranges are closed at both ends, so the
   closing `valid_to` is `effective - 1 day`. Setting it to `effective` makes
   both versions match on the change date, and every fact row on that date is
   counted twice. Pick a convention, write it next to the schema, and assert it
   with a tiling test.

### Tracked vs untracked attributes

A daily full extract re-sends every row every day. A Type 2 dimension that
versions on *any* difference produces 365 identical versions per key per year.
Declare which attributes are worth history (`state`) and which are corrections
applied in place (`phone`).

---

## 🔁 3. Materialised Aggregates and Incremental Refresh

A "materialised view" is a cache with a refresh policy. The caching is easy; the
policy is what goes wrong.

**Full refresh** is always correct and always O(fact). Fine at 10 million rows,
untenable at 10 billion.

**Incremental refresh** computes only rows past a watermark and merges the delta.
Cheap, and valid **only for additive measures**:

| Measure | Merges from deltas? | Why |
| :--- | :--- | :--- |
| `SUM` | ✅ | addition is associative |
| `COUNT` | ✅ | same |
| `MIN` / `MAX` | ✅ | idempotent under re-application |
| `AVG` | ⚠️ only as `SUM`/`COUNT` pair | the ratio itself does not merge |
| `COUNT(DISTINCT)` | ❌ | double-counts anything in both windows |
| median, percentile | ❌ | needs the full distribution |

Applying the additive merge to a distinct count returns a number that is wrong
and plausible. `MaterializedView` therefore carries a `supports_incremental`
flag and **raises** rather than silently doing a full refresh instead — a caller
who asked for incremental made a cost assumption, and hiding an O(fact)
recompute inside it is its own kind of lie.

---

## 🔀 4. Pipeline Orchestration

The nightly load is a DAG. Three properties, each a production incident when
missing:

**Topological order.** A task never runs before its inputs exist. Kahn's
algorithm, with the ready-queue seeded in sorted order so runs are deterministic
and logs are diffable.

**Cycle detection.** Reported as an error at ordering time, not discovered as a
hang at 3am.

**Idempotency.** A task that already succeeded for a given run key is skipped on
re-run. Without it a retried pipeline double-loads the fact table — and doubled
revenue is plausible enough to survive review for a quarter.

The corollary, which is the harder half: a task that **failed** must *not* be
marked complete, and its terminal error must propagate. A DAG that swallows the
last exception returns normally, the scheduler records success, downstream tasks
run against data that was never loaded, and tomorrow's run skips the retry that
would have fixed it. `debug_lab/` contains exactly this bug, and it is the one
that would page you at 3am except that it never pages anyone.

### Watermarks

Incremental extraction is `WHERE updated_at > watermark`. The subtlety: the mark
must advance to the maximum value **observed**, never to `now()`. Advancing to
wall-clock time skips every row written during the extract — permanently,
silently, with no gap in any row count to alert on.

### Backfills

A single-transaction backfill over two years holds locks for hours, blows out the
WAL, and cannot be resumed after a failure. Chunking is not an optimisation here;
it is the only version that finishes.

---

## 🧪 5. Two Tracks, and a Reconciliation Test

This module follows the course's two-track structure:

| Track | File | What it teaches |
| :--- | :--- | :--- |
| **A — Internals** | `project_solution/dimensional_engine.py` | build the mechanisms by hand, in memory |
| **B — Operation** | `project_solution/warehouse_live.py` | drive a real engine: DDL, SCD2 merge, `EXPLAIN`, refresh |

Track A is an **in-process model**, not a warehouse. It says so in its own
docstring. Everything is Python dicts and lists so each mechanism can be read,
stepped through and modified.

Track B runs against **real DuckDB** — real DDL, a real two-statement SCD2 merge
inside a transaction, a real materialised aggregate, and real `EXPLAIN` output
showing the join order the optimiser actually chose. DuckDB is embedded, so
unlike the server-backed modules in this course these tests need no Docker and
**never skip**. That is deliberate: the reconciliation test is the most
important one in the module and should not be the one that quietly stops running
on a bare machine.

**The reconciliation test** runs one logical aggregation through both — the same
three sales, the same SCD2 move — and asserts the two agree:

```python
assert star.aggregate([("customer_sk", "state")], "revenue") == wh.revenue_by_state()
```

Where the model and DuckDB disagree, the model is wrong, and the test says so.
That is what separates a hand-built model from a toy.

---

## 🛠️ 6. Hands-On Lab

You will implement:

1. **`SurrogateKeyAllocator`** — monotonic keys, one sequence per dimension.
2. **`DimensionTable`** — SCD Type 1 and Type 2, tracked vs untracked
   attributes, and `lookup_as_of`, the as-of join that preserves history.
3. **`FactTable`** — grain enforcement that rejects mixed-grain rows.
4. **`StarSchema`** — the star join as an aggregation over dimensions and fact.
5. **`MaterializedView`** — full refresh, watermark-incremental refresh,
   staleness detection, and the non-additive guard.
6. **`PipelineDAG`** — Kahn ordering, cycle detection, run-key idempotency,
   bounded retries, and correct failure propagation.
7. **`WatermarkStore`** and **`Backfill`** — monotonic marks and bounded batches.

Then run the same logic against real DuckDB and reconcile the two.

```bash
# Track A + B (no Docker needed - DuckDB is embedded)
cd project_solution
python -m pytest -q                      # 59 tests

# Grade your own work
cd starter
python -m pytest ../project_solution/test_dimensional_engine.py -q
```

Every test must fail with `NotImplementedError` on an untouched starter. If any
test passes before you have written anything, **stop** — the grading loop is
broken and is telling you your work is correct when it has not been done.

---

## 🚨 7. The Failure Modes This Module Is Really About

| Symptom in production | Cause | Caught by liveness monitoring? |
| :--- | :--- | :--- |
| Last year's revenue changed overnight | as-of join used the *current* dimension version | No |
| One day per dimension change is double-counted | `valid_to` off by one under closed intervals | No |
| A dashboard total is too low, but only for some keys | delta merge replaced instead of accumulating | No |
| A table silently stopped growing | watermark advanced to `now()` instead of max observed | No |
| A fixed pipeline never re-runs | task marked complete before it succeeded | No |
| Analysts emailed about a table that was never loaded | terminal exception swallowed, downstream ran anyway | No |

Six failure modes, none visible to "did the pipeline run?" monitoring. **In
analytics, silence is not success.** A crash gets fixed on Tuesday; a clean run
that publishes a plausible wrong number gets fixed next quarter, by accident.

Work `debug_lab/` and you will meet all six.

---

## 📂 Project Structure

```
Module_18_Analytics_Engineering_Dimensional_Modeling_Pipelines/
├── README.md
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── 00_interactive_dimensional_modeling.ipynb
├── 01_scd2_and_pipeline_demo.py
├── starter/
│   ├── conftest.py
│   └── dimensional_engine.py
├── project_solution/
│   ├── dimensional_engine.py          # Track A: internals
│   ├── warehouse_live.py              # Track B: real DuckDB
│   ├── test_dimensional_engine.py     # 39 tests
│   └── test_warehouse_live.py         # 20 tests, incl. reconciliation
└── debug_lab/
    ├── broken_warehouse_pipeline.py   # 6 planted defects, exit code 0
    ├── SYMPTOMS.md
    └── ANSWERS.md
```

---

## 🧭 Curriculum Graph Navigation

### ⬅️ Prerequisites

- [Module 17 — Columnar OLAP, DuckDB & ClickHouse](../Module_17_Columnar_OLAP_DuckDB_ClickHouse/01_README.md) — the engine this modelling sits on
- [Module 02 — Modern SQL Mastery](../Module_02_Modern_SQL_Mastery_Advanced_Queries/01_README.md) — window functions, used here for the tiling check
- [Module 01 — Storage Theory, ACID & the Relational Model](../Module_01_Storage_Theory_ACID_Relational_Model/01_README.md) — normal forms, which this module deliberately departs from

### ➡️ Next Steps

- [Module 19 — Search Engines: Elasticsearch & Lucene](../Module_19_Search_Engines_Elasticsearch_Lucene/01_README.md)
- [Module 22 — Query Optimization, CBO & Index Tuning](../Module_22_Query_Optimization_CBO_Index_Tuning/01_README.md) — why the star join gets the plan it gets
- [Module 24 — Production DBRE: Backups, Migrations & HA](../Module_24_Production_DBRE_Backups_Migrations_HA/01_README.md) — running the backfills this module designs

### 🏁 Phase Benchmark

- [Phase 6 Checkpoint](../Phase_Checkpoints/PHASE_06_CHECKPOINT.md) — covers Modules 17–19

# Module 18 Analytics Engineering: Project Guide

## 📌 Project Overview: A Nightly Warehouse Load That Cannot Lie About History

You are building the load pipeline and dimensional model behind a revenue
dashboard. The requirement that shapes every decision:

> Re-running any partition, at any time, must produce byte-identical numbers to
> the original run.

That single property rules out the naive implementation of almost every component
here. It is also the property that separates a warehouse from a pile of tables.

You will build it twice — once by hand in memory, once in real DuckDB — and a
reconciliation test will assert the two agree.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Audience | Scope | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Foundational** | First exposure to dimensional modelling | `SurrogateKeyAllocator`, `DimensionVersion.covers`, `DimensionTable` (Type 1 and Type 2), `lookup_as_of`, `FactTable.insert` | 3–4 h |
| **Tier 2 — Practitioner** | Comfortable with SQL and ETL | Everything in Tier 1 plus `StarSchema.aggregate`, `MaterializedView` (both refresh paths), `PipelineDAG`, `WatermarkStore`, `Backfill`, and all of Track B | 6–8 h |
| **Tier 3 — Architect** | Building real warehouses | Both stretch problems below, plus the full `debug_lab` with a written diagnosis per defect before opening `ANSWERS.md` | 10–14 h |

Tier 1 is a complete, coherent stopping point: you will have a working SCD2
dimension and a fact table that refuses mixed grain, which is the majority of the
value in this module.

---

## 1. Architectural Blueprint & Data Flow

```
   SOURCE SYSTEM (OLTP)                     WAREHOUSE
   ─────────────────────                    ─────────

   customers  orders                    ┌──────────────────┐
       │         │                      │   dim_customer   │
       │         │      ┌──────────────▶│  (SCD2 versions) │
       ▼         ▼      │               └────────┬─────────┘
   ┌─────────────────┐  │                        │ surrogate key
   │  WatermarkStore │  │                        │ resolved AS OF
   │  updated_at >   │──┘                        │ the event date
   │  last observed  │                           ▼
   └────────┬────────┘                  ┌──────────────────┐
            │                           │    fact_sales    │
            └──────────────────────────▶│ keys + date +    │
                                        │ measures only    │
                                        └────────┬─────────┘
                                                 │
   ┌──────────────────┐                          ▼
   │   PipelineDAG    │                 ┌──────────────────┐
   │  extract         │                 │ mv_revenue_by_   │
   │    └▶ load_dim   │                 │      state       │
   │         └▶ load_fact ──────────────▶│ full | incremental│
   │              └▶ refresh_view │      └──────────────────┘
   └──────────────────┘
     idempotent per run_key
```

**The critical path, in one sentence:** a source row's `updated_at` decides
whether it is extracted; its **event date** decides which dimension version it
joins to. Confusing those two is Defect 1 in the debug lab.

---

## 2. Directory Structure & Key Files

```
Module_18_Analytics_Engineering_Dimensional_Modeling_Pipelines/
├── README.md                            ← concepts, read first
├── PROJECT_GUIDE.md                     ← this file
├── SELF_ASSESSMENT_AND_CHALLENGES.md    ← quiz + diagnostics
├── TROUBLESHOOTING_AND_EDGE_CASES.md    ← when it goes wrong
├── 00_interactive_dimensional_modeling.ipynb
├── 01_scd2_and_pipeline_demo.py         ← runnable, measured
├── starter/
│   ├── conftest.py                      ← redirects imports to YOUR code
│   └── dimensional_engine.py            ← stubs; start here
├── project_solution/
│   ├── dimensional_engine.py            ← Track A reference
│   ├── warehouse_live.py                ← Track B, real DuckDB
│   ├── test_dimensional_engine.py       ← 39 tests
│   └── test_warehouse_live.py           ← 20 tests
└── debug_lab/
    ├── broken_warehouse_pipeline.py     ← 6 defects, exit 0
    ├── SYMPTOMS.md                      ← observable wrongness
    └── ANSWERS.md                       ← do not open early
```

---

## 3. Step-by-Step Implementation Roadmap

### Phase 1: Environment & Setup

DuckDB is embedded — there is nothing to start, and no Docker involved.

```bash
python -c "import duckdb; print(duckdb.__version__)"

cd project_solution
python -m pytest -q                 # 59 passed - the reference works

cd ../starter
python -m pytest ../project_solution/test_dimensional_engine.py -q
```

The last command must report **39 failed**. If anything passes, the grading loop
is broken — see `06_TROUBLESHOOTING_AND_EDGE_CASES.md`, entry 1.

### Phase 2: Building Core Capabilities (Tier 1 & 2)

Work in `starter/dimensional_engine.py`, in this order. Each step turns a
specific group of tests green.

1. **`SurrogateKeyAllocator.next_key`** → `test_surrogate_keys_are_monotonic_and_per_table`
2. **`DimensionVersion.covers`** — inclusive at both ends. Everything downstream
   depends on this being right.
3. **`DimensionTable.__init__`, `rows`, `current`, `version_count`** → the
   construction and read tests.
4. **`DimensionTable.upsert`** — the longest step. Handle the cases in this
   order: unseen key → no tracked change → Type 1 → out-of-order → new version.
5. **`DimensionTable.lookup_as_of`** → `test_scd2_preserves_history`.
   **The trap:** implementing this as `return self.current(...)` leaves most
   tests green and fails only that one. That test is the module.
6. **`FactTable.insert`** — three distinguishable rejections: missing grain keys,
   keys outside the grain, unknown measures.
7. **`StarSchema.add_dimension` / `aggregate`** → the star-join tests.
8. **`MaterializedView`** — `refresh` first, then `is_stale`, then
   `refresh_incremental`. Remember: no new rows means clear staleness *without*
   recomputing and without incrementing `refresh_count`.
9. **`PipelineDAG.topological_order`** — Kahn, sorted seeding, cycle detection.
10. **`PipelineDAG.run`** — skip-if-done, retry, and re-raise. A failed task must
    not be recorded as complete.
11. **`WatermarkStore`**, **`Backfill`** — small, and a satisfying finish.

Then read `project_solution/warehouse_live.py` and run its tests. You are not
asked to write Track B from scratch; you are asked to read the SQL and be able
to explain why the SCD2 merge is two statements in one transaction.

### Phase 3: Architect Stretch (Tier 3)

See the two stretch problems in
[`05_SELF_ASSESSMENT_AND_CHALLENGES.md`](05_SELF_ASSESSMENT_AND_CHALLENGES.md).

---

## 4. Verification & Self-Check Checklist

```bash
# Track A + B
cd project_solution && python -m pytest -q                   # 59 passed

# Grading loop (must FAIL on an untouched starter)
cd starter && python -m pytest ../project_solution/test_dimensional_engine.py -q

# The runnable demo, with real measurements
python 01_scd2_and_pipeline_demo.py

# The debug lab: runs clean, publishes wrong numbers
cd debug_lab && python broken_warehouse_pipeline.py; echo "exit=$?"
```

- [ ] All 59 tests pass from `project_solution/`.
- [ ] `test_model_and_duckdb_agree_on_revenue_by_state` passes — the model and
      the real engine agree.
- [ ] Your `lookup_as_of` returns a *different* key before and after a dimension
      change, for the same natural key.
- [ ] Re-running the same `run_key` loads nothing a second time.
- [ ] A task that always fails raises out of `run()` and is **not** marked
      complete.
- [ ] You can state, without looking, which measures may be merged from a delta
      and which may not.
- [ ] You have written a diagnosis for all six debug-lab defects before opening
      `ANSWERS.md`.

---

## 5. You Have Mastered This Module When You Can…

1. **Explain why a fact table stays narrow and a dimension goes wide**, in terms
   of what a columnar scan actually reads off disk.
2. **Choose SCD Type 1 or Type 2 for a given attribute** and defend it — and
   name an attribute in the *same* dimension that deserves the other treatment.
3. **Write the as-of join in SQL from memory**, and explain why the
   `9999-12-31` sentinel is what makes it a plain `BETWEEN`.
4. **State your interval convention** (closed or half-open) and produce the
   window-function query that proves a dimension's versions tile the timeline
   with no gap and no overlap.
5. **Decide whether a given measure can be incrementally refreshed**, and say
   what a distinct count does when you merge it additively.
6. **Explain why a watermark must advance to the maximum observed value**, and
   describe exactly what is lost when it advances to `now()`.
7. **Describe the two halves of pipeline idempotency** — skipping completed work,
   and *not* recording failed work as complete — and what breaks when you
   implement only the first.
8. **Look at a green pipeline run and say what evidence would still be missing**
   before you would trust the numbers it published.
9. **Justify a backfill's batch size** in terms of lock duration, WAL growth and
   resumability, rather than as a round number.
10. **Diagnose all six defects in `debug_lab/` from the output alone**, and say
    for each one why standard liveness monitoring would never catch it.

# Module 18: Troubleshooting & Edge Cases

Every entry below was hit while building or verifying this module, or is a
documented failure mode of the tools it uses. Symptoms first, because that is
what you have when it happens.

---

## 1. The starter tests pass before you have written anything

**Symptom**

```
cd starter
python -m pytest ../project_solution/test_dimensional_engine.py -q
39 passed
```

**This is the worst possible failure in a course.** It certifies non-work: you
fill in nothing, see green, and conclude you are finished.

**Cause.** pytest loads `conftest.py` files along the **test file's** path, not
the working directory's. The test lives in `project_solution/`, so
`starter/conftest.py` is only consulted because `starter/` is an ancestor of
nothing — it is picked up via `rootdir` collection, and if the solution directory
lands earlier on `sys.path` it wins. pytest's default `prepend` import mode puts
the test file's own directory at `sys.path[0]`, which is exactly the directory
you are trying to shadow.

**Check what actually got imported:**

```bash
cd starter
python -c "import dimensional_engine as m; print(m.__file__)"
```

That must print a path under `starter/`. If it prints `project_solution/`, the
redirect is not in effect.

**Fix.** Confirm `starter/conftest.py` exists and contains the `sys.path.insert`
for its own directory. Then clear stale bytecode, which is the usual real cause:

```bash
find .. -name "__pycache__" -type d -exec rm -rf {} +
```

**Expected correct output:** `39 failed`, every failure a `NotImplementedError`.

---

## 2. `duckdb.duckdb.CatalogException: Table with name mv_revenue_by_state already exists`

**Symptom.** `test_incremental_refresh_matches_a_full_refresh` fails on the
second consecutive run but passes on the first.

**Cause.** A test created the aggregate table without dropping it first. Every
test in this course must be idempotent, because they write to real databases —
a suite that only passes on a virgin database is a suite that will fail in CI on
the second commit of the day.

**Fix.** `create_materialized_aggregate` issues `DROP TABLE IF EXISTS` before
`CREATE TABLE AS`. If you add a new table, do the same, and verify by running
the suite twice back to back:

```bash
python -m pytest -q && python -m pytest -q
```

Both runs must report identical counts.

---

## 3. `duckdb.duckdb.TransactionException: cannot start a transaction within a transaction`

**Symptom.** `load_scd2_change` raises on the second call.

**Cause.** A previous `BEGIN TRANSACTION` was never committed or rolled back —
usually because an exception escaped between the `UPDATE` and the `INSERT`
without hitting the `ROLLBACK`.

**Fix.** The merge wraps both statements in `try`/`except` with an explicit
`ROLLBACK` before re-raising. Never write a bare `BEGIN` without that. If you are
debugging interactively and hit this, `conn.execute("ROLLBACK")` clears it.

**Why this matters beyond the error message.** If the `UPDATE` commits alone the
customer has *no* current row; if the `INSERT` commits alone the customer has
*two*, and every join against the dimension double-counts them. The transaction
is not tidiness — it is the difference between correct numbers and plausible
ones. `test_scd2_merge_is_atomic` asserts exactly this by injecting a failure
between the two statements.

---

## 4. `INSERT ... RETURNING` returns `None`

**Symptom.** `insert_customer_version` raises `TypeError: 'NoneType' object is
not subscriptable`.

**Cause.** `RETURNING` requires DuckDB ≥ 0.8. On older versions the statement
parses but yields no row.

**Fix.**

```bash
python -c "import duckdb; print(duckdb.__version__)"   # verified on 1.4.2
pip install --upgrade duckdb
```

On a pinned older version, replace `RETURNING` with a follow-up
`SELECT currval('seq_customer_sk')`.

---

## 5. `Sequence with name seq_customer_sk already exists`

**Symptom.** `create_schema()` fails on a persistent database file.

**Cause.** `DROP TABLE` does not drop sequences. On `:memory:` this never
surfaces because the whole database vanishes; on a file it surfaces the second
time you run.

**Fix.** `create_schema` issues `DROP SEQUENCE IF EXISTS` for each sequence. This
is the general shape of the trap: **anything you `CREATE` in a setup path needs a
matching `DROP IF EXISTS`**, including sequences, views, macros and indexes — not
just tables.

---

## 6. `test_aggregate_table_beats_the_raw_star_join` fails intermittently

**Symptom.**

```
AssertionError: aggregate 0.412ms did not beat raw join 0.398ms
```

**Cause.** A timing assertion on a machine that is doing other work. At small row
counts the raw join fits entirely in cache and the measurement is noise.

**Fix.** Three things, all present in the shipped test:

1. `seed_scale(rows=20_000)` — enough rows that the difference is structural
   rather than incidental.
2. `time_query(repeats=3)` takes the **best** of N, not the mean. This is a
   latency-floor measurement; the mean measures whatever else the OS decided to
   do.
3. A directional assertion (`mv_ms < raw_ms`) rather than a ratio threshold. A
   tight ratio here would be a flaky test rather than a strong one.

If it still fails, run it alone — a parallel `pytest -n auto` invalidates any
timing test.

---

## 7. Model and DuckDB disagree in the reconciliation test

**Symptom.**

```
AssertionError: assert {('OH',): 180.0} == {('OH',): 130.0, ('TX',): 50.0}
```

**This is the test doing its job.** One of the two implementations is wrong, and
the disagreement tells you which mechanism to look at.

**Diagnose in this order:**

1. **The as-of lookup.** Run
   `test_model_and_duckdb_agree_on_the_as_of_lookup` — it reconciles the
   mechanism rather than the total, so it isolates the cause. If it fails, the
   surrogate key resolution differs, and everything downstream follows.
2. **Interval boundaries.** Query the dimension for the change date itself. If
   DuckDB matches two rows and the model matches one, the `valid_to` arithmetic
   differs between them.
3. **Key allocation order.** Both sides must allocate surrogate keys in the same
   order for the comparison to be meaningful. The shipped test builds both in the
   same sequence for exactly this reason — if you reorder the inserts on one
   side only, the keys diverge and the test fails for an uninteresting reason.

---

## 8. `ValueError: no open version for customer_id='C1'`

**Symptom.** An SCD2 change is applied to a customer that was never loaded.

**Cause.** Pipeline task ordering — the dimension change ran before the initial
dimension load, or the initial load silently failed and its error was swallowed
(see `debug_lab` Defect 6).

**Why it raises instead of inserting.** Inserting a first version here would
"work" and produce a dimension whose earliest `valid_from` is the change date, so
every fact row before it resolves to `None` and silently drops out of every
aggregate. Failing loudly is the correct behaviour: this is a DAG ordering bug,
and it should be fixed in the DAG.

---

## 9. `DimensionalModelError: out-of-order load for 'C1'`

**Symptom.** A change with an `effective` date at or before the open version's
`valid_from`.

**Cause.** Either a late-arriving dimension row, or reprocessing a partition out
of chronological order.

**Fix — and this one is a design decision, not a code fix.** Late-arriving
dimension changes need an explicit correction path, because a retroactive change
means facts already loaded against the old version must be **re-keyed**. Silently
inserting a version with an overlapping range would corrupt the tiling invariant
and double-count. See Challenge 2B in
[`05_SELF_ASSESSMENT_AND_CHALLENGES.md`](05_SELF_ASSESSMENT_AND_CHALLENGES.md) — the
hard question is not the SQL, it is whether you are allowed to restate a report
you already published.

---

## 10. `DimensionalModelError: mv_revenue aggregates a non-additive measure`

**Symptom.** `refresh_incremental` raises on a view you expected to refresh
cheaply.

**Cause.** The view was constructed with `supports_incremental=False`, because
its measure cannot be merged from deltas.

**Fix.** Call `refresh()` for a full recompute — and understand why the
alternative was rejected. A distinct count merged additively double-counts every
entity appearing in both windows, producing a number that is wrong and
plausible. Falling back to a full refresh *silently* would also be wrong, in a
subtler way: the caller asked for an incremental refresh because they were
budgeting for O(delta) work, and quietly doing O(fact) inside it breaks that
contract without telling anyone.

For a genuinely large distinct count, the real answer is a sketch — see
[Module 12 — Redis Data Structures](../Module_12_Redis_Data_Structures_Persistence/01_README.md)
for HyperLogLog, which *is* mergeable, at a stated error bound.

---

## 11. The debug lab prints wrong numbers and exits 0

**Symptom.** Working as designed. `debug_lab/broken_warehouse_pipeline.py`
contains six planted defects, raises nothing, and returns exit code 0.

**What to do.** Read `debug_lab/SYMPTOMS.md`, write a diagnosis for each of the
six, and only then open `ANSWERS.md`. The diagnostic reasoning is the skill;
reading the answer first skips exactly the part worth practising.

**The point of the exercise:** none of the six defects is visible to liveness
monitoring. Exit code, unhandled-exception count, task-failure count and run
duration are all healthy. In analytics, silence is not success.

---

## 12. `UnicodeEncodeError: 'charmap' codec can't encode character '│'`

**Symptom.** `03_scd2_and_pipeline_demo.py` runs to the end of the DuckDB section
and then dies while printing the query plan. Only on Windows.

```
File "...\encodings\cp1252.py", line 19, in encode
UnicodeEncodeError: 'charmap' codec can't encode character '│'
```

**Cause.** DuckDB renders `EXPLAIN` as a box-drawing diagram using characters
like `│` (U+2502). The Windows console's default code page is cp1252, which has
no mapping for them, so `print` raises.

**Fix.** The demo strips the box-drawing glyphs and reports the plan's operators
instead. Two other ways to handle it, worth knowing because this bites any tool
that prints engine output on Windows:

```bash
# per-process, no code change
PYTHONIOENCODING=utf-8 python 01_scd2_and_pipeline_demo.py
```

```python
# or reconfigure the stream at the top of your script
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

**The general lesson.** Any string that came out of a database engine is
arbitrary Unicode, whatever your console can display. A script that dies while
*printing* a correct result is still a broken script — and this one only breaks
on the default terminal of the platform it was written on, which is why it
survived until the demo was run end to end.

---

## 13. Notebook: `ModuleNotFoundError: No module named 'dimensional_engine'`

**Symptom.** The notebook's first import cell fails even though the tests pass.

**Cause.** The kernel's working directory is the module root, not
`project_solution/`.

**Fix.** The notebook's setup cell inserts `project_solution` on `sys.path`
relative to the notebook's own location. If you moved the notebook, fix the
relative path rather than hard-coding an absolute one — an absolute path works on
exactly one machine, which is why `tools/check_links.py` fails the build on them.

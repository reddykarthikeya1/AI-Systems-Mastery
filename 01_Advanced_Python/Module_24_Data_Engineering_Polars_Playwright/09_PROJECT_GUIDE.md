# Module_24_Data_Engineering_Polars_Playwright: Project Implementation Guide

**Deliverable:** a high-throughput data engineering engine combining Polars LazyFrames, Apache Arrow memory, and DuckDB OLAP window queries.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_analytics_engine.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Polars DataFrame Ingestion
Initialize `MarketAnalyticsEngine` ingesting raw records into a columnar Polars DataFrame.

### Step 2 — Lazy Execution Graph
Implement `compute_sector_metrics_lazy(min_volume)` building an un-evaluated query plan with filter, projection, and grouping.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_analytics_engine.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — In-Process DuckDB SQL
Implement `rank_stocks_within_sector_duckdb()` executing analytical SQL window functions (`RANK() OVER(PARTITION BY sector ...)`) directly over the Polars memory space.

### Step 4 — Benchmark Verification
Verify that lazy filter pushdown executes substantially faster than eager loading on large datasets.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/analytics_engine.py`, replace `.filter(pl.col('volume') >= min_volume)` with post-aggregation filtering.
Run:
```bash
pytest ../project_solution/test_analytics_engine.py -k test_sector_metrics_volume_filter_threshold -v
```
Watch the metrics calculation include low-volume items in the turnover sum, then restore filter pushdown.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_analytics_engine.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Parquet Scan Partitioning:** Scan partitioned Parquet files directly from disk using `pl.scan_parquet`.
2. **Playwright Headless Scraper:** Harvest real-time ticker data from live web pages using async Playwright.
3. **Streaming Out-of-Core Execution:** Process datasets exceeding available RAM using `lazy_plan.collect(streaming=True)`.
4. **Arrow C Data Interface:** Pass Arrow memory buffers zero-copy between Polars, DuckDB, and PyArrow.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_sector_metrics_lazy_computation` | Proves Polars lazy execution computes sector turnover accurately |
| `test_duckdb_window_ranking` | Proves DuckDB partition window query assigns correct stock ranks |
| `test_sector_metrics_volume_filter_threshold` | Proves volume filtering excludes low-liquidity assets |
| `test_duckdb_sector_avg_price_window` | Proves DuckDB window averages match sector mathematical means |
| `test_perf_polars_lazy_scan_vs_eager` | Proves Polars lazy scan filter pushdown executes within performance SLA |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain columnar data storage (Apache Arrow) vs row-based Python dictionaries
- [ ] Construct lazy query graphs in Polars and inspect their execution plans with explain()
- [ ] Leverage filter and projection pushdown to minimize memory consumption
- [ ] Run complex OLAP analytical SQL queries with DuckDB directly on Polars DataFrames zero-copy
- [ ] Use window functions (RANK, DENSE_RANK, AVG OVER PARTITION) in financial analytics
- [ ] Automate browser scraping safely using Playwright with explicit waiting selectors
- [ ] Write performance benchmarks verifying columnar query execution speedups

# Design Rationale: Vectorized Data Processing with Polars & DuckDB

## Architectural Overview
A modern data engineering pipeline leveraging the Polars Rust query engine, LazyFrame execution plans, DuckDB in-memory columnar SQL, and Playwright headless browser harvesting.

## Key Design Decisions
1. **Polars LazyFrames with Predicate Pushdown:** Transformations are declared lazily, allowing the query optimizer to filter rows and prune columns before reading data into memory.
2. **Zero-Copy DuckDB SQL over Arrow:** In-memory Polars DataFrames are queried directly with DuckDB SQL using the Apache Arrow C Data Interface without serialization overhead.
3. **Async Playwright Browser Contexts:** Headless extraction uses isolated browser contexts with automated context cleanup, preventing resource and memory leaks.

## Rejected Alternatives
1. **Pandas for Multi-Gigabyte Data Ingestion:**
   - *Reason for Rejection:* Pandas allocates unboxed Python objects eagerly on a single thread, consuming 5–10x the memory of raw CSVs and causing OOM crashes.
2. **Iterating Over DataFrames with Python `for` Loops:**
   - *Reason for Rejection:* Iterating row-by-row drops out of compiled SIMD vectorization, executing 100x slower than Polars native expressions.

## Invariants & Guarantees
- Memory footprint is strictly bounded by lazy query plans.
- Window functions and rankings compute deterministically.

## Verification
```bash
pytest test_analytics_engine.py -v
pytest test_web_harvester.py -v
```

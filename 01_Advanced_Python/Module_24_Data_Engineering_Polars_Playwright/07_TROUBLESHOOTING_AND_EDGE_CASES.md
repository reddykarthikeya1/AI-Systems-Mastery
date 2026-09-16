# Module 24: Troubleshooting, Data Engineering Traps & Memory Spikes

This reference guide details common errors and optimization techniques when processing large datasets with Polars and DuckDB.

---

## 1. Out-of-Memory (OOM) Spikes: Eager vs Streaming Lazy

### The Bug
Calling `pl.read_csv("huge_50gb_file.csv")` immediately exhausts system RAM and crashes the process.

### The Fix
Always use **Lazy Scanning with Streaming Engine**:
```python
# ✅ Streams batches through RAM without blowing up memory:
df = pl.scan_csv("huge_50gb_file.csv").filter(pl.col("year") == 2026).collect(streaming=True)
```

---

## 2. Converting Polars to Pandas Unnecessarily

### The Mistake
```python
# ❌ Anti-pattern: Copies entire columnar memory into slow Python objects!
pandas_df = polars_df.to_pandas()
```

### The Rule
Keep data in Apache Arrow format across your entire pipeline. DuckDB and PyArrow can query Polars DataFrames natively with **zero memory copies**.

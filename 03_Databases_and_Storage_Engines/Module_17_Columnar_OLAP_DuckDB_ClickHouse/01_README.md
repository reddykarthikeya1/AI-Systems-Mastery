# Module 17: Columnar OLAP — DuckDB, ClickHouse & Parquet Compression

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

---

## 📊 1. Row Stores (OLTP) vs. Column Stores (OLAP)

To understand why columnar engines run analytical queries 100x to 1000x faster than relational databases, we must examine the physical memory and CPU cache line architecture:

```
[Row-Oriented (OLTP) Storage Layout]
Row 1: [ID: 1 | Name: "Alice" | Age: 30 | Salary: $120,000 | City: "San Francisco" | Bio: "..." ]
Row 2: [ID: 2 | Name: "Bob"   | Age: 45 | Salary: $160,000 | City: "New York"      | Bio: "..." ]
Row 3: [ID: 3 | Name: "Carol" | Age: 28 | Salary: $110,000 | City: "Seattle"       | Bio: "..." ]

[Column-Oriented (OLAP) Storage Layout]
IDs:      [ 1, 2, 3 ... ]
Names:    [ "Alice", "Bob", "Carol" ... ]
Ages:     [ 30, 45, 28 ... ]
Salaries: [ 120000, 160000, 110000 ... ]  <── ONLY THIS ARRAY IS READ!
Cities:   [ "San Francisco", "New York", "Seattle" ... ]
```

### The Analytical Query Bottleneck
Consider calculating the average salary across 100 million employees:
```sql
SELECT AVG(salary) FROM employees;
```

### In a Row-Oriented Store (PostgreSQL / MySQL / Oracle):
- The storage engine reads data in 8KB disk pages containing complete rows.
- To access `salary`, the CPU must load the entire row (Name, Address, Bio, Metadata) into its L1/L2/L3 cache lines (64 bytes each).
- **85% to 95% of memory bus bandwidth and disk I/O is completely wasted** loading columns that the query never requested!

### In a Column-Oriented Store (DuckDB / ClickHouse / Parquet):
- Each column is stored in an independent contiguous file or memory block.
- The query touches **only the `salary` column chunk**.
- 100% of bytes loaded into CPU cache lines are actively computed.
- Memory bus saturation drops by 10x to 50x.

---

## ⚡ 2. SIMD Vectorized Execution & Cache Locality

Traditional databases use the **Volcano Iterator Model** (Tuple-at-a-time):
- Every query operator calls `.next()` on its child operator to fetch a single row.
- For 100 million rows, this causes 100,000,000 virtual function calls, destroying branch predictors and instruction caches.

Modern OLAP engines (DuckDB, ClickHouse) use **Vectorized Execution**:
- Instead of passing 1 row, operators process a **Vector (Data Chunk)** of 1024 or 2048 values at a time.
- The values are contiguous in memory, allowing modern CPUs to process them with **SIMD (Single Instruction, Multiple Data)** instructions (Intel AVX-512, ARM Neon):
  ```
  CPU SIMD Register (512-bit) adds 8 x 64-bit floating point numbers in 1 CPU clock cycle!
  ```
- Vectorization eliminates virtual function call overhead and achieves near hardware-limit memory throughput.

---

## 🗜️ 3. Columnar Compression: RLE, Bit-Packing & Dictionary

Because values within a single column share the same data type and often exhibit repetitive patterns, columnar stores achieve **extreme compression ratios (5x to 20x)** that row stores cannot match:

### 1. Run-Length Encoding (RLE)
Consecutive repeated values are compressed into `(value, run_count)` pairs:
$$\text{Raw:} \quad [\text{"CA"}, \text{"CA"}, \text{"CA"}, \text{"CA"}, \text{"NY"}, \text{"NY"}] \implies \text{RLE:} \quad [(\text{"CA"}, 4), (\text{"NY"}, 2)]$$
- Extremely effective for sorted columns or low-cardinality flags (e.g. status codes, country codes).

### 2. Dictionary Encoding
Replaces long, repetitive strings with compact integer IDs:
- Creates a small dictionary table: `0: "PENDING", 1: "COMPLETED", 2: "FAILED"`.
- The data column replaces 9-byte strings with 1-byte integers (`uint8`), reducing memory consumption by **89%** before general compression (Snappy/ZSTD) is even applied.

### 3. Bit-Packing & Frame-of-Reference (FoR)
Standard databases store all integers as 32-bit (4-byte) or 64-bit (8-byte) words.
- If a column contains employee birth years between `1970` and `2005`:
  - Subtract baseline `1970` (Frame of Reference).
  - The resulting offsets range from `0` to `35`.
  - Storing numbers $0 \le x \le 35$ requires only **6 bits**!
  - 64-bit integers shrink to 6 bits, packing 10 values into a single 64-bit CPU register.

### 4. Delta Encoding
Stores only the difference between consecutive values:
$$\text{Timestamps:} \quad [1700000000, 1700000010, 1700000025] \implies \text{Delta:} \quad [1700000000, +10, +15]$$

---

## 📦 4. Apache Parquet Internals & Predicate Pushdown

Apache Parquet is the open standard columnar storage file format used across Hadoop, Spark, Snowflake, AWS Athena, and DuckDB:

```
┌────────────────────────────────────────────────────────┐
│ Parquet File                                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Row Group 1 (~512 MB, e.g. 1,000,000 rows)       │  │
│  │  - Column Chunk 'user_id'   (Min: 1, Max: 50000) │  │
│  │  - Column Chunk 'timestamp' (Min: 2026-01-01...) │  │
│  │  - Column Chunk 'amount'    (Min: 5.0, Max: 800) │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Row Group 2 (~512 MB, e.g. 1,000,000 rows)       │  │
│  │  - Column Chunk 'user_id'   (Min: 50001...)      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ File Metadata / Footer (Schema & Row Group Stats)│  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### Predicate Pushdown & Zone Map Pruning
The Parquet footer stores summary statistics (`min_value`, `max_value`, `null_count`) for every column chunk in every row group:
```sql
SELECT * FROM sales WHERE amount > 1000;
```
1. The engine reads only the small footer metadata (a few kilobytes).
2. For Row Group 1, `Max(amount) = 800`.
3. Because $800 < 1000$, the engine **completely skips reading Row Group 1 from disk**!
4. Querying petabyte-scale datasets skips 90%+ of all row groups without decompressing a single data page.

---

## 🦆 5. DuckDB: The "SQLite for Analytics"

DuckDB has revolutionized data engineering by providing an in-process, zero-dependency, C++ columnar analytics engine:
- **Zero-Copy Arrow Integration**: Reads Apache Arrow buffers, Polars DataFrames, and Pandas DataFrames directly in memory without data copying or serialization.
- **Out-of-Core Execution**: Can process datasets far larger than physical RAM by streaming and spilling partitioned blocks to disk.
- **Direct Parquet / S3 Querying**: Executes full SQL directly over local or remote Parquet files with automatic predicate pushdown.

---

## 🛠️ 6. Hands-On Lab: Building a Columnar Storage & Compression Engine

In this lab, you will implement:
1. **Columnar Chunk Storage**: Transform row-oriented tuples into contiguous columnar arrays.
2. **Run-Length Encoding (RLE) & Dictionary Compression**: Encode repetitive data and measure exact compression ratios.
3. **Bit-Packing / Frame of Reference**: Compress bounded integers into bit-packed buffers.
4. **Vectorized Aggregation Operators**: Compute `SUM`, `AVG`, `MIN`, `MAX` over columnar vectors with zero per-row object overhead.
5. **Predicate Pushdown & Zone Map Pruning**: Evaluate query filters against Row Group Min/Max statistics to skip irrelevant chunks.

---

## 📂 Project Structure
```
Module_17_Columnar_OLAP_DuckDB_ClickHouse/
├── README.md
├── 01_columnar_compression_simd_demo.py
├── starter/
│   └── columnar_engine.py
└── project_solution/
    ├── columnar_engine.py
    └── test_columnar_engine.py
```

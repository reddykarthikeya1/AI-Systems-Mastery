# Debug Lab Answers: Module 24

<details>
<summary>Bug 1: Unsanitized schema inference</summary>

### Root Cause
Polars infers column datatypes based on the input entries. A single non-numeric sentinel (e.g. `"N/A"`) causes the entire column to be typed as `String`.

### Fix
Clean null sentinels or explicitly cast with `strict=False`:
```python
df = df.with_columns(
    pl.col("price").cast(pl.Float64, strict=False).alias("price")
)
```
</details>

# 🐣 Interactive Foundations Playground: Data Engineering: Polars & Playwright Patterns

> *"Columnar table layouts accelerate analytical queries by processing contiguous memory vectors."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python

```

---

## 1. Columnar Table In-Memory Layout

Representing tables as dictionaries of column arrays allows vectorized filtering and projections.

```python
table = {
    "user_id": [101, 102, 103, 104],
    "amount": [25.0, 150.0, 75.5, 200.0],
    "status": ["completed", "pending", "completed", "completed"]
}

# Vectorized filter: status == 'completed'
completed_indices = [i for i, s in enumerate(table["status"]) if s == "completed"]
completed_sum = sum(table["amount"][i] for i in completed_indices)

assert completed_indices == [0, 2, 3]
assert completed_sum == 300.5
assert len(completed_indices) == 3
print(f"Columnar filter returned completed sum: ${completed_sum}")
```

---

## 2. Chunked Batch Processing

Chunking large record streams prevents memory exhaustion during ETL pipeline ingestion.

```python
def chunk_stream(iterable, chunk_size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

batches = list(chunk_stream(range(10), 3))
assert len(batches) == 4
assert batches[0] == [0, 1, 2]
assert batches[-1] == [9]
print(f"Stream split into {len(batches)} batches of size <= 3.")
```

---

## 3. Schema Projection and Selection

Selecting a subset of columns avoids loading unused data across pipeline boundaries.

```python
def project_columns(table, columns):
    return {col: table[col] for col in columns if col in table}

proj = project_columns(table, ["user_id", "amount"])
assert set(proj.keys()) == {"user_id", "amount"}
assert len(proj["user_id"]) == 4
print(f"Projected schema columns: {list(proj.keys())}")
```

---

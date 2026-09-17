"""Beginner playground for Module 24 - Data Engineering: Polars & Playwright Patterns.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. Columnar Table In-Memory Layout
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

# -------------------------------------------- 2. Chunked Batch Processing
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

# -------------------------------------------- 3. Schema Projection and Selection
def project_columns(table, columns):
    return {col: table[col] for col in columns if col in table}

proj = project_columns(table, ["user_id", "amount"])
assert set(proj.keys()) == {"user_id", "amount"}
assert len(proj["user_id"]) == 4
print(f"Projected schema columns: {list(proj.keys())}")

print()
print("All checks passed.")

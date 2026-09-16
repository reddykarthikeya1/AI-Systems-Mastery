"""Beginner playground for Module 17 - Columnar Storage - DuckDB and ClickHouse.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import zlib

# ----------------------------------------- 1. Two ways to put a table on disk
departments = ["eng", "sales", "ops", "hr"]
row_store = [(i, f"employee{i}", departments[i % 4], 40_000 + (i % 20) * 1_000)
             for i in range(10_000)]
column_store = {
    "id": [r[0] for r in row_store],
    "name": [r[1] for r in row_store],
    "dept": [r[2] for r in row_store],
    "salary": [r[3] for r in row_store],
}
print("rows:", len(row_store), "columns:", list(column_store))


# ------------------------------------- 2. Count what each layout has to touch
row_values_read = 0
row_total = 0
for row in row_store:
    row_values_read += len(row)          # the whole row arrives whether you want it or not
    row_total += row[3]

column_values_read = len(column_store["salary"])
column_total = sum(column_store["salary"])

print(f"row store   : read {row_values_read:,} values")
print(f"column store: read {column_values_read:,} values")
assert row_total == column_total, "identical answer"
assert column_values_read * 4 == row_values_read, "4 columns, so 4x the reading"


# ----------------------------------- 3. Compression is the second, bigger win
def compressed_size(values):
    raw = ",".join(str(v) for v in values).encode()
    return len(raw), len(zlib.compress(raw, 6))


dept_raw, dept_packed = compressed_size(column_store["dept"])
id_raw, id_packed = compressed_size(column_store["id"])

print(f"dept column: {dept_raw:>7,} -> {dept_packed:>6,} bytes "
      f"({dept_raw / dept_packed:.0f}x)")
print(f"id column  : {id_raw:>7,} -> {id_packed:>6,} bytes "
      f"({id_raw / id_packed:.0f}x)")
assert dept_raw / dept_packed > id_raw / id_packed, "repeated values pack far tighter"


# ---------------------------------------------------- 4. The honest trade-off
row_lookup_touches = 1
column_lookup_touches = len(column_store)

print(f"fetching one whole row: row store touches {row_lookup_touches} place,")
print(f"                        column store touches {column_lookup_touches} places")
assert column_lookup_touches > row_lookup_touches

assert row_store[4_271] == tuple(column_store[c][4_271] for c in
                                 ("id", "name", "dept", "salary"))
print("Same data. Pick the layout that matches the question you ask most.")


print()
print("All checks passed.")

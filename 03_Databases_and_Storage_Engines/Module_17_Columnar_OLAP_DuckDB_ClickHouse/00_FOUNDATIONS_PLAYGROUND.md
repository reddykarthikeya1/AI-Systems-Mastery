# Beginner Playground - Columnar Storage - DuckDB and ClickHouse

> *"A row store keeps one folder per customer. A column store keeps one folder per field - so 'total all salaries' opens exactly one folder instead of every folder you own."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import zlib
```

---

## 1. Two ways to put a table on disk

Disks and memory hand you *blocks*, not individual values. So the layout decides
what arrives alongside the thing you asked for.

- **Row store**: `[id, name, dept, salary][id, name, dept, salary]...`
  Ask for one employee and everything about them arrives together. Perfect for
  "show me this order". Ask for one *column* and 19 unwanted ones tag along.
- **Column store**: `[all ids][all names][all depts][all salaries]`
  Ask for one column and nothing else is read at all.

```python
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
```

---

## 2. Count what each layout has to touch

Same query, same answer, same data. The only difference is how many stored values
had to be read to produce it.

```python
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
```

---

## 3. Compression is the second, bigger win

A column holds one kind of thing. `dept` is the same four strings over and over,
and that repetition compresses enormously. `id` is all distinct and barely
compresses at all.

In a row store those values are interleaved with unrelated data, so the repetition
is hidden and the compressor cannot exploit it. Better compression means fewer
bytes off the disk, which is a second speed-up on top of the first.

```python
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
```

---

## 4. The honest trade-off

Now ask the opposite question: *give me everything about employee 4,271*.

The row store reads one contiguous chunk. The column store has to visit all four
column files and reassemble the row - and with 200 columns, 200 files.

Column stores are not better. They are better *at analytics*, and worse at
fetching and updating single rows. That is why a serious system runs both: a
row-store OLTP database for the application, and a columnar warehouse for the
reporting. Same data, two shapes, two jobs.

```python
row_lookup_touches = 1
column_lookup_touches = len(column_store)

print(f"fetching one whole row: row store touches {row_lookup_touches} place,")
print(f"                        column store touches {column_lookup_touches} places")
assert column_lookup_touches > row_lookup_touches

assert row_store[4_271] == tuple(column_store[c][4_271] for c in
                                 ("id", "name", "dept", "salary"))
print("Same data. Pick the layout that matches the question you ask most.")
```

---

## 5. Predict before you run

A table has 20 columns and 10 million rows. You run
`SELECT SUM(salary) FROM employees`. How many of the 200 million stored values
does a row store have to read? How many does a column store read?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

This is why your analytics query is slow on PostgreSQL and instant on DuckDB
running identical SQL on identical data. Not a better optimiser - a different
physical layout, chosen for a different question.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

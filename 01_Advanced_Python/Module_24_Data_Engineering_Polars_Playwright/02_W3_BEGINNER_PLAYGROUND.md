# W3Schools-Style Playground: Data Engineering & Columnar Processing

> *"Row-by-row loops crawl; columnar vectorized engines fly."*

Welcome to the **Module 24 Data Engineering Polars Playwright** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Data engineering processes millions of records efficiently. While standard Python lists process row-by-row, modern columnar engines (like Polars or DuckDB) execute operations across entire memory columns in parallel.

---

## 2. Micro-Code Example (3-5 Lines)

```python
# Columnar storage concept:
# Instead of a list of dicts: [{'age': 20}, {'age': 30}]
# Columnar stores arrays of identical types:
columnar_data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [70000, 85000, 95000]
}

# Fast columnar filter in pure Python:
high_earners = [
    columnar_data["name"][i]
    for i, s in enumerate(columnar_data["salary"])
    if s > 80000
]
print("High Earners:", high_earners)
```

### Line-by-Line Breakdown:
- Columnar memory keeps all numbers in contiguous RAM blocks, maximizing CPU cache lines.
- Vectorized operations apply a math instruction across an entire array simultaneously.
- **Headless Browser Automation:** Tools like Playwright control real web browsers via code for reliable data extraction and end-to-end testing.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Why is columnar memory faster for aggregation (like calculating average salary)?

<details><summary><b>Show Answer</b></summary>

The CPU only reads the salary column into cache, ignoring irrelevant columns like names or addresses.
</details>

---

### Drill 2: Quick Check
What does 'headless browser' mean?

<details><summary><b>Show Answer</b></summary>

A browser running in the background without a graphical user interface window.
</details>

---

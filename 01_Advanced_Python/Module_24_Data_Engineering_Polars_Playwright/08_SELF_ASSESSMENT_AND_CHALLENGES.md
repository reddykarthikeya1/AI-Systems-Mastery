# Module 24: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Polars, DuckDB, and Modern Data Engineering before moving to **Module 23**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Rust & Arrow:** Why is Polars fundamentally faster and more memory-efficient than Pandas?
2. **Columnar Memory:** How does Apache Arrow's columnar memory layout optimize analytical aggregations like `SUM()` and `AVG()`?
3. **Query Optimization:** What is **Predicate Pushdown**, and how does Polars use it to minimize data loaded from disk?
4. **Lazy vs Eager:** What is the mechanical difference between a Polars `DataFrame` and a `LazyFrame`?
5. **Out-of-Core Processing:** How does `collect(streaming=True)` allow Polars to process datasets that are larger than available system RAM?
6. **In-Process OLAP:** What is DuckDB, and how does it differ from traditional database servers like PostgreSQL?
7. **Zero-Copy Interop:** How do Polars and DuckDB exchange data in memory without serializing or copying byte buffers?
8. **Window Functions:** In SQL analytics, what does `AVG(sales) OVER(PARTITION BY region)` compute?
9. **Storage Formats:** Why is Apache Parquet significantly faster to query than CSV or JSON?
10. **Headless Scraping:** Why is Playwright preferred over basic HTTP libraries (`requests` / `httpx`) when scraping Single-Page Applications (SPAs)?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
Polars is written in Rust, utilizes multi-threaded parallel execution (Rayon), processes data in columnar Arrow format, and optimizes query execution graphs before running.

#### Answer 2:
Columnar memory stores values of the same column contiguously in RAM, allowing the CPU to load only that column into L1/L2 cache and use SIMD vector instructions.

#### Answer 3:
It moves filter conditions (`WHERE price > 100`) as early as possible in the query pipeline, discarding irrelevant rows at the file scanner level before loading them into memory.

#### Answer 4:
- `DataFrame`: Executes operations immediately in memory (eager).
- `LazyFrame`: Builds a logical execution plan without executing until `.collect()` is explicitly called.

#### Answer 5:
It breaks the dataset into memory-bounded chunk streams, processing batches through the CPU pipeline and freeing them continuously.

#### Answer 6:
DuckDB is an embedded in-process columnar analytical database engine that runs directly inside Python memory without external server processes or socket overhead.

#### Answer 7:
They both conform to the **Apache Arrow C-Data Interface**, passing pointers to existing memory buffers instead of copying data.

#### Answer 8:
It calculates the average sales for each region without collapsing individual rows, appending the regional average alongside each row.

#### Answer 9:
Parquet is columnar, compressed with Snappy/ZSTD, and contains min/max column chunk statistics that allow skipping unneeded data blocks.

#### Answer 10:
Playwright controls a real Chromium browser engine, executing JavaScript, waiting for network hydration, and interacting with client-rendered DOM nodes.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Polars Regional Sales GroupBy

**Goal:** Using Polars, group sales by `region` and compute total revenue (`price * qty`) and average discount.

<details>
<summary><b>Solution Code</b></summary>

```python
import polars as pl

df = pl.DataFrame({
    "region": ["North", "South", "North", "South"],
    "price": [100.0, 200.0, 150.0, 50.0],
    "qty": [2, 1, 3, 4],
    "discount": [0.1, 0.0, 0.15, 0.05],
})

res = (
    df.with_columns((pl.col("price") * pl.col("qty")).alias("revenue"))
    .group_by("region")
    .agg([
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("discount").mean().alias("avg_discount"),
    ])
)
print(res)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Fixed sleep instead of waiting for a condition

```python
page.goto(url)
page.wait_for_timeout(3000)          # "give it time to load"
rows = page.query_selector_all("#table tbody tr")
```

**Observed symptom:** Passes locally, fails ~15% of the time in CI, and always takes at least 3 seconds even when the page is ready in 200 ms.

**(a)** Why is a fixed sleep both too short and too long?

**(b)** What is the correct call?

**(c)** What is the general principle?

<details>
<summary><b>Show the diagnosis</b></summary>

**Too short** whenever CI is slower than your laptop — a loaded runner takes 4 s and the selector is empty. **Too long** in the common case, wasting 2.8 s on every run of every test. There is no value that is both reliable and fast.

**Correct:** wait for the *condition* — `page.wait_for_selector('#table tbody tr', state='attached')`. It returns the instant the element exists and fails fast with a clear error if it never does.

**Principle:** never sleep for a duration; wait for an observable state change. This generalises well beyond browsers — polling a queue, waiting for a container healthcheck, waiting for a file to appear. Every `sleep` in a test is a guess about someone else's timing, and it is the single largest source of flaky suites. Module 24's harvester waits on selectors, load state, and a stable element count, never on a clock.

</details>

---

### D2. Inferred dtype corrupts a numeric column

```python
import polars as pl

rows = [{"price": "10.50"}, {"price": "N/A"}, {"price": "8.25"}]
df = pl.DataFrame(rows)
print(df["price"].sum())
```

**Observed symptom:** Either a `SchemaError`, or a string concatenation, depending on version — never the numeric total you wanted.

**(a)** What dtype did Polars infer, and why?

**(b)** What are the two correct handling strategies?

**(c)** Why is this worse than an immediate crash?

<details>
<summary><b>Show the diagnosis</b></summary>

Every value is a string, and `"N/A"` is not parseable as a number, so the column is inferred as `Utf8`. Aggregations then either fail or do something string-shaped.

**Two strategies:** (1) **normalise at the boundary** — parse each value as you build the row and decide explicitly what `"N/A"` means (null, zero, or a rejected record). Module 24's `_parse_price` does this and raises on unparseable input. (2) **declare the schema** — `pl.DataFrame(rows, schema={'price': pl.Float64})` plus `cast(strict=False)` to turn unparseable values into nulls deliberately.

**Worse than a crash** because a silently-`Utf8` column flows downstream: joins still work, filters still work, and the wrong number appears in a report weeks later with no traceback pointing at the cause. Explicit schemas turn a silent data-quality bug into an immediate, local failure.

</details>

---

### D3. Eager collect defeats lazy evaluation

```python
import polars as pl

df = pl.read_csv("events_50gb.csv")            # eager
result = (df
          .filter(pl.col("country") == "IN")
          .group_by("user_id")
          .agg(pl.col("amount").sum()))
```

**Observed symptom:** `MemoryError`, or the process is OOM-killed.

**(a)** What did `read_csv` do that caused this?

**(b)** What is the lazy equivalent?

**(c)** What two optimisations does the lazy engine then apply?

<details>
<summary><b>Show the diagnosis</b></summary>

`read_csv` is **eager**: it materialises all 50 GB in memory before the filter is even seen.

**Lazy equivalent:**

```python
result = (pl.scan_csv('events_50gb.csv')
          .filter(pl.col('country') == 'IN')
          .group_by('user_id')
          .agg(pl.col('amount').sum())
          .collect())
```

`scan_csv` builds a query plan; `collect()` executes it.

**Two optimisations:** **predicate pushdown** — the `country == 'IN'` filter is applied *during* the scan, so non-matching rows are never materialised; and **projection pushdown** — only `country`, `user_id` and `amount` are read from disk, so unused columns cost nothing. Inspect the plan with `.explain()` before `.collect()`. This is the same idea as a database query planner, and it is why the lazy API is the default choice for anything larger than memory.

</details>

---

### D4. Scraping the DOM when an API exists

```python
rows = page.query_selector_all(".product-row")
products = [{"name": r.query_selector(".name").inner_text(),
             "price": r.query_selector(".price").inner_text()} for r in rows]
```

**Observed symptom:** Works for three weeks, then returns empty lists after the site ships a redesign.

**(a)** Why is DOM scraping fragile here?

**(b)** What should you check for first?

**(c)** How do you find it?

<details>
<summary><b>Show the diagnosis</b></summary>

CSS classes are **presentation**, not a contract. A redesign, a CSS-in-JS build producing hashed class names, or an A/B test all change them, and your selectors silently match nothing — returning an empty list rather than an error, which is the worst failure mode.

**Check first for an underlying JSON API.** If the page renders itself from `fetch('/api/products')`, read that instead: it is structured, typed, far cheaper, and stable across redesigns because it *is* an interface with consumers.

**Find it** in DevTools → Network → Fetch/XHR while the page loads, or programmatically by attaching a response listener — which is what Module 24's `harvest_via_api_interception` does. Also check for a `__NEXT_DATA__` script tag or similar embedded JSON, and for a documented public API before scraping at all.

</details>

---

### D5. Unbounded pagination crawl

```python
while True:
    scrape_current_page()
    next_link = page.query_selector("a.next")
    if not next_link:
        break
    next_link.click()
```

**Observed symptom:** The scraper makes 40,000 requests overnight and the target IP-bans you.

**(a)** Name the two failure modes in this loop.

**(b)** What bounds should be present?

**(c)** What is the ethical dimension you must handle separately?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two failure modes.** (1) No iteration bound — a site whose 'next' link is always present (a circular paginator, or an infinite calendar) loops forever. (2) No rate limit — requests go out as fast as the network allows, which looks exactly like an attack.

**Bounds needed:** a `max_pages` cap (Module 24's `harvest_all_pages` takes one and its test asserts it is respected), a delay between requests, a per-request timeout, and deduplication by URL or record id so a circular paginator is detected rather than followed.

**Ethical dimension:** check `robots.txt` and the terms of service, identify your bot honestly in the `User-Agent` (Module 24 sends `Module24-CourseHarvester/1.0`), and rate-limit out of courtesy rather than only to avoid a ban. Spoofing a browser UA to evade rate limits is both a reliability anti-pattern and the wrong thing to do — which is why this module's fixtures are local HTML rather than someone else's live site.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.

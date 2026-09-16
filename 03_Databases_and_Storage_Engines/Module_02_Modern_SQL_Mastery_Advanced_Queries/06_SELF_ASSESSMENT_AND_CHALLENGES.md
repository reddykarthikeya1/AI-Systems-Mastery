# Module 02 Modern SQL Mastery Advanced Queries: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Modern SQL Mastery & Advanced Analytics** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the formal difference between RANK() and DENSE_RANK() when ties occur in window ordering?** What is the formal difference between RANK() and DENSE_RANK() when ties occur in window ordering?
2. **Why does WHERE id NOT IN (SELECT foreign_id FROM t) evaluate to 0 rows if any foreign_id is NULL?** Why does WHERE id NOT IN (SELECT foreign_id FROM t) evaluate to 0 rows if any foreign_id is NULL?
3. **How does a Common Table Expression (CTE) differ from a subquery in execution optimization?** How does a Common Table Expression (CTE) differ from a subquery in execution optimization?
4. **Explain how RECURSIVE CTE termination works.?** Explain how RECURSIVE CTE termination works.
5. **What is an Anti-Join, and how is it implemented using NOT EXISTS?** What is an Anti-Join, and how is it implemented using NOT EXISTS?
6. **What is the default window frame when ORDER BY is specified without a ROWS clause?** What is the default window frame when ORDER BY is specified without a ROWS clause?
7. **How does LEAD(col, 1) OVER (...) differ from LAG(col, 1) OVER (...)?** How does LEAD(col, 1) OVER (...) differ from LAG(col, 1) OVER (...)?
8. **Why are correlated subqueries in a SELECT list often an anti-pattern?** Why are correlated subqueries in a SELECT list often an anti-pattern?
9. **How does COALESCE(val, 'N/A') differ from NULLIF(val1, val2)?** How does COALESCE(val, 'N/A') differ from NULLIF(val1, val2)?
10. **What is the difference between UNION and UNION ALL?** What is the difference between UNION and UNION ALL?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
RANK() leaves gaps in the sequence following ties (e.g. 1, 2, 2, 4), while DENSE_RANK() leaves no gaps (e.g. 1, 2, 2, 3).

#### Answer 2:
Because in three-valued logic, comparison with NULL yields UNKNOWN. Any condition WHERE UNKNOWN is treated as false.

#### Answer 3:
In modern query planners, non-recursive CTEs can be inlined or materialized as temp tables, whereas subqueries are typically inlined.

#### Answer 4:
The recursive member executes repeatedly, taking the previous iteration's result as input until it returns an empty result set.

#### Answer 5:
An anti-join returns rows from table A that have no matching record in table B: WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.id = A.id).

#### Answer 6:
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, which lumps duplicate peer values together.

#### Answer 7:
LEAD accesses the following row value, while LAG accesses the preceding row value.

#### Answer 8:
They execute once per row in the outer query ($O(N)$ execution), whereas a JOIN or window function executes in set-oriented batches.

#### Answer 9:
COALESCE returns the first non-null argument. NULLIF returns NULL if both arguments are equal; otherwise returns the first argument.

#### Answer 10:
UNION deduplicates rows by performing an expensive sort/hash set operation; UNION ALL simply appends streams without deduplication.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement a query calculating the 7-day moving average of daily sales per region.

### 🚀 Challenge 2: Architect Stretch Problem
Write a recursive CTE that computes transitive closure over an acyclic bill-of-materials graph.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. NOT IN with NULL subquery evaluating to empty set

```sql
SELECT customer_id, name 
FROM customers 
WHERE customer_id NOT IN (
    SELECT referrer_id FROM customers
);
```

**Observed symptom:** Query returns zero rows even though 90% of customers have never referred anyone.

**(a)** Why does SQL three-valued logic cause `NOT IN` to evaluate to empty when the subquery contains a single NULL?

**(b)** What is the exact Boolean expression SQL evaluates when checking `val NOT IN (1, 2, NULL)`?

**(c)** What is the production-safe rewrite using `NOT EXISTS` or `IS NOT NULL`?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** In SQL three-valued logic, `x NOT IN (a, b, NULL)` expands to `(x <> a) AND (x <> b) AND (x <> NULL)`. The comparison `x <> NULL` evaluates to `UNKNOWN`. Because `TRUE AND UNKNOWN` yields `UNKNOWN`, the `WHERE` clause filters out every row.

**Fix 1:** Add explicit null check: `SELECT referrer_id FROM customers WHERE referrer_id IS NOT NULL`.

**Fix 2 (Preferred):** Use `NOT EXISTS`: `WHERE NOT EXISTS (SELECT 1 FROM customers r WHERE r.referrer_id = customers.customer_id)`. `NOT EXISTS` uses two-valued logic and is null-safe.

</details>

---

### D2. Missing PARTITION BY in Window Function accumulating globally

```sql
SELECT 
    dept_id, 
    emp_name, 
    salary,
    SUM(salary) OVER (ORDER BY salary ROWS UNBOUNDED PRECEDING) AS running_total
FROM employees;
```

**Observed symptom:** The running total accumulates across all employees in the entire company instead of resetting per department.

**(a)** Why did the window function compute an enterprise-wide running total?

**(b)** What clause must be added to scope window calculations to individual departments?

**(c)** How does the default frame `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` handle peer duplicate salaries?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Missing `PARTITION BY dept_id`. Without a partition clause, the entire result set is treated as a single window partition.

**Fix:** Add partition clause: `SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary ROWS UNBOUNDED PRECEDING)`.

**RANGE vs ROWS:** `RANGE` treats duplicate values of the `ORDER BY` column as peers and aggregates them all together into the running total at once, whereas `ROWS` processes strictly row-by-row.

</details>

---

### D3. Correlated Subquery in SELECT clause inducing O(N) execution cliff

```sql
SELECT 
    o.order_id, 
    o.order_date,
    (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) AS item_count
FROM orders o;
```

**Observed symptom:** Query on 1,000,000 orders takes 120 seconds to execute, consuming 100% CPU on sequential index lookups.

**(a)** Why does a correlated scalar subquery in the SELECT list cause severe execution degradation?

**(b)** Rewrite this query using a `LEFT JOIN` and `GROUP BY`.

**(c)** Which query plan operator does the optimizer use when converting this into a set-oriented hash join?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** The scalar subquery executes once for every individual row in the outer `orders` table (an $O(N)$ correlated loop execution).

**Fix:** Rewrite to a set-oriented aggregation:
```sql
SELECT o.order_id, o.order_date, COALESCE(COUNT(oi.item_id), 0) AS item_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date;
```
**Optimizer Plan:** The database optimizer can now use a single `Hash Aggregate` over a `Hash Left Join`, completing in $O(N + M)$ time instead of 1,000,000 separate index seeks.

</details>

---

### D4. Lexicographical string sorting on numeric VARCHAR column

```sql
SELECT invoice_id, amount_due 
FROM invoices 
ORDER BY invoice_id ASC;
```

**Observed symptom:** Invoices sort as: 'INV-1', 'INV-10', 'INV-100', 'INV-2', 'INV-20', 'INV-3'.

**(a)** Why does 'INV-100' appear before 'INV-2' in standard ascending sort order?

**(b)** How can you write a deterministic expression in the ORDER BY clause to sort numerically by invoice number?

**(c)** What is the clean schema migration to prevent this ordering defect permanently?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** `invoice_id` is stored as `VARCHAR`/`TEXT`. Text strings are compared byte-by-byte lexicographically; character `'1'` has a lower ASCII/Unicode code point than `'2'`, so any string starting with `'1'` precedes `'2'` regardless of length.

**Fix:** Extract and cast the numeric suffix: `ORDER BY CAST(SUBSTRING(invoice_id FROM 5) AS INTEGER) ASC`.

**Schema Fix:** Split into a generated prefix column and an integer sequence: `id INT GENERATED ALWAYS AS IDENTITY`, formatting as `'INV-' || id` only in the presentation layer.

</details>

---

### D5. Unbounded Recursive CTE causing infinite loop and stack exhaustion

```sql
WITH RECURSIVE org_chart AS (
    SELECT emp_id, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org_chart o ON e.manager_id = o.emp_id
)
SELECT * FROM org_chart;
```

**Observed symptom:** Query hangs indefinitely, exhausting temp memory until terminating with `ERROR: statement timeout` or `recursion limit exceeded`.

**(a)** What data cycle in the `employees` table causes the recursive member to loop infinitely?

**(b)** How can you track visited nodes using an array in PostgreSQL to prevent cycles?

**(c)** What clause in modern PostgreSQL 14+ natively detects recursion cycles?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A cycle exists in employee manager hierarchy (e.g. Employee A reports to B, B reports to C, and C mistakenly reports to A). The recursive join continuously re-discovers previously visited nodes.

**Array Tracking Fix:** Track paths: `ARRAY[e.emp_id]` and terminate when `NOT (e.emp_id = ANY(o.path))`.

**PostgreSQL 14+ Native Fix:** Use `CYCLE emp_id SET is_cycle USING path`, which automatically flags and breaks cyclic iterations.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.

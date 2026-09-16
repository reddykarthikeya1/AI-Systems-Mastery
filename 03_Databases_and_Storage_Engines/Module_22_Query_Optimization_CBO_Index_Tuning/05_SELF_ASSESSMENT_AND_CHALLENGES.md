# Module 22 Query Optimization CBO Index Tuning: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the role of the Cost-Based Optimizer (CBO) in relational engines?** What is the role of the Cost-Based Optimizer (CBO) in relational engines?
2. **How does System R dynamic programming optimize multi-table join orderings?** How does System R dynamic programming optimize multi-table join orderings?
3. **Explain the differences between Nested Loop Join, Hash Join, and Sort-Merge Join.?** Explain the differences between Nested Loop Join, Hash Join, and Sort-Merge Join.
4. **What are Column Histograms and Most Common Values (MCV) lists in database statistics?** What are Column Histograms and Most Common Values (MCV) lists in database statistics?
5. **What is an 'Interesting Sort Order' in query planning?** What is an 'Interesting Sort Order' in query planning?
6. **Why does wrapping a column in a function (`WHERE UPPER(name) = 'ALICE'`) invalidate an index?** Why does wrapping a column in a function (`WHERE UPPER(name) = 'ALICE'`) invalidate an index?
7. **What is a Sargable (Search-Argument-Able) query?** What is a Sargable (Search-Argument-Able) query?
8. **How does Genetic Query Optimization (GEQO) prevent planning stalls on large queries?** How does Genetic Query Optimization (GEQO) prevent planning stalls on large queries?
9. **What is Selectivity in query cost estimation?** What is Selectivity in query cost estimation?
10. **What does the `random_page_cost` parameter in PostgreSQL represent?** What does the `random_page_cost` parameter in PostgreSQL represent?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
It explores equivalent relational algebra query execution plans and estimates their execution cost (I/O + CPU) to pick the cheapest plan.

#### Answer 2:
It builds optimal join plans bottom-up for sub-relations of size $k$, pruning sub-optimal permutations based on cost and interesting sort orders.

#### Answer 3:
Nested Loop: for each outer row, scans inner (fast with inner index); Hash Join: builds hash table on smaller relation, probes with larger; Sort-Merge: sorts both relations, merges linearly.

#### Answer 4:
Statistical summaries in `pg_statistic` estimating value distribution and selectivity for WHERE clause predicates.

#### Answer 5:
An ordering produced by an index or sort that satisfies subsequent `ORDER BY` or `GROUP BY` clauses, avoiding redundant sort operations.

#### Answer 6:
The index stores raw values of `name`, not computed `UPPER(name)`; the planner must fall back to a full table scan.

#### Answer 7:
A query predicate written such that the engine can utilize an index seek (e.g. `col >= val` instead of `col + 5 >= val`).

#### Answer 8:
It uses randomized heuristic algorithms rather than exhaustive enumeration when join count exceeds threshold (typically 12 relations).

#### Answer 9:
The estimated fraction of total rows that satisfy a predicate (between 0.0 and 1.0).

#### Answer 10:
The estimated cost to access a non-sequential disk page relative to `seq_page_cost` (tuned lower for SSDs, e.g. 1.1).

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement dynamic programming join enumeration for a 4-table join and calculate lowest cost plan.

### 🚀 Challenge 2: Architect Stretch Problem
Create extended statistics on correlated columns and verify query plan correction in PostgreSQL.

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

### D1. Stale Statistics Causing Optimizer to Choose Nested Loop over Hash Join

```sql
-- Table 'orders' grew from 1,000 rows to 15,000,000 rows after bulk import
-- Table 'customers' has 500,000 rows

SELECT c.customer_name, sum(o.total_amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
GROUP BY c.customer_name;
```

**Observed symptom:** Query previously ran in 400ms. Following the bulk import, the query runs for 48 minutes with 100% single-core CPU utilization.

**(a)** Why did the Cost-Based Optimizer (CBO) choose a Nested Loop join instead of a Hash Join or Merge Join?

**(b)** How does `EXPLAIN (ANALYZE)` reveal estimation errors (rows=... estimated vs actual)?

**(c)** What maintenance command updates catalog statistics, and how do you configure autovacuum analyze thresholds?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
The Cost-Based Optimizer relies on table statistics in `pg_statistic` (or `pg_class.reltuples`). Before the bulk import, `orders` had only 1,000 rows, for which a Nested Loop join is the lowest-cost plan. Because autovacuum/analyze had not yet executed after the bulk import, the planner believed `orders` still contained only 1,000 rows. In reality, scanning 15,000,000 rows in an unindexed or index-driven nested loop results in $50,000 	imes 15,000,000$ index/heap evaluations, turning a sub-second Hash Join into a 48-minute disaster.

**Diagnostic Commands:**
1. Run `EXPLAIN ANALYZE`:
   ```sql
   EXPLAIN ANALYZE SELECT ...;
   ```
   Look for: `Nested Loop (cost=... rows=10 width=...) (actual time=... rows=4500000)`. Notice the 1000x disparity between estimated rows and actual rows.
2. Check last analyze timestamp:
   ```sql
   SELECT relname, last_analyze, last_autoanalyze, reltuples FROM pg_stat_user_tables WHERE relname = 'orders';
   ```

**Production Fix:**
1. **Immediate Fix:** Run `ANALYZE` immediately after large bulk inserts or data migrations:
   ```sql
   ANALYZE orders;
   ANALYZE customers;
   ```
2. **Tune Auto-Analyze Thresholds:** For large tables, default 10% change thresholds take too long to trigger. Lower the threshold:
   ```sql
   ALTER TABLE orders SET (autovacuum_analyze_scale_factor = 0.02); -- Trigger at 2% changes
   ```

</details>

---

### D2. Missing Foreign Key Index Causing Table ShareLock Deadlocks

```sql
CREATE TABLE departments (
    dept_id serial PRIMARY KEY,
    name text
);

CREATE TABLE employees (
    emp_id serial PRIMARY KEY,
    dept_id int REFERENCES departments(dept_id) ON DELETE CASCADE,
    name text
);
-- Note: dept_id in employees is NOT indexed!

-- Transaction 1:
DELETE FROM departments WHERE dept_id = 5;

-- Concurrent Transaction 2:
UPDATE employees SET name = 'Bob' WHERE emp_id = 9921;
```

**Observed symptom:** Deleting a department blocks all updates to the employees table. Concurrently executing transactions fail with: ERROR: deadlock detected, or queries time out after waiting on ShareLock.

**(a)** Why does a foreign key without an index cause table-level locks or sequential scans during parent key updates/deletes?

**(b)** Does PostgreSQL automatically create indexes on Foreign Key columns?

**(c)** What SQL query finds all unindexed foreign keys across the entire database schema?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Unlike primary keys and unique constraints, **foreign key columns are NOT automatically indexed in PostgreSQL** (or MySQL). When a row in `departments` is deleted or its primary key updated, the database must check the `employees` table to enforce referential integrity (`ON DELETE CASCADE` or `RESTRICT`). Without an index on `employees(dept_id)`, Postgres must perform a **full sequential scan** of the entire `employees` table while holding a restrictive table lock (`ShareRowExclusiveLock` or `RowShareLock`), blocking all concurrent modifications and causing severe deadlock cycles.

**Diagnostic Commands:**
1. Find unindexed foreign keys in PostgreSQL:
   ```sql
   SELECT c.conrelid::regclass AS table_name,
          string_agg(a.attname, ', ') AS fk_columns,
          c.conname
   FROM pg_constraint c
   JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
   WHERE c.contype = 'f'
     AND NOT EXISTS (
       SELECT 1 FROM pg_index i
       WHERE i.indrelid = c.conrelid
         AND c.conkey = i.indkey[0:array_length(c.conkey, 1) - 1]
     )
   GROUP BY c.conrelid, c.conname;
   ```

**Production Fix:**
Create an explicit index on all foreign key referencing columns:
```sql
CREATE INDEX CONCURRENTLY idx_employees_dept_id ON employees(dept_id);
```
With the index present, cascade deletes and integrity checks perform an instant index seek without locking the entire table.

</details>

---

### D3. Function-Wrapped Column Preventing B-Tree Index Scan

```sql
CREATE TABLE users (
    id serial PRIMARY KEY,
    email text,
    created_at timestamp
);

CREATE INDEX idx_users_email ON users(email);

-- Query executed by authentication service:
SELECT id, email FROM users WHERE LOWER(email) = 'john.doe@example.com';
```

**Observed symptom:** Query latency is 850ms on a table of 10 million users. EXPLAIN shows: 'Seq Scan on users (cost=0.00..284100.00 rows=50000)' instead of using idx_users_email.

**(a)** Why cannot a standard B-Tree index on `email` be used when the query wraps the column in `LOWER(email)`?

**(b)** What is an Expression / Functional Index in relational databases?

**(c)** What DDL statement creates the necessary functional index or column collation to enable index seeks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A standard B-Tree index on `email` stores the exact raw string bytes sorted in binary or collation order (e.g. `'John.Doe@example.com'`). When a query evaluates `WHERE LOWER(email) = ...`, the index does not contain precomputed lowercased values. The database cannot predict the mathematical behavior of arbitrary functions across index nodes and is forced to perform a full sequential scan of all 10 million rows, computing `LOWER()` on every single row.

**Diagnostic Commands:**
1. Run `EXPLAIN` to confirm sequential scan:
   ```sql
   EXPLAIN SELECT id FROM users WHERE LOWER(email) = 'john.doe@example.com';
   -- Filter: (lower(email) = 'john.doe@example.com'::text)
   -- Rows Removed by Filter: 9999999
   ```

**Production Fix:**
1. **Option A: Create an Expression Index:**
   ```sql
   CREATE INDEX CONCURRENTLY idx_users_lower_email ON users(LOWER(email));
   ```
   Now `WHERE LOWER(email) = '...'` performs an instant B-Tree Index Scan ($< 0.5	ext{ ms}$).
2. **Option B: Use `citext` (Case-Insensitive Text Type):**
   ```sql
   CREATE EXTENSION IF NOT EXISTS citext;
   ALTER TABLE users ALTER COLUMN email TYPE citext;
   CREATE INDEX idx_users_email ON users(email);
   ```
   Any query `WHERE email = 'John.Doe@example.com'` is automatically case-insensitive and uses the index natively.

</details>

---

### D4. Data Skew and Histogram Bucket Misestimation on Tenant Queries

```sql
-- Multi-tenant SaaS table
CREATE TABLE audit_logs (
    id bigserial PRIMARY KEY,
    tenant_id int,
    action text,
    created_at timestamp
);
-- Tenant 1 (Mega-Enterprise): 45,000,000 rows (90% of table)
-- Tenants 2 through 10,000 (Small clients): ~500 rows each

CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id);

-- Query executed for Tenant 1:
SELECT * FROM audit_logs WHERE tenant_id = 1 AND action = 'LOGIN';
```

**Observed symptom:** When querying tenant 1, Postgres chooses an Index Scan. The query performs 45,000,000 random disk seeks across the heap and takes 4 minutes, causing massive disk I/O thrashing.

**(a)** Why is an Index Scan dramatically worse than a Sequential Scan when retrieving 90% of a table?

**(b)** How do Most Common Values (MCV) lists and histogram bounds guide optimizer decisions?

**(c)** How can you increase statistics target (`default_statistics_target`) or use partial indexes for skewed tenants?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
An Index Scan visits the B-Tree index, retrieves physical tuple pointers (TIDs), and performs random I/O seeks into heap pages to fetch each row. When fetching 1% or less of a table, random seeks are efficient. But when fetching 45,000,000 rows (90% of the table), scanning the sequential table heap sequentially in 128KB disk blocks is orders of magnitude faster than 45 million random seeks. If the optimizer's statistics target was too low, it failed to recognize that `tenant_id = 1` represents 90% of all data, incorrectly estimating low rows and selecting an Index Scan.

**Diagnostic Commands:**
1. Inspect MCV (Most Common Values) in `pg_stats`:
   ```sql
   SELECT most_common_vals, most_common_freqs
   FROM pg_stats
   WHERE tablename = 'audit_logs' AND attname = 'tenant_id';
   ```
2. Verify if `tenant_id = 1` is correctly recognized in MCV.

**Production Fix:**
1. **Increase Statistics Target for the Skewed Column:**
   ```sql
   ALTER TABLE audit_logs ALTER COLUMN tenant_id SET STATISTICS 1000;
   ANALYZE audit_logs;
   ```
   This expands the MCV list from 100 to 1,000 entries and increases histogram resolution, allowing the CBO to select Sequential Scan or Bitmap Scan for tenant 1, and Index Scan for smaller tenants.
2. **Partial Indexing:**
   Index only the high-cardinality long-tail tenants:
   ```sql
   CREATE INDEX idx_audit_small_tenants ON audit_logs(tenant_id) WHERE tenant_id != 1;
   ```

</details>

---

### D5. Correlated Subquery Optimization Breakdown and Bitmap Scan Degeneracy

```sql
SELECT p.product_id, p.product_name,
       (SELECT avg(r.rating) 
        FROM reviews r 
        WHERE r.product_id = p.product_id 
          AND r.created_at >= CURRENT_DATE - INTERVAL '30 days') AS recent_rating
FROM products p
WHERE p.is_active = true;
```

**Observed symptom:** Query takes 3 minutes for 20,000 active products, even though `reviews` has an index on `(product_id, created_at)`. Database CPU runs at 100%.

**(a)** What is a correlated subquery, and why does executing it in the `SELECT` clause cause $O(N)$ query loops?

**(b)** How can you view the subplan execution counts in `EXPLAIN ANALYZE`?

**(c)** How should this query be rewritten using a `LEFT JOIN` with pre-aggregation or a Lateral Join?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A scalar subquery placed in the `SELECT` projection list that references outer table columns (`p.product_id`) is a **correlated subquery**. In many query engines, this executes as a `SubPlan`: for every single row returned from `products` (20,000 active products), the subquery is invoked independently 20,000 separate times. Even with an index, executing 20,000 individual index lookups and aggregation loops incurs severe execution overhead compared to a single set-based join.

**Diagnostic Commands:**
1. Run `EXPLAIN ANALYZE`:
   ```sql
   EXPLAIN ANALYZE SELECT ...;
   ```
   Look for: `SubPlan 1: SubPlan Loops: 20000`. The high loop count confirms row-by-row correlated execution.

**Production Fix:**
Rewrite the query as a set-based `LEFT JOIN` with a pre-aggregated Common Table Expression (CTE) or subquery:
```sql
SELECT p.product_id, p.product_name, r.recent_rating
FROM products p
LEFT JOIN (
    SELECT product_id, avg(rating) AS recent_rating
    FROM reviews
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY product_id
) r ON p.product_id = r.product_id
WHERE p.is_active = true;
```
Now both relations are scanned once and joined via a single Hash Join in **35ms** (a 5,000x speedup).

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

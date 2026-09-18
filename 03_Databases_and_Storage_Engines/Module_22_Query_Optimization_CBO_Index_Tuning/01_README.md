# Module 22: Query Optimization, Cost-Based Optimizer (CBO) & Physical Joins

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 22**. In this module, you will master the brain of the database management system: the **Query Optimizer**. You will explore how declarative SQL text is parsed into Relational Algebra, transformed by rule-based heuristics, evaluated by a mathematical **Cost-Based Optimizer (CBO)**, and executed using the 3 canonical physical join algorithms: **Nested Loop Join, Hash Join, and Sort-Merge Join**.

---

## 🧠 1. The Query Lifecycle: Declarative SQL to Physical Execution

SQL is declarative: it tells the database *what* data is desired, not *how* to physically retrieve it from disk:

```
                      ┌────────────────────────────┐
                      │ SQL Query Text             │
                      └─────────────┬──────────────┘
                                    │ 1. Parser & Lexer
                                    ▼
                      ┌────────────────────────────┐
                      │ Abstract Syntax Tree (AST) │
                      └─────────────┬──────────────┘
                                    │ 2. Catalog Binder / Semantic Analysis
                                    ▼
                      ┌────────────────────────────┐
                      │ Initial Logical Plan       │
                      │ (Relational Algebra Tree)  │
                      └─────────────┬──────────────┘
                                    │ 3. Rule-Based Optimizer (RBO)
                                    │    - Predicate Pushdown (Filter early)
                                    │    - Projection Pruning (Drop unused cols)
                                    ▼
                      ┌────────────────────────────┐
                      │ Optimized Logical Plan     │
                      └─────────────┬──────────────┘
                                    │ 4. Cost-Based Optimizer (CBO)
                                    │    - Enumerate Join Orders (Selinger DP)
                                    │    - Estimate Selectivity via Histograms
                                    │    - Calculate Disk I/O & CPU Cost
                                    ▼
                      ┌────────────────────────────┐
                      │ Best Physical Plan         │
                      │ (HashJoin, IndexScan, etc.)│
                      └─────────────┬──────────────┘
                                    │ 5. Execution Engine (Volcano / Vectorized)
                                    ▼
                      ┌────────────────────────────┐
                      │ Final Result Rows          │
                      └────────────────────────────┘
```

---

## 📐 2. Relational Algebra & Logical Rewrites

Relational algebra defines mathematical transformations over relations. The optimizer uses mathematical equivalences to rewrite plans into cheaper representations:

### Core Operators
- **Selection ($\sigma_p$)**: Filters rows matching predicate $p$ (`WHERE age > 30`).
- **Projection ($\pi_{a, b}$)**: Restricts output to specified columns $a, b$ (`SELECT id, name`).
- **Join ($\bowtie_c$)**: Combines two relations matching condition $c$.

### Crucial Rewrite Rules
1. **Predicate Pushdown**:
   $$\sigma_p(R \bowtie S) \equiv (\sigma_p(R)) \bowtie S$$
   Pushing filters *below* joins reduces the cardinality of intermediate tuples before the expensive join operator runs!
2. **Projection Pushdown / Column Pruning**:
   Discard unused columns at the storage scan layer to minimize memory consumption and cache pollution.
3. **Subquery Flattening**:
   Converts correlated subqueries (`WHERE id IN (SELECT ...)`) into Semi-Joins or Inner Joins, enabling join reordering algorithms to optimize them globally.

---

## 💰 3. The Cost-Based Optimizer (CBO) & Cost Model

The CBO evaluates multiple physical candidate plans and selects the one with the lowest estimated **Cost Score**. In PostgreSQL and Oracle, Cost represents a normalized unit of single sequential page read time:

$$\text{Total Cost} = (N_{\text{seq}} \cdot \text{seq\_cost}) + (N_{\text{rand}} \cdot \text{rand\_cost}) + (T \cdot \text{cpu\_tuple}) + (O \cdot \text{cpu\_operator})$$

### PostgreSQL Default Constants
- `seq_page_cost = 1.0` (Sequential 8KB page read)
- `random_page_cost = 4.0` (Random 8KB page read on HDD; typically lowered to `1.1` on NVMe SSDs)
- `cpu_tuple_cost = 0.01` (CPU cost to parse and evaluate one row)
- `cpu_operator_cost = 0.0025` (CPU cost per operator comparison, e.g. `<` or `=`)

### Statistics & Selectivity Estimation
To estimate the number of tuples ($T$) produced by an operator, the CBO inspects catalog tables (`pg_statistic`):
1. **Number of Distinct Values (NDV)**: If a column has 100 distinct values, equality selectivity $S \approx 1 / 100 = 0.01$.
2. **Most Common Values (MCV) & Frequencies**: Explicit frequencies for high-skew terms (e.g. `status = 'ACTIVE'` represents 92% of the table).
3. **Equi-Depth Histograms**: For range predicates (`amount > 500`), the histogram divides the distribution into bins of equal row counts to estimate the exact percentage of rows matched.

### The Join Ordering Problem & The Selinger Optimizer
For a query joining $N$ tables, there are $\frac{(2N-2)!}{(N-1)!}$ possible binary join trees. For 10 tables, that is **17,643,225 plans**!
- **Dynamic Programming (The Selinger 1979 Algorithm)**: Builds optimal 1-table access paths, combines them into optimal 2-table joins, then 3-table joins, pruning suboptimal sub-plans using the Principle of Optimality.
- **Genetic Query Optimizer (GEQO)**: Triggered when joins exceed `geqo_threshold` (default 12 tables) to avoid combinatorial explosion.

---

## ⚙️ 4. The Three Physical Join Algorithms

Every database engine relies on 3 primary algorithms to physically join two relations ($R$ and $S$):

| Join Algorithm | Time Complexity | Space Complexity | Requires Sorted? | Best Workload Condition |
| :--- | :--- | :--- | :--- | :--- |
| **Nested Loop Join** | $O(|R| \cdot |S|)$ | $O(1)$ | No | Tiny outer relation ($|R| \le 100$) with indexed inner relation ($O(|R| \log |S|)$) |
| **Hash Join** | $O(|R| + |S|)$ | $O(|R|)$ | No | Large unsorted relations with equality predicates (`R.id = S.id`) fitting in RAM |
| **Sort-Merge Join** | $O(|R| \log |R| + |S| \log |S|)$ | $O(1)$ | Yes | Both relations already sorted, or non-equi joins (`<`, `<=`) |

### 1. Nested Loop Join (NLJ)
```python
for r in Outer_Relation:
    for s in Inner_Relation:
        if r.key == s.key:
            yield (r, s)
```
- **Index Nested Loop Join**: If `Inner_Relation` has an index on `key`, the inner loop is replaced by an $O(\log |S|)$ B-Tree index lookup.

### 2. Hash Join (HJ)
1. **Build Phase**: The smaller relation is chosen as the build input. A hash table is built in memory mapping `join_key -> row(s)`.
2. **Probe Phase**: The larger relation streams sequentially, hashing its join key and probing the in-memory hash table for matches.
- If the build table exceeds `work_mem`, PostgreSQL spills partitions to disk (**Grace Hash Join**).

### 3. Sort-Merge Join (SMJ)
1. Both inputs are sorted on the join key.
2. Two pointers step through both relations simultaneously in a single linear pass. If both relations are pre-sorted (e.g., from an Index Scan), Sort-Merge Join runs in pure $O(|R| + |S|)$ with **zero auxiliary memory**!

---

## 🛠️ 5. Hands-On Lab: Building a Cost-Based Query Optimizer & Join Engine

In this lab, you will implement:
1. **Rule-Based Rewriter**: Apply predicate pushdown and column projection pruning to relational algebra trees.
2. **Catalog Statistics & Selectivity Estimator**: Compute selectivity using Uniform Distribution and Most Common Value (MCV) frequency tables.
3. **Cost-Based Plan Scorer**: Implement the exact cost formula evaluating sequential scans, index scans, and join costs.
4. **Physical Join Implementations**:
   - `nested_loop_join(outer, inner, condition)`
   - `hash_join(left, right, left_key, right_key)`
   - `sort_merge_join(left, right, left_key, right_key)`

---

## 📂 Project Structure
```
Module_22_Query_Optimization_CBO_Index_Tuning/
├── README.md
├── 01_query_optimizer_cbo_and_joins_demo.py
├── starter/
│   └── query_optimizer.py
└── project_solution/
    ├── query_optimizer.py
    └── test_query_optimizer.py
```

---
## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/query_optimizer.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | query_optimizer.py (CBO, System R join dynamic programming) | explain_live.py (psycopg2 EXPLAIN ANALYZE BUFFERS, index advisor) |
| **Verification** | `project_solution/test_query_optimizer.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Join Permutation Explosion: Dynamic programming join enumeration exploding exponentially ($O(3^N)$) on $>12$ joins.
2. Correlated Column Blindness: Multi-column filters assuming attribute independence, miscalculating selectivity by 1000x.
3. Non-Sargable Function Wrapping: Wrapping indexed columns in functions forcing the planner into full table scans.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT attempt to force specific index hints in production queries unless automated statistics and optimizer settings have failed and query regression is imminent.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_22_Query_Optimization_CBO_Index_Tuning -v

# Operational Diagnostics & Health Verification
psql -h localhost -U postgres -c "EXPLAIN (ANALYZE, COSTS, BUFFERS) SELECT ...;"
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_query_optimization.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.


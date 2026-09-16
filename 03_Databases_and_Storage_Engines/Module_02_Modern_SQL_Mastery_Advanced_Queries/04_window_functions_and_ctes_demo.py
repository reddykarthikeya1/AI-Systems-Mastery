"""Module 02: Window Functions, CTEs, and Recursive Hierarchies Demo.

Demonstrates:
1. Window Ranking: ROW_NUMBER(), RANK(), DENSE_RANK().
2. Running Aggregates: SUM(...) OVER (PARTITION BY ... ORDER BY ...).
3. Recursive CTE: Organization hierarchy traversal.
"""

import sqlite3

def run_demo():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY,
            salesperson TEXT,
            region TEXT,
            amount REAL,
            sale_date TEXT
        );

        INSERT INTO sales VALUES
            (1, 'Alice', 'North', 500.0, '2026-01-01'),
            (2, 'Bob', 'North', 300.0, '2026-01-02'),
            (3, 'Alice', 'North', 700.0, '2026-01-03'),
            (4, 'Charlie', 'South', 400.0, '2026-01-01'),
            (5, 'Diana', 'South', 600.0, '2026-01-02'),
            (6, 'Diana', 'South', 200.0, '2026-01-03');
    """)

    print("--- 1. WINDOW FUNCTIONS: Running Total and Department Ranking ---")
    cur.execute("""
        SELECT 
            salesperson,
            region,
            amount,
            SUM(amount) OVER (PARTITION BY region ORDER BY sale_date) AS running_region_total,
            DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rank_in_region
        FROM sales
        ORDER BY region, sale_date
    """)
    for row in cur.fetchall():
        print(f"  {row[0]:<8} | {row[1]:<6} | ${row[2]:<6} | Running: ${row[3]:<7} | Rank: {row[4]}")

    print("\n--- 2. RECURSIVE CTE: Manager-to-Report Tree Hierarchy ---")
    cur.executescript("""
        CREATE TABLE org_chart (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            manager_id INTEGER
        );
        INSERT INTO org_chart VALUES
            (1, 'CEO Elizabeth', NULL),
            (2, 'VP Frank', 1),
            (3, 'VP Grace', 1),
            (4, 'Director Hank', 2),
            (5, 'Engineer Ian', 4);
    """)

    cur.execute("""
        WITH RECURSIVE OrgHierarchy AS (
            SELECT emp_id, name, manager_id, 0 AS level, name AS path
            FROM org_chart
            WHERE manager_id IS NULL

            UNION ALL

            SELECT o.emp_id, o.name, o.manager_id, h.level + 1, h.path || ' -> ' || o.name
            FROM org_chart o
            JOIN OrgHierarchy h ON o.manager_id = h.emp_id
        )
        SELECT level, name, path FROM OrgHierarchy ORDER BY level, emp_id;
    """)
    for row in cur.fetchall():
        indent = "  " * (row[0] + 1)
        print(f"{indent}[L{row[0]}] {row[1]} ({row[2]})")

    conn.close()

if __name__ == "__main__":
    run_demo()

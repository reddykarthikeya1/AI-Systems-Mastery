from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# ----------------------------------------------------------------------
# 1. MODULE 02 DEMO SCRIPTS
# ----------------------------------------------------------------------
m02_dir = root / "Module_02_Modern_SQL_Mastery_Advanced_Queries"

m02_demo1 = '''"""Module 02: Advanced SQL Joins and Correlated Subqueries Demo.

Demonstrates:
1. Inner, Left Outer, Right Outer, and Full Outer Joins using in-memory SQLite.
2. Correlated Subqueries vs Self-Joins.
3. Anti-Joins using NOT EXISTS vs NOT IN (NULL hazard).
"""

import sqlite3

def run_demo():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL
        );
        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            dept_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        );

        INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Design'), (3, 'Marketing');
        INSERT INTO employees VALUES
            (101, 'Alice', 120000, 1),
            (102, 'Bob', 95000, 1),
            (103, 'Charlie', 88000, 2),
            (104, 'Diana', 110000, NULL);
    """)

    print("--- 1. LEFT OUTER JOIN: Employees without departments ---")
    cur.execute("""
        SELECT e.name, e.salary, COALESCE(d.dept_name, 'Unassigned') AS dept
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
    """)
    for row in cur.fetchall():
        print(f"  {row[0]:<10} | ${row[1]:<8} | {row[2]}")

    print("\\n--- 2. CORRELATED SUBQUERY: Employees earning above department average ---")
    cur.execute("""
        SELECT e.name, e.salary, e.dept_id
        FROM employees e
        WHERE e.salary > (
            SELECT AVG(salary)
            FROM employees e2
            WHERE e2.dept_id = e.dept_id
        )
    """)
    for row in cur.fetchall():
        print(f"  Above avg: {row[0]} (${row[1]}) in dept {row[2]}")

    print("\\n--- 3. ANTI-JOIN: Departments with NO employees ---")
    cur.execute("""
        SELECT d.dept_name
        FROM departments d
        WHERE NOT EXISTS (
            SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id
        )
    """)
    for row in cur.fetchall():
        print(f"  Empty Dept: {row[0]}")

    conn.close()

if __name__ == "__main__":
    run_demo()
'''

m02_demo2 = '''"""Module 02: Window Functions, CTEs, and Recursive Hierarchies Demo.

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

    print("\\n--- 2. RECURSIVE CTE: Manager-to-Report Tree Hierarchy ---")
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
'''

(m02_dir / "01_joins_and_subqueries_demo.py").write_text(m02_demo1, encoding="utf-8")
(m02_dir / "02_window_functions_and_ctes_demo.py").write_text(m02_demo2, encoding="utf-8")

# ----------------------------------------------------------------------
# 2. MODULE 03 DEMO SCRIPTS
# ----------------------------------------------------------------------
m03_dir = root / "Module_03_Embedded_Databases_SQLite_WAL"

m03_demo1 = '''"""Module 03: SQLite WAL Mode Benchmarking Demo.

Demonstrates:
1. Performance differences between ROLLBACK journal (DELETE) and Write-Ahead Logging (WAL).
2. Concurrency: Readers not blocking writers in WAL mode.
3. Synchronous pragma trade-offs: NORMAL vs FULL.
"""

import sqlite3
import tempfile
import time
from pathlib import Path

def benchmark_mode(journal_mode: str, num_inserts: int = 500) -> float:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / f"bench_{journal_mode}.db"
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute(f"PRAGMA journal_mode = {journal_mode};")
        cur.execute("PRAGMA synchronous = NORMAL;")
        cur.execute("CREATE TABLE bench_log (id INTEGER PRIMARY KEY, val TEXT, ts REAL);")
        conn.commit()

        start = time.perf_counter()
        for i in range(num_inserts):
            cur.execute("INSERT INTO bench_log (val, ts) VALUES (?, ?);", (f"record_{i}", time.time()))
            conn.commit()

        elapsed = time.perf_counter() - start
        conn.close()
        return elapsed

def run_demo():
    print("Benchmarking 500 individual committed INSERT transactions:")
    t_delete = benchmark_mode("DELETE", 300)
    print(f"  DELETE Journal Mode: {t_delete:.3f} s ({300/t_delete:.1f} txn/s)")

    t_wal = benchmark_mode("WAL", 300)
    print(f"  WAL Mode:            {t_wal:.3f} s ({300/t_wal:.1f} txn/s)")
    if t_wal > 0:
        print(f"  WAL Speedup:         {t_delete / t_wal:.2f}x faster!")

if __name__ == "__main__":
    run_demo()
'''

m03_demo2 = '''"""Module 03: Custom Python Aggregate & Scalar Functions in SQLite Demo.

Demonstrates:
1. create_function: Custom scalar hashing and distance functions.
2. create_aggregate: Custom stateful aggregators (geometric mean, standard deviation).
3. create_collation: Custom natural human sorting.
"""

import math
import sqlite3

class GeometricMean:
    def __init__(self):
        self.log_sum = 0.0
        self.count = 0

    def step(self, value):
        if value is not None and value > 0:
            self.log_sum += math.log(value)
            self.count += 1

    def finalize(self):
        if self.count == 0:
            return None
        return math.exp(self.log_sum / self.count)

def haversine_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0  # Earth radius km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def run_demo():
    conn = sqlite3.connect(":memory:")
    conn.create_function("haversine_km", 4, haversine_dist)
    conn.create_aggregate("geom_mean", 1, GeometricMean)

    cur = conn.cursor()
    cur.execute("SELECT haversine_km(40.7128, -74.0060, 51.5074, -0.1278) AS nyc_to_london;")
    dist = cur.fetchone()[0]
    print(f"Custom Scalar Function: NYC to London = {dist:.1f} km")

    cur.executescript("""
        CREATE TABLE growth_rates (company TEXT, multiplier REAL);
        INSERT INTO growth_rates VALUES ('A', 1.2), ('A', 1.5), ('A', 1.1), ('B', 2.0), ('B', 0.5);
    """)

    cur.execute("SELECT company, geom_mean(multiplier) FROM growth_rates GROUP BY company;")
    print("\\nCustom Aggregate Function (Geometric Mean):")
    for row in cur.fetchall():
        print(f"  Company {row[0]}: Geometric Mean Multiplier = {row[1]:.3f}")

    conn.close()

if __name__ == "__main__":
    run_demo()
'''

(m03_dir / "01_sqlite_wal_benchmarking_demo.py").write_text(m03_demo1, encoding="utf-8")
(m03_dir / "02_custom_python_sql_functions_demo.py").write_text(m03_demo2, encoding="utf-8")

# ----------------------------------------------------------------------
# 3. STARTERS FOR MODULES 01, 02, 03
# ----------------------------------------------------------------------
m01_starter = root / "Module_01_Storage_Theory_ACID_Relational_Model" / "starter"
m01_starter.mkdir(parents=True, exist_ok=True)
(m01_starter / "csv_engine_starter.py").write_text('''"""Module 01 Starter Skeleton: Transactional Flat-File CSV Engine.

Complete the TODO sections to implement BEGIN, COMMIT, ROLLBACK, and WAL Recovery.
"""

from __future__ import annotations
import csv
from pathlib import Path
from typing import Any

class TransactionalCSVEngineStarter:
    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)
        self.wal_path = self.data_path.with_suffix(".wal")
        self.in_transaction = False
        self.uncommitted_rows: list[dict[str, Any]] = []
        self._recover_wal()

    def _recover_wal(self) -> None:
        # TODO: Check if self.wal_path exists.
        # If it has a BEGIN and COMMIT, replay to CSV. If incomplete, discard.
        pass

    def begin(self) -> None:
        if self.in_transaction:
            raise RuntimeError("Transaction already in progress")
        self.in_transaction = True
        self.uncommitted_rows = []
        with open(self.wal_path, "a", encoding="utf-8") as f:
            f.write("BEGIN\\n")

    def insert(self, row: dict[str, Any]) -> None:
        if not self.in_transaction:
            raise RuntimeError("Must call begin() before insert()")
        self.uncommitted_rows.append(row)
        # TODO: Append ROW entry to WAL

    def commit(self) -> None:
        if not self.in_transaction:
            raise RuntimeError("No active transaction to commit")
        # TODO: Write COMMIT to WAL, flush uncommitted_rows to CSV, truncate WAL
        self.in_transaction = False

    def rollback(self) -> None:
        if not self.in_transaction:
            raise RuntimeError("No active transaction to rollback")
        # TODO: Truncate/remove WAL, clear uncommitted_rows
        self.in_transaction = False
''', encoding="utf-8")

m02_starter = root / "Module_02_Modern_SQL_Mastery_Advanced_Queries" / "starter"
m02_starter.mkdir(parents=True, exist_ok=True)
(m02_starter / "sql_mastery_starter.py").write_text('''"""Module 02 Starter Skeleton: Advanced SQL Queries.

Complete the query functions using sqlite3 in-memory database.
"""

import sqlite3

def get_top_earners_per_department(conn: sqlite3.Connection) -> list[tuple]:
    """TODO: Write a query using DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)

    to return the top 2 earners per department.
    """
    cur = conn.cursor()
    # TODO: Implement query
    return []

def calculate_monthly_running_totals(conn: sqlite3.Connection) -> list[tuple]:
    """TODO: Write a query using SUM(amount) OVER (ORDER BY sale_date)

    to compute the running total of sales.
    """
    cur = conn.cursor()
    # TODO: Implement query
    return []
''', encoding="utf-8")

m03_starter = root / "Module_03_Embedded_Databases_SQLite_WAL" / "starter"
m03_starter.mkdir(parents=True, exist_ok=True)
(m03_starter / "sqlite_wal_starter.py").write_text('''"""Module 03 Starter Skeleton: Embedded SQLite WAL & Custom Functions.

Complete the implementation of WAL configuration and custom Python functions.
"""

import sqlite3

def configure_production_wal(conn: sqlite3.Connection) -> dict[str, str]:
    """TODO: Set PRAGMA journal_mode = WAL, synchronous = NORMAL, cache_size = -64000.

    Return a dictionary of the resulting pragmas.
    """
    cur = conn.cursor()
    # TODO: Execute pragmas
    return {}

def register_custom_collations(conn: sqlite3.Connection) -> None:
    """TODO: Register a case-insensitive, whitespace-trimmed natural collation."""
    pass
''', encoding="utf-8")

print("Demos and starters built successfully.")

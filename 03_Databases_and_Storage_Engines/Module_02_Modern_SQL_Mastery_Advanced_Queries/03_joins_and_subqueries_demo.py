"""Module 02: Advanced SQL Joins and Correlated Subqueries Demo.

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

    print("\n--- 2. CORRELATED SUBQUERY: Employees earning above department average ---")
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

    print("\n--- 3. ANTI-JOIN: Departments with NO employees ---")
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

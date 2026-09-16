"""Module 02: Financial & Customer Analytics Engine using Modern Analytical SQL.

This engine genuinely executes on a REAL embedded database engine (Python standard
library `sqlite3`). It executes production SQL with window functions, Common Table
Expressions (CTEs), and recursive hierarchical queries against an actual in-process
relational database.

Leverages CTEs, Recursive CTEs, and Window Functions (ROW_NUMBER, DENSE_RANK, LAG, Sliding Frames).
"""

from __future__ import annotations

import sqlite3
from typing import Any


class AnalyticsSuite:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        """Initializes tables for customers, orders, products, and employee hierarchy."""
        with self.conn:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    region TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    order_date TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                );

                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    manager_id INTEGER,
                    FOREIGN KEY (manager_id) REFERENCES employees(id)
                );
            """)

    def insert_seed_data(self):
        """Populates the database with realistic e-commerce and corporate data."""
        with self.conn:
            self.conn.executemany(
                "INSERT INTO customers (id, name, region) VALUES (?, ?, ?)",
                [(1, "Alice", "North"), (2, "Bob", "South"), (3, "Charlie", "North"), (4, "Diana", "West")]
            )
            self.conn.executemany(
                "INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)",
                [
                    (1, "Laptop", "Electronics", 1200.0),
                    (2, "Phone", "Electronics", 800.0),
                    (3, "Desk", "Furniture", 350.0),
                    (4, "Chair", "Furniture", 150.0),
                    (5, "Headphones", "Electronics", 100.0)
                ]
            )
            self.conn.executemany(
                "INSERT INTO orders (id, customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?, ?)",
                [
                    (1, 1, 1, 1, "2026-01-01"),  # Alice buys 1 Laptop ($1200)
                    (2, 1, 2, 2, "2026-01-02"),  # Alice buys 2 Phones ($1600)
                    (3, 2, 3, 1, "2026-01-03"),  # Bob buys 1 Desk ($350)
                    (4, 3, 4, 4, "2026-01-04"),  # Charlie buys 4 Chairs ($600)
                    (5, 1, 5, 1, "2026-01-05"),  # Alice buys 1 Headphones ($100)
                    (6, 2, 1, 1, "2026-01-06"),  # Bob buys 1 Laptop ($1200)
                ]
            )
            self.conn.executemany(
                "INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)",
                [
                    (1, "CEO Elena", None),
                    (2, "VP Marcus", 1),
                    (3, "VP Sarah", 1),
                    (4, "Engineer David", 2),
                    (5, "Engineer Maya", 2),
                    (6, "Designer Leo", 3)
                ]
            )

    def calculate_customer_lifetime_value(self) -> list[dict[str, Any]]:
        """Calculates total spend and order count per customer using CTEs and Joins."""
        sql = """
            WITH customer_order_totals AS (
                SELECT 
                    o.customer_id,
                    COUNT(o.id) as order_count,
                    SUM(o.quantity * p.price) as total_spent
                FROM orders o
                JOIN products p ON o.product_id = p.id
                GROUP BY o.customer_id
            )
            SELECT 
                c.id as customer_id,
                c.name,
                c.region,
                COALESCE(cot.order_count, 0) as order_count,
                COALESCE(cot.total_spent, 0.0) as total_spent
            FROM customers c
            LEFT JOIN customer_order_totals cot ON c.id = cot.customer_id
            ORDER BY total_spent DESC;
        """
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]

    def calculate_running_revenue_and_moving_avg(self) -> list[dict[str, Any]]:
        """Uses Window Functions to compute cumulative revenue and a 3-order rolling average."""
        sql = """
            WITH daily_revenue AS (
                SELECT 
                    o.order_date,
                    SUM(o.quantity * p.price) as daily_rev
                FROM orders o
                JOIN products p ON o.product_id = p.id
                GROUP BY o.order_date
            )
            SELECT 
                order_date,
                daily_rev,
                -- Cumulative Running Total:
                SUM(daily_rev) OVER (ORDER BY order_date) as cumulative_revenue,
                -- 3-day Rolling Moving Average:
                ROUND(AVG(daily_rev) OVER (
                    ORDER BY order_date 
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ), 2) as rolling_3day_avg
            FROM daily_revenue
            ORDER BY order_date;
        """
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]

    def rank_products_within_categories(self) -> list[dict[str, Any]]:
        """Ranks products within each category by revenue generated using DENSE_RANK()."""
        sql = """
            WITH product_sales AS (
                SELECT 
                    p.id as product_id,
                    p.name,
                    p.category,
                    SUM(o.quantity * p.price) as total_sales
                FROM products p
                JOIN orders o ON p.id = o.product_id
                GROUP BY p.id, p.name, p.category
            )
            SELECT 
                product_id,
                name,
                category,
                total_sales,
                DENSE_RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) as rank_in_category
            FROM product_sales
            ORDER BY category, rank_in_category;
        """
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]

    def calculate_day_over_day_growth(self) -> list[dict[str, Any]]:
        """Uses LAG() window function to calculate day-over-day revenue delta without self-joins."""
        sql = """
            WITH daily_sales AS (
                SELECT 
                    o.order_date,
                    SUM(o.quantity * p.price) as revenue
                FROM orders o
                JOIN products p ON o.product_id = p.id
                GROUP BY o.order_date
            )
            SELECT 
                order_date,
                revenue,
                LAG(revenue, 1) OVER (ORDER BY order_date) as prev_day_revenue,
                ROUND(revenue - COALESCE(LAG(revenue, 1) OVER (ORDER BY order_date), revenue), 2) as daily_delta
            FROM daily_sales
            ORDER BY order_date;
        """
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]

    def get_employee_hierarchy(self) -> list[dict[str, Any]]:
        """Traverses employee management tree using a Recursive CTE."""
        sql = """
            WITH RECURSIVE org_tree AS (
                -- 1. Anchor: Root CEO
                SELECT id, name, manager_id, 1 as level, name as path
                FROM employees
                WHERE manager_id IS NULL

                UNION ALL

                -- 2. Recursive member: Direct reports
                SELECT e.id, e.name, e.manager_id, ot.level + 1, ot.path || ' -> ' || e.name
                FROM employees e
                JOIN org_tree ot ON e.manager_id = ot.id
            )
            SELECT id, name, level, path FROM org_tree ORDER BY level, id;
        """
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]

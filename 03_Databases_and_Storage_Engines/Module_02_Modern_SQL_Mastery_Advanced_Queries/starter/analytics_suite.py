"""Module 02 Starter Skeleton: Analytical SQL Suite.

Complete the analytical query methods using window functions, CTEs, and recursive CTEs.
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
                    (1, 1, 1, 1, "2026-01-01"),
                    (2, 1, 2, 2, "2026-01-02"),
                    (3, 2, 3, 1, "2026-01-03"),
                    (4, 3, 4, 4, "2026-01-04"),
                    (5, 1, 5, 1, "2026-01-05"),
                    (6, 2, 1, 1, "2026-01-06"),
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
        raise NotImplementedError("TODO: Implement calculate_customer_lifetime_value")

    def calculate_running_revenue_and_moving_avg(self) -> list[dict[str, Any]]:
        raise NotImplementedError("TODO: Implement calculate_running_revenue_and_moving_avg")

    def rank_products_within_categories(self) -> list[dict[str, Any]]:
        raise NotImplementedError("TODO: Implement rank_products_within_categories")

    def calculate_day_over_day_growth(self) -> list[dict[str, Any]]:
        raise NotImplementedError("TODO: Implement calculate_day_over_day_growth")

    def get_employee_hierarchy(self) -> list[dict[str, Any]]:
        raise NotImplementedError("TODO: Implement get_employee_hierarchy")

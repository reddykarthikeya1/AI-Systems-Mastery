"""Module 02 Starter Skeleton: Advanced SQL Queries.

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

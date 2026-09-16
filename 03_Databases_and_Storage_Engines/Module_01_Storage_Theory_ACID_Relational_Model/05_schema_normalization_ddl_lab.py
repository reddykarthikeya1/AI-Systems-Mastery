"""Module 01: Interactive Normalization & DDL Design Lab.

Demonstrates the 3 Classic Data Anomalies (Insertion, Deletion, Update) on flat unnormalized
data, then constructs an enterprise 3NF relational schema in SQLite enforcing ACID foreign keys.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List


def demonstrate_flat_data_anomalies() -> None:
    print("=" * 80)
    print(" PART 1: THE 3 ANOMALIES OF UNNORMALIZED FLAT STORAGE")
    print("=" * 80)

    # Simulated flat spreadsheet records
    flat_table: List[Dict[str, Any]] = [
        {"order_id": 101, "cust_name": "Alice Smith", "cust_city": "Austin", "item": "Laptop", "price": 1200.0},
        {"order_id": 101, "cust_name": "Alice Smith", "cust_city": "Austin", "item": "Mouse", "price": 25.0},
        {"order_id": 102, "cust_name": "Bob Jones", "cust_city": "Seattle", "item": "Keyboard", "price": 80.0},
    ]

    print("\n--- 1. The Update Anomaly ---")
    print(" Alice moves from Austin to New York. The application updates only the first matching record:")
    # Bug: only row 0 is updated, row 1 is missed
    flat_table[0]["cust_city"] = "New York"
    print(f" Record 1: Alice's City = '{flat_table[0]['cust_city']}'")
    print(f" Record 2: Alice's City = '{flat_table[1]['cust_city']}'")
    print(" [CORRUPTION DETECTED] Database is now in an inconsistent split-brain state for Alice!\n")

    print("--- 2. The Deletion Anomaly ---")
    print(" Bob cancels Order #102. The application deletes the row:")
    cancelled_order = [row for row in flat_table if row["order_id"] != 102]
    print(f" Remaining rows: {len(cancelled_order)}")
    # Check if Keyboard product catalog metadata was lost
    has_keyboard = any(row["item"] == "Keyboard" for row in cancelled_order)
    print(f" Does the store still have product info for 'Keyboard'? {has_keyboard}")
    print(" [DATA LOSS DETECTED] Deleting an order accidentally destroyed product catalog history!\n")

    print("--- 3. The Insertion Anomaly ---")
    print(" Store wants to stock a brand-new product ('Monitor', $350) before anyone has bought it.")
    print(" In flat storage, how do you insert it when 'order_id' and 'cust_name' are required?")
    print(" You are forced to insert fake/null order data: {'order_id': NULL, 'cust_name': 'DUMMY', ...}")
    print(" [POLLUTION DETECTED] Database schema cannot represent entities independently!\n")


def demonstrate_3nf_relational_ddl() -> None:
    print("=" * 80)
    print(" PART 2: CONSTRUCTING THE 3NF RELATIONAL SCHEMA WITH FOREIGN KEYS")
    print("=" * 80)

    # Use in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce relational referential integrity!
    cursor = conn.cursor()

    # Step 1: Create normalized 3NF tables
    ddl_script = """
    -- 1. Customers Table (Independent Entity)
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );

    -- 2. Products Table (Independent Entity)
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK(price >= 0)
    );

    -- 3. Orders Table (Header Relationship)
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
    );

    -- 4. Order Items Table (M:N Intersection Entity in 3NF)
    CREATE TABLE order_items (
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price REAL NOT NULL CHECK(unit_price >= 0),
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """
    cursor.executescript(ddl_script)
    print(" [DDL SUCCESS] Created 4 normalized 3NF tables with foreign key constraints.")

    # Step 2: Populate independent entities (Solves Insertion Anomaly!)
    cursor.execute("INSERT INTO customers (name, city) VALUES ('Alice Smith', 'Austin');")
    cursor.execute("INSERT INTO customers (name, city) VALUES ('Bob Jones', 'Seattle');")
    
    # Notice: We can add the new 'Monitor' without any order!
    cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 1200.0);")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Mouse', 25.0);")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Keyboard', 80.0);")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Monitor', 350.0);")  # Added independently!

    print(" [INSERTION ANOMALY SOLVED] 'Monitor' product catalog created with zero orders.")

    # Step 3: Insert balanced orders
    cursor.execute("INSERT INTO orders (order_id, customer_id, order_date) VALUES (101, 1, '2026-09-08');")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (101, 1, 1, 1200.0);")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (101, 2, 2, 25.0);")

    cursor.execute("INSERT INTO orders (order_id, customer_id, order_date) VALUES (102, 2, '2026-09-08');")
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (102, 3, 1, 80.0);")

    # Step 4: Test Foreign Key Invariant (Preventing Corruption)
    print("\n Attempting to insert an order item for non-existent product ID 999...")
    try:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (101, 999, 1, 50.0);")
    except sqlite3.IntegrityError as e:
        print(f" [INTEGRITY GUARD] Database REJECTED invalid insertion: '{e}'")

    # Step 5: Test Update Anomaly Resolution
    print("\n Updating Alice's city from Austin to New York in the single Customers table:")
    cursor.execute("UPDATE customers SET city = 'New York' WHERE customer_id = 1;")
    print(" [UPDATE ANOMALY SOLVED] Updated 1 single row. All orders now automatically reflect New York.")

    # Step 6: Query Reconstituted Invoice via Relational JOIN
    query = """
    SELECT 
        o.order_id,
        c.name AS customer,
        c.city,
        p.name AS product,
        oi.quantity,
        oi.unit_price,
        (oi.quantity * oi.unit_price) AS line_total
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    ORDER BY o.order_id, p.name;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\n--- RECONSTITUTED INVOICE REPORT (Via Relational 3NF SQL JOIN) ---")
    print(f" {'Order':<6} | {'Customer':<12} | {'City':<10} | {'Product':<10} | {'Qty':<4} | {'Unit':<8} | {'Total':<8}")
    print(" " + "-" * 75)
    for r in rows:
        print(f" {r[0]:<6} | {r[1]:<12} | {r[2]:<10} | {r[3]:<10} | {r[4]:<4} | ${r[5]:<7.2f} | ${r[6]:<7.2f}")

    conn.close()
    print("\n" + "=" * 80)
    print(" LAB COMPLETE: 3NF RELATIONAL MODEL GUARANTEES ZERO DATA ANOMALIES!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_flat_data_anomalies()
    demonstrate_3nf_relational_ddl()

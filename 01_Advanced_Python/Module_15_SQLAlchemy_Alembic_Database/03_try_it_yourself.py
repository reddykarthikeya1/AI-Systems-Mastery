"""
Module 15: Interactive SQLite Database Sandbox
Run: python try_it_yourself.py
"""

import sqlite3


def main():
    print("=" * 60)
    print("  MODULE 15: DATABASE PERSISTENCE PLAYGROUND [*]")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    sample_items = [("Keyboard", 79.99), ("Mouse", 29.50), ("Monitor", 249.00)]
    cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_items)
    conn.commit()

    print(f"Inserted {len(sample_items)} items into SQLite table.")
    print("\nQuerying products priced above $50.00:")
    cursor.execute("SELECT id, name, price FROM products WHERE price > 50.00")
    for row in cursor.fetchall():
        print(f"  Item #{row[0]}: {row[1]} - ${row[2]:.2f}")

    conn.close()
    print("\n[OK] Database query and transaction executed successfully!")


if __name__ == "__main__":
    main()

"""Chapter 12 - SQL and database internals (sqlite3).

1. top_customers: aggregate query. Tables: customers(id, name), orders(id, customer_id, amount).
2. add_index_for_events: make `SELECT * FROM events WHERE user_id = ?` use an index.
3. transfer (debugging): a failed transfer leaves money missing.
"""

BUGGY = {
    "transfer": '''def transfer(conn, src, dst, amount):
    """Move `amount` between rows of acct(id, bal). Atomic: if the destination does not exist (KeyError) or the
    source would go negative (ValueError), the database must be unchanged."""
    conn.execute("UPDATE acct SET bal = bal - ? WHERE id = ?", (amount, src))
    conn.commit()
    cur = conn.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amount, dst))
    if cur.rowcount != 1:
        raise KeyError(dst)
    conn.commit()''',
}


def top_customers(conn, n):
    """Return up to n (name, total_spent) rows for customers that have orders, highest total first, ties by name."""
    return conn.execute(
        "SELECT c.name, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.id "
        "GROUP BY c.id ORDER BY total DESC, c.name ASC LIMIT ?", (n,)).fetchall()


def add_index_for_events(conn):
    """Create whatever index makes `SELECT * FROM events WHERE user_id = ?` avoid a full scan (table events(id, user_id, kind)).
    Return the EXPLAIN QUERY PLAN detail text of that query."""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id)")
    rows = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = ?", (1,)).fetchall()
    return " ".join(r[-1] for r in rows)


def transfer(conn, src, dst, amount):
    """Move `amount` between rows of acct(id, bal). Atomic: if the destination does not exist (KeyError) or the
    source would go negative (ValueError), the database must be unchanged."""
    with conn:
        cur = conn.execute("UPDATE acct SET bal = bal - ? WHERE id = ? AND bal >= ?", (amount, src, amount))
        if cur.rowcount != 1:
            raise ValueError("insufficient funds or unknown source")
        cur = conn.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amount, dst))
        if cur.rowcount != 1:
            raise KeyError(dst)


def _db():
    import sqlite3
    return sqlite3.connect(":memory:")


def t_top_customers_ordering(m):
    c = _db()
    c.executescript("""CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INT, amount INT);
        INSERT INTO customers VALUES (1,'bo'),(2,'al'),(3,'cy'),(4,'none');
        INSERT INTO orders(customer_id, amount) VALUES (1,10),(1,5),(2,15),(3,7);""")
    assert m.top_customers(c, 2) == [("al", 15), ("bo", 15)]
    assert [r[0] for r in m.top_customers(c, 10)] == ["al", "bo", "cy"]


def t_top_customers_does_not_double_count(m):
    c = _db()
    c.executescript("""CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INT, amount INT);
        INSERT INTO customers VALUES (1,'same'),(2,'same');
        INSERT INTO orders(customer_id, amount) VALUES (1,1),(2,2);""")
    assert sorted(m.top_customers(c, 5)) == [("same", 1), ("same", 2)]


def t_index_used(m):
    c = _db()
    c.execute("CREATE TABLE events(id INTEGER PRIMARY KEY, user_id INT, kind TEXT)")
    c.executemany("INSERT INTO events(user_id, kind) VALUES (?, 'x')", [(i % 50,) for i in range(1000)])
    plan = m.add_index_for_events(c)
    assert "USING" in plan and "INDEX" in plan and "SCAN" not in plan.replace("SEARCH", "")


def t_transfer_is_atomic(m):
    c = _db()
    c.execute("CREATE TABLE acct(id INTEGER PRIMARY KEY, bal INT)")
    c.executemany("INSERT INTO acct VALUES (?, ?)", [(1, 100), (2, 0)])
    c.commit()
    m.transfer(c, 1, 2, 30)
    assert c.execute("SELECT id, bal FROM acct ORDER BY id").fetchall() == [(1, 70), (2, 30)]
    try:
        m.transfer(c, 1, 99, 10)
    except KeyError:
        pass
    else:
        raise AssertionError("unknown destination must raise KeyError")
    assert c.execute("SELECT bal FROM acct WHERE id = 1").fetchone() == (70,)
    try:
        m.transfer(c, 1, 2, 1000)
    except ValueError:
        pass
    else:
        raise AssertionError("overdraft must raise ValueError")
    assert c.execute("SELECT id, bal FROM acct ORDER BY id").fetchall() == [(1, 70), (2, 30)]

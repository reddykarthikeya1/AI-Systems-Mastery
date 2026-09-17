"""Tests for Module 06: Real MySQL & InnoDB Storage Engine (Track B)."""

from __future__ import annotations

import threading
import time
import pytest

def _mysql_is_up() -> bool:
    try:
        from mysql_live import MySQLLiveClient
        client = MySQLLiveClient()
        return client.ping()
    except Exception:
        return False

requires_mysql = pytest.mark.skipif(
    not _mysql_is_up(),
    reason="MySQL not reachable on localhost:13306 - start with: make up mysql"
)

pytestmark = [pytest.mark.requires_mysql, requires_mysql]


def test_mysql_live_ping():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    assert client.ping() is True


def test_innodb_clustered_index_primary_lookup():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    client.setup_innodb_tables()

    conn = client.get_connection()
    with conn.cursor() as cur:
        cur.execute("REPLACE INTO innodb_users (user_id, email, score) VALUES (1, 'alice@example.com', 95);")
        conn.commit()

        # Primary key lookup hits the Clustered Index directly
        cur.execute("EXPLAIN SELECT * FROM innodb_users WHERE user_id = 1;")
        plan = cur.fetchone()
        assert plan["type"] == "const"
        assert plan["key"] == "PRIMARY"
    conn.close()


def test_innodb_secondary_index_bookmark_lookup():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    client.setup_innodb_tables()

    conn = client.get_connection()
    with conn.cursor() as cur:
        cur.execute("REPLACE INTO innodb_users (user_id, email, score) VALUES (2, 'bob@example.com', 88);")
        conn.commit()

        # Secondary index lookup uses idx_score, then bookmarks into PRIMARY
        cur.execute("EXPLAIN SELECT * FROM innodb_users WHERE score = 88;")
        plan = cur.fetchone()
        assert plan["key"] == "idx_score"
    conn.close()


def test_innodb_row_locking_deadlock_detection():
    from mysql_live import MySQLLiveClient
    import pymysql
    client = MySQLLiveClient()
    client.setup_innodb_tables()

    conn = client.get_connection()
    with conn.cursor() as cur:
        cur.execute("REPLACE INTO innodb_users (user_id, email, score) VALUES (10, 'u10@ex.com', 10), (20, 'u20@ex.com', 20);")
        conn.commit()
    conn.close()

    conn1 = client.get_connection()
    conn2 = client.get_connection()

    deadlock_happened = False

    def t1():
        nonlocal deadlock_happened
        try:
            with conn1.cursor() as cur:
                cur.execute("UPDATE innodb_users SET score = score + 1 WHERE user_id = 10;")
                time.sleep(0.1)
                cur.execute("UPDATE innodb_users SET score = score + 1 WHERE user_id = 20;")
                conn1.commit()
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1213:  # ER_LOCK_DEADLOCK
                deadlock_happened = True
                conn1.rollback()

    def t2():
        nonlocal deadlock_happened
        try:
            with conn2.cursor() as cur:
                cur.execute("UPDATE innodb_users SET score = score + 1 WHERE user_id = 20;")
                time.sleep(0.1)
                cur.execute("UPDATE innodb_users SET score = score + 1 WHERE user_id = 10;")
                conn2.commit()
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1213:
                deadlock_happened = True
                conn2.rollback()

    th1 = threading.Thread(target=t1)
    th2 = threading.Thread(target=t2)
    th1.start()
    th2.start()
    th1.join()
    th2.join()

    assert deadlock_happened is True
    conn1.close()
    conn2.close()


def test_innodb_status_deadlock_section():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    section = client.get_innodb_status_deadlock_section()
    assert isinstance(section, str)


def test_mysql_binlog_status_and_format():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    conn = client.get_connection()
    with conn.cursor() as cur:
        cur.execute("SHOW VARIABLES LIKE 'binlog_format';")
        res = cur.fetchone()
        assert res is not None
        assert res["Value"].upper() in ("ROW", "MIXED", "STATEMENT")
    conn.close()


def test_innodb_foreign_key_cascade():
    from mysql_live import MySQLLiveClient
    client = MySQLLiveClient()
    conn = client.get_connection()
    with conn.cursor() as cur:
        # pymysql sends ONE statement per execute() unless CLIENT.MULTI_STATEMENTS
        # is enabled - which it deliberately is not, because multi-statement
        # execution is a SQL-injection amplifier. One statement per call.
        cur.execute("DROP TABLE IF EXISTS child;")     # child first: FK ordering
        cur.execute("DROP TABLE IF EXISTS parent;")
        cur.execute("""
            CREATE TABLE parent (
                id INT PRIMARY KEY
            ) ENGINE=InnoDB;
        """)
        cur.execute("""
            CREATE TABLE child (
                id INT PRIMARY KEY,
                parent_id INT,
                FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)
        cur.execute("INSERT INTO parent VALUES (1);")
        cur.execute("INSERT INTO child VALUES (10, 1);")
        conn.commit()

        # Delete from parent -> cascades to child
        cur.execute("DELETE FROM parent WHERE id = 1;")
        conn.commit()

        cur.execute("SELECT count(*) AS cnt FROM child WHERE id = 10;")
        assert cur.fetchone()["cnt"] == 0
    conn.close()


def test_track_a_innodb_model_reconciliation():
    """Track A <-> Track B: Handbuilt InnoDBClusteredTable vs real MySQL InnoDB indexes."""
    from innodb_engine import InnoDBClusteredTable

    # Model
    model = InnoDBClusteredTable(table_name="users", primary_key="user_id")
    model.create_secondary_index("email")
    model.insert({"user_id": 100, "email": "reconcile@ex.com", "score": 500})

    # Clustered Index point lookup
    row_pk = model.get_by_primary_key(100)
    assert row_pk is not None and row_pk["email"] == "reconcile@ex.com"

    # Secondary index lookup. Returns (row, was_covering_index) - the second
    # value is the lesson: InnoDB secondary leaves store only
    # (indexed_column, primary_key), so anything else needs a second traversal
    # of the clustered index (a "bookmark lookup").
    row_sec, covering = model.get_by_secondary_index("email", "reconcile@ex.com")
    assert row_sec is not None and row_sec["user_id"] == 100
    assert covering is False, "fetching 'score' cannot be served by the index alone"

    # Projecting only what the index already holds IS covered - no bookmark
    # lookup, which is why covering indexes are worth designing for.
    covered_row, covering = model.get_by_secondary_index(
        "email", "reconcile@ex.com", projected_columns=["email", "user_id"]
    )
    assert covered_row == {"email": "reconcile@ex.com", "user_id": 100}
    assert covering is True, "a projection inside the index must avoid the clustered lookup"

"""Tests for Module 23: ANSI SQL Isolation Levels & Deadlocks (Track B)."""

from __future__ import annotations

import threading
import time

import pytest


def _postgres_is_up() -> bool:
    try:
        from isolation_live import IsolationLiveClient
        client = IsolationLiveClient()
        return client.ping()
    except Exception:
        return False

requires_postgres = pytest.mark.skipif(
    not _postgres_is_up(),
    reason="PostgreSQL not reachable on localhost:15432 - start with: make up postgres"
)

pytestmark = [pytest.mark.requires_postgres, requires_postgres]


def test_isolation_live_ping():
    from isolation_live import IsolationLiveClient
    client = IsolationLiveClient()
    assert client.ping() is True


def test_read_committed_observes_non_repeatable_read():
    from isolation_live import IsolationLiveClient
    client = IsolationLiveClient()
    tbl = "iso_nr_test"
    client.setup_bank_accounts(tbl)

    conn_writer = client.get_connection("READ COMMITTED")
    with conn_writer.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'Alice', 100.0);")
        conn_writer.commit()

    conn_reader = client.get_connection("READ COMMITTED")
    with conn_reader.cursor() as cur_r:
        cur_r.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        val1 = float(cur_r.fetchone()[0])
        assert val1 == 100.0

        # Writer commits an update mid-reader transaction
        with conn_writer.cursor() as cur_w:
            cur_w.execute(f"UPDATE {tbl} SET balance = 250.0 WHERE id = 1;")
            conn_writer.commit()

        # Under READ COMMITTED, reader re-reads the modified committed value (Non-Repeatable Read!)
        cur_r.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        val2 = float(cur_r.fetchone()[0])
        assert val2 == 250.0

    conn_reader.close()
    conn_writer.close()


def test_repeatable_read_prevents_non_repeatable_read():
    from isolation_live import IsolationLiveClient
    client = IsolationLiveClient()
    tbl = "iso_rr_test"
    client.setup_bank_accounts(tbl)

    conn_writer = client.get_connection("READ COMMITTED")
    with conn_writer.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'Alice', 100.0);")
        conn_writer.commit()

    conn_reader = client.get_connection("REPEATABLE READ")
    with conn_reader.cursor() as cur_r:
        cur_r.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        val1 = float(cur_r.fetchone()[0])
        assert val1 == 100.0

        # Writer commits an update mid-reader transaction
        with conn_writer.cursor() as cur_w:
            cur_w.execute(f"UPDATE {tbl} SET balance = 250.0 WHERE id = 1;")
            conn_writer.commit()

        # Under REPEATABLE READ, reader MUST see original snapshot balance (100.0)!
        cur_r.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        val2 = float(cur_r.fetchone()[0])
        assert val2 == 100.0

    conn_reader.close()
    conn_writer.close()


def test_repeatable_read_prevents_phantom_reads():
    from isolation_live import IsolationLiveClient
    client = IsolationLiveClient()
    tbl = "iso_phantom_test"
    client.setup_bank_accounts(tbl)

    conn_writer = client.get_connection("READ COMMITTED")
    with conn_writer.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'Alice', 500.0);")
        conn_writer.commit()

    conn_reader = client.get_connection("REPEATABLE READ")
    with conn_reader.cursor() as cur_r:
        cur_r.execute(f"SELECT count(*) FROM {tbl} WHERE balance > 200.0;")
        cnt1 = cur_r.fetchone()[0]
        assert cnt1 == 1

        # Writer inserts new row matching the range predicate and commits
        with conn_writer.cursor() as cur_w:
            cur_w.execute(f"INSERT INTO {tbl} VALUES (2, 'Bob', 600.0);")
            conn_writer.commit()

        # Under PostgreSQL REPEATABLE READ, count must still be 1 (Phantoms prevented)
        cur_r.execute(f"SELECT count(*) FROM {tbl} WHERE balance > 200.0;")
        cnt2 = cur_r.fetchone()[0]
        assert cnt2 == 1

    conn_reader.close()
    conn_writer.close()


def test_write_skew_anomaly_under_repeatable_read():
    """Demonstrates write skew: Both doctors see 2 on-call, both take leave, resulting in 0 on-call!"""
    from isolation_live import IsolationLiveClient
    client = IsolationLiveClient()
    tbl = "iso_doctors_skew"
    client.setup_oncall_doctors(tbl)

    conn_init = client.get_connection("READ COMMITTED")
    with conn_init.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'Alice', true), (2, 'Bob', true);")
        conn_init.commit()
    conn_init.close()

    conn1 = client.get_connection("REPEATABLE READ")
    conn2 = client.get_connection("REPEATABLE READ")

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    # Both read total on-call doctors
    cur1.execute(f"SELECT count(*) FROM {tbl} WHERE on_call = true;")
    assert cur1.fetchone()[0] == 2

    cur2.execute(f"SELECT count(*) FROM {tbl} WHERE on_call = true;")
    assert cur2.fetchone()[0] == 2

    # Both decide to go off-call since count >= 2
    cur1.execute(f"UPDATE {tbl} SET on_call = false WHERE id = 1;")
    cur2.execute(f"UPDATE {tbl} SET on_call = false WHERE id = 2;")

    conn1.commit()
    conn2.commit()  # Under REPEATABLE READ this commits without error (Write Skew anomaly!)

    # Anomaly realized: 0 doctors on-call!
    conn_check = client.get_connection("READ COMMITTED")
    with conn_check.cursor() as cur:
        cur.execute(f"SELECT count(*) FROM {tbl} WHERE on_call = true;")
        assert cur.fetchone()[0] == 0
    conn_check.close()

    conn1.close()
    conn2.close()


def test_serializable_aborts_write_skew_serialization_failure():
    """SERIALIZABLE isolation prevents Write Skew via Serializable Snapshot Isolation (SSI)."""
    from isolation_live import IsolationLiveClient
    import psycopg2
    client = IsolationLiveClient()
    tbl = "iso_doctors_ssi"
    client.setup_oncall_doctors(tbl)

    conn_init = client.get_connection("READ COMMITTED")
    with conn_init.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'Alice', true), (2, 'Bob', true);")
        conn_init.commit()
    conn_init.close()

    conn1 = client.get_connection("SERIALIZABLE")
    conn2 = client.get_connection("SERIALIZABLE")

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    cur1.execute(f"SELECT count(*) FROM {tbl} WHERE on_call = true;")
    cur2.execute(f"SELECT count(*) FROM {tbl} WHERE on_call = true;")

    cur1.execute(f"UPDATE {tbl} SET on_call = false WHERE id = 1;")
    cur2.execute(f"UPDATE {tbl} SET on_call = false WHERE id = 2;")

    conn1.commit()

    # Conn 2 commit MUST fail with psycopg2.errors.SerializationFailure (SQLSTATE 40001)
    with pytest.raises(psycopg2.errors.SerializationFailure):
        conn2.commit()

    conn1.close()
    conn2.close()


def test_deadlock_detection_opposite_order_locking():
    """Induces circular wait on two rows and verifies PostgreSQL 40P01 deadlock detected."""
    from isolation_live import IsolationLiveClient
    import psycopg2
    client = IsolationLiveClient()
    tbl = "iso_deadlock_test"
    client.setup_bank_accounts(tbl)

    conn_init = client.get_connection("READ COMMITTED")
    with conn_init.cursor() as cur:
        cur.execute(f"DELETE FROM {tbl}; INSERT INTO {tbl} VALUES (1, 'A', 10.0), (2, 'B', 20.0);")
        conn_init.commit()
    conn_init.close()

    conn1 = client.get_connection("READ COMMITTED")
    conn2 = client.get_connection("READ COMMITTED")

    deadlock_detected = False

    def txn1():
        nonlocal deadlock_detected
        try:
            with conn1.cursor() as cur:
                cur.execute(f"UPDATE {tbl} SET balance = balance + 1 WHERE id = 1;")
                time.sleep(0.1)
                cur.execute(f"UPDATE {tbl} SET balance = balance + 1 WHERE id = 2;")
                conn1.commit()
        except psycopg2.errors.DeadlockDetected:
            deadlock_detected = True
            conn1.rollback()

    def txn2():
        nonlocal deadlock_detected
        try:
            with conn2.cursor() as cur:
                cur.execute(f"UPDATE {tbl} SET balance = balance + 1 WHERE id = 2;")
                time.sleep(0.1)
                cur.execute(f"UPDATE {tbl} SET balance = balance + 1 WHERE id = 1;")
                conn2.commit()
        except psycopg2.errors.DeadlockDetected:
            deadlock_detected = True
            conn2.rollback()

    t1 = threading.Thread(target=txn1)
    t2 = threading.Thread(target=txn2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert deadlock_detected is True
    conn1.close()
    conn2.close()


def test_track_a_consensus_model_reconciliation():
    """Track A <-> Track B: the 2PC model's all-or-nothing rule vs real PostgreSQL atomicity.

    The hand-built `TwoPhaseCommitCoordinator` claims that a transaction commits
    only if EVERY participant votes yes. PostgreSQL makes the same promise for a
    single transaction across many statements. This test asserts both, so a
    divergence between the model and reality shows up as a failure rather than as
    a misconception the learner carries forward.
    """
    from consensus_engine import ParticipantShard, TwoPhaseCommitCoordinator

    # --- Track A: the model ------------------------------------------------
    healthy = [ParticipantShard(f"shard_{i}") for i in range(3)]
    assert TwoPhaseCommitCoordinator(healthy).execute_transaction() is True
    assert all(p.state == "COMMITTED" for p in healthy)

    # One dissenting vote must abort every participant, including those that
    # already voted to prepare. That is the whole point of the prepare phase.
    mixed = [ParticipantShard("ok_1"), ParticipantShard("bad", should_fail=True),
             ParticipantShard("ok_2")]
    assert TwoPhaseCommitCoordinator(mixed).execute_transaction() is False
    assert all(p.state == "ABORTED" for p in mixed), (
        "a single NO vote must roll back the participants that voted YES"
    )

    # --- Track B: the real thing -------------------------------------------
    from isolation_live import IsolationLiveClient

    client = IsolationLiveClient()
    tbl = "atomicity_recon_m22"

    setup = client.get_connection()
    try:
        with setup.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {tbl};")
            cur.execute(f"CREATE TABLE {tbl} (id INT PRIMARY KEY, note TEXT NOT NULL);")
        setup.commit()
    finally:
        setup.close()

    # Three inserts in one transaction; the third violates NOT NULL.
    conn = client.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO {tbl} VALUES (1, 'first');")
            cur.execute(f"INSERT INTO {tbl} VALUES (2, 'second');")
            try:
                cur.execute(f"INSERT INTO {tbl} VALUES (3, NULL);")
            except Exception:
                conn.rollback()
            else:
                conn.commit()
    finally:
        conn.close()

    check = client.get_connection()
    try:
        with check.cursor() as cur:
            cur.execute(f"SELECT count(*) FROM {tbl};")
            surviving = cur.fetchone()[0]
            cur.execute(f"DROP TABLE IF EXISTS {tbl};")
        check.commit()
    finally:
        check.close()

    assert surviving == 0, (
        f"expected all-or-nothing, found {surviving} rows. PostgreSQL and the 2PC "
        "model must agree: one failed participant aborts the whole transaction."
    )

"""Automated pytest test suite for Module 03 SQLite WAL Engine."""

import pytest
from sqlite_wal_engine import SQLiteWALEngine


@pytest.fixture
def wal_engine(tmp_path):
    """Provides a file-backed SQLite WAL engine."""
    db_file = tmp_path / "production_test.db"
    engine = SQLiteWALEngine(db_file)
    yield engine
    engine.close()


def test_wal_mode_enabled(wal_engine):
    cursor = wal_engine.conn.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    assert mode.upper() == "WAL"


def test_custom_sha256_checksum_generation(wal_engine):
    row_id = wal_engine.insert_audit_log("alice@corp.com", "LOGIN_ATTEMPT", 37.7749, -122.4194)
    assert row_id == 1

    cursor = wal_engine.conn.execute("SELECT * FROM audit_logs WHERE id = 1")
    row = dict(cursor.fetchone())
    assert row["user_email"] == "alice@corp.com"
    # Checksum was computed via SHA256 in SQL
    assert len(row["checksum"]) == 64


def test_custom_regex_query(wal_engine):
    wal_engine.insert_audit_log("alice@corp.com", "LOGIN", 0.0, 0.0)
    wal_engine.insert_audit_log("bob@external.org", "DOWNLOAD", 0.0, 0.0)
    wal_engine.insert_audit_log("charlie@corp.com", "LOGOUT", 0.0, 0.0)

    # Search only internal corp.com emails using custom SQL REGEXP function
    results = wal_engine.find_logs_by_email_regex(r"^[^@]+@corp\.com$")
    assert len(results) == 2
    emails = [r["user_email"] for r in results]
    assert "alice@corp.com" in emails
    assert "charlie@corp.com" in emails
    assert "bob@external.org" not in emails


def test_custom_haversine_distance_query(wal_engine):
    # San Francisco coordinates: 37.7749, -122.4194
    wal_engine.insert_audit_log("sf_user@test.com", "LOGIN", 37.7749, -122.4194)

    # Oakland coordinates (~13 km away from SF): 37.8044, -122.2712
    wal_engine.insert_audit_log("oakland_user@test.com", "LOGIN", 37.8044, -122.2712)

    # New York City coordinates (~4130 km away): 40.7128, -74.0060
    wal_engine.insert_audit_log("nyc_user@test.com", "LOGIN", 40.7128, -74.0060)

    # Find users within 50 km of San Francisco
    nearby = wal_engine.find_logs_within_radius(37.7749, -122.4194, max_km=50.0)
    assert len(nearby) == 2
    assert nearby[0]["user_email"] == "sf_user@test.com"
    assert nearby[0]["distance_km"] == 0.0
    assert nearby[1]["user_email"] == "oakland_user@test.com"
    assert nearby[1]["distance_km"] < 20.0


def test_wal_checkpoint_truncate(wal_engine):
    for i in range(10):
        wal_engine.insert_audit_log(f"user_{i}@test.com", "ACTION", 0.0, 0.0)
    busy, log_frames, checkpointed = wal_engine.checkpoint("TRUNCATE")
    assert busy == 0
    assert checkpointed >= 0


def test_explain_query_plan_table_scan_vs_index_scan(wal_engine):
    # Before adding index: SCAN audit_logs
    plan_scan = wal_engine.explain_query_plan("SELECT * FROM audit_logs WHERE user_email = 'test@corp.com'")
    assert any("SCAN" in step["detail"] for step in plan_scan)

    # After adding index: SEARCH audit_logs USING INDEX
    wal_engine.conn.execute("CREATE INDEX idx_audit_email ON audit_logs(user_email);")
    plan_index = wal_engine.explain_query_plan("SELECT * FROM audit_logs WHERE user_email = 'test@corp.com'")
    assert any("SEARCH" in step["detail"] and "USING INDEX" in step["detail"] for step in plan_index)


def test_synchronous_modes_tradeoff(tmp_path):
    res = SQLiteWALEngine.benchmark_synchronous_modes(tmp_path, n_writes=30)
    assert "OFF" in res and "NORMAL" in res and "FULL" in res
    assert res["OFF"] > 0
    assert res["NORMAL"] > 0
    assert res["FULL"] > 0


def test_wal_vs_delete_concurrency_writers(tmp_path):
    res = SQLiteWALEngine.benchmark_wal_vs_delete_concurrency(tmp_path, n_threads=3, writes_per_thread=20)
    assert "WAL" in res and "DELETE" in res
    # Under WAL, zero lock contention failures should occur with busy_timeout
    assert res["WAL"]["errors"] == 0


@pytest.mark.perf
def test_sqlite_wal_write_throughput(wal_engine):
    import time
    start = time.perf_counter()
    with wal_engine.conn:
        for i in range(200):
            wal_engine.conn.execute("INSERT INTO audit_logs (user_email, action) VALUES (?, ?)", (f"u{i}@test.com", "BATCH"))
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0  # 200 batched writes under WAL must finish under 1 second


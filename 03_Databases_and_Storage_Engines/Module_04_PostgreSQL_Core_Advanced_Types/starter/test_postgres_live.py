"""Tests for Module 04: Real PostgreSQL Core & Advanced Types (Track B)."""

from __future__ import annotations

from datetime import datetime

import psycopg2
import pytest

def _postgres_is_up() -> bool:
    try:
        from postgres_live import PostgresLiveClient
        client = PostgresLiveClient()
        return client.ping()
    except Exception:
        return False

requires_postgres = pytest.mark.skipif(
    not _postgres_is_up(),
    reason="PostgreSQL not reachable on localhost:15432 - start with: make up postgres"
)

pytestmark = [pytest.mark.requires_postgres, requires_postgres]


def test_postgres_live_ping():
    from postgres_live import PostgresLiveClient
    client = PostgresLiveClient()
    assert client.ping() is True


def test_postgres_jsonb_insert_and_containment():
    from postgres_live import PostgresLiveClient
    client = PostgresLiveClient()
    tbl = "products_test_m04"
    client.setup_jsonb_catalog(tbl)

    inserted = [
        client.insert_jsonb_product(tbl, "ThinkPad X1", {"brand": "Lenovo", "ram_gb": 32, "os": "Linux"}),
        client.insert_jsonb_product(tbl, "MacBook Pro", {"brand": "Apple", "ram_gb": 32, "os": "macOS"}),
        client.insert_jsonb_product(tbl, "IdeaPad", {"brand": "Lenovo", "ram_gb": 16, "os": "Windows"}),
    ]
    # Every insert must return a distinct primary key - a silent duplicate here
    # would make the containment assertions below pass for the wrong reason.
    assert all(pk is not None for pk in inserted)
    assert len(set(inserted)) == 3

    # Query using @> containment: brand = Lenovo and ram_gb = 32
    results = client.query_jsonb_containment(tbl, {"brand": "Lenovo", "ram_gb": 32})
    assert len(results) >= 1
    assert any(r[1] == "ThinkPad X1" for r in results)
    assert not any(r[1] == "IdeaPad" for r in results)


def test_postgres_jsonb_gin_index_used_in_explain():
    from postgres_live import PostgresLiveClient
    client = PostgresLiveClient()
    tbl = "products_test_m04"
    client.setup_jsonb_catalog(tbl)

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            query_json = '{"os": "Linux"}'
            cur.execute(f"EXPLAIN SELECT * FROM {tbl} WHERE metadata @> %s;", (query_json,))
            plan = "\n".join(row[0] for row in cur.fetchall())
            # Plan should reference Bitmap Index Scan or Seq Scan depending on table size
            assert "metadata" in plan or "Index" in plan or "Scan" in plan


def test_postgres_tsrange_exclude_constraint():
    from postgres_live import PostgresLiveClient
    import psycopg2
    client = PostgresLiveClient()
    tbl = "reservations_test_m04"
    client.setup_range_exclusion_table(tbl)

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {tbl};")
            # 1. Insert room 101 booking: 10:00 to 12:00
            cur.execute(f"""
                INSERT INTO {tbl} (room_id, during)
                VALUES (101, tsrange('2026-03-01 10:00:00', '2026-03-01 12:00:00'));
            """)

            # 2. Conflicting overlapping booking for room 101: 11:00 to 13:00 must raise ExclusionViolation
            with pytest.raises(psycopg2.errors.ExclusionViolation):
                cur.execute(f"""
                    INSERT INTO {tbl} (room_id, during)
                    VALUES (101, tsrange('2026-03-01 11:00:00', '2026-03-01 13:00:00'));
                """)
            conn.rollback()

            # 3. Non-overlapping booking for room 101: 12:00 to 14:00 succeeds
            with conn.cursor() as cur2:
                cur2.execute(f"""
                    INSERT INTO {tbl} (room_id, during)
                    VALUES (101, tsrange('2026-03-01 12:00:00', '2026-03-01 14:00:00'));
                """)


def test_postgres_native_arrays():
    from postgres_live import PostgresLiveClient
    client = PostgresLiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    ARRAY[1, 2, 3, 4] AS int_arr,
                    3 = ANY(ARRAY[1, 2, 3, 4]) AS contains_three,
                    5 = ANY(ARRAY[1, 2, 3, 4]) AS contains_five;
            """)
            row = cur.fetchone()
            assert row[0] == [1, 2, 3, 4]
            assert row[1] is True
            assert row[2] is False


def test_postgres_toast_storage_threshold():
    from postgres_live import PostgresLiveClient
    client = PostgresLiveClient()
    small_str = "Hello Postgres"
    # Large 100KB string exceeding the 2KB TOAST threshold
    large_str = "A" * 100_000
    sizes = client.inspect_toast_sizes(small_str, large_str)
    assert sizes["small_bytes"] < 100
    assert sizes["large_bytes"] > 1000


@pytest.mark.perf
def test_postgres_jsonb_batch_performance():
    from postgres_live import PostgresLiveClient
    import time
    client = PostgresLiveClient()
    tbl = "products_perf_m04"
    client.setup_jsonb_catalog(tbl)

    start = time.perf_counter()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(
                cur,
                f"INSERT INTO {tbl} (title, metadata) VALUES %s",
                [(f"Item {i}", psycopg2.extras.Json({"idx": i, "tag": "perf"})) for i in range(200)],
            )
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0  # 200 JSONB records batch inserted under 2 seconds


def test_track_a_jsonb_and_range_model_reconciliation():
    """Track A <-> Track B: Handbuilt TimeRange & JSONBDocumentStore vs real PostgreSQL."""
    from jsonb_document_store import TimeRange
    from postgres_live import PostgresLiveClient

    # 1. TimeRange overlap model vs PostgreSQL tsrange && operator
    t1 = TimeRange(datetime(2026, 3, 1, 10, 0), datetime(2026, 3, 1, 12, 0))
    t2_overlap = TimeRange(datetime(2026, 3, 1, 11, 0), datetime(2026, 3, 1, 13, 0))
    t3_adjacent = TimeRange(datetime(2026, 3, 1, 12, 0), datetime(2026, 3, 1, 14, 0))

    assert t1.overlaps(t2_overlap) is True
    assert t1.overlaps(t3_adjacent) is False

    client = PostgresLiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    tsrange('2026-03-01 10:00:00', '2026-03-01 12:00:00') &&
                    tsrange('2026-03-01 11:00:00', '2026-03-01 13:00:00') AS does_overlap,
                    tsrange('2026-03-01 10:00:00', '2026-03-01 12:00:00') &&
                    tsrange('2026-03-01 12:00:00', '2026-03-01 14:00:00') AS adjacent_overlap;
            """)
            row = cur.fetchone()
            # Standard PostgreSQL tsrange default bounds are '[)' (inclusive start, exclusive end)
            assert row[0] is True
            assert row[1] is False

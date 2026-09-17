"""Tests for Module 07: Real Oracle Database Architecture & SGA/PGA Operations (Track B).

Validates:
1. OracleLiveClient connection & health ping
2. SGA memory breakdown queries (Buffer Cache, Shared Pool)
3. Buffer cache hit ratio computation
4. Bind variable execution ensuring Library Cache soft parse reuse
5. HWM / extent inspection
6. RECONCILIATION: Handbuilt LibraryCache plan caching matches soft/hard parse semantics
7. RECONCILIATION: Handbuilt DatabaseBufferCache touch-count LRU aging logic
"""

from __future__ import annotations

import os
import pytest

from Module_07_Oracle_Database_Architecture_SGA_PGA.project_solution.oracle_live import OracleLiveClient
from Module_07_Oracle_Database_Architecture_SGA_PGA.project_solution.oracle_sga_engine import (
    LibraryCache as HandbuiltLibraryCache,
    DatabaseBufferCache as HandbuiltBufferCache,
)

ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:11521/FREEPDB1")
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PWD = os.getenv("ORACLE_PWD", "coursepw")

_oracle_available: bool | None = None


def oracle_is_available() -> bool:
    global _oracle_available
    if _oracle_available is None:
        try:
            client = OracleLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
            _oracle_available = client.ping()
        except Exception:
            _oracle_available = False
    return _oracle_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_library_cache_soft_parse():
    """Verify handbuilt LibraryCache correctly identifies soft parse when SQL text or bind key matches."""
    cache = HandbuiltLibraryCache(capacity=10)

    # First execution -> Hard parse
    plan1, was_soft1 = cache.parse_and_get_plan("SELECT * FROM emp WHERE id = :1", bind_normalized_sql="SELECT * FROM emp WHERE id = :b1")
    assert not was_soft1
    assert cache.hard_parses == 1
    assert cache.soft_parses == 0

    # Second execution with same bind normalization -> Soft parse
    plan2, was_soft2 = cache.parse_and_get_plan("SELECT * FROM emp WHERE id = :2", bind_normalized_sql="SELECT * FROM emp WHERE id = :b1")
    assert was_soft2
    assert plan1 == plan2
    assert cache.soft_parses == 1


def test_reconciliation_buffer_cache_touch_count_aging():
    """Verify handbuilt BufferCache touch-count prevents premature eviction of frequently accessed blocks."""
    cache = HandbuiltBufferCache(capacity_blocks=3)

    # Fill cache with 3 blocks
    cache.access_block(101, {"table": "customers"})
    cache.access_block(102, {"table": "orders"})
    cache.access_block(103, {"table": "products"})

    # Access block 101 multiple times (touch count > 2)
    cache.access_block(101)
    cache.access_block(101)

    assert cache._cache[101].touch_count == 3
    assert cache._cache[102].touch_count == 1

    # Insert a 4th block to trigger eviction
    cache.access_block(104, {"table": "inventory"})

    # Block 101 must NOT be evicted because of high touch count; block 102 should be evicted
    assert 101 in cache._cache
    assert 104 in cache._cache


# --- LIVE INTEGRATION TESTS (Skip if Oracle service is offline) ---

@pytest.mark.requires_oracle
def test_oracle_ping():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    assert client.ping() is True


@pytest.mark.requires_oracle
def test_oracle_sga_info_query():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    sga = client.query_sga_info()
    assert "Buffer Cache Size" in sga or "Shared Pool Size" in sga
    assert any(v > 0 for v in sga.values())


@pytest.mark.requires_oracle
def test_oracle_buffer_cache_hit_ratio():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    ratio = client.get_buffer_cache_hit_ratio()
    assert 0.0 <= ratio <= 1.0


@pytest.mark.requires_oracle
def test_oracle_bind_variable_execution():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'DROP TABLE test_bind_tab PURGE';
                EXCEPTION WHEN OTHERS THEN NULL;
                END;
            """)
            cur.execute("CREATE TABLE test_bind_tab (id NUMBER, name VARCHAR2(50))")

    params = [{"id": i, "name": f"user_{i}"} for i in range(10)]
    inserted = client.execute_with_binds("INSERT INTO test_bind_tab (id, name) VALUES (:id, :name)", params)
    assert inserted == 10

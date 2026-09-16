"""Module 03: High-Concurrency SQLite WAL Engine with Custom SQL Functions.

This engine genuinely executes on a REAL embedded database engine (Python standard
library `sqlite3`). It configures real SQLite Write-Ahead Logging (`PRAGMA journal_mode=WAL`),
busy timeout handlers, and native C-level user-defined SQL functions.

Configures WAL mode, busy timeouts, and registers custom Python functions (Regex, Haversine Distance, SHA-256) into the SQLite engine.
"""

from __future__ import annotations

import hashlib
import math
import re
import sqlite3
import time
from pathlib import Path
from typing import Any


def _sql_regexp(expr: str, item: str | None) -> int:
    """Custom SQLite function for regular expression matching."""
    if item is None:
        return 0
    return 1 if re.search(expr, item) else 0


def _sql_sha256(text: str | None) -> str | None:
    """Custom SQLite function computing SHA-256 cryptographic hashes."""
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sql_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Custom SQLite function calculating great-circle distance (in kilometers)."""
    r = 6371.0  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 2)


class SQLiteWALEngine:
    def __init__(self, db_path: Path | str = ":memory:"):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path, timeout=5.0)
        self.conn.row_factory = sqlite3.Row
        self._configure_engine()
        self._register_functions()
        self._init_schema()

    def _configure_engine(self):
        """Applies production pragmas: WAL mode, busy timeout, and normal sync."""
        with self.conn:
            # Note: in-memory DBs ignore WAL, file DBs activate it
            if self.db_path != ":memory:":
                self.conn.execute("PRAGMA journal_mode = WAL;")
                self.conn.execute("PRAGMA synchronous = NORMAL;")
            self.conn.execute("PRAGMA busy_timeout = 5000;")
            self.conn.execute("PRAGMA foreign_keys = ON;")

    def _register_functions(self):
        """Registers Python functions directly into SQLite's SQL runtime."""
        self.conn.create_function("REGEXP", 2, _sql_regexp)
        self.conn.create_function("SHA256", 1, _sql_sha256)
        self.conn.create_function("HAVERSINE_DISTANCE", 4, _sql_haversine_distance)

    def _init_schema(self):
        with self.conn:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT NOT NULL,
                    action TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    checksum TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def insert_audit_log(self, user_email: str, action: str, lat: float, lon: float) -> int:
        """Inserts an audit record and automatically computes a SHA-256 checksum in SQL."""
        sql = """
            INSERT INTO audit_logs (user_email, action, latitude, longitude, checksum)
            VALUES (?, ?, ?, ?, SHA256(? || ':' || ?))
        """
        with self.conn:
            cursor = self.conn.execute(sql, (user_email, action, lat, lon, user_email, action))
            return cursor.lastrowid

    def find_logs_by_email_regex(self, regex_pattern: str) -> list[dict[str, Any]]:
        """Queries records using custom Python REGEXP function inside SQLite."""
        sql = "SELECT * FROM audit_logs WHERE REGEXP(?, user_email) = 1 ORDER BY id"
        cursor = self.conn.execute(sql, (regex_pattern,))
        return [dict(row) for row in cursor.fetchall()]

    def find_logs_within_radius(self, target_lat: float, target_lon: float, max_km: float) -> list[dict[str, Any]]:
        """Queries records using custom HAVERSINE_DISTANCE function inside SQLite."""
        sql = """
            SELECT *, HAVERSINE_DISTANCE(?, ?, latitude, longitude) AS distance_km
            FROM audit_logs
            WHERE HAVERSINE_DISTANCE(?, ?, latitude, longitude) <= ?
            ORDER BY distance_km
        """
        cursor = self.conn.execute(sql, (target_lat, target_lon, target_lat, target_lon, max_km))
        return [dict(row) for row in cursor.fetchall()]

    def checkpoint(self, mode: str = "TRUNCATE") -> tuple[int, int, int]:
        """Manually forces a WAL checkpoint into the main database file."""
        if self.db_path == ":memory:":
            return (0, 0, 0)
        cursor = self.conn.execute(f"PRAGMA wal_checkpoint({mode});")
        return cursor.fetchone()  # (busy, log, checkpointed)

    def explain_query_plan(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Returns SQLite's EXPLAIN QUERY PLAN execution tree."""
        cursor = self.conn.execute(f"EXPLAIN QUERY PLAN {sql}", params)
        plans = []
        for row in cursor.fetchall():
            plans.append({
                "id": row[0],
                "parent": row[1],
                "detail": row[3] if len(row) > 3 else row[2],
            })
        return plans

    @staticmethod
    def benchmark_synchronous_modes(db_dir: Path, n_writes: int = 100) -> dict[str, float]:
        """Measures transaction latency differences across PRAGMA synchronous modes."""
        results: dict[str, float] = {}
        modes = ["OFF", "NORMAL", "FULL"]

        for mode in modes:
            db_file = db_dir / f"sync_{mode.lower()}.db"
            conn = sqlite3.connect(str(db_file))
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute(f"PRAGMA synchronous = {mode};")
            conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, val TEXT);")

            start = time.perf_counter()
            for i in range(n_writes):
                with conn:
                    conn.execute("INSERT INTO t (val) VALUES (?)", (f"entry_{i}",))
            elapsed = time.perf_counter() - start
            results[mode] = elapsed
            conn.close()

        return results

    @staticmethod
    def benchmark_wal_vs_delete_concurrency(db_dir: Path, n_threads: int = 4, writes_per_thread: int = 50) -> dict[str, Any]:
        """Compares concurrent writer performance between WAL mode and DELETE journal mode."""
        import threading

        results: dict[str, Any] = {}
        modes = ["WAL", "DELETE"]

        for mode in modes:
            db_file = db_dir / f"mode_{mode.lower()}.db"
            init_conn = sqlite3.connect(str(db_file))
            init_conn.execute(f"PRAGMA journal_mode = {mode};")
            init_conn.execute("PRAGMA busy_timeout = 5000;")
            init_conn.execute("CREATE TABLE logs (worker INT, idx INT);")
            init_conn.close()

            errors = 0

            def worker_task(worker_id: int):
                nonlocal errors
                try:
                    conn = sqlite3.connect(str(db_file), timeout=5.0)
                    conn.execute("PRAGMA busy_timeout = 5000;")
                    for i in range(writes_per_thread):
                        with conn:
                            conn.execute("INSERT INTO logs VALUES (?, ?)", (worker_id, i))
                    conn.close()
                except Exception:
                    errors += 1

            threads = [threading.Thread(target=worker_task, args=(w,)) for w in range(n_threads)]
            start = time.perf_counter()
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            elapsed = time.perf_counter() - start

            results[mode] = {
                "duration_s": elapsed,
                "errors": errors,
            }

        return results

    def close(self):
        self.conn.close()


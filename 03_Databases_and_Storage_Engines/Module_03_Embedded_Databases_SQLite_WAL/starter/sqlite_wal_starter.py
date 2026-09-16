"""Module 03 Starter Skeleton: Embedded SQLite WAL & Custom Functions.

Complete the implementation of WAL configuration and custom Python functions.
"""

import sqlite3

def configure_production_wal(conn: sqlite3.Connection) -> dict[str, str]:
    """TODO: Set PRAGMA journal_mode = WAL, synchronous = NORMAL, cache_size = -64000.

    Return a dictionary of the resulting pragmas.
    """
    cur = conn.cursor()
    # TODO: Execute pragmas
    return {}

def register_custom_collations(conn: sqlite3.Connection) -> None:
    """TODO: Register a case-insensitive, whitespace-trimmed natural collation."""
    pass

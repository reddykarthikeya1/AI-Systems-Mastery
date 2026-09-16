"""Module 06: Real MySQL & InnoDB Storage Engine Client (Track B).

Interacts directly with MySQL 8.0 via PyMySQL to demonstrate:
1. InnoDB Clustered Index (Primary Key) vs Secondary Index Bookmark Lookup.
2. Inducing a deadlock and parsing the LATEST DETECTED DEADLOCK section of SHOW ENGINE INNODB STATUS.
3. Row-based binary logging (CDC) configuration and event inspection.
4. Foreign key cascading referential integrity under InnoDB.
"""

from __future__ import annotations

import os

import re
from typing import Any

try:
    import pymysql
    import pymysql.cursors
except ImportError:
    pymysql = None  # type: ignore


class MySQLLiveClient:
    """Production MySQL/InnoDB driver client."""

    def __init__(
        self,
        host: str = os.environ.get("COURSE_DB_HOST", "localhost"),
        port: int = int(os.environ.get("COURSE_MYSQL_PORT", "13306")),
        user: str = "root",
        password: str = "coursepw",
        database: str = "coursedb",
    ):
        if pymysql is None:
            raise RuntimeError("pymysql is not installed. Install with: pip install pymysql")
        self.conn_params = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": False,
        }

    def get_connection(self):
        return pymysql.connect(**self.conn_params)

    def ping(self) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                res = cur.fetchone()
            conn.close()
            return res is not None
        except Exception:
            return False

    def setup_innodb_tables(self) -> None:
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS innodb_users (
                    user_id INT NOT NULL AUTO_INCREMENT,
                    email VARCHAR(255) NOT NULL,
                    score INT NOT NULL DEFAULT 0,
                    PRIMARY KEY (user_id),
                    UNIQUE KEY uq_email (email),
                    KEY idx_score (score)
                ) ENGINE = InnoDB;
            """)
            conn.commit()
        conn.close()

    def get_innodb_status_deadlock_section(self) -> str:
        """Extracts the LATEST DETECTED DEADLOCK section from SHOW ENGINE INNODB STATUS."""
        conn = self.get_connection()
        status_text = ""
        with conn.cursor() as cur:
            cur.execute("SHOW ENGINE INNODB STATUS;")
            row = cur.fetchone()
            status_text = row.get("Status", "")
        conn.close()

        match = re.search(r"------------------------\nLATEST DETECTED DEADLOCK\n------------------------(.*?)\n------------", status_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return status_text

    def query_binlog_status(self) -> dict[str, Any]:
        """Inspects active binlog coordinates (File, Position)."""
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("SHOW MASTER STATUS;")
            row = cur.fetchone()
        conn.close()
        return row or {}

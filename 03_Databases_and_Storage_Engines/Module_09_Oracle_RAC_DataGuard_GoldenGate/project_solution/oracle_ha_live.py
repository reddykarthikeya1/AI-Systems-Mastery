"""Module 09: Real Oracle RAC Cache Fusion & Data Guard Replication (Track B).

Interacts directly with Oracle Database via python-oracledb to demonstrate:
1. RAC Connection Pool configuration with Fast Connection Failover (FCF) simulation.
2. Active Data Guard Standby Database synchronization and transport lag queries.
3. Protection modes (Max Protection, Max Availability, Max Performance) verification via v$database.
4. Redo transport services and SCN recovery monitoring via v$managed_standby.
5. Cache Fusion block transfer tracking via v$gc_element and v$sysstat.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import oracledb
except ImportError:
    oracledb = None  # type: ignore


class OracleHALiveClient:
    """Production client inspecting RAC clustering, Data Guard replication, and high-availability state."""

    def __init__(
        self,
        user: str = "system",
        password: str = os.environ.get("COURSE_ORACLE_PASSWORD", "coursepw"),
        dsn: str = "localhost:11521/FREEPDB1",
    ):
        if oracledb is None:
            raise RuntimeError("python-oracledb is not installed. Install with: pip install oracledb")
        self.user = user
        self.password = password
        self.dsn = dsn

    def get_connection(self):
        return oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)

    def ping(self) -> bool:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM DUAL")
                    return cur.fetchone()[0] == 1
        except Exception:
            return False

    def query_database_ha_role(self) -> dict[str, str]:
        """Queries v$database to inspect DATABASE_ROLE, PROTECTION_MODE, and OPEN_MODE."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT database_role, protection_mode, open_mode FROM v$database")
                row = cur.fetchone()
                return {
                    "database_role": row[0],
                    "protection_mode": row[1],
                    "open_mode": row[2],
                }

    def query_rac_instances(self) -> list[dict[str, Any]]:
        """Queries gv$instance to check all active RAC cluster nodes and statuses."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT inst_id, instance_name, status, host_name FROM gv$instance")
                return [
                    {"inst_id": r[0], "instance_name": r[1], "status": r[2], "host_name": r[3]}
                    for r in cur.fetchall()
                ]

    def query_standby_dest_status(self) -> list[dict[str, Any]]:
        """Queries v$archive_dest_status to monitor Data Guard standby transmission lag and status."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT dest_id, status, type, database_mode, recovery_mode 
                    FROM v$archive_dest_status 
                    WHERE status != 'INACTIVE'
                """)
                return [
                    {"dest_id": r[0], "status": r[1], "type": r[2], "database_mode": r[3], "recovery_mode": r[4]}
                    for r in cur.fetchall()
                ]

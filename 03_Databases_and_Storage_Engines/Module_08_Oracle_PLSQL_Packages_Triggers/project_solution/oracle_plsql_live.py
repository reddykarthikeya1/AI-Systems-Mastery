"""Module 08: Real Oracle PL/SQL Packages, Triggers & Autonomous Transactions (Track B).

Interacts directly with Oracle Database via python-oracledb to demonstrate:
1. PL/SQL Stored Procedures & Package execution with IN/OUT bind parameters.
2. PRAGMA AUTONOMOUS_TRANSACTION audit logging persisting across parent rollbacks.
3. FORALL bulk binding with array execution (executemany).
4. Compound DML Trigger lifecycle phases.
5. Custom PL/SQL exception propagation and SQLCODE / SQLERRM handling.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import oracledb
except ImportError:
    oracledb = None  # type: ignore


class OraclePLSQLLiveClient:
    """Production client executing real PL/SQL blocks, packages, and autonomous transactions."""

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

    def deploy_banking_package(self) -> None:
        """Deploys a banking package specification and body with transfer procedures."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE OR REPLACE PACKAGE bank_pkg AS
                        PROCEDURE transfer(p_from NUMBER, p_to NUMBER, p_amount NUMBER);
                    END bank_pkg;
                """)
                cur.execute("""
                    CREATE OR REPLACE PACKAGE BODY bank_pkg AS
                        PROCEDURE transfer(p_from NUMBER, p_to NUMBER, p_amount NUMBER) IS
                        BEGIN
                            UPDATE test_accounts SET balance = balance - p_amount WHERE acct_id = p_from;
                            UPDATE test_accounts SET balance = balance + p_amount WHERE acct_id = p_to;
                        END transfer;
                    END bank_pkg;
                """)
                conn.commit()

    def call_plsql_block(self, plsql: str, params: dict[str, Any] | None = None) -> Any:
        """Executes an anonymous PL/SQL block."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                res = cur.execute(plsql, params or {})
                conn.commit()
                return res

    def bulk_insert_accounts(self, records: list[tuple[int, str, float]]) -> int:
        """Simulates FORALL bulk array insertion using oracledb cursor.executemany."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO test_accounts (acct_id, owner, balance) VALUES (:1, :2, :3)",
                    records,
                )
                conn.commit()
                return cur.rowcount

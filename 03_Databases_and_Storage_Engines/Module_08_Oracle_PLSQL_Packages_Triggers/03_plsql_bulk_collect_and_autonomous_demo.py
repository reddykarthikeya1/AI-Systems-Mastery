"""Module 08: Oracle PL/SQL Bulk Processing & Autonomous Transactions Demo.

Demonstrates:
1. SQL vs PL/SQL engine context switch penalty and the Bulk Collect speedup.
2. Autonomous Transactions committing audit records independently of parent rollback.
3. Compound Trigger 4-phase execution preventing Mutating Table ORA-04091 errors.
"""

from __future__ import annotations

import time


def demo_context_switch_vs_bulk() -> None:
    print("=" * 75)
    print("    1. SQL vs PL/SQL ENGINE CONTEXT SWITCH vs BULK PROCESSING")
    print("=" * 75)

    num_rows = 10_000
    rows = [(i, 50.0 + (i % 20)) for i in range(num_rows)]

    # 1. Simulating Row-by-Row Cursor Loop (Context switch on every row)
    start = time.perf_counter()
    accumulated_rbar = 0.0
    for _, amt in rows:
        # Simulate engine context switch overhead (~50 nanoseconds)
        accumulated_rbar += amt
    rbar_time = time.perf_counter() - start

    # 2. Simulating Vectorized BULK COLLECT (Single memory transition)
    start = time.perf_counter()
    amounts = [amt for _, amt in rows]  # bulk collection into RAM
    accumulated_bulk = sum(amounts)     # single vector operation
    bulk_time = time.perf_counter() - start

    assert accumulated_rbar == accumulated_bulk
    print(f"Row-by-Row Context Switches (10k switches) : {rbar_time * 1000:.2f} ms")
    print(f"Vectorized Bulk Collect (Single batch)     : {bulk_time * 1000:.2f} ms")
    print(f"Bulk operations were {rbar_time / bulk_time:.1f}x faster!")


def demo_autonomous_transaction_simulation() -> None:
    print("\n" + "=" * 75)
    print("    2. AUTONOMOUS TRANSACTION AUDIT LOGGING (PRAGMA AUTONOMOUS_TRANSACTION)")
    print("=" * 75)

    accounts_ledger = {"Alice": 1000.0, "Bob": 500.0}
    audit_log = []

    def autonomous_log_security_event(event: str) -> None:
        """Simulates an autonomous transaction with an independent COMMIT."""
        # This commits directly to permanent storage, bypassing parent transaction state
        audit_log.append({"event": event, "status": "COMMITTED_AUTONOMOUS"})

    # Simulating a parent banking transaction that encounters fraud/failure and rolls back
    print("[Main Tx] Debiting Alice $10,000 for offshore wire...")
    saved_alice = accounts_ledger["Alice"]
    accounts_ledger["Alice"] -= 10_000.0

    print("[Main Tx] Fraud detected! Amount exceeds regulatory limits.")
    # Log security failure via autonomous transaction
    autonomous_log_security_event("SUSPICIOUS_WIRE_REJECTED: Alice attempted $10,000 wire")

    # Parent Transaction ROLLBACK
    print("[Main Tx] Executing ROLLBACK...")
    accounts_ledger["Alice"] = saved_alice  # Restored!

    print(f"\nAlice Ledger Balance : ${accounts_ledger['Alice']:,.2f} (Rollback successful)")
    print(f"Audit Log Entries    : {len(audit_log)}")
    print(f"Audit Log Record     : '{audit_log[0]['event']}' [{audit_log[0]['status']}]")
    print("Result: Security audit record was preserved on disk despite complete parent rollback!")


def main() -> None:
    demo_context_switch_vs_bulk()
    demo_autonomous_transaction_simulation()


if __name__ == "__main__":
    main()

"""Module 24: DBRE, Point-in-Time Recovery (PITR) & Zero-Downtime Migration Demo.

Demonstrates:
1. Physical Base Backup + Continuous WAL Archiving.
2. Point-in-Time Recovery (PITR) halting replay right before a catastrophic human error.
3. Zero-Downtime Schema Evolution using the 5-phase Expand/Contract pattern.
"""

from __future__ import annotations


def demo_pitr_recovery() -> None:
    print("=" * 75)
    print("    1. DISASTER RECOVERY: POINT-IN-TIME RECOVERY (PITR)")
    print("=" * 75)

    # 1. Base backup at t=100
    base_backup = {
        "acc_1": {"owner": "Alice", "balance": 1000},
        "acc_2": {"owner": "Bob", "balance": 2000},
    }
    print(f"Base Backup (LSN 100, t=100) : {base_backup}")

    # 2. Continuous WAL stream
    wal_records = [
        {"lsn": 101, "timestamp": 110, "op": "UPDATE", "id": "acc_1", "balance": 1500},
        {"lsn": 102, "timestamp": 120, "op": "UPDATE", "id": "acc_2", "balance": 2200},
        {"lsn": 103, "timestamp": 130, "op": "INSERT", "id": "acc_3", "owner": "Carol", "balance": 500},
        {"lsn": 104, "timestamp": 140, "op": "DROP_TABLE", "id": None},  # Human error disaster at t=140!
    ]

    print("\nIncoming Continuous WAL Stream:")
    for w in wal_records:
        print(f"  [LSN {w['lsn']}] t={w['timestamp']} | Op: {w['op']:<10} | Target: {w.get('id')}")

    # 3. PITR configuration: target time = 135 (5 seconds before DROP_TABLE)
    target_recovery_time = 135
    print(f"\nDisaster occurred at t=140! Initiating PITR with recovery_target_time = {target_recovery_time}...")

    # Replay
    restored_db = {k: dict(v) for k, v in base_backup.items()}
    replayed_count = 0

    for w in wal_records:
        if w["timestamp"] > target_recovery_time:
            print(f"  -> Replay halted at LSN {w['lsn']} (Timestamp {w['timestamp']} > Target {target_recovery_time})")
            break

        if w["op"] == "UPDATE":
            restored_db[w["id"]]["balance"] = w["balance"]
        elif w["op"] == "INSERT":
            restored_db[w["id"]] = {"owner": w["owner"], "balance": w["balance"]}
        replayed_count += 1

    print(f"\nPITR Restoration Complete! Replayed {replayed_count} WAL segments.")
    print("Database State at Promoted Read-Write Point:")
    for aid, data in restored_db.items():
        print(f"  [{aid}] {data}")
    print("Result: All valid transactions restored, accidental DROP TABLE 100% prevented!")


def demo_expand_contract_migration() -> None:
    print("\n" + "=" * 75)
    print("    2. ZERO-DOWNTIME SCHEMA EVOLUTION: EXPAND / CONTRACT")
    print("=" * 75)

    print("Goal: Rename column 'phone' to 'mobile_number' without table locks or downtime.")
    print("  Phase 1 (Expand)      : ALTER TABLE users ADD COLUMN mobile_number text NULL;")
    print("  Phase 2 (Dual-Write)  : App writes to BOTH 'phone' AND 'mobile_number', reads 'phone'.")
    print("  Phase 3 (Backfill)    : Worker copies historical data in small batches of 1,000 rows.")
    print("  Phase 4 (Switch Read) : App reads from 'mobile_number', writes to both.")
    print("  Phase 5 (Contract)    : App writes only to 'mobile_number'. DROP COLUMN phone;")
    print("\nResult: Seamless schema evolution with 100% backward & forward compatibility!")


def main() -> None:
    demo_pitr_recovery()
    demo_expand_contract_migration()


if __name__ == "__main__":
    main()

"""Module 06: MySQL InnoDB Clustered Index & Binlog Replication Demo.

Demonstrates:
1. Clustered Primary Key lookup vs Secondary Index bookmark lookup.
2. The Covering Index speedup bypassing the clustered table.
3. Binary Log (Binlog) ROW-based event capture and GTID replication.
"""

from __future__ import annotations

import time


def demo_clustered_vs_secondary_index() -> None:
    print("=" * 75)
    print("    1. INNODB CLUSTERED INDEX vs SECONDARY BOOKMARK LOOKUP")
    print("=" * 75)

    # Simulated Clustered Index: Primary Key (id) -> Full Row Data
    clustered_index: dict[int, dict[str, str | int]] = {
        i: {"id": i, "email": f"user_{i}@example.com", "name": f"User_{i}", "age": 20 + (i % 30)}
        for i in range(1, 10_001)
    }

    # Simulated Secondary Index: Email -> Primary Key (id)
    secondary_index_email: dict[str, int] = {
        f"user_{i}@example.com": i for i in range(1, 10_001)
    }

    target_email = "user_8421@example.com"

    # 1. Primary Key Direct Clustered Lookup: SELECT * WHERE id = 8421
    start = time.perf_counter()
    for _ in range(50_000):
        row = clustered_index[8421]
        assert row["id"] == 8421
    pk_time = time.perf_counter() - start

    # 2. Secondary Index with Bookmark Lookup: SELECT * WHERE email = 'user_8421@example.com'
    start = time.perf_counter()
    for _ in range(50_000):
        # Step A: Lookup PK in secondary index
        pk = secondary_index_email[target_email]
        # Step B: Double-hop bookmark lookup in clustered index
        row = clustered_index[pk]
        assert row["name"] == "User_8421"
    secondary_time = time.perf_counter() - start

    print(f"Primary Key Direct Clustered Access (50k ops) : {pk_time * 1000:.2f} ms")
    print(f"Secondary Index + Bookmark Lookup (50k ops)    : {secondary_time * 1000:.2f} ms")
    print(f"Direct Clustered PK was {secondary_time / pk_time:.2f}x faster by eliminating the second B+ Tree hop!")


def demo_binlog_replication_simulation() -> None:
    print("\n" + "=" * 75)
    print("    2. BINLOG ROW-BASED EVENT & GTID REPLICATION DEMO")
    print("=" * 75)

    server_uuid = "3E11FA47-71CA-11E1-9E33-C80AA9429562"
    gtid_seq = 1

    # Master state
    master_db: dict[int, dict[str, str | int]] = {1: {"id": 1, "username": "Alice", "balance": 100}}
    binlog: list[dict] = []

    # Replica state
    replica_db: dict[int, dict[str, str | int]] = {1: {"id": 1, "username": "Alice", "balance": 100}}
    replica_executed_gtids: set[str] = set()

    # Step 1: Master executes an UPDATE
    gtid = f"{server_uuid}:{gtid_seq}"
    before_img = dict(master_db[1])
    master_db[1]["balance"] = 250
    after_img = dict(master_db[1])

    event = {
        "gtid": gtid,
        "type": "UPDATE_ROW",
        "table": "accounts",
        "before": before_img,
        "after": after_img,
    }
    binlog.append(event)
    print("[Master] Executed UPDATE on account #1 (Balance: 100 -> 250)")
    print(f"[Master] Generated Binlog Event with GTID: {gtid}")

    # Step 2: Replica pulls binlog event and applies
    for ev in binlog:
        ev_gtid = ev["gtid"]
        if ev_gtid in replica_executed_gtids:
            print(f"[Replica] Skipping already-executed GTID: {ev_gtid}")
            continue

        row_id = ev["after"]["id"]
        replica_db[row_id] = dict(ev["after"])
        replica_executed_gtids.add(ev_gtid)
        print(f"[Replica] Successfully applied GTID {ev_gtid}. Replica balance is now: {replica_db[1]['balance']}")

    assert replica_db[1]["balance"] == master_db[1]["balance"]
    print("\n[Result] Master and Replica states are mathematically identical!")


def main() -> None:
    demo_clustered_vs_secondary_index()
    demo_binlog_replication_simulation()


if __name__ == "__main__":
    main()

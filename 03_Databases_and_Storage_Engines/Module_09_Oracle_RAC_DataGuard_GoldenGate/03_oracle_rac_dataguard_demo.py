"""Module 09: Oracle RAC Cache Fusion & Data Guard Replication Demo.

Demonstrates:
1. Cache Fusion: Interconnect memory-to-memory block transfer vs disk write-and-read.
2. Active Data Guard: Redo shipping, standby real-time apply, and read-only offloading.
3. Standby Failover/Switchover lifecycle.
"""

from __future__ import annotations

import time


def demo_cache_fusion_interconnect() -> None:
    print("=" * 75)
    print("    1. ORACLE RAC CACHE FUSION: INTERCONNECT vs DISK PING")
    print("=" * 75)

    # Simulation setup:
    # Node 1 updates Block #50. Node 2 needs to read Block #50.
    block_data = {"block_id": 50, "account": "ACC_CORP_99", "balance": 10_000_000}
    print(f"Target Block #{block_data['block_id']}: {block_data['account']} (${block_data['balance']:,})")

    # 1. Traditional Cluster without Cache Fusion (Disk write from Node 1, then disk read by Node 2)
    # Disk write: ~5ms, Disk read: ~5ms -> Total ~10ms
    start = time.perf_counter()
    time.sleep(0.005)  # Disk write
    time.sleep(0.005)  # Disk read
    disk_transfer_duration = time.perf_counter() - start

    # 2. Oracle RAC Cache Fusion over 100Gbps InfiniBand Interconnect (RDMA in-memory transfer)
    # Microsecond memory copy over private interconnect (~15-50 microseconds)
    start = time.perf_counter()
    time.sleep(0.00005)  # Interconnect RDMA transfer
    cache_fusion_duration = time.perf_counter() - start

    print(f"Traditional Disk-Mediated Transfer : {disk_transfer_duration * 1000:.2f} ms")
    print(f"Oracle RAC Cache Fusion Interconnect: {cache_fusion_duration * 1000:.2f} ms")
    print(f"Cache Fusion was {disk_transfer_duration / cache_fusion_duration:.1f}x faster by bypassing physical disk I/O!")


def demo_dataguard_replication() -> None:
    print("\n" + "=" * 75)
    print("    2. ORACLE ACTIVE DATA GUARD: REDO APPLY & STANDBY OFFLOADING")
    print("=" * 75)

    primary_redo_stream = [
        "SCN 1001: INSERT INTO INVOICES (ID, AMOUNT) VALUES (1, 50000)",
        "SCN 1002: UPDATE INVOICES SET STATUS = 'PAID' WHERE ID = 1",
    ]

    standby_applied_scns: list[str] = []

    print("[Primary] Streaming 2 Redo Vectors over WAN to Standby (Dublin)...")
    for redo in primary_redo_stream:
        # Standby MRP process applies redo
        standby_applied_scns.append(redo)
        print(f"  -> Standby Applied: {redo}")

    print("\n[Standby] Standby database is open READ-ONLY with Real-Time Apply.")
    print("  -> Business Intelligence (BI) and reporting queries offloaded to Standby.")
    print("  -> Primary CPU utilization remains 100% dedicated to mission-critical OLTP writes.")


def main() -> None:
    demo_cache_fusion_interconnect()
    demo_dataguard_replication()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Module 00: Interactive Capacity Estimation Demo.

Simulates back-of-the-envelope capacity estimations for high-scale platforms
(Twitter / X and Netflix video metadata).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project_solution to sys.path for demo execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "project_solution"))

from interview_capacity_calculator import CapacityCalculator, SystemCapacityProfile


def print_banner(title: str) -> None:
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)


def run_demo() -> None:
    print_banner("SYSTEM DESIGN INTERVIEW: CAPACITY ESTIMATION SIMULATION")

    # Scenario 1: Twitter / X Scale Microblogging
    print("\n[Scenario 1: Microblogging Platform (Twitter / X Scale)]")
    print("  - Daily Active Users (DAU): 500,000,000 (500 Million)")
    print("  - Read/Write Ratio: 10:1 (20 Timeline reads, 2 Tweet writes per day)")
    print("  - Write Payload Size: 250 Bytes (JSON text + metadata)")
    print("  - Read Payload Size: 2,000 Bytes (2 KB timeline batch)")

    twitter_profile = SystemCapacityProfile(
        dau=500_000_000,
        reads_per_user_day=20.0,
        writes_per_user_day=2.0,
        read_payload_bytes=2_000,
        write_payload_bytes=250,
        peak_multiplier=2.5,
    )

    report = CapacityCalculator.generate_full_report(twitter_profile)

    print("\n  [Calculated Capacity Numbers]:")
    print(f"    • Average Write QPS:    {report['qps']['avg_write_qps']:>12,.2f} req/sec")
    print(f"    • Peak Write QPS (2.5x): {report['qps']['peak_write_qps']:>12,.2f} req/sec")
    print(f"    • Average Read QPS:     {report['qps']['avg_read_qps']:>12,.2f} req/sec")
    print(f"    • Peak Read QPS (2.5x):  {report['qps']['peak_read_qps']:>12,.2f} req/sec")
    print(f"    • Network Ingress:      {report['bandwidth']['ingress_mb_per_sec']:>12,.2f} MB/s ({report['bandwidth']['ingress_mbps']:,.1f} Mbps)")
    print(f"    • Network Egress:       {report['bandwidth']['egress_mb_per_sec']:>12,.2f} MB/s ({report['bandwidth']['egress_mbps']:,.1f} Mbps)")
    print(f"    • Daily Storage Growth: {report['storage']['daily_storage_gb']:>12,.2f} GB/day")
    print(f"    • 5-Year Storage Total: {report['storage']['multi_year_storage_tb']:>12,.2f} TB")
    print(f"    • RAM Cache Sizing:     {report['cache']['ram_cache_required_gb']:>12,.2f} GB (80/20 rule)")

    print("\n  [Architectural Decisions Derived from Numbers]:")
    print("    1. Write QPS (~28.9k peak): Requires sharded database cluster with connection pooling.")
    print("    2. Read QPS (~289k peak): Single database CANNOT handle this; requires Redis cache cluster.")
    print("    3. RAM Cache (4,000 GB): Deploy ~32x 128GB Redis nodes in a distributed cache ring.")
    print("    4. 5-Year Storage (456 TB): Well within distributed Cassandra / DynamoDB capacity.")

    print_banner("CAPACITY SIMULATION COMPLETE (Exit 0)")


if __name__ == "__main__":
    run_demo()

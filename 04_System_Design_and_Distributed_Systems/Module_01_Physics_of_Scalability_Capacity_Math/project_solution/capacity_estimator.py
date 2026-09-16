"""Module 01: In-Process Architectural Simulation Model: Capacity Planner & System Sizing Engine.

Computes theoretical and empirical infrastructure requirements for high-scale systems
including QPS, bandwidth, storage growth over time, and RAM cache sizing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

SECONDS_PER_DAY = 86_400


@dataclass(frozen=True)
class QPSMetrics:
    avg_read_qps: float
    avg_write_qps: float
    avg_total_qps: float
    peak_read_qps: float
    peak_write_qps: float
    peak_total_qps: float


@dataclass(frozen=True)
class BandwidthMetrics:
    ingress_mb_per_sec: float
    egress_mb_per_sec: float
    ingress_mbps: float  # Megabits per second
    egress_mbps: float   # Megabits per second


@dataclass(frozen=True)
class StorageMetrics:
    daily_raw_storage_gb: float
    daily_replicated_storage_gb: float
    total_raw_storage_tb: float
    total_replicated_storage_tb: float


@dataclass(frozen=True)
class CacheMetrics:
    daily_read_volume_gb: float
    recommended_cache_ram_gb: float
    nodes_required_64gb_ram: int


@dataclass(frozen=True)
class CapacityReport:
    qps: QPSMetrics
    bandwidth: BandwidthMetrics
    storage: StorageMetrics
    cache: CacheMetrics


class CapacityEstimator:
    """Calculates full architectural capacity requirements given user load and payload profiles."""

    def __init__(
        self,
        dau: int,
        read_ops_per_user_day: float,
        write_ops_per_user_day: float,
        avg_read_payload_bytes: int,
        avg_write_payload_bytes: int,
        peak_multiplier: float = 2.5,
        retention_years: int = 5,
        replication_factor: int = 3,
        cache_coverage_ratio: float = 0.20,
    ) -> None:
        if dau <= 0:
            raise ValueError("DAU must be greater than zero.")
        if read_ops_per_user_day < 0 or write_ops_per_user_day < 0:
            raise ValueError("Operations per user cannot be negative.")
        if avg_read_payload_bytes <= 0 or avg_write_payload_bytes <= 0:
            raise ValueError("Payload sizes must be positive integers.")

        self.dau = dau
        self.read_ops_per_user_day = read_ops_per_user_day
        self.write_ops_per_user_day = write_ops_per_user_day
        self.avg_read_payload_bytes = avg_read_payload_bytes
        self.avg_write_payload_bytes = avg_write_payload_bytes
        self.peak_multiplier = peak_multiplier
        self.retention_years = retention_years
        self.replication_factor = replication_factor
        self.cache_coverage_ratio = cache_coverage_ratio

    def estimate_qps(self) -> QPSMetrics:
        daily_reads = self.dau * self.read_ops_per_user_day
        daily_writes = self.dau * self.write_ops_per_user_day

        avg_read_qps = daily_reads / SECONDS_PER_DAY
        avg_write_qps = daily_writes / SECONDS_PER_DAY
        avg_total_qps = avg_read_qps + avg_write_qps

        return QPSMetrics(
            avg_read_qps=round(avg_read_qps, 2),
            avg_write_qps=round(avg_write_qps, 2),
            avg_total_qps=round(avg_total_qps, 2),
            peak_read_qps=round(avg_read_qps * self.peak_multiplier, 2),
            peak_write_qps=round(avg_write_qps * self.peak_multiplier, 2),
            peak_total_qps=round(avg_total_qps * self.peak_multiplier, 2),
        )

    def estimate_bandwidth(self) -> BandwidthMetrics:
        qps = self.estimate_qps()

        # bytes/sec = qps * avg_payload_bytes
        ingress_bytes_per_sec = qps.peak_write_qps * self.avg_write_payload_bytes
        egress_bytes_per_sec = qps.peak_read_qps * self.avg_read_payload_bytes

        ingress_mb_per_sec = ingress_bytes_per_sec / 1_000_000
        egress_mb_per_sec = egress_bytes_per_sec / 1_000_000

        # 1 Byte = 8 bits
        ingress_mbps = ingress_mb_per_sec * 8
        egress_mbps = egress_mb_per_sec * 8

        return BandwidthMetrics(
            ingress_mb_per_sec=round(ingress_mb_per_sec, 2),
            egress_mb_per_sec=round(egress_mb_per_sec, 2),
            ingress_mbps=round(ingress_mbps, 2),
            egress_mbps=round(egress_mbps, 2),
        )

    def estimate_storage(self) -> StorageMetrics:
        daily_writes = self.dau * self.write_ops_per_user_day
        daily_raw_bytes = daily_writes * self.avg_write_payload_bytes

        daily_raw_storage_gb = daily_raw_bytes / 1_000_000_000
        daily_replicated_storage_gb = daily_raw_storage_gb * self.replication_factor

        total_days = self.retention_years * 365
        total_raw_storage_tb = (daily_raw_storage_gb * total_days) / 1000
        total_replicated_storage_tb = total_raw_storage_tb * self.replication_factor

        return StorageMetrics(
            daily_raw_storage_gb=round(daily_raw_storage_gb, 2),
            daily_replicated_storage_gb=round(daily_replicated_storage_gb, 2),
            total_raw_storage_tb=round(total_raw_storage_tb, 2),
            total_replicated_storage_tb=round(total_replicated_storage_tb, 2),
        )

    def estimate_cache(self) -> CacheMetrics:
        daily_reads = self.dau * self.read_ops_per_user_day
        daily_read_bytes = daily_reads * self.avg_read_payload_bytes
        daily_read_volume_gb = daily_read_bytes / 1_000_000_000

        # Pareto 80/20 rule: 20% of the daily read data generates 80% of traffic
        recommended_cache_ram_gb = daily_read_volume_gb * self.cache_coverage_ratio

        # Sizing in terms of 64GB RAM production nodes (assuming 75% max memory allocation safety)
        usable_ram_per_node = 64 * 0.75  # 48GB usable
        nodes_required = math.ceil(recommended_cache_ram_gb / usable_ram_per_node)
        nodes_required = max(nodes_required, 2)  # Minimum 2 nodes for high-availability failover

        return CacheMetrics(
            daily_read_volume_gb=round(daily_read_volume_gb, 2),
            recommended_cache_ram_gb=round(recommended_cache_ram_gb, 2),
            nodes_required_64gb_ram=nodes_required,
        )

    def generate_full_report(self) -> CapacityReport:
        return CapacityReport(
            qps=self.estimate_qps(),
            bandwidth=self.estimate_bandwidth(),
            storage=self.estimate_storage(),
            cache=self.estimate_cache(),
        )


if __name__ == "__main__":
    # Example: Sizing a Twitter-Scale Newsfeed Platform
    # 300 Million DAU, 20 read queries/day, 2 write tweets/day
    planner = CapacityEstimator(
        dau=300_000_000,
        read_ops_per_user_day=20,
        write_ops_per_user_day=2,
        avg_read_payload_bytes=5_000,   # 5 KB timeline payload
        avg_write_payload_bytes=1_000,  # 1 KB tweet payload
        peak_multiplier=3.0,
        retention_years=5,
        replication_factor=3,
        cache_coverage_ratio=0.20,
    )

    report = planner.generate_full_report()
    print("=" * 75)
    print("                 TWITTER-SCALE CAPACITY SIZING REPORT")
    print("=" * 75)
    print(f"Average Total QPS   : {report.qps.avg_total_qps:,.0f} req/s")
    print(f"Peak Total QPS      : {report.qps.peak_total_qps:,.0f} req/s")
    print(f"Peak Ingress BW     : {report.bandwidth.ingress_mbps:,.2f} Mbps")
    print(f"Peak Egress BW      : {report.bandwidth.egress_mbps:,.2f} Mbps")
    print(f"Daily Replicated DB : {report.storage.daily_replicated_storage_gb:,.2f} GB/day")
    print(f"5-Year Replicated DB: {report.storage.total_replicated_storage_tb:,.2f} TB")
    print(f"Recommended RAM     : {report.cache.recommended_cache_ram_gb:,.2f} GB")
    print(f"Redis Cluster Nodes : {report.cache.nodes_required_64gb_ram} nodes (64GB RAM each)")
    print("=" * 75)

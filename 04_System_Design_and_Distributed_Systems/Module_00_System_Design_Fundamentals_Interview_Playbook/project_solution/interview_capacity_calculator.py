"""Module 00: Interview Capacity Estimation Calculator.

Reference capacity planning engine for calculating QPS, Bandwidth, Storage,
and RAM cache requirements in System Design interviews.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SystemCapacityProfile:
    dau: int
    reads_per_user_day: float
    writes_per_user_day: float
    read_payload_bytes: int
    write_payload_bytes: int
    peak_multiplier: float = 2.5
    storage_years: int = 5
    cache_read_ratio: float = 0.20  # Pareto 80/20 rule

    def __post_init__(self) -> None:
        if self.dau <= 0:
            raise ValueError("DAU must be strictly positive.")
        if self.reads_per_user_day < 0 or self.writes_per_user_day < 0:
            raise ValueError("Requests per user cannot be negative.")
        if self.read_payload_bytes <= 0 or self.write_payload_bytes <= 0:
            raise ValueError("Payload bytes must be strictly positive.")


class CapacityCalculator:
    """Calculates back-of-the-envelope capacity estimations for distributed systems."""

    SECONDS_PER_DAY: int = 86_400

    @classmethod
    def calculate_qps(cls, profile: SystemCapacityProfile) -> dict[str, float]:
        """Calculate average and peak queries per second for reads and writes."""
        avg_read_qps = (profile.dau * profile.reads_per_user_day) / cls.SECONDS_PER_DAY
        peak_read_qps = avg_read_qps * profile.peak_multiplier

        avg_write_qps = (profile.dau * profile.writes_per_user_day) / cls.SECONDS_PER_DAY
        peak_write_qps = avg_write_qps * profile.peak_multiplier

        total_avg_qps = avg_read_qps + avg_write_qps
        total_peak_qps = peak_read_qps + peak_write_qps

        return {
            "avg_read_qps": round(avg_read_qps, 2),
            "peak_read_qps": round(peak_read_qps, 2),
            "avg_write_qps": round(avg_write_qps, 2),
            "peak_write_qps": round(peak_write_qps, 2),
            "total_avg_qps": round(total_avg_qps, 2),
            "total_peak_qps": round(total_peak_qps, 2),
        }

    @classmethod
    def calculate_bandwidth(cls, profile: SystemCapacityProfile) -> dict[str, float]:
        """Calculate network ingress (writes) and egress (reads) in MB/s and Mbps."""
        qps_data = cls.calculate_qps(profile)

        # Ingress (bytes arriving at system from writes)
        ingress_bytes_per_sec = qps_data["avg_write_qps"] * profile.write_payload_bytes
        ingress_mb_per_sec = ingress_bytes_per_sec / 1_000_000
        ingress_mbps = (ingress_bytes_per_sec * 8) / 1_000_000

        # Egress (bytes served by system from reads)
        egress_bytes_per_sec = qps_data["avg_read_qps"] * profile.read_payload_bytes
        egress_mb_per_sec = egress_bytes_per_sec / 1_000_000
        egress_mbps = (egress_bytes_per_sec * 8) / 1_000_000

        return {
            "ingress_mb_per_sec": round(ingress_mb_per_sec, 2),
            "ingress_mbps": round(ingress_mbps, 2),
            "egress_mb_per_sec": round(egress_mb_per_sec, 2),
            "egress_mbps": round(egress_mbps, 2),
        }

    @classmethod
    def calculate_storage(cls, profile: SystemCapacityProfile) -> dict[str, float]:
        """Calculate daily and multi-year storage accumulation in GB and TB."""
        total_daily_writes = profile.dau * profile.writes_per_user_day
        daily_storage_bytes = total_daily_writes * profile.write_payload_bytes
        daily_storage_gb = daily_storage_bytes / 1_000_000_000

        annual_storage_tb = (daily_storage_gb * 365) / 1_000
        multi_year_storage_tb = annual_storage_tb * profile.storage_years

        return {
            "daily_storage_gb": round(daily_storage_gb, 2),
            "annual_storage_tb": round(annual_storage_tb, 2),
            "multi_year_storage_tb": round(multi_year_storage_tb, 2),
        }

    @classmethod
    def calculate_cache_size(cls, profile: SystemCapacityProfile) -> dict[str, float]:
        """Calculate RAM cache size required under the 80/20 Pareto principle."""
        total_daily_reads = profile.dau * profile.reads_per_user_day
        daily_read_bytes = total_daily_reads * profile.read_payload_bytes
        daily_read_volume_gb = daily_read_bytes / 1_000_000_000

        cache_ram_gb = daily_read_volume_gb * profile.cache_read_ratio

        return {
            "daily_read_volume_gb": round(daily_read_volume_gb, 2),
            "ram_cache_required_gb": round(cache_ram_gb, 2),
        }

    @classmethod
    def generate_full_report(cls, profile: SystemCapacityProfile) -> dict[str, Any]:
        """Generate complete capacity estimation report for architectural review."""
        return {
            "qps": cls.calculate_qps(profile),
            "bandwidth": cls.calculate_bandwidth(profile),
            "storage": cls.calculate_storage(profile),
            "cache": cls.calculate_cache_size(profile),
        }

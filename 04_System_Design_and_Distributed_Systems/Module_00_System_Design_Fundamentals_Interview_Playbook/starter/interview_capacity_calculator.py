"""STARTER - Module 00: Interview Capacity Estimation Calculator.

Implement the core back-of-the-envelope capacity calculations for System Design interviews.
Run pytest to verify your solution against the specification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


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
    def calculate_qps(cls, profile: SystemCapacityProfile) -> Dict[str, float]:
        """Calculate average and peak queries per second for reads and writes.
        
        Formula:
          avg_qps = (DAU * requests_per_day) / 86400
          peak_qps = avg_qps * peak_multiplier
        """
        raise NotImplementedError("Module 00: implement calculate_qps()")

    @classmethod
    def calculate_bandwidth(cls, profile: SystemCapacityProfile) -> Dict[str, float]:
        """Calculate network ingress (writes) and egress (reads) in MB/s and Mbps.
        
        Formula:
          bytes_per_sec = qps * payload_bytes
          mb_per_sec = bytes_per_sec / 1,000,000
          mbps = (bytes_per_sec * 8) / 1,000,000
        """
        raise NotImplementedError("Module 00: implement calculate_bandwidth()")

    @classmethod
    def calculate_storage(cls, profile: SystemCapacityProfile) -> Dict[str, float]:
        """Calculate daily and multi-year storage accumulation in GB and TB.
        
        Formula:
          daily_gb = (daily_writes * write_payload_bytes) / 10^9
          annual_tb = (daily_gb * 365) / 1000
          multi_year_tb = annual_tb * storage_years
        """
        raise NotImplementedError("Module 00: implement calculate_storage()")

    @classmethod
    def calculate_cache_size(cls, profile: SystemCapacityProfile) -> Dict[str, float]:
        """Calculate RAM cache size required under the 80/20 Pareto principle.
        
        Formula:
          daily_read_volume_gb = (daily_reads * read_payload_bytes) / 10^9
          cache_ram_gb = daily_read_volume_gb * cache_read_ratio
        """
        raise NotImplementedError("Module 00: implement calculate_cache_size()")

    @classmethod
    def generate_full_report(cls, profile: SystemCapacityProfile) -> Dict[str, Any]:
        """Generate complete capacity estimation report for architectural review."""
        return {
            "qps": cls.calculate_qps(profile),
            "bandwidth": cls.calculate_bandwidth(profile),
            "storage": cls.calculate_storage(profile),
            "cache": cls.calculate_cache_size(profile),
        }

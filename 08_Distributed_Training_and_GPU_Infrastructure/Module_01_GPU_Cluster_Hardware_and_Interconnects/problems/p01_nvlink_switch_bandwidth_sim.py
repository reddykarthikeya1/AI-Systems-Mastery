"""Problem 01 — Nvlink Switch Bandwidth Sim

Topic: 01 GPU Cluster Hardware and Interconnects
Target: Production-grade implementation

Calculate theoretical and effective transfer time across NVLink and InfiniBand.

Example:
    >>> nvlink_switch_bandwidth_sim(1024**3, 900 * 8, bus_efficiency=0.9)
    1.3256

Hints:
    Hint 1: A real link never sustains its rated peak bandwidth, so the
        transfer time has to be computed against a *derated* bandwidth,
        not the raw advertised link speed.
    Hint 2: `bus_bandwidth_gbps` is gigabits/sec, so convert to bytes/sec
        with `* 1e9 / 8.0`, scale that by `bus_efficiency` to get the
        effective bandwidth, then divide `tensor_size_bytes` by it and
        convert seconds to milliseconds with `* 1000.0`.
    Hint 3: A zero or negative effective bandwidth (e.g. `bus_bandwidth_gbps
        <= 0` or `bus_efficiency <= 0`) must return `0.0` instead of
        raising a `ZeroDivisionError`. Round the final time to 4 decimals.
"""

from __future__ import annotations


def nvlink_switch_bandwidth_sim(tensor_size_bytes: int, bus_bandwidth_gbps: float, bus_efficiency: float = 0.85) -> float:
    """Compute transfer time in milliseconds:
    effective_bandwidth_bytes_sec = (bus_bandwidth_gbps * 1e9 / 8.0) * bus_efficiency
    transfer_time_ms = (tensor_size_bytes / effective_bandwidth_bytes_sec) * 1000.0
    Returns transfer_time_ms rounded to 4 decimals.
    """
    raise NotImplementedError("Implement nvlink_switch_bandwidth_sim")

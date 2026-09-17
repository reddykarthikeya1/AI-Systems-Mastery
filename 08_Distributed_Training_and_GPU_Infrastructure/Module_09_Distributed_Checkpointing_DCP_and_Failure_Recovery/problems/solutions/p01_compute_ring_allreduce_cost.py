"""Reference Solution — Problem 01: compute_ring_allreduce_cost

Topic: Distributed Checkpointing DCP and Failure Recovery
"""

from __future__ import annotations

def compute_ring_allreduce_cost(param_bytes: int, world_size: int, bus_bandwidth_gbps: float) -> dict[str, float]:
    if world_size <= 1:
        return {"comm_bytes": 0.0, "time_ms": 0.0}
    # Ring AllReduce sends 2 * (N - 1) / N * size
    comm_bytes = 2.0 * ((world_size - 1) / world_size) * param_bytes
    bus_bandwidth_bytes_per_sec = bus_bandwidth_gbps * 1e9 / 8.0
    time_sec = comm_bytes / bus_bandwidth_bytes_per_sec if bus_bandwidth_bytes_per_sec > 0 else 0.0
    return {"comm_bytes": comm_bytes, "time_ms": round(time_sec * 1000.0, 4)}


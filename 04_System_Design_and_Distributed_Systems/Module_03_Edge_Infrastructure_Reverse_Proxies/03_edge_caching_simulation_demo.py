"""Module 03: Edge CDN Simulation & Latency Benchmark Demo.

Simulates global user requests accessing an origin server in US-East
with and without Edge CDN Point of Presence (PoP) caching.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientRegion:
    name: str
    origin_rtt_ms: float
    edge_rtt_ms: float


REGIONS = [
    ClientRegion("New York (US-East)", origin_rtt_ms=10.0, edge_rtt_ms=2.0),
    ClientRegion("London (Europe)", origin_rtt_ms=90.0, edge_rtt_ms=4.0),
    ClientRegion("Tokyo (Asia-East)", origin_rtt_ms=180.0, edge_rtt_ms=3.0),
    ClientRegion("Sydney (Oceania)", origin_rtt_ms=240.0, edge_rtt_ms=5.0),
]


class MockEdgeCDN:
    def __init__(self, cache_hit_ratio: float = 0.85) -> None:
        self.cache_hit_ratio = cache_hit_ratio
        self.edge_hits = 0
        self.origin_misses = 0

    def request_asset(self, region: ClientRegion, is_cacheable: bool = True) -> float:
        """Simulates requesting an asset from a client region.

        Returns total latency experienced by user in milliseconds.
        """
        # Determine if asset hits edge PoP cache
        if is_cacheable and (self.edge_hits / max(1, self.edge_hits + self.origin_misses) < self.cache_hit_ratio):
            self.edge_hits += 1
            # User only pays edge PoP roundtrip
            return region.edge_rtt_ms
        else:
            self.origin_misses += 1
            # Cache miss: Edge PoP fetches from origin, user pays Edge + Origin RTT
            return region.edge_rtt_ms + region.origin_rtt_ms


def main() -> None:
    print("=" * 75)
    print("      EDGE CDN POINT OF PRESENCE (PoP) GLOBAL LATENCY SIMULATION")
    print("=" * 75)

    cdn = MockEdgeCDN(cache_hit_ratio=0.85)
    num_requests_per_region = 100

    print(f"\nSimulating {num_requests_per_region} requests per region (Target: 85% Cache Hit Ratio)...\n")
    print(f"{'Client Region':<22} | {'Direct Origin (No CDN)':<23} | {'With Edge CDN':<15} | {'Speedup':<10}")
    print("-" * 75)

    for region in REGIONS:
        # 1. Without CDN (Direct Origin)
        direct_latencies = [region.origin_rtt_ms for _ in range(num_requests_per_region)]
        avg_direct = sum(direct_latencies) / len(direct_latencies)

        # 2. With Edge CDN
        cdn_latencies = [cdn.request_asset(region) for _ in range(num_requests_per_region)]
        avg_cdn = sum(cdn_latencies) / len(cdn_latencies)

        speedup = avg_direct / avg_cdn
        print(f"{region.name:<22} | {avg_direct:<6.1f} ms latency        | {avg_cdn:<6.1f} ms        | {speedup:<4.1f}x faster")

    total_requests = cdn.edge_hits + cdn.origin_misses
    actual_hit_ratio = (cdn.edge_hits / total_requests) * 100
    print("=" * 75)
    print(f"Total Requests Processed : {total_requests}")
    print(f"Edge Cache Hits (Shield) : {cdn.edge_hits} ({actual_hit_ratio:.1f}%)")
    print(f"Origin Hits (Uncached)   : {cdn.origin_misses} ({100 - actual_hit_ratio:.1f}%)")
    print(f"Origin Load Offload      : {actual_hit_ratio:.1f}% reduction in origin backend traffic!")
    print("=" * 75)


if __name__ == "__main__":
    main()

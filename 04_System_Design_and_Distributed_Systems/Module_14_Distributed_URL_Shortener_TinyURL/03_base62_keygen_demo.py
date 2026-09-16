#!/usr/bin/env python3
"""Module 14 Demo: Base62 Encoding & Key Generation Service (KGS) Simulation."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from url_shortener_service import (
    Base62Encoder,
    KeyGenerationService,
    URLShortenerService,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 14: DISTRIBUTED URL SHORTENER (TINYURL) ARCHITECTURE DEMO")
    print("=" * 72)

    # 1. Base62 Bijective Demonstration
    print("\n--- 1. Base62 Bijective Encoding Mechanics ---")
    sample_ids = [1, 62, 125, 1_000_000, 100_000_000, 3_521_614_606_207]
    for num in sample_ids:
        encoded = Base62Encoder.encode(num, min_length=7)
        decoded = Base62Encoder.decode(encoded)
        print(f"  Base10: {num:14,d} ──(Base62)──► Short Token: '{encoded}' ──(Decode)──► {decoded:,d}")

    # 2. Key Generation Service
    print("\n--- 2. Key Generation Service (KGS) Pre-Allocation ---")
    kgs = KeyGenerationService(start_id=10_000_000, block_size=5)
    print("Web Worker 1 requesting ID block from KGS...")
    start1, end1 = kgs.allocate_block()
    print(f"  Worker 1 assigned ID range: [{start1:,} ... {end1 - 1:,}] (Can generate 5 URLs without central lock)")

    print("Web Worker 2 requesting ID block from KGS...")
    start2, end2 = kgs.allocate_block()
    print(f"  Worker 2 assigned ID range: [{start2:,} ... {end2 - 1:,}]")

    # 3. End-to-End Shortener & Redirection
    print("\n--- 3. End-to-End URL Shortening & Click Analytics ---")
    service = URLShortenerService(kgs)

    target_url = "https://github.com/system-design/advanced-curriculum"
    short_link = service.shorten_url(target_url)
    token = short_link.split("/")[-1]

    print(f"Original: {target_url}")
    print(f"Shortened: {short_link} (Token: '{token}')")

    print("\nSimulating user clicks (Resolving short URL):")
    for click in range(1, 4):
        dest = service.resolve_url(short_link)
        print(f"  Click #{click}: Redirecting HTTP 302 -> {dest}")

    stats = service.get_analytics(token)
    print(f"\nReal-Time Telemetry: Total Clicks Recorded = {stats['clicks']}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()

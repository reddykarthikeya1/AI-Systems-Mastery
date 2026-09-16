#!/usr/bin/env python3
"""Module 17 Demo: Geohash Spatial Indexing & Ride Dispatch Matching."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from geospatial_dispatch import (
    DispatchMatcher,
    DriverStatus,
    Geohash,
    GeospatialIndex,
    haversine_distance_km,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 17: GEOSPATIAL RIDE-SHARING DISPATCH (UBER / LYFT) DEMO")
    print("=" * 72)

    # 1. Geohash demonstration
    print("\n--- 1. Hierarchical Geohash Spatial Grid Encoding ---")
    points = [
        ("San Francisco (Market St)", 37.7749, -122.4194),
        ("San Francisco (Embarcadero)", 37.7955, -122.3937),
        ("Oakland City Center", 37.8044, -122.2712),
        ("New York (Times Square)", 40.7580, -73.9855),
    ]

    for name, lat, lon in points:
        gh5 = Geohash.encode(lat, lon, precision=5)
        gh7 = Geohash.encode(lat, lon, precision=7)
        print(f"  {name:<28} | Lat: {lat:7.4f}, Lon: {lon:9.4f} | Prefix (Level 5): {gh5} | Exact (Level 7): {gh7}")

    print("\nNotice that SF Market St and SF Embarcadero share the same 5-char prefix ('9q8yy')!")
    print("-> Proximity search in Geohash reduces to a simple B-Tree string prefix lookup!")

    # 2. Driver Location Indexing & Dispatch
    print("\n--- 2. Real-Time Location Ingest & Dispatch Matcher ---")
    index = GeospatialIndex(precision=5)
    matcher = DispatchMatcher(index)

    # Place 3 drivers around San Francisco
    drivers = [
        ("driver-sarah", 37.7780, -122.4180, DriverStatus.AVAILABLE),
        ("driver-miguel", 37.7710, -122.4220, DriverStatus.AVAILABLE),
        ("driver-kenji", 37.7750, -122.4190, DriverStatus.IN_TRIP),  # Busy with another passenger
    ]

    for d_id, lat, lon, status in drivers:
        index.update_driver_location(d_id, lat, lon)
        index.drivers[d_id].status = status
        dist_to_center = haversine_distance_km(37.7749, -122.4194, lat, lon)
        print(f"Driver '{d_id:<12}' | Status: {status.value:<10} | Distance: {dist_to_center * 1000:.0f}m")

    # Rider requests pickup at SF City Hall
    pickup_lat, pickup_lon = 37.7749, -122.4194
    print(f"\nRider 'Alex' requests ride at ({pickup_lat}, {pickup_lon})...")

    assigned_driver = matcher.dispatch_ride("rider-alex", pickup_lat, pickup_lon, max_radius_km=3.0)

    if assigned_driver:
        print(f"MATCH SUCCESSFUL! Assigned Driver: {assigned_driver.driver_id}")
        print(f"  Driver new status: {assigned_driver.status.value}")
    else:
        print("NO DRIVERS AVAILABLE!")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()

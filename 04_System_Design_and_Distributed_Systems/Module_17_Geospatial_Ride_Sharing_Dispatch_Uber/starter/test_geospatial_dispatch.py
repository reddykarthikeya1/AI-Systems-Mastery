"""Unit tests for Geospatial Ride-Sharing Dispatch Platform."""

from __future__ import annotations

from geospatial_dispatch import (
    DispatchMatcher,
    DriverStatus,
    Geohash,
    GeospatialIndex,
    haversine_distance_km,
)


def test_geohash_encoding_consistency() -> None:
    # San Francisco Coordinates (Market St)
    lat, lon = 37.7749, -122.4194
    gh = Geohash.encode(lat, lon, precision=6)
    assert len(gh) == 6
    # San Francisco Geohash begins with '9q8yy'
    assert gh.startswith("9q8y")


def test_haversine_distance_calculation() -> None:
    # Distance between NYC (40.7128, -74.0060) and Philadelphia (39.9526, -75.1652)
    dist = haversine_distance_km(40.7128, -74.0060, 39.9526, -75.1652)
    # True distance is ~130 km
    assert 120.0 < dist < 140.0


def test_driver_location_update_and_cell_migration() -> None:
    idx = GeospatialIndex(precision=5)
    idx.update_driver_location("driver-1", 37.7749, -122.4194)

    initial_cell = idx.driver_cell["driver-1"]
    assert "driver-1" in idx.cells[initial_cell]

    # Move driver to Oakland (across bay)
    idx.update_driver_location("driver-1", 37.8044, -122.2712)
    new_cell = idx.driver_cell["driver-1"]

    assert new_cell != initial_cell
    # Invariant: Driver must be removed from old cell and added to new cell
    assert "driver-1" not in idx.cells[initial_cell]
    assert "driver-1" in idx.cells[new_cell]


def test_dispatch_matches_nearest_available_driver() -> None:
    idx = GeospatialIndex(precision=5)
    matcher = DispatchMatcher(idx)

    # Pickup point in downtown SF
    pickup_lat, pickup_lon = 37.7749, -122.4194

    # Driver 1: Very close (0.3 km)
    idx.update_driver_location("d-near", 37.7770, -122.4190)
    # Driver 2: Farther away (2.5 km)
    idx.update_driver_location("d-far", 37.7950, -122.4000)
    # Driver 3: Close (0.5 km) but IN_TRIP (unavailable)
    idx.update_driver_location("d-busy", 37.7755, -122.4192)
    idx.drivers["d-busy"].status = DriverStatus.IN_TRIP

    # Dispatch request
    assigned = matcher.dispatch_ride("rider-alex", pickup_lat, pickup_lon, max_radius_km=5.0)

    assert assigned is not None
    assert assigned.driver_id == "d-near"
    assert assigned.status == DriverStatus.DISPATCHED


def test_dispatch_returns_none_when_no_driver_in_radius() -> None:
    idx = GeospatialIndex(precision=5)
    matcher = DispatchMatcher(idx)

    # Driver in San Jose (60 km away from SF)
    idx.update_driver_location("d-sj", 37.3382, -121.8863)

    assigned = matcher.dispatch_ride("rider-sf", 37.7749, -122.4194, max_radius_km=10.0)
    assert assigned is None

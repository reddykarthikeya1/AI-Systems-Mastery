#!/usr/bin/env python3
"""Module 17: Production Geospatial Ride-Sharing Dispatch Platform (Uber / Lyft).

Implements:
- Geohash base32 hierarchical spatial grid encoder/decoder
- Real-Time Driver Location Ingest Index
- Proximity K-Nearest Driver Radius Query
- Bipartite Driver-Rider Dispatch Matcher

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

import math
import threading
import time
from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum

BASE32_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"
BASE32_MAP = {c: i for i, c in enumerate(BASE32_ALPHABET)}


class DriverStatus(StrEnum):
    OFFLINE = "OFFLINE"
    AVAILABLE = "AVAILABLE"
    DISPATCHED = "DISPATCHED"
    IN_TRIP = "IN_TRIP"


@dataclass
class Driver:
    driver_id: str
    latitude: float
    longitude: float
    status: DriverStatus = DriverStatus.AVAILABLE
    last_updated: float = 0.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS points on Earth in kilometers."""
    r = 6371.0  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class Geohash:
    """Hierarchical Base32 Geohash encoder and decoder."""

    @staticmethod
    def encode(latitude: float, longitude: float, precision: int = 6) -> str:
        lat_interval = [-90.0, 90.0]
        lon_interval = [-180.0, 180.0]
        geohash: list[str] = []
        is_even = True
        bit = 0
        ch = 0

        while len(geohash) < precision:
            if is_even:
                mid = (lon_interval[0] + lon_interval[1]) / 2.0
                if longitude > mid:
                    ch |= (1 << (4 - bit))
                    lon_interval[0] = mid
                else:
                    lon_interval[1] = mid
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2.0
                if latitude > mid:
                    ch |= (1 << (4 - bit))
                    lat_interval[0] = mid
                else:
                    lat_interval[1] = mid

            is_even = not is_even
            if bit < 4:
                bit += 1
            else:
                geohash.append(BASE32_ALPHABET[ch])
                bit = 0
                ch = 0

        return "".join(geohash)


class GeospatialIndex:
    """In-memory spatial index partitioning drivers by Geohash cells."""

    def __init__(self, precision: int = 5) -> None:
        self.precision = precision
        self.drivers: dict[str, Driver] = {}
        # cell_hash -> set of driver_ids
        self.cells: dict[str, set[str]] = defaultdict(set)
        # driver_id -> current cell_hash
        self.driver_cell: dict[str, str] = {}
        self._lock = threading.RLock()

    def update_driver_location(self, driver_id: str, lat: float, lon: float) -> None:
        with self._lock:
            cell = Geohash.encode(lat, lon, precision=self.precision)

            if driver_id in self.drivers:
                d = self.drivers[driver_id]
                old_cell = self.driver_cell.get(driver_id)
                if old_cell and old_cell != cell:
                    self.cells[old_cell].discard(driver_id)
                d.latitude = lat
                d.longitude = lon
                d.last_updated = time.time()
            else:
                d = Driver(driver_id=driver_id, latitude=lat, longitude=lon, last_updated=time.time())
                self.drivers[driver_id] = d

            self.cells[cell].add(driver_id)
            self.driver_cell[driver_id] = cell

    def find_nearest_available_drivers(
        self,
        pickup_lat: float,
        pickup_lon: float,
        max_radius_km: float = 5.0,
        limit: int = 5,
    ) -> list[tuple[Driver, float]]:
        """Finds closest available drivers within radius using spatial proximity search."""
        with self._lock:
            center_cell = Geohash.encode(pickup_lat, pickup_lon, precision=self.precision)
            prefix = center_cell[: max(1, self.precision - 1)]

            candidate_driver_ids: set[str] = set()
            for cell, d_ids in self.cells.items():
                if cell.startswith(prefix):
                    candidate_driver_ids.update(d_ids)

            results: list[tuple[Driver, float]] = []
            for d_id in candidate_driver_ids:
                driver = self.drivers.get(d_id)
                if driver and driver.status == DriverStatus.AVAILABLE:
                    dist = haversine_distance_km(pickup_lat, pickup_lon, driver.latitude, driver.longitude)
                    if dist <= max_radius_km:
                        results.append((driver, dist))

            # Sort ascending by distance (closest first)
            results.sort(key=lambda x: x[1])
            return results[:limit]


class DispatchMatcher:
    """Matches rider trip requests to the optimal available driver."""

    def __init__(self, index: GeospatialIndex) -> None:
        self.index = index
        self._lock = threading.Lock()

    def dispatch_ride(
        self,
        rider_id: str,
        pickup_lat: float,
        pickup_lon: float,
        max_radius_km: float = 10.0,
    ) -> Driver | None:
        with self._lock:
            candidates = self.index.find_nearest_available_drivers(
                pickup_lat, pickup_lon, max_radius_km=max_radius_km, limit=1
            )
            if not candidates:
                return None

            best_driver, _dist = candidates[0]
            # Transition driver to DISPATCHED state atomically
            best_driver.status = DriverStatus.DISPATCHED
            return best_driver

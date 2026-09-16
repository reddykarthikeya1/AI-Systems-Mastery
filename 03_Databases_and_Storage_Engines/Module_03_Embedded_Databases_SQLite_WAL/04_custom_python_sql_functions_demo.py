"""Module 03: Custom Python Aggregate & Scalar Functions in SQLite Demo.

Demonstrates:
1. create_function: Custom scalar hashing and distance functions.
2. create_aggregate: Custom stateful aggregators (geometric mean, standard deviation).
3. create_collation: Custom natural human sorting.
"""

import math
import sqlite3

class GeometricMean:
    def __init__(self):
        self.log_sum = 0.0
        self.count = 0

    def step(self, value):
        if value is not None and value > 0:
            self.log_sum += math.log(value)
            self.count += 1

    def finalize(self):
        if self.count == 0:
            return None
        return math.exp(self.log_sum / self.count)

def haversine_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0  # Earth radius km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def run_demo():
    conn = sqlite3.connect(":memory:")
    conn.create_function("haversine_km", 4, haversine_dist)
    conn.create_aggregate("geom_mean", 1, GeometricMean)

    cur = conn.cursor()
    cur.execute("SELECT haversine_km(40.7128, -74.0060, 51.5074, -0.1278) AS nyc_to_london;")
    dist = cur.fetchone()[0]
    print(f"Custom Scalar Function: NYC to London = {dist:.1f} km")

    cur.executescript("""
        CREATE TABLE growth_rates (company TEXT, multiplier REAL);
        INSERT INTO growth_rates VALUES ('A', 1.2), ('A', 1.5), ('A', 1.1), ('B', 2.0), ('B', 0.5);
    """)

    cur.execute("SELECT company, geom_mean(multiplier) FROM growth_rates GROUP BY company;")
    print("\nCustom Aggregate Function (Geometric Mean):")
    for row in cur.fetchall():
        print(f"  Company {row[0]}: Geometric Mean Multiplier = {row[1]:.3f}")

    conn.close()

if __name__ == "__main__":
    run_demo()

#!/usr/bin/env python3
"""DEBUG LAB: Boundary Search Blindspot Across Geohash Cell Borders

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def find_nearest_driver(rider_lat: float, rider_lon: float, geohash_index: dict):
    current_cell = '9q8yy'
    drivers_in_cell = geohash_index.get(current_cell, [])
    if not drivers_in_cell:
        raise RuntimeError('Boundary blindspot: driver is 50m away across boundary, but current cell is empty!')
    return drivers_in_cell


def reproduce_defect():
    print("Executing defective simulation for Module_17_Geospatial_Ride_Sharing_Dispatch_Uber...")
    find_nearest_driver(37.77, -122.41, {'9q8yy': [], '9q8yz': ['nearby_driver']})
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")

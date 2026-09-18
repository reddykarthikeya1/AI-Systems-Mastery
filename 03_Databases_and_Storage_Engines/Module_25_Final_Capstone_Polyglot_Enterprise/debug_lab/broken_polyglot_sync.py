"""DEBUG LAB: Dual-Write Inconsistency Between Relational DB and Redis Cache

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

from typing import Callable

class Database:
    def __init__(self) -> None:
        self.rows: dict[str, float] = {}

class Cache:
    def __init__(self) -> None:
        self.entries: dict[str, float] = {}

class FlakyNetwork:
    """Simulates the second of two uncoordinated writes silently dropping."""

    def __init__(self, drop_on_call_number: int) -> None:
        self.call_count = 0
        self.drop_on_call_number = drop_on_call_number

    def send(self, fn: Callable, *args) -> bool:
        self.call_count += 1
        if self.call_count == self.drop_on_call_number:
            return False  # packet lost
        fn(*args)
        return True

def update_price(db: Database, cache: Cache, network: FlakyNetwork, sku: str, price: float) -> None:
    network.send(lambda: db.rows.__setitem__(sku, price))     # write 1: database
    network.send(lambda: cache.entries.__setitem__(sku, price))  # write 2: cache, uncoordinated

def reproduce_defect() -> None:
    print("Updating a price in the database and the cache with two separate writes...")
    db, cache = Database(), Cache()
    db.rows["sku-1"] = 19.99
    cache.entries["sku-1"] = 19.99
    network = FlakyNetwork(drop_on_call_number=2)  # the cache write is the one that drops

    update_price(db, cache, network, "sku-1", 24.99)

    print(f"Database price for sku-1: {db.rows['sku-1']}")
    print(f"Cache price for sku-1:    {cache.entries['sku-1']}")
    if db.rows["sku-1"] != cache.entries["sku-1"]:
        print("[DEFECT OBSERVED] The database and cache now permanently disagree -- "
              "the two writes were never coordinated, so the dropped cache update "
              "is never retried or reconciled.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()

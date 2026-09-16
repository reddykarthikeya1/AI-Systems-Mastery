#!/usr/bin/env python3
"""Module 11: Memory Management, GC & __slots__ Demonstration.

This script demonstrates object reference counting, cyclic garbage collection (gc),
and RAM savings using __slots__.
"""

from __future__ import annotations

import gc
import sys


class StandardRecord:
    def __init__(self, record_id: int, symbol: str, price: float) -> None:
        self.record_id = record_id
        self.symbol = symbol
        self.price = price


class SlottedRecord:
    __slots__ = ("price", "record_id", "symbol")

    def __init__(self, record_id: int, symbol: str, price: float) -> None:
        self.record_id = record_id
        self.symbol = symbol
        self.price = price


def demo_cyclic_gc() -> None:
    print("=" * 60)
    print("  1. Cyclic Reference Detection & Garbage Collection (gc)")
    print("=" * 60)

    class CyclicNode:
        def __init__(self, name: str) -> None:
            self.name = name
            self.partner: CyclicNode | None = None

    # Create cyclic reference: A -> B and B -> A
    node_a = CyclicNode("Node_A")
    node_b = CyclicNode("Node_B")
    node_a.partner = node_b
    node_b.partner = node_a

    # Delete references from local namespace
    del node_a
    del node_b

    # Trigger garbage collection manually to reclaim cyclic garbage
    unreachable_objects = gc.collect()
    print(f"Cyclic Garbage Collector reclaimed: {unreachable_objects} isolated objects.")


def demo_slots_benchmark() -> None:
    print("\n" + "=" * 60)
    print("  2. Memory Benchmarking: Standard vs __slots__")
    print("=" * 60)

    std = StandardRecord(101, "AAPL", 150.25)
    slotted = SlottedRecord(101, "AAPL", 150.25)

    std_instance_bytes = sys.getsizeof(std) + sys.getsizeof(std.__dict__)
    slotted_instance_bytes = sys.getsizeof(slotted)

    print(f"Standard Class Instance (__dict__) : {std_instance_bytes} bytes")
    print(f"Slotted Class Instance (__slots__) : {slotted_instance_bytes} bytes")
    print(f"Memory Saved Per Object           : {std_instance_bytes - slotted_instance_bytes} bytes ({(1 - slotted_instance_bytes/std_instance_bytes)*100:.1f}% reduction)")


def main() -> None:
    demo_cyclic_gc()
    demo_slots_benchmark()


if __name__ == "__main__":
    main()

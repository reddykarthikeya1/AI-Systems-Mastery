"""
================================================================================
LAB 03: Memory Leak Hunting & Tracemalloc Profiling
================================================================================
Zero-Prerequisite Intuition:
Imagine you throw away an empty cardboard box in your trash can, but you tied a
thick rope from the box to your dining room table.
The garbage truck arrives, tries to lift the trash can, but cannot carry it away
because the rope holds it to the table!
In Python, this is a "Reference Cycle". Two objects hold pointers to each other,
so Python's automatic reference counter can never decrement to 0.

Run this script to observe memory leaking live, and hunt it with tracemalloc!
================================================================================
"""

import gc
import tracemalloc

class LeakyNode:
    def __init__(self, name: str):
        self.name = name
        self.partner = None
        # Allocate 100 KB payload per node
        self.payload = bytearray(100 * 1024)

def simulate_leaky_session():
    # Disable cyclical GC temporarily to isolate the reference counting leak
    gc.disable()
    
    # Start tracking memory allocations by Python file and line number
    tracemalloc.start()
    
    snapshot_before = tracemalloc.take_snapshot()
    
    print("--- [EXPERIMENT] Allocating Circular Object Pairs ---")
    # Allocate 100 circular pairs
    leaked_nodes = []
    for i in range(100):
        node_a = LeakyNode(f"NodeA_{i}")
        node_b = LeakyNode(f"NodeB_{i}")
        
        # Tie the rope between them: Circular Reference!
        node_a.partner = node_b
        node_b.partner = node_a
        
        # Even if we delete our local variables, they hold each other alive!
        del node_a
        del node_b

    snapshot_after = tracemalloc.take_snapshot()
    
    # Compare memory growth between the two snapshots
    top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
    
    print("\n=== TOP 3 MEMORY GROWTH ALLOCATION SITES ===")
    for stat in top_stats[:3]:
        print(f"File & Line: {stat.traceback}")
        print(f"Memory Gained: {stat.size_diff / 1024:.2f} KB | Total Allocations: {stat.count_diff}\n")
    
    # Re-enable GC and trigger a cyclical collection pass
    print("--- [THE FIX] Triggering Cyclical Garbage Collector (gc.collect()) ---")
    unreachable_count = gc.collect()
    print(f"[SUCCESS] GC successfully broke cycles and reclaimed {unreachable_count} orphaned objects!")
    
    tracemalloc.stop()

if __name__ == "__main__":
    simulate_leaky_session()

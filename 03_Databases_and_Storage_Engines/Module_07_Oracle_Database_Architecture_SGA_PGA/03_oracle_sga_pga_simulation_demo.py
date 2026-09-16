"""Module 07: Oracle Database SGA & Library Cache Simulation Demo.

Demonstrates:
1. The Shared Pool: Hard Parse (expensive plan compilation) vs Soft Parse (bind variable reuse).
2. The Database Buffer Cache: Touch-count LRU block eviction algorithm.
3. The Log Writer (LGWR): Commit flush of the circular Redo Log Buffer.
"""

from __future__ import annotations

import time


def demo_library_cache_parsing() -> None:
    print("=" * 75)
    print("    1. ORACLE SHARED POOL: HARD PARSE vs SOFT PARSE (BIND VARIABLES)")
    print("=" * 75)

    # Simulated Library Cache storing compiled execution plans
    library_cache: dict[str, str] = {}
    hard_parses = 0
    soft_parses = 0

    def execute_sql(sql_statement: str, is_bind: bool = False) -> None:
        nonlocal hard_parses, soft_parses
        # Normalize statement for bind variables
        cache_key = "SELECT * FROM EMPLOYEES WHERE EMP_ID = :1" if is_bind else sql_statement

        if cache_key in library_cache:
            soft_parses += 1
            # Fast soft parse (~10-50 microseconds)
            time.sleep(0.00001)
        else:
            hard_parses += 1
            # Expensive hard parse: syntax, semantics, optimizer plan search (~2000 microseconds)
            time.sleep(0.0002)
            library_cache[cache_key] = "PLAN_HASH_982471204"

    # Scenario A: Anti-pattern - Literal values (1,000 queries with literal IDs)
    start = time.perf_counter()
    for i in range(500):
        execute_sql(f"SELECT * FROM EMPLOYEES WHERE EMP_ID = {i}", is_bind=False)
    literal_duration = time.perf_counter() - start

    # Scenario B: Best practice - Bind variables (500 queries with :1)
    library_cache.clear()
    hard_parses = 0
    soft_parses = 0
    start = time.perf_counter()
    for _ in range(500):
        execute_sql("SELECT * FROM EMPLOYEES WHERE EMP_ID = :1", is_bind=True)
    bind_duration = time.perf_counter() - start

    print(f"Literal Values Total Duration  : {literal_duration * 1000:.2f} ms (500 Hard Parses!)")
    print(f"Bind Variables Total Duration  : {bind_duration * 1000:.2f} ms (1 Hard Parse, 499 Soft Parses)")
    print(f"Bind variables executed {literal_duration / bind_duration:.1f}x faster while preserving Shared Pool RAM!")


def demo_buffer_cache_touch_count() -> None:
    print("\n" + "=" * 75)
    print("    2. ORACLE DATABASE BUFFER CACHE: TOUCH-COUNT LRU AGING")
    print("=" * 75)

    # Touch-count LRU: A block must be touched multiple times before moving to the hot end
    blocks = {
        101: {"block_id": 101, "table": "ACCOUNTS", "touch_count": 5},
        102: {"block_id": 102, "table": "CURRENCY", "touch_count": 12},
        103: {"block_id": 103, "table": "LOGS_STAGING", "touch_count": 1},
    }

    print("Current Buffer Cache Blocks and Touch Counts:")
    for b_id, b in blocks.items():
        print(f"  Block #{b_id:<3} ({b['table']:<12}) -> Touches: {b['touch_count']}")

    print("\nSimulating Buffer Pool Pressure (Need to allocate space for Block #104)...")
    # Least-touched block is evicted first
    eviction_candidate = min(blocks.values(), key=lambda x: x["touch_count"])
    print(f"  -> Evicted Block #{eviction_candidate['block_id']} ({eviction_candidate['table']}) with only {eviction_candidate['touch_count']} touch!")
    print("  -> Frequently accessed tables (ACCOUNTS, CURRENCY) remain safely pinned in RAM.")


def main() -> None:
    demo_library_cache_parsing()
    demo_buffer_cache_touch_count()


if __name__ == "__main__":
    main()

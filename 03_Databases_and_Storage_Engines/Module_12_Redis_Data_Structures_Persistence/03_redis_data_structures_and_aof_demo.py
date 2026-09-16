"""Module 12: Redis Data Structures & AOF Persistence Demo.

Demonstrates:
1. SkipList multi-level forward pointers for Sorted Set (ZSET) range lookups.
2. Append-Only File (AOF) logging and BGREWRITEAOF log compaction.
"""

from __future__ import annotations


def demo_aof_rewrite_compaction() -> None:
    print("=" * 75)
    print("    1. REDOS AOF PERSISTENCE: APPEND-ONLY LOG vs BGREWRITEAOF")
    print("=" * 75)

    # Simulating 100 mutations on user account balance
    raw_aof_commands = []
    current_balance = 0

    # Initial deposit
    raw_aof_commands.append("*3\r\n$3\r\nSET\r\n$15\r\naccount:alice\r\n$3\r\n100\r\n")
    current_balance = 100

    # 99 consecutive micro-deposits of $10
    for _ in range(99):
        raw_aof_commands.append("*3\r\n$4\r\nINCRBY\r\n$15\r\naccount:alice\r\n$2\r\n10\r\n")
        current_balance += 10

    uncompressed_size = sum(len(cmd) for cmd in raw_aof_commands)
    print(f"Historical AOF Log Entries : {len(raw_aof_commands)} commands")
    print(f"Raw AOF File Size on Disk  : {uncompressed_size:,} bytes")
    print(f"Current State in RAM       : account:alice = ${current_balance}")

    # Simulating BGREWRITEAOF (Background AOF Rewrite)
    # Background worker reads RAM and outputs the single state-setting command
    compacted_aof = [f"*3\r\n$3\r\nSET\r\n$15\r\naccount:alice\r\n${len(str(current_balance))}\r\n{current_balance}\r\n"]
    compacted_size = sum(len(cmd) for cmd in compacted_aof)

    print("\nExecuting BGREWRITEAOF...")
    print(f"  -> Compacted AOF Entries : {len(compacted_aof)} command")
    print(f"  -> Compacted File Size   : {compacted_size} bytes ({(1 - compacted_size / uncompressed_size) * 100:.1f}% disk reduction!)")
    print("  -> Result: 100 mutations compacted into 1 canonical SET command.")


def demo_skiplist_concept() -> None:
    print("\n" + "=" * 75)
    print("    2. REDIS SORTED SET: SKIPLIST RANGE TRAVERSAL")
    print("=" * 75)

    # Conceptual SkipList levels over sorted elements
    scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"Sorted Elements (Level 1): {scores}")
    print("Skip Level 2 (step 2)    : [10, 30, 50, 70, 90]")
    print("Skip Level 3 (step 4)    : [10, 50, 90]")

    target = 70
    print(f"\nSearching for Target Score: {target}")
    print("  -> Level 3 jump: 10 -> 50 (next 90 > target, drop to Level 2)")
    print("  -> Level 2 jump: 50 -> 70 (Found match in only 3 hops instead of 7 sequential scans!)")
    print("  -> SkipLists provide O(log N) search and range slicing without B-Tree rotation locks.")


def main() -> None:
    demo_aof_rewrite_compaction()
    demo_skiplist_concept()


if __name__ == "__main__":
    main()

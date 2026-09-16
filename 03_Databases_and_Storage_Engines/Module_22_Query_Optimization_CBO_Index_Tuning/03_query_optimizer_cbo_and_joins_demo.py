"""Module 22: Query Optimization, Cost-Based Optimizer & Joins Demo.

Demonstrates:
1. Relational Algebra Rule-Based Optimization: Predicate Pushdown.
2. Cost-Based Optimizer (CBO) cost equation and Index Scan tipping point.
3. Physical Join Algorithms: Nested Loop, Hash Join, and Sort-Merge Join.
"""

from __future__ import annotations


def demo_predicate_pushdown() -> None:
    print("=" * 75)
    print("    1. RULE-BASED OPTIMIZATION: PREDICATE PUSHDOWN")
    print("=" * 75)

    print("Query: SELECT * FROM orders o JOIN customers c ON o.cust_id = c.id WHERE c.country = 'USA'")

    orders_count = 1_000_000
    customers_total = 100_000
    usa_customers = 5_000  # 5% selectivity

    print("\nInitial Unoptimized Plan (Join First, Filter After):")
    print(f"  Step 1: Join Orders ({orders_count:,}) with Customers ({customers_total:,})")
    print(f"  -> Intermediate tuples produced: {orders_count:,} rows")
    print("  Step 2: Filter where country = 'USA'")
    print(f"  -> Cost: Massive memory overhead storing {orders_count:,} un-filtered joined tuples.")

    print("\nOptimized Plan with Predicate Pushdown (Filter First, Join After):")
    print(f"  Step 1: Filter Customers where country = 'USA' ({customers_total:,} -> {usa_customers:,})")
    print(f"  Step 2: Join Orders ({orders_count:,}) with filtered Customers ({usa_customers:,})")
    print("  -> Join hash table shrunk by 95%! (From 100k down to 5k entries)")


def demo_cbo_tipping_point() -> None:
    print("\n" + "=" * 75)
    print("    2. COST-BASED OPTIMIZER: THE INDEX SCAN TIPPING POINT")
    print("=" * 75)

    pages = 10_000
    total_tuples = 1_000_000
    seq_cost = 1.0
    rand_cost = 4.0
    cpu_tuple = 0.01

    print(f"Table Statistics: Pages = {pages:,} (80 MB), Total Tuples = {total_tuples:,}")
    print(f"Cost Parameters : seq_page_cost = {seq_cost}, random_page_cost = {rand_cost}, cpu_tuple = {cpu_tuple}\n")

    # Sequential Scan Cost: 10,000 * 1.0 + 1,000,000 * 0.01 = 20,000
    seq_scan_cost = (pages * seq_cost) + (total_tuples * cpu_tuple)
    print(f"Sequential Scan Baseline Cost: {seq_scan_cost:,.1f}")

    selectivities = [0.001, 0.01, 0.05, 0.10, 0.20]  # 0.1%, 1%, 5%, 10%, 20%
    print("\nEvaluating Index Scan vs Seq Scan across selectivities:")

    for sel in selectivities:
        matched_tuples = total_tuples * sel
        # In unclustered index scan, each matched tuple could trigger a random page read
        rand_pages = min(pages, matched_tuples)
        index_scan_cost = (rand_pages * rand_cost) + (matched_tuples * (cpu_tuple + 0.0025))
        is_index_cheaper = index_scan_cost < seq_scan_cost
        winner = "INDEX SCAN" if is_index_cheaper else "SEQ SCAN"
        print(f"  Selectivity: {sel * 100:>4.1f}% ({matched_tuples:>7,.0f} rows) -> Index Cost: {index_scan_cost:>9,.1f} | Best Plan: {winner}")

    print("\nTakeaway: When a query matches > 5-10% of a table, an Index Scan's random I/O")
    print("causes the CBO to correctly abandon the index and choose a Sequential Scan!")


def demo_join_algorithms() -> None:
    print("\n" + "=" * 75)
    print("    3. PHYSICAL JOIN ALGORITHMS EXECUTION")
    print("=" * 75)

    left = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}, {"id": 3, "name": "Carol"}]
    right = [{"cust_id": 1, "val": 100}, {"cust_id": 2, "val": 250}, {"cust_id": 1, "val": 70}]

    # 1. Hash Join (Build Left, Probe Right)
    hash_table = {}
    for r in left:
        hash_table[r["id"]] = r

    hash_matches = []
    for s in right:
        cid = s["cust_id"]
        if cid in hash_table:
            hash_matches.append({**hash_table[cid], **s})

    print(f"Hash Join Matches ({len(hash_matches)} rows):")
    for m in hash_matches:
        print(f"  {m}")


def main() -> None:
    demo_predicate_pushdown()
    demo_cbo_tipping_point()
    demo_join_algorithms()


if __name__ == "__main__":
    main()

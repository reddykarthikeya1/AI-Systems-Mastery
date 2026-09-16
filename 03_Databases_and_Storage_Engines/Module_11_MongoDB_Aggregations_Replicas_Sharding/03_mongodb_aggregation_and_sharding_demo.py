"""Module 11: MongoDB Aggregation Pipeline & Shard Routing Demo.

Demonstrates:
1. Multi-stage aggregation pipeline ($match, $unwind, $group, $sort).
2. Targeted Query (single-shard direct route) vs Scatter-Gather (cluster broadcast).
"""

from __future__ import annotations

from collections import defaultdict
import hashlib


def demo_aggregation_pipeline() -> None:
    print("=" * 75)
    print("    1. MONGODB AGGREGATION PIPELINE: $match -> $unwind -> $group")
    print("=" * 75)

    orders = [
        {"order_id": 1, "customer": "Alice", "status": "COMPLETED", "items": [{"prod": "Laptop", "price": 1200}, {"prod": "Mouse", "price": 25}]},
        {"order_id": 2, "customer": "Bob", "status": "CANCELLED", "items": [{"prod": "Monitor", "price": 300}]},
        {"order_id": 3, "customer": "Charlie", "status": "COMPLETED", "items": [{"prod": "Keyboard", "price": 100}, {"prod": "Mouse", "price": 25}]},
        {"order_id": 4, "customer": "Alice", "status": "COMPLETED", "items": [{"prod": "Laptop", "price": 1200}]},
    ]

    print(f"Input: {len(orders)} raw customer order documents.")

    # Stage 1: $match status == "COMPLETED"
    stage_match = [o for o in orders if o["status"] == "COMPLETED"]
    print(f"  -> Stage 1 ($match status='COMPLETED') : {len(stage_match)} documents")

    # Stage 2: $unwind "$items"
    stage_unwind = []
    for o in stage_match:
        for item in o["items"]:
            stage_unwind.append({"order_id": o["order_id"], "customer": o["customer"], "item": item})
    print(f"  -> Stage 2 ($unwind '$items')           : {len(stage_unwind)} unwound item records")

    # Stage 3: $group by item.prod -> compute total revenue & count
    revenue_by_prod: dict[str, dict[str, float | int]] = defaultdict(lambda: {"revenue": 0.0, "count": 0})
    for record in stage_unwind:
        p_name = record["item"]["prod"]
        revenue_by_prod[p_name]["revenue"] += record["item"]["price"]
        revenue_by_prod[p_name]["count"] += 1

    print("\n  -> Stage 3 ($group by item.prod with $sum revenue & count):")
    for prod, stats in sorted(revenue_by_prod.items(), key=lambda x: x[1]["revenue"], reverse=True):
        print(f"     • {prod:<10} | Revenue: ${stats['revenue']:,.2f} | Units Sold: {stats['count']}")


def demo_sharding_router() -> None:
    print("\n" + "=" * 75)
    print("    2. SHARDED CLUSTER: TARGETED ROUTING vs SCATTER-GATHER")
    print("=" * 75)

    num_shards = 4

    def get_shard_for_key(account_id: str) -> int:
        """Hashed Shard Key routing function: MD5(key) % num_shards."""
        h = int(hashlib.md5(account_id.encode("utf-8")).hexdigest(), 16)
        return h % num_shards

    # Scenario A: Targeted query with Shard Key
    query_account = "ACC_99214"
    target_shard = get_shard_for_key(query_account)
    print(f"Targeted Query: db.accounts.find({{ account_id: '{query_account}' }})")
    print(f"  -> mongos computes hash -> Dispatches DIRECTLY to Shard #{target_shard} (1 network hop!)")

    # Scenario B: Scatter-gather query without Shard Key
    print("\nScatter-Gather Query: db.accounts.find({ status: 'ACTIVE' })")
    print(f"  -> No shard key in query! mongos must broadcast to ALL {num_shards} shards!")
    print("  -> Waits for all 4 shards to respond, merges sorted streams in mongos RAM.")
    print("  -> Latency is bounded by the SLOWEST shard in the cluster!")


def main() -> None:
    demo_aggregation_pipeline()
    demo_sharding_router()


if __name__ == "__main__":
    main()

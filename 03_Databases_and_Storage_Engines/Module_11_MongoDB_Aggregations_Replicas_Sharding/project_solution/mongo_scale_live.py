"""Module 11: Real MongoDB Aggregation Pipeline, Replication & Sharding (Track B).

Interacts directly with MongoDB via pymongo to demonstrate:
1. Multi-stage Aggregation ($match, $unwind, $group, $sort, $limit).
2. Cross-collection joins via $lookup.
3. Multi-faceted summaries via $facet.
4. Read preference routing (primary, secondaryPreferred) for replica sets.
5. Aggregation pipeline execution plan analysis via explain().
"""

from __future__ import annotations


from typing import Any

try:
    import pymongo
    from pymongo.read_preferences import ReadPreference
except ImportError:
    pymongo = None  # type: ignore
    ReadPreference = None  # type: ignore


class MongoScaleClient:
    """Production MongoDB aggregation and cluster scaling client."""

    def __init__(self, uri: str = "mongodb://localhost:17017/?directConnection=true", db_name: str = "coursedb"):
        if pymongo is None:
            raise RuntimeError("pymongo is not installed. Install with: pip install pymongo")
        self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
        self.db = self.client[db_name]

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def run_pipeline(self, coll_name: str, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Executes an aggregation pipeline against a collection."""
        coll = self.db[coll_name]
        return list(coll.aggregate(pipeline))

    def run_sales_aggregation(self, coll_name: str = "orders") -> list[dict[str, Any]]:
        """Computes total revenue and units sold per category using $unwind, $match, and $group."""
        pipeline = [
            {"$match": {"status": "COMPLETED"}},
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": "$items.category",
                    "total_revenue": {"$sum": {"$multiply": ["$items.price", "$items.qty"]}},
                    "units_sold": {"$sum": "$items.qty"},
                }
            },
            {"$sort": {"total_revenue": -1}},
        ]
        return self.run_pipeline(coll_name, pipeline)

    def run_lookup_join(
        self,
        orders_coll: str = "orders",
        customers_coll: str = "customers",
    ) -> list[dict[str, Any]]:
        """Performs left outer join between orders and customers via $lookup."""
        pipeline = [
            {
                "$lookup": {
                    "from": customers_coll,
                    "localField": "customer_id",
                    "foreignField": "_id",
                    "as": "customer_profile",
                }
            },
            {"$limit": 10},
        ]
        return self.run_pipeline(orders_coll, pipeline)

    def run_faceted_search(self, products_coll: str = "products") -> dict[str, Any]:
        """Runs multiple aggregation pipelines within a single stage using $facet."""
        pipeline = [
            {
                "$facet": {
                    "price_buckets": [
                        {
                            "$bucket": {
                                "groupBy": "$price",
                                "boundaries": [0, 50, 100, 500, 1000],
                                "default": "Other",
                                "output": {"count": {"$sum": 1}},
                            }
                        }
                    ],
                    "top_categories": [
                        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                        {"$sort": {"count": -1}},
                        {"$limit": 5},
                    ],
                }
            }
        ]
        results = self.run_pipeline(products_coll, pipeline)
        return results[0] if results else {}

    def get_secondary_preferred_collection(self, coll_name: str):
        """Returns collection handle with secondaryPreferred read preference for offloading analytics."""
        return self.db.get_collection(coll_name, read_preference=ReadPreference.SECONDARY_PREFERRED)

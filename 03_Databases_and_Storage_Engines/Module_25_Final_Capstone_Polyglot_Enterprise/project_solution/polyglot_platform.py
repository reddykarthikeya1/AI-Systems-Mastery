"""Module 25: Enterprise Polyglot Persistence Platform (Solution).

This is a pure-Python MODEL of an enterprise polyglot persistence coordinator, built to make the
mechanism visible. It does not connect to external production database clusters. For the real driver,
real queries and real operational behaviour across multiple real database engines, see `polyglot_live.py`.

Implements:
1. PostgresOLTPEngine: Relational transactional engine enforcing the Transactional Outbox pattern & rollback.
2. RedisCacheEngine: In-memory Cache-Aside store, SortedSet spend leaderboard, and Fenced Distributed Lock.
3. SearchCatalogEngine: Inverted index (BM25 lexical ranking) and Vector Semantic Search (cosine similarity).
4. ColumnarAnalyticsEngine: Vectorized OLAP aggregations and windowed rollups.
5. SagaOrchestrator: Distributed transaction coordinator with forward steps and compensating actions.
6. PolyglotPlatform: Master coordinator integrating CDC event relay, DLQ quarantine, idempotency deduplication,
   cache stampede protection, and cross-engine reconciliation audit.
"""

from __future__ import annotations

import math
import re
import time
from typing import Any, Callable


class PostgresOLTPEngine:
    """Relational source of truth enforcing the Transactional Outbox pattern."""

    def __init__(self) -> None:
        self.orders: dict[str, dict[str, Any]] = {}
        self.outbox_events: list[dict[str, Any]] = []
        self.next_event_id: int = 1
        self._tx_active: bool = False
        self._tx_orders_staging: dict[str, dict[str, Any]] = {}
        self._tx_outbox_staging: list[dict[str, Any]] = []

    def begin_transaction(self) -> None:
        self._tx_active = True
        self._tx_orders_staging = {}
        self._tx_outbox_staging = []

    def create_order(
        self,
        order_id: str,
        customer: str,
        total: float,
        description: str,
        embedding: list[float] | None = None,
    ) -> None:
        order_data = {
            "order_id": order_id,
            "customer": customer,
            "total": float(total),
            "description": description,
            "embedding": embedding or [0.1, 0.2, 0.3],
            "status": "CREATED",
        }
        event_data = {
            "event_id": self.next_event_id,
            "event_type": "ORDER_CREATED",
            "order_id": order_id,
            "payload": dict(order_data),
            "retry_count": 0,
        }

        if self._tx_active:
            self._tx_orders_staging[order_id] = order_data
            self._tx_outbox_staging.append(event_data)
        else:
            # Auto-commit mode
            self.orders[order_id] = dict(order_data)
            self.outbox_events.append(event_data)
            self.next_event_id += 1

    def commit_transaction(self) -> None:
        if not self._tx_active:
            return
        for oid, odata in self._tx_orders_staging.items():
            self.orders[oid] = odata
        for evt in self._tx_outbox_staging:
            evt["event_id"] = self.next_event_id
            self.outbox_events.append(evt)
            self.next_event_id += 1
        self._tx_active = False
        self._tx_orders_staging.clear()
        self._tx_outbox_staging.clear()

    def rollback_transaction(self) -> None:
        self._tx_active = False
        self._tx_orders_staging.clear()
        self._tx_outbox_staging.clear()

    def get_order(self, order_id: str) -> dict[str, Any] | None:
        if order_id in self.orders:
            return dict(self.orders[order_id])
        return None

    def update_order_status(self, order_id: str, status: str) -> None:
        if order_id in self.orders:
            self.orders[order_id]["status"] = status


class RedisCacheEngine:
    """In-memory cache, SortedSet leaderboard, and Fenced Distributed Lock manager."""

    def __init__(self) -> None:
        self.cache: dict[str, Any] = {}
        self.leaderboard: dict[str, float] = {}
        self.locks: dict[str, dict[str, Any]] = {}
        self._lock_counter: int = 0

    def get(self, key: str) -> Any | None:
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value

    def invalidate(self, key: str) -> None:
        self.cache.pop(key, None)

    def zadd_incr(self, member: str, delta: float) -> float:
        self.leaderboard[member] = self.leaderboard.get(member, 0.0) + delta
        return self.leaderboard[member]

    def ztop(self, k: int = 5) -> list[tuple[str, float]]:
        return sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)[:k]

    def acquire_lock(self, resource: str, owner: str, ttl_seconds: float = 10.0) -> int | None:
        now = time.time()
        existing = self.locks.get(resource)
        if existing is not None and existing["expires_at"] > now:
            return None  # Lock held by someone else
        self._lock_counter += 1
        fencing_token = self._lock_counter
        self.locks[resource] = {
            "owner": owner,
            "fencing_token": fencing_token,
            "expires_at": now + ttl_seconds,
        }
        return fencing_token

    def release_lock(self, resource: str, owner: str, fencing_token: int) -> bool:
        existing = self.locks.get(resource)
        if existing is None:
            return False
        if existing["owner"] == owner and existing["fencing_token"] == fencing_token:
            del self.locks[resource]
            return True
        return False


class SearchCatalogEngine:
    """Inverted index with BM25 lexical ranking and Cosine Vector Search."""

    def __init__(self) -> None:
        self.documents: dict[str, dict[str, Any]] = {}
        self.postings: dict[str, list[str]] = {}

    def _tokenize(self, text: str) -> list[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9]+\b", text)]

    def index_document(
        self,
        doc_id: str,
        text: str,
        source: dict[str, Any],
        vector: list[float] | None = None,
    ) -> None:
        tokens = self._tokenize(text)
        self.documents[doc_id] = {
            "text": text,
            "source": source,
            "tokens": tokens,
            "vector": vector or [0.0, 0.0, 0.0],
        }

        for term in set(tokens):
            if term not in self.postings:
                self.postings[term] = []
            if doc_id not in self.postings[term]:
                self.postings[term].append(doc_id)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        total_docs = len(self.documents)
        scores: dict[str, float] = {}

        for term in set(query_terms):
            matched_doc_ids = self.postings.get(term, [])
            n_q = len(matched_doc_ids)
            if n_q == 0:
                continue

            idf = math.log(1.0 + (total_docs - n_q + 0.5) / (n_q + 0.5))
            for doc_id in matched_doc_ids:
                tf = self.documents[doc_id]["tokens"].count(term)
                scores[doc_id] = scores.get(doc_id, 0.0) + (idf * tf)

        sorted_hits = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            {"_id": did, "_score": round(score, 4), "_source": self.documents[did]["source"]}
            for did, score in sorted_hits
        ]

    def search_vector(self, query_vec: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        """Cosine similarity vector nearest-neighbor search."""
        if not self.documents or not query_vec:
            return []

        def cosine_similarity(v1: list[float], v2: list[float]) -> float:
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = math.sqrt(sum(a * a for a in v1))
            norm2 = math.sqrt(sum(b * b for b in v2))
            if norm1 == 0.0 or norm2 == 0.0:
                return 0.0
            return dot / (norm1 * norm2)

        results = []
        for did, doc in self.documents.items():
            sim = cosine_similarity(query_vec, doc.get("vector", []))
            results.append({"_id": did, "_score": round(sim, 4), "_source": doc["source"]})

        results.sort(key=lambda x: x["_score"], reverse=True)
        return results[:top_k]


class ColumnarAnalyticsEngine:
    """Columnar analytics warehouse for fast OLAP aggregations."""

    def __init__(self) -> None:
        self.sales: list[float] = []
        self.records: list[dict[str, Any]] = []

    def append_sale(self, amount: float, customer: str = "", order_id: str = "") -> None:
        self.sales.append(float(amount))
        self.records.append({"order_id": order_id, "customer": customer, "amount": float(amount)})

    def sum_revenue(self) -> float:
        return float(sum(self.sales))

    def avg_order_value(self) -> float:
        return float(sum(self.sales) / len(self.sales)) if self.sales else 0.0

    def revenue_by_customer(self) -> dict[str, float]:
        revs: dict[str, float] = {}
        for r in self.records:
            c = r["customer"]
            revs[c] = revs.get(c, 0.0) + r["amount"]
        return revs


class SagaOrchestrator:
    """Manages multi-step distributed saga with forward execution and compensating rollbacks."""

    def __init__(self, platform: PolyglotPlatform) -> None:
        self.platform = platform
        self.inventory: dict[str, int] = {"item_1": 100, "item_2": 2}
        self.payment_balance: dict[str, float] = {"Alice": 1000.0, "BrokeUser": 5.0}

    def execute_order_saga(
        self,
        order_id: str,
        customer: str,
        item_id: str,
        quantity: int,
        total_cost: float,
        description: str,
    ) -> tuple[bool, str]:
        compensations: list[Callable[[], None]] = []

        # Step 1: Reserve Inventory
        available = self.inventory.get(item_id, 0)
        if available < quantity:
            return False, "SAGA_FAILED: Insufficient inventory"

        self.inventory[item_id] -= quantity
        compensations.append(lambda: self._compensate_inventory(item_id, quantity))

        # Step 2: Authorize Payment
        balance = self.payment_balance.get(customer, 0.0)
        if balance < total_cost:
            # Trigger compensating actions in reverse
            for comp in reversed(compensations):
                comp()
            return False, "SAGA_FAILED: Insufficient funds"

        self.payment_balance[customer] -= total_cost
        compensations.append(lambda: self._compensate_payment(customer, total_cost))

        # Step 3: Write Order to OLTP & Outbox
        self.platform.place_order(order_id, customer, total_cost, description)
        return True, "SAGA_SUCCESS"

    def _compensate_inventory(self, item_id: str, quantity: int) -> None:
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity

    def _compensate_payment(self, customer: str, amount: float) -> None:
        self.payment_balance[customer] = self.payment_balance.get(customer, 0.0) + amount


class PolyglotPlatform:
    """Unified coordinator integrating OLTP, Cache, Search, Analytics, and CDC Relay."""

    def __init__(self) -> None:
        self.oltp = PostgresOLTPEngine()
        self.cache = RedisCacheEngine()
        self.search = SearchCatalogEngine()
        self.analytics = ColumnarAnalyticsEngine()
        self.processed_event_ids: set[int] = set()
        self.dead_letter_queue: list[dict[str, Any]] = []
        self._single_flight_in_progress: set[str] = set()

    def place_order(
        self,
        order_id: str,
        customer: str,
        total: float,
        description: str,
        embedding: list[float] | None = None,
    ) -> None:
        self.oltp.create_order(order_id, customer, total, description, embedding)

    def process_cdc_events(self, max_batch_size: int = 100, poison_predicate: Callable[[dict[str, Any]], bool] | None = None) -> int:
        """Processes unpublished outbox events with idempotency and DLQ quarantine."""
        events = list(self.oltp.outbox_events[:max_batch_size])
        self.oltp.outbox_events = self.oltp.outbox_events[max_batch_size:]

        processed_count = 0
        for event in events:
            eid = event["event_id"]

            # Idempotency deduplication check
            if eid in self.processed_event_ids:
                continue

            # Poison pill check
            if poison_predicate and poison_predicate(event):
                event["error"] = "Poison pill quarantined"
                self.dead_letter_queue.append(event)
                continue

            if event["event_type"] == "ORDER_CREATED":
                payload = event["payload"]
                oid = payload["order_id"]
                cust = payload["customer"]
                tot = payload["total"]
                desc = payload["description"]
                emb = payload.get("embedding", [0.1, 0.2, 0.3])

                # 1. Invalidate stale cache
                self.cache.invalidate(f"order:{oid}")
                # 2. Update real-time customer leaderboard
                self.cache.zadd_incr(cust, tot)
                # 3. Index in lexical catalog search and vector index
                self.search.index_document(oid, desc, payload, vector=emb)
                # 4. Ingest into columnar warehouse
                self.analytics.append_sale(tot, customer=cust, order_id=oid)

                self.processed_event_ids.add(eid)
                processed_count += 1

        return processed_count

    def get_order_cache_aside(self, order_id: str) -> dict[str, Any] | None:
        cache_key = f"order:{order_id}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        # Single-flight / cache stampede guard
        if cache_key in self._single_flight_in_progress:
            # Return current database state without duplicate stampede
            return self.oltp.get_order(order_id)

        self._single_flight_in_progress.add(cache_key)
        try:
            order = self.oltp.get_order(order_id)
            if order is not None:
                self.cache.set(cache_key, order)
            return order
        finally:
            self._single_flight_in_progress.discard(cache_key)

    def search_catalog(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        return self.search.search(query, top_k)

    def search_similar_orders(self, query_vector: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        return self.search.search_vector(query_vector, top_k)

    def get_analytics_summary(self) -> dict[str, float]:
        return {
            "total_revenue": self.analytics.sum_revenue(),
            "avg_order_value": self.analytics.avg_order_value(),
        }

    def get_customer_leaderboard(self, top_k: int = 5) -> list[tuple[str, float]]:
        return self.cache.ztop(top_k)

    def audit_reconciliation(self) -> tuple[bool, dict[str, float]]:
        """Audits consistency across OLTP, Analytics Warehouse, and Redis Leaderboard."""
        oltp_total = sum(o["total"] for o in self.oltp.orders.values())
        olap_total = self.analytics.sum_revenue()
        redis_total = sum(score for _, score in self.cache.leaderboard.items())

        balanced = math.isclose(oltp_total, olap_total, abs_tol=1e-3) and math.isclose(oltp_total, redis_total, abs_tol=1e-3)
        return balanced, {
            "oltp_total": oltp_total,
            "olap_total": olap_total,
            "redis_total": redis_total,
        }

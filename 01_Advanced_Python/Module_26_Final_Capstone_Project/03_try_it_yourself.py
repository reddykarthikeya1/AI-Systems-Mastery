"""Beginner playground for Module 26 - Final Capstone Project: Production Engine.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

# -------------------------------------------- 1. Domain Entity and Value Model
@dataclass
class Order:
    id: str
    total: float
    status: str = "created"

    def complete(self):
        if self.total <= 0:
            raise ValueError("Invalid order total")
        self.status = "completed"

order = Order("ord-001", 129.50)
assert order.status == "created"
order.complete()
assert order.status == "completed"
print(f"Order {order.id} transitioned to {order.status}.")

# -------------------------------------------- 2. In-Memory Repository Pattern
class OrderRepository:
    def __init__(self):
        self._storage: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._storage[order.id] = order

    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._storage.get(order_id)

repo = OrderRepository()
repo.save(order)
retrieved = repo.find_by_id("ord-001")
assert retrieved is not None
assert retrieved.total == 129.50
assert repo.find_by_id("missing") is None
print("Repository pattern retrieved stored entity.")

# -------------------------------------------- 3. End-to-End Service Layer Integration
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repo = repository

    def checkout(self, order_id: str, amount: float) -> Order:
        o = Order(id=order_id, total=amount)
        o.complete()
        self.repo.save(o)
        return o

service = OrderService(repo)
res_order = service.checkout("ord-002", 75.0)
assert res_order.status == "completed"
assert repo.find_by_id("ord-002") is not None
print("Capstone service layer checkout pipeline verified end-to-end.")

print()
print("All checks passed.")

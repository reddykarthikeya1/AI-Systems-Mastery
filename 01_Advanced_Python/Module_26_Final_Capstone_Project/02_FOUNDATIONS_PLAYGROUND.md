# 🐣 Interactive Foundations Playground: Final Capstone Project: Production Engine

> *"Production-grade software integrates clean architecture, repository patterns, and automated tests."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from dataclasses import dataclass
from typing import Dict, Optional
```

---

## 1. Domain Entity and Value Model

Domain entities encapsulate business identity and invariant validation rules.

```python
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
```

---

## 2. In-Memory Repository Pattern

The repository pattern abstracts data persistence behind a uniform collection interface.

```python
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
```

---

## 3. End-to-End Service Layer Integration

The service layer orchestrates business workflows across repositories.

```python
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
```

---

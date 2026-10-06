# LLD Case Study 6: Distributed Inventory Management System

> **Target Patterns:** Observer Pattern, Strategy Pattern, State Pattern  
> **Key Engineering Focus:** Stock level invariants, multi-warehouse fulfillment strategies, automatic replenishment alerts, and order lifecycle states.

---

## 1. Problem Statement & Functional Requirements

Design an enterprise inventory management backend supporting multi-warehouse fulfillment and low-stock alerts.

### Requirements:
1. **Multi-Warehouse Fulfillment (Strategy Pattern):** Route orders to warehouses based on customizable strategies (e.g. Nearest Warehouse First vs Consolidate into Single Shipment).
2. **Low Stock Alerts (Observer Pattern):** When stock for a SKU drops below its threshold, automatically trigger replenishment purchase orders.
3. **Order Inventory State Machine (State Pattern):** Orders transition from `Draft` $\rightarrow$ `StockReserved` $\rightarrow$ `Dispatched` $\rightarrow$ `Delivered` (or `Released` if canceled).
4. **Thread-Safe Inventory Mutations:** Prevent overselling under high concurrency.

---

## 2. Architecture & UML Class Diagram

```mermaid
classDiagram
    class InventoryObserver {
        <<interface>>
        +onLowStock(String sku, int currentQty, int threshold) void
    }

    class FulfillmentStrategy {
        <<interface>>
        +selectWarehouse(List~Warehouse~ warehouses, String sku, int qty) Warehouse
    }

    class Warehouse {
        +String warehouseId
        +String location
        +Map~String, int~ stock
        +reserveStock(String sku, int qty) bool
        +deductStock(String sku, int qty) void
    }

    class InventoryManager {
        -List~Warehouse~ warehouses
        -List~InventoryObserver~ observers
        -FulfillmentStrategy strategy
        +fulfillOrder(String orderId, String sku, int qty) bool
    }

    InventoryManager o-- Warehouse : Coordinates
    InventoryManager o-- FulfillmentStrategy : Fulfillment Strategy
    InventoryManager o-- InventoryObserver : Publishes Alerts
```

---

## 3. Production-Grade Python Implementation

```python
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# --- Observer Pattern: Replenishment Alerting ---
class StockAlertObserver(ABC):
    @abstractmethod
    def on_low_stock(self, warehouse_id: str, sku: str, current_quantity: int) -> None:
        pass

class ProcurementAlertService(StockAlertObserver):
    def on_low_stock(self, warehouse_id: str, sku: str, current_quantity: int) -> None:
        print(f"[Procurement Alert] Warehouse '{warehouse_id}': SKU '{sku}' low stock ({current_quantity} remaining)! Auto-generating PO.")

# --- Warehouse Entity ---
class Warehouse:
    def __init__(self, warehouse_id: str, city: str):
        self.warehouse_id = warehouse_id
        self.city = city
        self.inventory: Dict[str, int] = {}
        self.thresholds: Dict[str, int] = {}
        self.lock = threading.Lock()

    def set_stock(self, sku: str, quantity: int, threshold: int = 10):
        with self.lock:
            self.inventory[sku] = quantity
            self.thresholds[sku] = threshold

    def get_stock(self, sku: str) -> int:
        with self.lock:
            return self.inventory.get(sku, 0)

    def deduct(self, sku: str, quantity: int) -> tuple[bool, int]:
        with self.lock:
            available = self.inventory.get(sku, 0)
            if available < quantity:
                return False, available
            self.inventory[sku] = available - quantity
            return True, self.inventory[sku]

# --- Strategy Pattern: Fulfillment Routing ---
class FulfillmentStrategy(ABC):
    @abstractmethod
    def pick_warehouse(self, warehouses: List[Warehouse], customer_city: str, sku: str, qty: int) -> Optional[Warehouse]:
        pass

class NearestWarehouseStrategy(FulfillmentStrategy):
    def pick_warehouse(self, warehouses: List[Warehouse], customer_city: str, sku: str, qty: int) -> Optional[Warehouse]:
        # Filter warehouses that hold sufficient inventory
        capable = [w for w in warehouses if w.get_stock(sku) >= qty]
        if not capable:
            return None
        # Prioritize exact city match, otherwise first capable
        exact_match = next((w for w in capable if w.city.lower() == customer_city.lower()), None)
        return exact_match or capable[0]

# --- Inventory Central Manager ---
class InventoryManager:
    def __init__(self, strategy: FulfillmentStrategy):
        self.warehouses: List[Warehouse] = []
        self.strategy = strategy
        self.observers: List[StockAlertObserver] = []

    def add_warehouse(self, w: Warehouse):
        self.warehouses.append(w)

    def register_observer(self, obs: StockAlertObserver):
        self.observers.append(obs)

    def fulfill_order(self, customer_city: str, sku: str, qty: int) -> bool:
        warehouse = self.strategy.pick_warehouse(self.warehouses, customer_city, sku, qty)
        if not warehouse:
            print(f"[Fulfillment Error] Out of stock for SKU '{sku}' across all warehouses!")
            return False

        success, remaining = warehouse.deduct(sku, qty)
        if not success:
            return False

        print(f"[Fulfillment Success] Dispatched {qty} of '{sku}' from {warehouse.warehouse_id} ({warehouse.city}). Remaining: {remaining}")

        # Check threshold trigger
        if remaining <= warehouse.thresholds.get(sku, 10):
            for obs in self.observers:
                obs.on_low_stock(warehouse.warehouse_id, sku, remaining)
        return True

# --- Verification Driver ---
if __name__ == "__main__":
    manager = InventoryManager(strategy=NearestWarehouseStrategy())
    manager.register_observer(ProcurementAlertService())

    # Setup warehouses
    w_sf = Warehouse("WH-01", "San Francisco")
    w_sf.set_stock("MACBOOK-PRO-16", quantity=12, threshold=5)

    w_ny = Warehouse("WH-02", "New York")
    w_ny.set_stock("MACBOOK-PRO-16", quantity=25, threshold=5)

    manager.add_warehouse(w_sf)
    manager.add_warehouse(w_ny)

    # Order in SF: Should route to WH-01
    manager.fulfill_order(customer_city="San Francisco", sku="MACBOOK-PRO-16", qty=8)
    # Remaining in SF is 4 (triggers low stock observer!)
```


---

## 4. Edge Cases, Tests and Extensions

### Where the design is right and where it leaks

| Concern | Status | Detail |
| :--- | :--- | :--- |
| Overselling under concurrency | Safe | `deduct` checks and subtracts inside one lock, so two threads can never both take the last unit |
| Pick-then-deduct race | **Weak** | `pick_warehouse` reads stock without holding the lock; the winner can be drained before `deduct` runs, and `fulfill_order` then fails the whole order even though another warehouse could serve it |
| Low-stock alert | Fires after every deduction at or below the threshold | Alert storms: fire once per crossing, then re-arm when stock rises above the threshold |
| Multi-line orders | Not modelled | Reserve all lines or none; otherwise partial fulfilment strands stock |
| Reservations vs stock | Not modelled | Carts need a time-limited reservation, separate from on-hand quantity |

### Tests, including the race

The first test proves there is no overselling. The second reproduces the pick-then-deduct race deterministically, and shows the fix: try candidates in preference order until one deduction succeeds. This block extends the implementation above.

```python
# continues: inventory implementation above
import io, contextlib, threading

def quiet(fn, *a):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a)

# 1. No overselling: 20 racing orders for 1 unit each, 10 in stock
wh = Warehouse("W1", "Austin"); wh.set_stock("SKU", 10, threshold=0)
mgr = InventoryManager(NearestWarehouseStrategy()); mgr.add_warehouse(wh)
ok = []
ts = [threading.Thread(target=lambda: ok.append(quiet(mgr.fulfill_order, "Austin", "SKU", 1))) for _ in range(20)]
[t.start() for t in ts]; [t.join() for t in ts]
assert sum(ok) == 10 and wh.get_stock("SKU") == 0

# 2. The race: the chosen warehouse is drained between pick and deduct
class DrainAfterPick(NearestWarehouseStrategy):
    def pick_warehouse(self, warehouses, city, sku, qty):
        w = super().pick_warehouse(warehouses, city, sku, qty)
        w.deduct(sku, w.get_stock(sku))          # a competing order empties it
        return w

a, b = Warehouse("A", "Austin"), Warehouse("B", "Boston")
a.set_stock("SKU", 5); b.set_stock("SKU", 5)
m1 = InventoryManager(DrainAfterPick()); m1.add_warehouse(a); m1.add_warehouse(b)
assert quiet(m1.fulfill_order, "Austin", "SKU", 1) is False      # order lost although B has stock

# Fix: iterate over candidates in preference order
class RobustInventoryManager(InventoryManager):
    def fulfill_order(self, customer_city, sku, qty):
        ranked = sorted(self.warehouses, key=lambda w: w.city.lower() != customer_city.lower())
        for w in ranked:
            ok, remaining = w.deduct(sku, qty)
            if ok:
                if remaining <= w.thresholds.get(sku, 10):
                    for o in self.observers:
                        o.on_low_stock(w.warehouse_id, sku, remaining)
                return True
        return False

a2, b2 = Warehouse("A", "Austin"), Warehouse("B", "Boston")
a2.set_stock("SKU", 0); b2.set_stock("SKU", 5)
m2 = RobustInventoryManager(NearestWarehouseStrategy()); m2.add_warehouse(a2); m2.add_warehouse(b2)
assert quiet(m2.fulfill_order, "Austin", "SKU", 1) is True and b2.get_stock("SKU") == 4

# 3. Observer fires at the threshold
class Recorder(StockAlertObserver):
    def __init__(self): self.calls = []
    def on_low_stock(self, wid, sku, qty): self.calls.append((wid, sku, qty))
rec = Recorder(); w3 = Warehouse("W3", "Reno"); w3.set_stock("S", 6, threshold=5)
m3 = InventoryManager(NearestWarehouseStrategy()); m3.add_warehouse(w3); m3.register_observer(rec)
quiet(m3.fulfill_order, "Reno", "S", 1)
assert rec.calls == [("W3", "S", 5)]
print("inventory tests passed")
```

### Extensions interviewers ask for

1. **Reservations:** add `reserve(sku, qty, ttl)` that moves units from `available` to `reserved`; a background sweep returns expired reservations. Checkout converts a reservation into a deduction.
2. **Atomic multi-warehouse split orders:** if no single warehouse has 5 units, take 3 from one and 2 from another; do it as a two-phase reserve-then-commit so a failure rolls everything back.
3. **Database-backed stock:** replace the in-process lock with `UPDATE stock SET qty = qty - :n WHERE sku = :s AND qty >= :n` and check the affected row count; the database performs the same check-and-subtract atomically.
4. **Cheapest shipping instead of nearest:** swap the `FulfillmentStrategy`; nothing else changes, which is the point of the pattern.

### Follow-up questions

- *Why is a lock per warehouse better than one global lock?* Orders for different warehouses never contend; the cost is that cross-warehouse operations need a consistent lock order to avoid deadlock.
- *How do you stop alert storms?* Keep a per-SKU `alerted` flag, set it on the downward crossing, clear it when stock goes back above the threshold.
- *What changes when stock lives in a database?* The check-and-subtract moves into one SQL statement or a `SELECT ... FOR UPDATE` transaction; the in-memory lock disappears and idempotency keys on orders become the new concern.

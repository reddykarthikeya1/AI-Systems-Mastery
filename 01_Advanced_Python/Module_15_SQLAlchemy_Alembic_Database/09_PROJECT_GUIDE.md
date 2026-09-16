# Module_15_SQLAlchemy_Alembic_Database: Project Implementation Guide

**Deliverable:** an asynchronous relational database service built on SQLAlchemy 2.0, Mapped annotations, async sessions, and atomic order placement.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_inventory_db.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Declarative Mapped Models
Define `Customer`, `Product`, `Order`, and `OrderItem` using SQLAlchemy 2.0 `Mapped` and `mapped_column` annotations.

### Step 2 — Database Relationships
Establish bidirectional relationships (`relationship(back_populates=...)`) linking Customer to Orders and Orders to OrderItems.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_inventory_db.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Async Inventory Service
Implement `InventoryService` with methods `create_customer`, `add_product`, and `place_order`.

### Step 4 — Atomic Transactions & Eager Loading
In `place_order`, verify stock, decrement inventory, compute total amount, commit atomically, and eager load items via `selectinload`.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/inventory_db.py`, comment out the line that decrements product stock (`prod.stock -= qty`) in `place_order`.
Run:
```bash
pytest ../project_solution/test_inventory_db.py -k test_place_order_with_multiple_items_and_quantities -v
```
Watch the test fail when asserting decremented inventory stock, then restore the decrement logic.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_inventory_db.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Pessimistic Row Locking:** Add `with_for_update()` in order placement to prevent race conditions during checkout.
2. **Alembic Migration Suite:** Generate an Alembic migration script adding an `inventory_sku` unique index.
3. **Soft Delete Mixin:** Implement a reusable SQLAlchemy mixin adding `is_deleted` and `deleted_at`.
4. **Read Replica Routing:** Configure async engine routing queries to a read replica and writes to primary.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_create_customer_and_products` | Proves customers and products persist with primary keys |
| `test_place_order_decrements_inventory` | Proves orders decrement inventory and calculate totals |
| `test_place_order_insufficient_stock_raises_error` | Proves ordering more than available stock raises ValueError |
| `test_place_order_missing_product_raises_value_error` | Proves non-existent product IDs raise ValueError |
| `test_customer_orders_relationship` | Proves customer relationship eager loads associated orders |

---

## 🎓 You have mastered this module when you can…

- [ ] Write modern SQLAlchemy 2.0 models using DeclarativeBase and Mapped annotations
- [ ] Configure async database engines and sessionmakers using aiosqlite or asyncpg
- [ ] Manage database transaction lifecycles using async with session.begin():
- [ ] Prevent N+1 query performance traps using selectinload and joinedload
- [ ] Implement foreign keys, unique constraints, and cascade delete options
- [ ] Handle concurrency conflicts and row locking in high-throughput transactions
- [ ] Write async unit tests verifying database state using in-memory SQLite

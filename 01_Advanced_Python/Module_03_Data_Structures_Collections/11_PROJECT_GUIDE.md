# Module_03_Data_Structures_Collections: Project Implementation Guide

**Deliverable:** an algorithmic limit order matching engine using heaps, deques, and dictionaries to achieve price-time priority matching.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_matching_engine.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Order Domain Model
Define slotted `Order` and `Trade` dataclasses with price, quantity, timestamp, and order type.

### Step 2 — Priority Queues
Implement buy book (max-heap) and sell book (min-heap) using `heapq` and negate buy prices for max-heap ordering.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_matching_engine.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Limit Order Matching Core
Implement `process_order` matching crossing prices (`bid >= ask`) at resting order prices and generating `Trade` records.

### Step 4 — Depth and Volume Summaries
Implement `get_depth` aggregating resting volume at each distinct price level.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/matching_engine.py`, remove the minus sign from the buy order heap push (`-order.price`).
Run:
```bash
pytest ../project_solution/test_matching_engine.py -k test_matching_engine_time_priority -v
```
Watch the test fail as bids match lowest-price first instead of highest-price first, then restore the negation.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_matching_engine.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Iceberg Orders:** Implement hidden quantity orders that replenish visible quantity on fill.
2. **Stop-Loss Triggers:** Add a trigger order queue executing limit orders once market price reaches threshold.
3. **Order Modification:** Implement in-place price/quantity amendments without losing queue priority.
4. **Market Data Streaming:** Implement a generator yielding Level 2 market data updates.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_matching_engine_basic` | Proves matching engine executes trades when prices cross |
| `test_matching_engine_time_priority` | Proves FIFO time priority at identical price levels |
| `test_matching_engine_partial_fills` | Proves residual order volume remains resting in book |
| `test_matching_engine_volume_tracking` | Proves cumulative traded volume matches executed quantities |
| `test_matching_engine_empty_depth` | Proves empty book depth queries return empty collections safely |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the time complexity of list, dict, set, deque, and heapq operations
- [ ] Implement a max-heap in Python using heapq with negated priority keys
- [ ] Avoid mutating collections during active iteration
- [ ] Use __slots__ on data structures to optimize memory consumption
- [ ] Implement price-time priority matching algorithms
- [ ] Explain how Python handles hash collisions under the hood
- [ ] Audit data structure pipelines for shallow copy reference sharing traps

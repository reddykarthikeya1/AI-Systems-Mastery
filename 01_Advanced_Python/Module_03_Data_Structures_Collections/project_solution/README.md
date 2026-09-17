# Design Rationale: High-Frequency Order Book Matching Engine

## Architectural Overview
An in-memory financial order book matching continuous buy and sell limit orders using priority heaps (`heapq`), compact lookup tables, and fast FIFO fill queues (`collections.deque`).

## Key Design Decisions
1. **Dual Priority Heaps for Order Matching:** Buy orders are structured as a max-heap (via negative prices) and sell orders as a min-heap, guaranteeing $O(1)$ best-bid-offer lookups and $O(\log N)$ insertions.
2. **`collections.deque` for Price-Level Queues:** Multiple orders at the identical price level are stored in deques, ensuring strict FIFO priority matching in $O(1)$ time per fill without array-shifting penalties.
3. **Integer Penny Pricing:** All currency values are stored as integer pennies, completely eliminating IEEE 754 floating-point rounding errors during financial execution.

## Rejected Alternatives
1. **Sorting Python Lists on Every Order Insertion:**
   - *Reason for Rejection:* Sorting an array on each incoming order requires $O(N \log N)$ operations, saturating CPU at 500 orders/second compared to $O(\log N)$ heap push.
2. **Using Python `list.pop(0)` for Order FIFO Queues:**
   - *Reason for Rejection:* `list.pop(0)` shifts all subsequent pointers in memory ($O(N)$), causing quadratic degradation under high transaction volume.

## Invariants & Guarantees
- Price-time priority strictly maintained across all trades.
- No partial execution leaves orphan dangling bids with non-positive volume.

## Verification
```bash
pytest test_matching_engine.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |


# Phase 1 Checkpoint Exam: Python Systems Foundations

> **Phase Scope:** Modules 00–03 (Tooling, Fundamentals, Functions & Closures, Data Structures)  
> **Allocated Time:** 90 Minutes  
> **Format:** Closed-solution, test-driven timed build challenge.

---

## 🎯 The Exam Mission: High-Frequency Limit Order Book

You are tasked with building a high-throughput, memory-bounded, in-memory Limit Order Book matching engine for an algorithmic trading desk. The system receives buy/sell orders, maintains price-time priority queues, matches crossing orders, and tracks portfolio cash and position balances without using any third-party libraries.

### Constraints & Invariants
1. **Zero External Dependencies:** Only Python standard library (`collections`, `heapq`, `dataclasses`, `enum`, `typing`).
2. **Numeric Precision:** Never compare floating point currency values with direct `==`. Use integer cents or `math.isclose`.
3. **Immutability & Encapsulation:** Order IDs and timestamps must be immutable once created.
4. **Time Complexity:** 
   - Insert Order: \(O(\log N)\) or better.
   - Match Highest/Lowest Priority: \(O(1)\) best price lookup.
   - Cancel Order: \(O(1)\) lookup and tombstone flag.

---

## 📋 Functional Requirements

### 1. Domain Types (`order_book.py`)
- `OrderType`: Enum with `BUY` (bid) and `SELL` (ask).
- `Order`: Immutable dataclass or slotted class with `order_id: str`, `trader_id: str`, `order_type: OrderType`, `price_cents: int`, `qty: int`, `timestamp: float`.
- `Trade`: Slotted dataclass recording `trade_id: str`, `buy_order_id: str`, `sell_order_id: str`, `price_cents: int`, `qty: int`.

### 2. State Encapsulation via Closures / Slotted State
Implement `create_trader_portfolio(initial_cash_cents: int)` returning a tuple of functions:
- `get_balance() -> dict[str, int]` (cash and security inventory)
- `execute_trade(order_type: OrderType, price_cents: int, qty: int) -> None`
- `is_solvent() -> bool` (cash >= 0 and position >= 0)

### 3. Matching Engine Core
Class `LimitOrderBook`:
- `add_order(order: Order) -> list[Trade]`: Matches immediately if bid >= ask; otherwise rests in book.
- `cancel_order(order_id: str) -> bool`: Returns `True` if cancelled, `False` if already filled or missing.
- `get_spread() -> tuple[int | None, int | None]`: Returns `(highest_bid, lowest_ask)`.
- `depth_summary() -> dict[str, int]`: Aggregates total volume per active price level.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Tooling & Hygiene** | Python 3.11+ type hints, clean AST, no shadowed builtins, isolated virtualenv | 15 pts |
| **Order Book Logic** | Correct price-time priority matching; crossing orders execute at resting price | 25 pts |
| **State & Closures** | Closures completely encapsulate trader balances; zero state leakage | 20 pts |
| **Data Structure Efficiency** | Heap or deque usage guarantees \(O(\log N)\) inserts, no dict mutation during loops | 20 pts |
| **Edge Cases & Invariants** | Partial fills handled; zero/negative orders rejected; cancelled orders ignored | 20 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 2.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_00_Environment_Tooling_Workflow \
      Module_01_Python_Fundamentals \
      Module_02_Functions_Scopes_Closures \
      Module_03_Data_Structures_Collections \
      -q

python tools/check_links.py --quiet
ruff check .
```

If any of that is red, fix it first. The exam assumes a working environment.

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer. When it ends, stop and submit what you have. |
| **No solution exists** | There is deliberately no reference implementation for this exam. The rubric is the specification. |
| **Modules are open-book** | Re-read any README, demo or troubleshooting guide. That is not cheating; it is what the job looks like. |
| **`project_solution/` is closed-book** | Do not read the module solutions during the exam. Copying them measures nothing. |
| **Write your own tests** | Untested code scores zero on the correctness criteria, however elegant it looks. |
| **Working beats complete** | A subset that runs and is tested outscores a full implementation that does not import. |

---

## 🔬 Self-Verification Harness

Produce this evidence before you score yourself. An unmeasured claim earns no
points.

```bash
# 1. It imports and runs at all
python -m your_solution            # must not traceback

# 2. Your tests pass
pytest your_tests.py -v            # paste the summary line

# 3. It is clean
ruff check .
mypy --strict your_solution.py     # advisory, but note the count

# 4. Coverage of your own code
pytest --cov=your_solution --cov-report=term-missing
```

Record the four outputs. The rubric below is scored against **evidence**, not
against intent.

---

## ⏱️ If You Run Out of Time

Score what exists and be honest about the gap. Partial credit is real:

1. **Submit the working subset.** Delete or clearly comment out anything that
   does not run — a broken import costs you every point in the file.
2. **Write down what is missing**, in one line per requirement. Naming your own
   gap accurately is itself a senior skill and earns the analysis criteria.
3. **Keep your tests.** Tests for the parts you finished are worth more than
   untested code for the parts you did not.

---

## 🔁 If You Score Below the Threshold

This is diagnostic information, not a verdict. Do exactly this:

1. Identify which **rubric row** you lost the most points on.
2. Go back to: **Modules 01–03 READMEs, then their `debug_lab/` directories**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 00–03 taught you a set of tools. This exam tests **whether you can build a small program from nothing and reason about what Python does with your data**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.

# Design Rationale: Async E-Commerce Inventory & Order Ledger Database

## Architectural Overview
A modern relational persistence layer built on SQLAlchemy 2.0 and Alembic, implementing async sessions, typed `Mapped[]` declarations, and eager loading to eliminate $N+1$ queries.

## Key Design Decisions
1. **SQLAlchemy 2.0 Declarative Mapping:** Models use typed `Mapped[int] = mapped_column()` syntax, enabling full static type checking with Mypy and clean DDL schema generation.
2. **`selectinload` for Relationship Traversal:** Related entities (Orders and Customers) are eagerly resolved using `selectinload()`, executing in exactly 2 optimized SQL queries and preventing $N+1$ query cascades.
3. **Isolated Session Scoping (`async_sessionmaker`):** Each concurrent async request acquires an independent session instance with `expire_on_commit=False`, avoiding cross-task data corruption.

## Rejected Alternatives
1. **Implicit Lazy Loading in Async Code:**
   - *Reason for Rejection:* In async SQLAlchemy, accessing an unloaded relationship attribute outside an active awaitable query raises a fatal `DetachedInstanceError`.
2. **Using `joinedload` on Multiple Large One-to-Many Relationships:**
   - *Reason for Rejection:* `joinedload` generates a massive Cartesian product of joined rows, consuming huge network bandwidth and server RAM compared to `selectinload`.

## Invariants & Guarantees
- All database operations are non-blocking and awaitable.
- Order placements decrement stock atomically within isolated database transactions.

## Verification
```bash
pytest test_inventory_db.py -v
```

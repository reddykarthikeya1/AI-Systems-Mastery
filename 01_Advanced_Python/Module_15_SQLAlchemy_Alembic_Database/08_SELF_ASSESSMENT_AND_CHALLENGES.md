# Module 15: Self-Assessment Quiz & Mastery Challenges

Test your understanding of SQLAlchemy 2.0, async databases, and relationship mapping before moving to **Module 14**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **ACID Properties:** What do the four letters in ACID stand for in relational database transactions?
2. **2.0 Declarative Syntax:** What are the benefits of using `Mapped[int]` and `mapped_column()` over legacy `Column(Integer)` in SQLAlchemy 2.0?
3. **The $N+1$ Problem:** Explain the $N+1$ query problem and why it causes extreme database slowdowns.
4. **Eager Loading Strategies:** What is the mechanical difference between `selectinload` and `joinedload`?
5. **Async Attribute Expiration:** Why is `expire_on_commit=False` critical when defining an `async_sessionmaker`?
6. **Query Result Parsing:** What is the difference between `result.scalars().all()`, `result.scalar_one()`, and `result.scalar_one_or_none()`?
7. **Database Migrations:** What is the role of Alembic, and how does `alembic revision --autogenerate` detect schema changes?
8. **Referential Integrity:** How does a `ForeignKey` constraint protect database relationships from orphan rows?
9. **Transaction Rollback:** If an exception occurs inside an `async with session.begin():` block, what happens to uncommitted database changes?
10. **Async SQLite Driver:** What Python driver package enables asynchronous operations with SQLite databases in SQLAlchemy?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **Atomicity:** All operations in a transaction succeed or all roll back (all-or-nothing).
- **Consistency:** Data remains valid according to all schema rules and constraints.
- **Isolation:** Concurrent transactions do not interfere with each other.
- **Durability:** Committed data is permanently stored on non-volatile disk.

#### Answer 2:
It provides 100% full static type checking with Mypy/Pyright, autocompletion in IDEs, and removes ambiguity between Python types and database SQL types.

#### Answer 3:
Querying $N$ parent rows and then executing 1 separate SQL query per row to load its children results in $1 + N$ total queries. For 1,000 users, this executes 1,001 queries instead of 1 or 2 optimized queries.

#### Answer 4:
- `selectinload`: Emits a second `SELECT ... WHERE parent_id IN (...)` query (best for 1-to-many collections).
- `joinedload`: Performs an SQL `LEFT OUTER JOIN` in a single query (best for many-to-1 relationships).

#### Answer 5:
It prevents model attributes from expiring on commit, allowing objects to be read in Python memory without triggering unauthorized background async I/O.

#### Answer 6:
- `scalars().all()`: Returns a list of all matching model instances.
- `scalar_one()`: Returns exactly 1 instance, raising an exception if 0 or $>1$ exist.
- `scalar_one_or_none()`: Returns 1 instance or `None` if no match is found.

#### Answer 7:
Alembic tracks versioned migration scripts and compares declarative Python metadata against live database catalogs to generate automated `ALTER TABLE` statements.

#### Answer 8:
It ensures that foreign keys must match existing primary keys in the referenced table, rejecting insertions with invalid references.

#### Answer 9:
The transaction is automatically **rolled back (`ROLLBACK`)**, leaving the database in its exact state prior to the transaction.

#### Answer 10:
**`aiosqlite`**.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Async Aggregate Revenue Query

**Goal:** Write an async function that calculates total sales across all orders using `func.sum()` in SQLAlchemy 2.0.

<details>
<summary><b>Solution Code</b></summary>

```python
import asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]

async def get_total_revenue(session: AsyncSession) -> float:
    stmt = select(func.coalesce(func.sum(Order.amount), 0.0))
    result = await session.execute(stmt)
    return float(result.scalar_one())
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. N+1 query

```python
users = session.execute(select(User)).scalars().all()
for user in users:
    print(user.name, len(user.orders))     # lazy relationship
```

**Observed symptom:** Loading 500 users issues 501 queries and the endpoint takes 4 s.

**(a)** Where does the 501st query come from?

**(b)** Name two loader strategies that fix it and when each is better.

**(c)** How would you detect this automatically in CI?

<details>
<summary><b>Show the diagnosis</b></summary>

One query fetches the users; then accessing `user.orders` triggers a **separate lazy-load query per user** — 1 + 500.

**Two strategies:** `selectinload(User.orders)` issues a second query with `WHERE user_id IN (...)` — two queries total, and the best default for one-to-many. `joinedload(User.orders)` uses a single LEFT JOIN — one query, but it multiplies rows and can be slower for large collections. Use `joinedload` for many-to-one, `selectinload` for one-to-many.

**Detect in CI:** count queries in a test. Attach an event listener to `before_cursor_execute` and assert the count is below a threshold, or use `sqlalchemy.event` with a fixture that fails the test above N queries. A query-count assertion is a performance test that never flakes, unlike a timing one.

</details>

---

### D2. Async engine with a sync driver

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite:///app.db")
```

**Observed symptom:** `InvalidRequestError: The asyncio extension requires an async driver to be used.`

**(a)** What is wrong with the URL?

**(b)** What are the correct URLs for SQLite and PostgreSQL?

**(c)** Why can't SQLAlchemy just wrap the sync driver for you?

<details>
<summary><b>Show the diagnosis</b></summary>

The URL selects the **default synchronous DBAPI** (`sqlite3`). An async engine needs an async driver.

**Correct:** `sqlite+aiosqlite:///app.db` and `postgresql+asyncpg://user:pw@host/db`.

**Why not wrap it:** a sync driver blocks the calling thread on every network round trip. Wrapping it in a threadpool *is* possible — that is essentially what `run_in_executor` does — but it gives you thread-per-query concurrency, not event-loop concurrency, so you lose the entire scalability benefit while keeping all of `asyncio`'s complexity. SQLAlchemy refuses explicitly rather than let you build something that looks async and performs worse than sync code.

</details>

---

### D3. Session shared across requests

```python
from sqlalchemy.orm import Session

session = Session(engine)          # module level

def get_user(user_id: int):
    return session.get(User, user_id)
```

**Observed symptom:** Under concurrent load: `InvalidRequestError: This session is provisionally in a transaction`, random `DetachedInstanceError`, and occasionally one request seeing another's uncommitted data.

**(a)** Why is a module-level Session wrong?

**(b)** What is the correct lifecycle, and how do you wire it in FastAPI?

**(c)** What is the difference between the Session and the connection pool here?

<details>
<summary><b>Show the diagnosis</b></summary>

A `Session` is a **unit of work** holding an identity map and a transaction. It is explicitly *not* thread-safe or task-safe. Sharing one means concurrent requests interleave in the same transaction.

**Correct lifecycle:** one session per request, created at the start and closed at the end. In FastAPI:

```python
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
```

then `session: AsyncSession = Depends(get_session)`.

**Session vs pool:** the *engine* owns a connection pool and **is** meant to be shared and module-level — creating an engine per request would destroy pooling. The session is the short-lived thing. Confusing the two is the root of this bug: share the engine, never the session.

</details>

---

### D4. Alembic autogenerate misses a change

```python
# models.py
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)      # newly added
```

**Observed symptom:** `alembic revision --autogenerate` produces an empty migration.

**(a)** Name three reasons autogenerate produces nothing.

**(b)** What must `env.py` contain?

**(c)** Which schema changes can autogenerate *never* detect?

<details>
<summary><b>Show the diagnosis</b></summary>

**Three causes:** (1) `target_metadata` in `env.py` is `None` or points at the wrong `Base`; (2) the module defining `User` was never imported, so it is not in the metadata; (3) the database is already at that state, so there is genuinely no diff.

**`env.py` needs:** `from myapp.models import Base` and `target_metadata = Base.metadata`, with every model module imported (often via the package `__init__`).

**Never detected:** server-side defaults changes, constraint *name* changes, `CHECK` constraints, most index option changes, enum value additions, and anything requiring data migration. Autogenerate is a **draft**, not an authority — always read the generated migration and always test the downgrade path.

</details>

---

### D5. Commit without refresh

```python
new_user = User(email="a@b.c")
session.add(new_user)
session.commit()
print(new_user.id)
```

**Observed symptom:** In some configurations, printing `new_user.id` issues a surprise SELECT; in others it raises `DetachedInstanceError`.

**(a)** What does `commit()` do to the instance's attributes?

**(b)** How do you get the generated id efficiently?

**(c)** What does `expire_on_commit=False` change, and what is its risk?

<details>
<summary><b>Show the diagnosis</b></summary>

By default `commit()` **expires** every attribute on every instance in the session. The next attribute access triggers a refresh SELECT — and if the session is already closed, a `DetachedInstanceError` instead.

**Get the id efficiently:** `session.flush()` before commit — the INSERT executes and the primary key is populated without ending the transaction. Or `session.refresh(new_user)` afterwards, or use `returning()` on the insert.

**`expire_on_commit=False`** keeps attributes loaded after commit, which is the usual choice for async sessions (where an implicit lazy refresh cannot happen inside a sync attribute access). The risk is **staleness**: your in-memory object no longer reflects concurrent changes by other transactions, and you will not be told.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.

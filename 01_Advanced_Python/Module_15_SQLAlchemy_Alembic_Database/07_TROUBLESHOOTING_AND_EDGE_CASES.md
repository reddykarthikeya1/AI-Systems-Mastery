# Module 15: Troubleshooting, SQLAlchemy Traps & MissingGreenlet Errors

This reference guide details common database pitfalls when building asynchronous applications with SQLAlchemy 2.0.

---

## 1. `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called`

### The Bug
```python
async with session_factory() as session:
    user = (await session.execute(select(User))).scalar_one()
    # Accessing relationship without eager loading:
    print(user.posts) # ❌ MissingGreenlet crash!
```

### Why It Happens
In synchronous SQLAlchemy, accessing `user.posts` triggers a hidden background SQL query to fetch related posts. In async Python, background I/O cannot happen transparently without `await`.

### The Fix
Always use **`selectinload`** (or `joinedload`) in your query statement:
```python
stmt = select(User).options(selectinload(User.posts))
user = (await session.execute(stmt)).scalar_one()
print(user.posts) # ✅ Works cleanly!
```

---

## 2. `expire_on_commit=False` in Async Session Factories

### The Gotcha
By default, SQLAlchemy expires all model attributes after `await session.commit()`. If you access `user.username` after the session closes, it tries to re-query the database and crashes.

### The Fix
Always configure `expire_on_commit=False` when constructing `async_sessionmaker`:
```python
session_factory = async_sessionmaker(engine, expire_on_commit=False)
```

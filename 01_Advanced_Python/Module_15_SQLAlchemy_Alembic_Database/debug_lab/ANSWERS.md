# Debug Lab Answers: Module 15

<details>
<summary>Bug 1: Uncommitted session transaction</summary>

### Root Cause
SQLAlchemy sessions run inside a transaction by default. If the session closes without `commit()`, SQLite automatically issues a `ROLLBACK`.

### Fix
Explicitly call `await session.commit()` or use `async with session.begin():`:
```python
async with session_factory() as session:
    async with session.begin():
        session.add(Product(sku="SKU-999"))
```
</details>

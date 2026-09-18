# Debug Lab Solution & Forensic Post-Mortem

## Incident: Dual-Write Inconsistency Between Relational DB and Redis Cache

---

### 🔍 Forensic Root Cause Analysis
`update_price()` issues two independent, uncoordinated writes -- one to the
database, one to the cache -- over the same unreliable network, with no
transaction or shared outcome linking them. When the network drops the second
call (the cache write), the caller has no signal that anything went wrong: the
database now holds the new price while the cache still serves the old one,
and nothing will ever retry or reconcile the dropped write. The two stores
diverge permanently.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def update_price_via_cdc(db, cache, sku, new_price):
    """Single source of truth: write only to the database, and let a
    change-data-capture stream (or cache invalidation, not re-population)
    propagate the change to the cache asynchronously and reliably."""
    db.rows[sku] = new_price          # the only write the caller performs
    outbox.publish("price_changed", {"sku": sku, "price": new_price})
    # a durable, retrying consumer applies this event to the cache --
    # or simpler: the consumer just invalidates the key and lets the
    # next read repopulate it from the database.
```

The durable fix is architectural: never perform two independent writes to two
systems and call it done. Use the database as the single source of truth with
an outbox/CDC pipeline to propagate changes, or invalidate (don't repopulate)
the cache and let reads repair it from the database.

---

### 🛡️ Production Prevention Invariants
1. **One source of truth per fact**; every other store is a reconstructible
   projection, never a peer written independently.
2. **Outbox pattern / CDC** for propagating changes across stores reliably,
   instead of sequential uncoordinated writes from the request path.
3. **Cache invalidate-then-lazy-reload**, not invalidate-then-immediately-rewrite,
   so a dropped propagation self-heals on the next read.

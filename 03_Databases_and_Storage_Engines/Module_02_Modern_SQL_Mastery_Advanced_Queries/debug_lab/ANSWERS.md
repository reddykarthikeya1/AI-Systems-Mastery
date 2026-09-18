# Debug Lab Solution & Forensic Post-Mortem

## Incident: Running Total Generates Identical Duplicate Numbers on Duplicate Dates

---

### 🔍 Forensic Root Cause Analysis
`running_total()` computes each row's peer group (every row sharing the same
`sale_date`) and adds the *whole group's* amount at once, then assigns that
same cumulative value to every row in the group. This mirrors a `SUM(amount)
OVER (ORDER BY sale_date)` window in SQL, which defaults to a `RANGE` frame:
`RANGE` frames are defined by peer values, not physical row position, so every
row that shares an `ORDER BY` key sees an identical running total.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def running_total_rows_frame(rows: list[tuple[str, int]]) -> list[int]:
    """Equivalent to SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN
    UNBOUNDED PRECEDING AND CURRENT ROW) -- each physical row gets its own total."""
    totals = []
    running = 0
    for _date, amount in rows:
        running += amount
        totals.append(running)
    return totals
```

In SQL, the fix is to make the frame explicit:
```sql
SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

---

### 🛡️ Production Prevention Invariants
1. **Always specify the frame explicitly** (`ROWS` vs `RANGE`) on any window
   function whose `ORDER BY` key can contain duplicates.
2. **Regression fixtures with duplicate keys:** every window-function test
   suite must include at least one duplicate-key case.
3. **Code review checklist:** flag any `OVER (ORDER BY ...)` with no explicit
   frame clause during review.

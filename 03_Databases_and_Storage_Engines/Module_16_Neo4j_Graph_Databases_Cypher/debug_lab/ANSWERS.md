# Debug Lab Solution & Forensic Post-Mortem

## Incident: Cartesian Product OutOfMemoryError in Cypher Path Match

---

### 🔍 Forensic Root Cause Analysis
`match_missing_relationship()` matches `Person` and `Company` as two entirely
independent node scans joined only by a `WHERE` filter on `city`, with no
graph relationship (edge) connecting them in the `MATCH` pattern itself. The
query planner has no edge to traverse, so it must materialize every possible
`(person, company)` pair -- a full Cartesian product -- before the `WHERE`
clause can even be applied. With 300 people and 300 companies that is 90,000
pairs held in memory to filter down to what a real `WORKS_AT` traversal would
have found directly in 50 steps.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def match_with_relationship(self):
    """Follows the real WORKS_AT edge instead of an unrelated node scan,
    so the planner only ever visits pairs that are actually connected."""
    return [
        (pid, cid) for pid, cid in self.works_at
        if self.person_city(pid) == self.company_city(cid)
    ]
```

In Cypher: `MATCH (a:Person)-[:WORKS_AT]->(b:Company) WHERE a.city = b.city`
instead of `MATCH (a:Person), (b:Company) WHERE a.city = b.city`.

---

### 🛡️ Production Prevention Invariants
1. **Never comma-separate two `MATCH` patterns** unless a Cartesian product is
   genuinely intended (and bounded).
2. **`EXPLAIN`/`PROFILE` every Cypher query in review**, flagging any
   `CartesianProduct` operator.
3. **Cardinality guardrails** in the driver/middleware that reject queries
   whose estimated row count exceeds a safety threshold.

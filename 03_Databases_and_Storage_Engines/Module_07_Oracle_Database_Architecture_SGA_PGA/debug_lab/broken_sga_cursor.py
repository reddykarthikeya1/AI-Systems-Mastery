"""DEBUG LAB: ORA-04031 Shared Pool Out of Memory via Literal SQL

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class SharedPool:
    """A toy Library Cache with a fixed number of cursor slots."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[str, object] = {}
        self.evictions = 0

    def _store(self, sql: str) -> None:
        if sql in self.cache:
            return
        if len(self.cache) >= self.capacity:
            self.cache.pop(next(iter(self.cache)))
            self.evictions += 1
        self.cache[sql] = object()

    def parse_literal(self, emp_id: int) -> None:
        sql = f"SELECT * FROM emp WHERE id = {emp_id}"  # literal baked into the text
        self._store(sql)

    def parse_bind(self, emp_id: int) -> None:
        sql = "SELECT * FROM emp WHERE id = :emp_id"  # one shared, sharable statement
        self._store(sql)

def reproduce_defect() -> None:
    print("Running 5,000 employee lookups through a 1,000-slot shared pool...")
    literal_pool = SharedPool(capacity=1000)
    for emp_id in range(5000):
        literal_pool.parse_literal(emp_id)

    bind_pool = SharedPool(capacity=1000)
    for emp_id in range(5000):
        bind_pool.parse_bind(emp_id)

    print(f"Cursor evictions with literal SQL: {literal_pool.evictions}")
    print(f"Cursor evictions with bind variables: {bind_pool.evictions}")
    if literal_pool.evictions > 0 and bind_pool.evictions == 0:
        print("[DEFECT OBSERVED] Every lookup hard-parses a brand-new, unsharable "
              "statement, churning the shared pool instead of reusing one plan.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()

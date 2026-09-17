"""Problem 01 — Deterministic Audit Trigger

Topic: 08 Oracle PLSQL Packages Triggers
Target: Production-grade implementation

Record state changes in audit trail for INSERT/UPDATE/DELETE events.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def deterministic_audit_trigger(event_type: str, old_row: dict | None, new_row: dict | None) -> dict:
    """Return audit dict:
    - 'action': event_type ('INSERT', 'UPDATE', 'DELETE')
    - 'delta': dict of changed fields {field: (old_val, new_val)}
    - 'timestamp_token': 'DETERMINISTIC_COMMIT'
    """
    raise NotImplementedError("Implement deterministic_audit_trigger")

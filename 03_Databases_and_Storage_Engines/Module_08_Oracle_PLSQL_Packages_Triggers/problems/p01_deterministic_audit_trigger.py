"""Problem 01 — Deterministic Audit Trigger

Topic: 08 Oracle PLSQL Packages Triggers
Target: Production-grade implementation

Record state changes in audit trail for INSERT/UPDATE/DELETE events.

Example:
    >>> deterministic_audit_trigger(
    ...     'UPDATE', {'salary': 5000, 'dept': 'Eng'}, {'salary': 6000, 'dept': 'Eng'}
    ... )
    {'action': 'UPDATE', 'delta': {'salary': (5000, 6000)}, 'timestamp_token': 'DETERMINISTIC_COMMIT'}

Hints:
    Hint 1: The three event types don't share one delta rule — INSERT only
        has a "new" side, DELETE only has an "old" side, and UPDATE is the
        only case that actually compares two rows field by field.
    Hint 2: Build delta as a dict comprehension over new_row's items for
        INSERT and old_row's items for DELETE; for UPDATE, iterate the union
        of both rows' keys (set(old) | set(new)) and compare old.get(k) to
        new.get(k).
    Hint 3: UPDATE's delta must include only fields whose value actually
        changed — an unchanged field like 'dept' above must NOT appear in
        delta even though it's present in both rows — and old_row/new_row
        can be None, which should be treated as an empty dict rather than
        raising on .items() or .get().
"""

from __future__ import annotations


def deterministic_audit_trigger(event_type: str, old_row: dict | None, new_row: dict | None) -> dict:
    """Return audit dict:
    - 'action': event_type ('INSERT', 'UPDATE', 'DELETE')
    - 'delta': dict of changed fields {field: (old_val, new_val)}
    - 'timestamp_token': 'DETERMINISTIC_COMMIT'
    """
    raise NotImplementedError("Implement deterministic_audit_trigger")

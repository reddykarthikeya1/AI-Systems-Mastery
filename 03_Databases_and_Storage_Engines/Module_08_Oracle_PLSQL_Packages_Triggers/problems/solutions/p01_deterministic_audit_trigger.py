"""Reference Solution — Problem 01: Deterministic Audit Trigger

Topic: 08 Oracle PLSQL Packages Triggers
"""

from __future__ import annotations


def deterministic_audit_trigger(event_type: str, old_row: dict | None, new_row: dict | None) -> dict:
    delta = {}
    if event_type == 'INSERT':
        delta = {k: (None, v) for k, v in (new_row or {}).items()}
    elif event_type == 'DELETE':
        delta = {k: (v, None) for k, v in (old_row or {}).items()}
    elif event_type == 'UPDATE':
        old = old_row or {}
        new = new_row or {}
        for k in set(old) | set(new):
            if old.get(k) != new.get(k):
                delta[k] = (old.get(k), new.get(k))
    return {
        'action': event_type,
        'delta': delta,
        'timestamp_token': 'DETERMINISTIC_COMMIT'
    }

"""Problem 01 — Change Data Capture Sync

Topic: 25 Final Capstone Polyglot Enterprise
Target: Production-grade implementation

Materialize idempotent real-time CDC updates into read-optimized aggregate view.

Example:
    >>> events = [
    ...     {'op': 'UPDATE', 'account_id': 'A1', 'amount': 150.0, 'seq': 2},
    ...     {'op': 'INSERT', 'account_id': 'A1', 'amount': 100.0, 'seq': 1},
    ...     {'op': 'DELETE', 'account_id': 'A2', 'seq': 3},
    ... ]
    >>> change_data_capture_sync(events, {'A2': 50.0})
    {'A1': 150.0}

Hints:
    Hint 1: CDC events can arrive out of order (note seq=2 listed before
        seq=1 above), so the input list's order is not the order to apply
        them in — "idempotent real-time sync" means the final state must
        depend only on logical sequence, not arrival order.
    Hint 2: Sort cdc_events by their 'seq' field first, then fold them one
        at a time into a copy of existing_view, dispatching on 'op' with a
        plain dict assignment or dict.pop.
    Hint 3: INSERT and UPDATE behave identically here (both just set
        view[account_id] = amount), DELETE removes the key entirely (use
        pop with a default so deleting an account not currently in the view
        doesn't raise), and the events list, once sorted by seq, must be
        replayed in full even though it was given out of seq order.
"""

from __future__ import annotations


def change_data_capture_sync(cdc_events: list[dict], existing_view: dict[str, float]) -> dict[str, float]:
    """cdc_events: list of {'op': 'INSERT'|'UPDATE'|'DELETE', 'account_id': str, 'amount': float, 'seq': int}.
    Apply events in ascending 'seq' order.
    Returns updated view mapping account_id -> final balance.
    """
    raise NotImplementedError("Implement change_data_capture_sync")

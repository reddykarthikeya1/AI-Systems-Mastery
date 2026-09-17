"""Problem 01 — Change Data Capture Sync

Topic: 25 Final Capstone Polyglot Enterprise
Target: Production-grade implementation

Materialize idempotent real-time CDC updates into read-optimized aggregate view.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def change_data_capture_sync(cdc_events: list[dict], existing_view: dict[str, float]) -> dict[str, float]:
    """cdc_events: list of {'op': 'INSERT'|'UPDATE'|'DELETE', 'account_id': str, 'amount': float, 'seq': int}.
    Apply events in ascending 'seq' order.
    Returns updated view mapping account_id -> final balance.
    """
    raise NotImplementedError("Implement change_data_capture_sync")

"""Reference Solution — Problem 01: Change Data Capture Sync

Topic: 25 Final Capstone Polyglot Enterprise
"""

from __future__ import annotations


def change_data_capture_sync(cdc_events: list[dict], existing_view: dict[str, float]) -> dict[str, float]:
    view = dict(existing_view)
    sorted_events = sorted(cdc_events, key=lambda e: e['seq'])
    for e in sorted_events:
        acct = e['account_id']
        op = e['op']
        amt = e.get('amount', 0.0)
        if op == 'INSERT':
            view[acct] = amt
        elif op == 'UPDATE':
            view[acct] = amt
        elif op == 'DELETE':
            view.pop(acct, None)
    return view

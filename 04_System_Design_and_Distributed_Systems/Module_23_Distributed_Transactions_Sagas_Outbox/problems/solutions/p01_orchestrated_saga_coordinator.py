"""Reference Solution — Problem 01: Orchestrated Saga Coordinator

Topic: 23 Distributed Transactions Sagas Outbox
"""

from __future__ import annotations


def orchestrated_saga_coordinator(steps: list[dict]) -> tuple[bool, list[str]]:
    executed = []
    for s in steps:
        if not s.get('succeeds', False):
            rollbacks = [x['compensate'] for x in reversed(executed)]
            return (False, rollbacks)
        executed.append(s)
    return (True, [])

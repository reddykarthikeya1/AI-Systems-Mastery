"""Problem 01 — Orchestrated Saga Coordinator

Topic: 23 Distributed Transactions Sagas Outbox
Target: Production-grade implementation

Execute forward saga steps and invoke compensating rollbacks on failure.

Example:
    >>> orchestrated_saga_coordinator([
    ...     {'name': 'reserve_flight', 'succeeds': True, 'compensate': 'cancel_flight'},
    ...     {'name': 'reserve_hotel', 'succeeds': False, 'compensate': 'cancel_hotel'},
    ... ])
    (False, ['cancel_flight'])

Hints:
    Hint 1: A saga runs forward until the first failure, then unwinds only
        the steps that already committed -- it never compensates the step
        that just failed, or any step after it.
    Hint 2: Keep a running list of successfully executed steps as you
        iterate; the moment a step fails, build the compensation list from
        that "executed" list in REVERSE order and stop processing.
    Hint 3: The failing step itself contributes no compensation entry
        (only previously succeeded steps do), and rollback order is the
        reverse of execution order, like unwinding a stack; if every step
        succeeds, the compensation list must come back empty, `[]`, not
        omitted.
"""

from __future__ import annotations


def orchestrated_saga_coordinator(steps: list[dict]) -> tuple[bool, list[str]]:
    """Each step dict has: {'name': str, 'succeeds': bool, 'compensate': str}.
    Execute steps in order.
    If a step has succeeds == False:
        Halt and execute 'compensate' action for all PREVIOUSLY succeeded steps in reverse order.
        Returns (False, list_of_executed_compensations).
    If all steps succeed:
        Returns (True, []).
    """
    raise NotImplementedError("Implement orchestrated_saga_coordinator")

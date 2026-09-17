"""Problem 01 — Strict Two Phase Locking

Topic: 23 Transactions Isolation Consensus Raft
Target: Production-grade implementation

Manage lock acquisitions and detect deadlocks using cycle detection.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def strict_two_phase_locking(lock_requests: list[tuple[str, str, str]]) -> tuple[dict[str, list[str]], list[str]]:
    """Each request is (tx_id, resource, mode) where mode is 'S' or 'X'.
    Maintain lock table. If conflict arises, add wait edge.
    If wait cycle is detected (deadlock), reject/abort that transaction.
    Returns (acquired_locks, aborted_txs).
    """
    raise NotImplementedError("Implement strict_two_phase_locking")

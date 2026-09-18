"""Problem 01 — Strict Two Phase Locking

Topic: 23 Transactions Isolation Consensus Raft
Target: Production-grade implementation

Manage lock acquisitions and detect deadlocks using cycle detection.

Example:
    >>> reqs = [
    ...     ('tx1', 'R1', 'X'),
    ...     ('tx2', 'R2', 'X'),
    ...     ('tx1', 'R2', 'X'),
    ...     ('tx2', 'R1', 'X'),
    ... ]
    >>> strict_two_phase_locking(reqs)
    ({'tx1': ['R1', 'R2'], 'tx2': ['R2']}, ['tx2'])

Hints:
    Hint 1: A conflicting request doesn't just block — it records a
        "waits-for" relationship between transactions, and it's the shape of
        that whole waits-for graph, not any single request, that decides
        whether anyone actually gets aborted.
    Hint 2: Track resource_owners (resource -> list of (tx, mode)) to detect
        conflicts (X vs anything, or X held by someone else), record a
        waits-for edge from the requester to each conflicting owner, then
        run a visited/on-stack depth-first search from the requesting
        transaction to check whether that graph now contains a cycle.
    Hint 3: A conflicting request that does NOT close a cycle is still
        granted (see tx1 acquiring R2 above despite conflicting with tx2) —
        only the request that would complete a cycle causes that
        transaction to be aborted, its pending waits-for edges dropped, and
        every later request from it skipped.
"""

from __future__ import annotations


def strict_two_phase_locking(lock_requests: list[tuple[str, str, str]]) -> tuple[dict[str, list[str]], list[str]]:
    """Each request is (tx_id, resource, mode) where mode is 'S' or 'X'.
    Maintain lock table. If conflict arises, add wait edge.
    If wait cycle is detected (deadlock), reject/abort that transaction.
    Returns (acquired_locks, aborted_txs).
    """
    raise NotImplementedError("Implement strict_two_phase_locking")

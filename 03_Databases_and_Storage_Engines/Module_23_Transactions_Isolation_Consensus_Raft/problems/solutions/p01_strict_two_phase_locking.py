"""Reference Solution — Problem 01: Strict Two Phase Locking

Topic: 23 Transactions Isolation Consensus Raft
"""

from __future__ import annotations


def strict_two_phase_locking(lock_requests: list[tuple[str, str, str]]) -> tuple[dict[str, list[str]], list[str]]:
    acquired = {}
    aborted = []
    # Simplified simulation: track resource owners
    resource_owners = {}  # res -> list of (tx_id, mode)
    waits_for = {}        # tx_id -> set of tx_ids
    
    def has_cycle(start_tx: str, visited: set, stack: set) -> bool:
        visited.add(start_tx)
        stack.add(start_tx)
        for neighbor in waits_for.get(start_tx, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True
        stack.remove(start_tx)
        return False

    for tx, res, mode in lock_requests:
        if tx in aborted:
            continue
        owners = resource_owners.get(res, [])
        conflict = False
        for owner_tx, owner_mode in owners:
            if owner_tx != tx:
                if mode == 'X' or owner_mode == 'X':
                    conflict = True
                    waits_for.setdefault(tx, set()).add(owner_tx)
        if conflict:
            if has_cycle(tx, set(), set()):
                aborted.append(tx)
                if tx in waits_for:
                    del waits_for[tx]
                continue
        resource_owners.setdefault(res, []).append((tx, mode))
        acquired.setdefault(tx, []).append(res)
    return (acquired, aborted)

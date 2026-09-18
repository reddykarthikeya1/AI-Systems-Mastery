"""Problem 01 — Distributed Inventory Reservation

Topic: 20 Flash Sale Inventory Reservation Amazon
Target: Production-grade implementation

Atomically reserve inventory stock with expiration cleanup.

Example:
    >>> distributed_inventory_reservation({'item_gpu': 3}, [('ord_1', 'item_gpu', 2), ('ord_2', 'item_gpu', 2), ('ord_3', 'item_gpu', 1)])
    ({'item_gpu': 0}, ['ord_1', 'ord_3'])

Hints:
    Hint 1: Reservations must be processed strictly in order, since each
        one's success depends on how much stock the earlier reservations
        in the same batch already consumed.
    Hint 2: Copy the inventory dict (never mutate the caller's input),
        then walk the reservation list once, checking and decrementing
        stock per item as you go while collecting successful order ids.
    Hint 3: An `item_id` absent from inventory must be treated as having
        0 stock (`inv.get(item, 0)`) so it's rejected instead of raising
        a KeyError; a rejected reservation must NOT partially decrement
        inventory or appear in the result list -- as when `ord_2` fails
        after `ord_1` already took 2 of the 3 available units.
"""

from __future__ import annotations


def distributed_inventory_reservation(inventory: dict[str, int], reservations: list[tuple[str, str, int]]) -> tuple[dict[str, int], list[str]]:
    """reservations: list of (order_id, item_id, qty).
    For each request, if inventory[item_id] >= qty:
        decrement inventory[item_id] by qty and accept order.
    Else:
        reject order.
    Returns (remaining_inventory, successful_order_ids).
    """
    raise NotImplementedError("Implement distributed_inventory_reservation")

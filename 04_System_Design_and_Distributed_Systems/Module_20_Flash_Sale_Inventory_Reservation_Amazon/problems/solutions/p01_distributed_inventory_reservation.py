"""Reference Solution — Problem 01: Distributed Inventory Reservation

Topic: 20 Flash Sale Inventory Reservation Amazon
"""

from __future__ import annotations


def distributed_inventory_reservation(inventory: dict[str, int], reservations: list[tuple[str, str, int]]) -> tuple[dict[str, int], list[str]]:
    inv = dict(inventory)
    success = []
    for oid, item, qty in reservations:
        if inv.get(item, 0) >= qty:
            inv[item] -= qty
            success.append(oid)
    return (inv, success)

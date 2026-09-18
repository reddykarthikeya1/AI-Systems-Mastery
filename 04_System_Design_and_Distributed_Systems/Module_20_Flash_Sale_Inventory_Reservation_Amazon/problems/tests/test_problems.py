"""Tests for Distributed Inventory Reservation."""
from __future__ import annotations

import pytest
from p01_distributed_inventory_reservation import distributed_inventory_reservation


def test_distributed_inventory_reservation():
    inv = {'item_gpu': 3}
    reqs = [
        ('ord_1', 'item_gpu', 2),
        ('ord_2', 'item_gpu', 2),  # out of stock
        ('ord_3', 'item_gpu', 1),
    ]
    rem, succ = distributed_inventory_reservation(inv, reqs)
    assert succ == ['ord_1', 'ord_3']
    assert rem['item_gpu'] == 0

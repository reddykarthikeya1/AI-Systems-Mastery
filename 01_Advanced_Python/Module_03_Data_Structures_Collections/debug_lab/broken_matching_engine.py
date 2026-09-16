#!/usr/bin/env python3
"""Broken Order Matching Engine demonstrating collection mutation and hashing traps."""

from copy import copy

def cancel_expired_orders(orders_dict: dict[str, int], expiry_threshold: int):
    for order_id, age in orders_dict.items():
        if age > expiry_threshold:
            del orders_dict[order_id]

def duplicate_order_portfolio(portfolio: dict[str, list[dict]]) -> dict[str, list[dict]]:
    return copy(portfolio)

def register_trader_tokens(traders: list[dict]) -> set:
    seen = set()
    for trader in traders:
        seen.add(trader)
    return seen

if __name__ == "__main__":
    active_orders = {"ORD-1": 10, "ORD-2": 55, "ORD-3": 12, "ORD-4": 80}
    try:
        cancel_expired_orders(active_orders, 50)
    except RuntimeError as err:
        print(f"Dictionary mutation crashed: {err}")

    original = {"trader_1": [{"symbol": "AAPL", "qty": 100}]}
    cloned = duplicate_order_portfolio(original)
    cloned["trader_1"][0]["qty"] = 999
    print(f"Original order qty after clone mutated: {original['trader_1'][0]['qty']} (Expected: 100)")

    traders_list = [{"id": 1}, {"id": 2}]
    try:
        register_trader_tokens(traders_list)
    except TypeError as err:
        print(f"Set insertion crashed: {err}")

#!/usr/bin/env python3
"""Broken RPG State Engine demonstrating scope, closure, and default parameter traps."""

sum = 100

def create_inventory_item(item_name: str, tags: list[str] = []) -> list[str]:
    tags.append(item_name)
    return tags

def make_multiplier_handlers():
    handlers = []
    for i in range(3):
        handlers.append(lambda x: x * i)
    return handlers

def calculate_team_score(scores: list[int]) -> int:
    # Crashes because 'sum' was shadowed at module level!
    return sum(scores)

if __name__ == "__main__":
    p1 = create_inventory_item("Sword")
    p2 = create_inventory_item("Shield")
    print(f"P1 tags: {p1}")
    print(f"P2 tags: {p2} (Expected only ['Shield']!)")

    funcs = make_multiplier_handlers()
    results = [f(10) for f in funcs]
    print(f"Multipliers of 10: {results} (Expected [0, 10, 20], got all the same!)")

    try:
        total = calculate_team_score([10, 20, 30])
    except TypeError as err:
        print(f"Team score crashed: {err}")

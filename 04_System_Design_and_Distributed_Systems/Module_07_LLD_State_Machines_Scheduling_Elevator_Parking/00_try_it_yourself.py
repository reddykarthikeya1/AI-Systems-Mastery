"""Beginner playground for Module 07 - Low-Level Design - State Machines, Elevators and Car Parks.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ---------------------------------------- 1. Booleans multiply; states do not
flags = ["paid", "shipped", "cancelled", "refunded"]
combinations = 2 ** len(flags)
legal_states = ["new", "paid", "shipped", "cancelled", "refunded"]

print(f"{len(flags)} booleans -> {combinations} combinations")
print(f"states an order can really be in -> {len(legal_states)}")
print(f"nonsense combinations you must defend against -> {combinations - len(legal_states)}")
assert combinations == 16
assert combinations - len(legal_states) == 11


# ------------------ 2. A transition table makes illegal moves unrepresentable
TRANSITIONS = {
    "new": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": {"delivered", "returned"},
    "cancelled": set(),
    "refunded": set(),
    "delivered": {"returned"},
    "returned": {"refunded"},
}


class Order:
    def __init__(self):
        self.state = "new"
        self.history = ["new"]

    def move_to(self, new_state):
        if new_state not in TRANSITIONS[self.state]:
            raise ValueError(f"cannot go from {self.state} to {new_state}")
        self.state = new_state
        self.history.append(new_state)
        return self.state


order = Order()
print(" ", order.move_to("paid"))
print(" ", order.move_to("shipped"))
try:
    order.move_to("cancelled")
except ValueError as exc:
    print("  refused:", exc)

assert order.state == "shipped"
assert order.history == ["new", "paid", "shipped"]


# ------------------------------- 3. Terminal states, and the bug they prevent
cancelled_order = Order()
cancelled_order.move_to("cancelled")
print("state:", cancelled_order.state, "- outgoing edges:", TRANSITIONS["cancelled"])

blocked = 0
for late_event in ("paid", "shipped", "refunded"):
    try:
        cancelled_order.move_to(late_event)
    except ValueError:
        blocked += 1

assert blocked == 3, "every late event bounced off a terminal state"
assert cancelled_order.state == "cancelled"
print("Three duplicate webhooks arrived. None of them did anything.")


# ----------------------------------- 4. The same machine, running an elevator
def travel_first_come(current, requests):
    distance = 0
    for floor in requests:
        distance += abs(floor - current)
        current = floor
    return distance


def travel_sweep(current, requests):
    going_up = sorted(f for f in requests if f >= current)
    going_down = sorted((f for f in requests if f < current), reverse=True)
    distance = 0
    for floor in going_up + going_down:
        distance += abs(floor - current)
        current = floor
    return distance


calls = [8, 1, 7, 2, 6]
naive = travel_first_come(3, calls)
swept = travel_sweep(3, calls)
print(f"floors travelled, first-come order: {naive}")
print(f"floors travelled, sweep policy:     {swept}")
assert swept < naive, "same requests, same machine, far less travel"
print("Identical state machine. The policy is where the engineering is.")


print()
print("All checks passed.")

# Beginner Playground - Low-Level Design - State Machines, Elevators and Car Parks

> *"A traffic light cannot go from red straight to green. Not because the code checks - because the wiring makes it impossible."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Booleans multiply; states do not

Four independent booleans give you sixteen combinations. Maybe five of them are
real. The other eleven are bugs waiting for a race condition or a retry.

With one `state` field and a table of legal moves, the illegal combinations cannot
be represented at all. You do not have to defend against them - they do not exist.

```python
flags = ["paid", "shipped", "cancelled", "refunded"]
combinations = 2 ** len(flags)
legal_states = ["new", "paid", "shipped", "cancelled", "refunded"]

print(f"{len(flags)} booleans -> {combinations} combinations")
print(f"states an order can really be in -> {len(legal_states)}")
print(f"nonsense combinations you must defend against -> {combinations - len(legal_states)}")
assert combinations == 16
assert combinations - len(legal_states) == 11
```

---

## 2. A transition table makes illegal moves unrepresentable

List the legal edges once. Anything not on the list is rejected by construction,
in one place, rather than by an `if` somewhere in every handler.

```python
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
```

---

## 3. Terminal states, and the bug they prevent

`cancelled` and `refunded` have no outgoing edges. Once there, an order stays
there - so a late-arriving duplicate webhook cannot resurrect a cancelled order
into a shipped one.

A retry that arrives twice is normal. The state machine makes the second one
harmless without any extra code.

```python
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
```

---

## 4. The same machine, running an elevator

An elevator is the classic interview question and it is the same structure: a
state, a set of legal transitions, and a rule for choosing the next one.

The interesting part is not the transitions - it is the *policy*. Serving requests
in arrival order makes the car yo-yo. Serving everything in the current direction
before turning around (the "elevator algorithm", which is also how disk schedulers
work) cuts the travel enormously.

```python
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
```

---

## 5. Predict before you run

An order can be paid, shipped, cancelled and refunded. Modelled as four
independent boolean flags, how many combinations exist? How many of them are
states a real order could actually be in?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

'Cancelled but also shipped' is a real production bug and a real refund. It
comes from modelling state as a handful of booleans that can be set
independently, instead of one value that can only move along legal edges.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

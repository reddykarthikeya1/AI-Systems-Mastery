"""Beginner playground for Module 06 - Design Patterns for Scalable Systems.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations


# --------------------------------- 1. Strategy: pick the algorithm at runtime
class CardPayment:
    def pay(self, amount):
        return f"charged {amount} to a card"


class PayPalPayment:
    def pay(self, amount):
        return f"sent {amount} via PayPal"


class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy

    def complete(self, amount):
        return self.strategy.pay(amount)


print(" ", Checkout(CardPayment()).complete(50))
print(" ", Checkout(PayPalPayment()).complete(50))


class CryptoPayment:                       # added later - nothing above changed
    def pay(self, amount):
        return f"transferred {amount} on-chain"


print(" ", Checkout(CryptoPayment()).complete(50))
assert "on-chain" in Checkout(CryptoPayment()).complete(50)
print("Three payment methods. Zero edits to Checkout.")


# ------------------------------------- 2. Observer: publish once, notify many
class OrderPlaced:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, handler):
        self.subscribers.append(handler)

    def publish(self, order_id):
        return [handler(order_id) for handler in self.subscribers]


event = OrderPlaced()
event.subscribe(lambda oid: f"emailed the customer about {oid}")
event.subscribe(lambda oid: f"queued {oid} for picking")
event.subscribe(lambda oid: f"recorded {oid} in analytics")

for line in event.publish("order-7"):
    print(" ", line)
assert len(event.publish("order-7")) == 3
print("The order code does not know any of these exist. That is the point.")


# ----------------- 3. Circuit breaker: stop knocking on a door nobody answers
class CircuitBreaker:
    def __init__(self, threshold=3):
        self.failures = 0
        self.threshold = threshold
        self.state = "closed"

    def call(self, dependency):
        if self.state == "open":
            return "failed fast - circuit is open, nothing was attempted"
        try:
            result = dependency()
            self.failures = 0
            return result
        except RuntimeError:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
            return "call failed"


def broken_service():
    raise RuntimeError("timeout after 30 seconds")


breaker = CircuitBreaker()
for attempt in range(5):
    print(f"  attempt {attempt + 1}: {breaker.call(broken_service)}")

assert breaker.state == "open"
assert "nothing was attempted" in breaker.call(broken_service)
print("Attempts 4 and 5 cost nothing. Without this they cost 30 seconds each.")


# -------------------------------------- 4. When a pattern is the wrong answer
class UserFactory:
    def create(self, kind):
        if kind == "user":
            return {"kind": "user"}
        raise ValueError(kind)


direct = {"kind": "user"}
via_factory = UserFactory().create("user")
print("factory output:", via_factory, "- identical to the literal:", direct)
assert via_factory == direct, "one implementation, so the factory adds nothing"
print("A factory with one product is a dictionary with extra steps.")


print()
print("All checks passed.")

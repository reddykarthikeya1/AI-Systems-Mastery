# Beginner Playground - Design Patterns for Scalable Systems

> *"A pattern is a name for something you were going to build anyway. The value is that saying 'use a strategy here' takes two seconds and a diagram takes ten minutes."*


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

## 1. Strategy: pick the algorithm at runtime

The `if/elif` chain grows forever and every new branch means editing a file that
already works. Strategy makes each option a separate object, so adding one touches
nothing that existed before.

This is the Open/Closed Principle with a name: open to extension, closed to
modification.

```python
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
```

---

## 2. Observer: publish once, notify many

When an order is placed, several things must happen: email the customer, tell the
warehouse, update analytics. Hard-coding those calls means editing the order code
every time the list changes.

Observer inverts it: the order announces what happened, and interested parties
subscribe. This is the in-process shape of the event-driven architectures later in
this course.

```python
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
```

---

## 3. Circuit breaker: stop knocking on a door nobody answers

A failing dependency does not just fail - it fails *slowly*, holding your threads
open until you run out. Then your service fails too, and so does everything
calling you.

A circuit breaker counts failures, and after a threshold it stops trying and fails
instantly. Fast failure leaves you resources to serve everything else.

```python
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
```

---

## 4. When a pattern is the wrong answer

Patterns have a cost: indirection. Every one you add is another hop a reader has to
follow to find out what actually happens.

Use one when you can *name the axis of change* - "payment methods will keep being
added". If you cannot name it, you are guessing, and a `Factory` that produces one
kind of object is pure overhead.

The honest order of operations: write the simple version, wait for the second
case, then refactor to the pattern. The second case tells you the axis; the first
one cannot.

```python
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
```

---

## 5. Predict before you run

You have a payment class with an `if method == 'card' ... elif 'paypal' ...`
chain. A new payment method arrives every quarter. How many existing, working,
tested lines does each new method force you to edit?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Patterns are worth exactly as much as the change they make cheap. Reach for
one when you can name the axis along which the code will vary; skip it when
you cannot, because a pattern applied to a guess is just extra indirection.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

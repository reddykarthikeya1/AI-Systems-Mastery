# Beginner Playground - SOLID Principles and Clean Architecture

> *"A Swiss army knife does eleven jobs badly. The reason is not that it tries hard enough - it is that every blade has to share one handle."*

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

## 1. Single responsibility: one reason to change

Not "one method" or "one job" - **one reason to change**. The class below changes
when the pricing rules change, *and* when the email template changes, *and* when
the database schema changes. Three teams, one file, three ways to break each
other.

```python
class OrderManagerDoingEverything:
    def process(self, order):
        total = sum(item["price"] for item in order["items"])          # pricing
        record = f"INSERT INTO orders VALUES ({order['id']}, {total})"  # persistence
        message = f"Dear {order['customer']}, your total is {total}"    # messaging
        return total, record, message


reasons_to_change = ["pricing rules", "database schema", "email wording"]
print("reasons this one class changes:", len(reasons_to_change))
assert len(reasons_to_change) == 3, "three teams, one file, three ways to collide"
```

---

## 2. Split it, and each piece becomes testable alone

Same behaviour, three objects. Now the pricing tests need no database and the
email tests need no pricing rules.

```python
class Pricing:
    def total(self, order):
        return sum(item["price"] for item in order["items"])


class OrderRepository:
    def __init__(self):
        self.saved = []

    def save(self, order_id, total):
        self.saved.append((order_id, total))


class Notifier:
    def __init__(self):
        self.sent = []

    def send(self, customer, total):
        self.sent.append(f"Dear {customer}, your total is {total}")


order = {"id": 1, "customer": "ana", "items": [{"price": 30}, {"price": 12}]}
pricing, repository, notifier = Pricing(), OrderRepository(), Notifier()
amount = pricing.total(order)
repository.save(order["id"], amount)
notifier.send(order["customer"], amount)

print("total:", amount)
print("saved:", repository.saved)
print("sent: ", notifier.sent)
assert amount == 42
assert pricing.total(order) == 42, "testable with no database and no mail server"
```

---

## 3. Dependency inversion: plug and socket

A kettle does not know which power station it is connected to. It knows the shape
of the socket.

Make the high-level policy depend on an *interface*, not on a concrete class. Then
swapping the storage engine - or using a fake one in tests - touches nothing that
matters.

```python
class InMemoryRepository:
    def __init__(self):
        self.saved = []

    def save(self, order_id, total):
        self.saved.append((order_id, total))


class PostgresRepository:
    def __init__(self):
        self.statements = []

    def save(self, order_id, total):
        self.statements.append(f"INSERT INTO orders VALUES ({order_id}, {total})")


class CheckoutService:
    # Knows only that `repository` has .save(). Nothing else.
    def __init__(self, repository):
        self.repository = repository

    def checkout(self, order):
        total = Pricing().total(order)
        self.repository.save(order["id"], total)
        return total


fake = InMemoryRepository()
real = PostgresRepository()
assert CheckoutService(fake).checkout(order) == CheckoutService(real).checkout(order)
print("with the fake:", fake.saved)
print("with postgres:", real.statements)
print("The service source code is byte-for-byte identical in both runs.")
```

---

## 4. Liskov: a subclass must not break the promise

If code works with a `Repository`, it must work with *every* `Repository`. A
subclass that raises where the parent succeeds is not a specialisation - it is a
landmine, and it explodes in code that never mentioned it.

The giveaway is any override whose body is `raise NotImplementedError` or which
quietly narrows what the parent accepted.

```python
class ReadOnlyRepository(InMemoryRepository):
    def save(self, order_id, total):
        raise RuntimeError("this repository does not accept writes")


def run_checkout(repository):
    return CheckoutService(repository).checkout(order)


print("with a normal repository:", run_checkout(InMemoryRepository()))
try:
    run_checkout(ReadOnlyRepository())
    raise AssertionError("expected the substitution to fail")
except RuntimeError as exc:
    print("with the 'compatible' subclass:", exc)

print("Nothing in CheckoutService is wrong. It was handed a broken promise.")
```

---

## 5. Predict before you run

A class sends email, formats reports and talks to the database. How many
separate reasons does it have to change? Now count how many teams can be
blocked by the same file.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

These principles sound abstract until your first "I cannot test this without
a live database" moment. Dependency inversion is what turns that from a
rewrite into a five-line change.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

# Beginner Playground - MongoDB - Document Modelling and BSON

> *"A relational database files the invoice, the address and the line items in three different cabinets. A document database keeps one folder per customer with everything in it."*

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

## 1. One folder instead of three cabinets

In SQL, an order that needs a customer and some line items is three tables and
two joins. In MongoDB it can be one document that contains all of it.

The win is that a read your application performs constantly becomes a single
lookup. The cost is that anything you duplicate into that document now has to be
kept up to date in every copy.

```python
lookups = {"count": 0}


def fetch(store, key):
    lookups["count"] += 1
    return store[key]


embedded_orders = {
    "order_1": {
        "customer": {"name": "alice", "city": "Dublin"},
        "lines": [
            {"product": "mug", "qty": 2, "price": 1200},
            {"product": "hat", "qty": 1, "price": 2500},
        ],
    }
}

lookups["count"] = 0
order = fetch(embedded_orders, "order_1")
total = sum(line["qty"] * line["price"] for line in order["lines"])
print(f"embedded: total {total} cents in {lookups['count']} lookup(s)")
assert lookups["count"] == 1, "everything needed was in one document"
assert total == 4900
```

---

## 2. The referenced design, and the N+1 problem

Store ids instead of copies and the same page needs one lookup for the order plus
one per product. That is the **N+1 query problem**, and it is the single most
common cause of a page that is fine in testing and unusable in production.

```python
products = {
    "mug": {"name": "mug", "price": 1200},
    "hat": {"name": "hat", "price": 2500},
}
referenced_orders = {
    "order_1": {"customer_id": "alice", "lines": [("mug", 2), ("hat", 1)]}
}
customers = {"alice": {"name": "alice", "city": "Dublin"}}

lookups["count"] = 0
ref_order = fetch(referenced_orders, "order_1")
fetch(customers, ref_order["customer_id"])
ref_total = sum(qty * fetch(products, name)["price"] for name, qty in ref_order["lines"])
print(f"referenced: total {ref_total} cents in {lookups['count']} lookup(s)")
assert ref_total == total, "same answer"
assert lookups["count"] == 4, "1 order + 1 customer + 2 products"
print("Now imagine a page showing 20 orders. Embedded: 20. Referenced: 80+.")
```

---

## 3. So why would anyone reference?

Because a copy is a promise to keep it up to date. Embed the product price into
ten thousand orders and a price change means ten thousand writes - or, far worse,
ten thousand rows that quietly disagree.

The rule that survives contact with production:

- **Embed** what is read together and changes together - an address on an order.
- **Reference** what is shared and changes independently - a product catalogue.

And note that an order *should* keep the price it was bought at. That is not
duplication, it is history. Embedding is correct there for a second reason.

```python
products["mug"]["price"] = 1500
print("catalogue price changed to 1500")

recomputed = sum(qty * products[name]["price"] for name, qty in ref_order["lines"])
print("referenced order now totals:", recomputed, "- the past was rewritten")
assert recomputed != total, "the historical order silently changed value"

still_correct = sum(line["qty"] * line["price"] for line in order["lines"])
print("embedded order still totals:", still_correct, "- what the customer actually paid")
assert still_correct == 4900
```

---

## 4. The trap: documents that grow without limit

A BSON document is capped at 16 MB. That sounds enormous until somebody embeds an
array that grows forever - every comment on a post, every event for a user.

The failure is not a clean error at 16 MB either. Long before that, every read of
the document drags the whole array across the network, including the 99% of it
nobody asked for.

Unbounded array means reference. No exceptions.

```python
post = {"title": "hello", "comments": []}
for i in range(5_000):
    post["comments"].append({"by": f"user{i}", "text": "nice post" * 10})

approx_bytes = sum(len(c["by"]) + len(c["text"]) for c in post["comments"])
print(f"comments embedded: {len(post['comments'])}, roughly {approx_bytes / 1024:.0f} KB")
print("every read of this post pays for ALL of it, to show maybe 10 comments")
assert approx_bytes > 400_000
assert len(post["comments"]) > 1_000, "this array has no natural ceiling"
```

---

## 5. Predict before you run

Fetching one order with its five line items: how many lookups does the
embedded design need, and how many does the referenced design need? Now do it
for a page showing 20 orders.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

"Should I embed or reference" is the only MongoDB design question that really
matters, and the answer is decided by how the data is *read*, not by how it
looks in a diagram. Get it wrong and you rebuild the collection later, live.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

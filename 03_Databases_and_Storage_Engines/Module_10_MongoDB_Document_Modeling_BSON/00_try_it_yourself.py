"""Beginner playground for Module 10 - MongoDB - Document Modelling and BSON.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------ 1. One folder instead of three cabinets
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


# ------------------------------ 2. The referenced design, and the N+1 problem
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


# ------------------------------------------ 3. So why would anyone reference?
products["mug"]["price"] = 1500
print("catalogue price changed to 1500")

recomputed = sum(qty * products[name]["price"] for name, qty in ref_order["lines"])
print("referenced order now totals:", recomputed, "- the past was rewritten")
assert recomputed != total, "the historical order silently changed value"

still_correct = sum(line["qty"] * line["price"] for line in order["lines"])
print("embedded order still totals:", still_correct, "- what the customer actually paid")
assert still_correct == 4900


# ----------------------------- 4. The trap: documents that grow without limit
post = {"title": "hello", "comments": []}
for i in range(5_000):
    post["comments"].append({"by": f"user{i}", "text": "nice post" * 10})

approx_bytes = sum(len(c["by"]) + len(c["text"]) for c in post["comments"])
print(f"comments embedded: {len(post['comments'])}, roughly {approx_bytes / 1024:.0f} KB")
print("every read of this post pays for ALL of it, to show maybe 10 comments")
assert approx_bytes > 400_000
assert len(post["comments"]) > 1_000, "this array has no natural ceiling"


print()
print("All checks passed.")

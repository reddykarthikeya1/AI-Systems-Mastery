"""Beginner playground for Module 25 - Observability, Distributed Tracing and SRE.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import statistics

# -------------------------------- 1. Three signals, three different questions
metrics = {"http_requests_total": 148_233, "error_rate": 0.004}
log_line = {"request_id": "abc123", "msg": "payment declined", "code": "insufficient"}
span = {"trace_id": "abc123", "service": "payments", "ms": 812}

print("metric:", metrics)
print("log:   ", log_line)
print("trace: ", span)
assert log_line["request_id"] == span["trace_id"], "one id ties them together"
print("That shared id is what makes the three usable as one tool.")


# ---------------------------------------------- 2. A trace is a tree of spans
spans = [
    {"id": "1", "parent": None, "service": "gateway", "ms": 950},
    {"id": "2", "parent": "1", "service": "auth", "ms": 20},
    {"id": "3", "parent": "1", "service": "orders", "ms": 900},
    {"id": "4", "parent": "3", "service": "inventory", "ms": 15},
    {"id": "5", "parent": "3", "service": "pricing-db", "ms": 870},
]

by_parent = {}
for s in spans:
    by_parent.setdefault(s["parent"], []).append(s)


def show(parent=None, depth=0):
    for s in by_parent.get(parent, []):
        print(f"  {'  ' * depth}{s['service']:<12} {s['ms']:>4} ms")
        show(s["id"], depth + 1)


show()
slowest_leaf = max((s for s in spans if s["id"] not in by_parent), key=lambda s: s["ms"])
print("the time is in:", slowest_leaf["service"])
assert slowest_leaf["service"] == "pricing-db"
assert slowest_leaf["ms"] / spans[0]["ms"] > 0.9, "one call is 90% of the request"


# --------------------------------------- 3. Why the average hides the problem
latencies = [80] * 980 + [3_000] * 20          # 98% fast, 2% dreadful


def percentile(values, p):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * p / 100))]


print(f"mean: {statistics.mean(latencies):>6.0f} ms")
print(f"p50:  {percentile(latencies, 50):>6.0f} ms")
print(f"p99:  {percentile(latencies, 99):>6.0f} ms")
assert statistics.mean(latencies) < 200, "the average looks perfectly healthy"
assert percentile(latencies, 99) == 3_000, "and 1 in 50 users waits 3 seconds"


# ---------------------------- 4. The percentile mistake almost everyone makes
server_a = [50] * 990 + [100] * 10
server_b = [50] * 900 + [5_000] * 100

p99_a = percentile(server_a, 99)
p99_b = percentile(server_b, 99)
averaged = (p99_a + p99_b) / 2
true_p99 = percentile(server_a + server_b, 99)

print(f"server A p99: {p99_a:>6} ms")
print(f"server B p99: {p99_b:>6} ms")
print(f"average of the two p99s: {averaged:>6.0f} ms   <- meaningless")
print(f"true p99 of all traffic: {true_p99:>6} ms")
assert averaged != true_p99, "averaging percentiles gives the wrong answer"
print("Store histograms. Compute percentiles at query time, never before.")


# --------------------- 5. Error budgets make reliability a budget, not a wish
SLO = 0.999
MONTHLY_REQUESTS = 100_000_000

budget = MONTHLY_REQUESTS * (1 - SLO)
failed_so_far = 62_000
remaining = budget - failed_so_far

print(f"allowed failures this month: {budget:>10,.0f}")
print(f"used so far:                 {failed_so_far:>10,}")
print(f"remaining:                   {remaining:>10,.0f} ({remaining / budget:.0%})")
assert round(budget) == 100_000
assert remaining > 0, "budget left, so feature work continues"

burn_rate = failed_so_far / budget
print(f"burn rate at this point in the month: {burn_rate:.0%}")
assert burn_rate < 1.0
print("Budget exhausted means a freeze. Written down in advance, argued about never.")


print()
print("All checks passed.")

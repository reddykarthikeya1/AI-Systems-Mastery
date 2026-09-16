"""Beginner playground for Module 04 - Load Balancing Algorithms and Health Probes.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ----------------------------------------------------------- 1. Dealing cards
servers = ["server-A", "server-B"]


def round_robin(request_index):
    return servers[request_index % len(servers)]


for i in range(4):
    print(f"  request {i} -> {round_robin(i)}")
assert [round_robin(i) for i in range(4)] == ["server-A", "server-B"] * 2


# --------------------------------------- 2. Even requests, wildly uneven work
request_costs = [10 if i % 2 == 0 else 1 for i in range(100)]

rr_load = dict.fromkeys(servers, 0)
rr_count = dict.fromkeys(servers, 0)
for i, cost in enumerate(request_costs):
    chosen = round_robin(i)
    rr_load[chosen] += cost
    rr_count[chosen] += 1

print("requests each:", rr_count)
print("work each:    ", rr_load)
assert rr_count["server-A"] == rr_count["server-B"], "perfectly even by count"
assert rr_load["server-A"] == 10 * rr_load["server-B"], "10x apart by work"
print("Your monitoring is green. One server is on fire.")


# ------------------------------ 3. Least connections picks the shortest queue
def least_loaded(load_by_server):
    return min(load_by_server, key=load_by_server.get)


lc_load = dict.fromkeys(servers, 0)
for cost in request_costs:
    lc_load[least_loaded(lc_load)] += cost

print("work each, least-connections:", lc_load)
imbalance_rr = max(rr_load.values()) / min(rr_load.values())
imbalance_lc = max(lc_load.values()) / min(lc_load.values())
print(f"imbalance - round robin: {imbalance_rr:.1f}x, least connections: "
      f"{imbalance_lc:.2f}x")
assert imbalance_lc < 1.1, "near-perfect balance of actual work"
assert imbalance_lc < imbalance_rr


# ------------------------------ 4. Health checks: the shallow probe that lies
class Server:
    def __init__(self, name, process_up, db_pool_free):
        self.name = name
        self.process_up = process_up
        self.db_pool_free = db_pool_free

    def shallow_probe(self):
        return self.process_up

    def deep_probe(self):
        return self.process_up and self.db_pool_free > 0


fleet = [Server("app-1", True, 10), Server("app-2", True, 0)]
for server in fleet:
    print(f"  {server.name}: shallow says {server.shallow_probe()}, "
          f"deep says {server.deep_probe()}")

assert fleet[1].shallow_probe(), "the process is running, so a shallow probe passes"
assert not fleet[1].deep_probe(), "but every request it receives will fail"


# --------------------------- 5. And the check that takes down the whole fleet
PANIC_THRESHOLD = 0.5


def routable(fleet_health):
    healthy = [name for name, ok in fleet_health.items() if ok]
    if len(healthy) / len(fleet_health) < PANIC_THRESHOLD:
        return list(fleet_health)          # fail open: trust nobody's verdict
    return healthy


normal = {"app-1": True, "app-2": True, "app-3": False}
wobble = {"app-1": False, "app-2": False, "app-3": False}

print("one genuinely sick server ->", routable(normal))
print("every probe failing at once ->", routable(wobble))
assert routable(normal) == ["app-1", "app-2"], "drop the sick one, as intended"
assert len(routable(wobble)) == 3, "do not remove the entire fleet on one signal"


print()
print("All checks passed.")

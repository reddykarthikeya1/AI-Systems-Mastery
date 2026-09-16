# Beginner Playground - Load Balancing Algorithms and Health Probes

> *"Round robin is dealing cards - everybody gets the same number. Least connections is picking the shortest supermarket queue - which is what you actually do, because the trolleys differ."*

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

## 1. Dealing cards

Round robin hands out requests in turn. It is stateless, instant, and completely
fair *by count*.

Fairness by count is only fairness at all if every request costs the same. That
assumption is worth checking, because it is usually false.

```python
servers = ["server-A", "server-B"]


def round_robin(request_index):
    return servers[request_index % len(servers)]


for i in range(4):
    print(f"  request {i} -> {round_robin(i)}")
assert [round_robin(i) for i in range(4)] == ["server-A", "server-B"] * 2
```

---

## 2. Even requests, wildly uneven work

Now alternate a cheap request with an expensive one. Round robin gives each server
exactly half the requests - and gives one of them all of the expensive ones.

The request-count dashboard shows a perfect 50/50 split the entire time.

```python
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
```

---

## 3. Least connections picks the shortest queue

Instead of counting turns, track how much each server currently has outstanding
and send the next request to the least busy one. This is what a human does at a
supermarket: you do not take turns, you look.

```python
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
```

---

## 4. Health checks: the shallow probe that lies

A probe that returns 200 as long as the process is running will happily keep
sending traffic to a server whose database connection pool is exhausted. The
process is alive. The service is not.

A useful probe checks the dependencies the request actually needs - and separates
**liveness** (should I be restarted?) from **readiness** (should I get traffic?).
Conflating them is how a slow start-up turns into an endless restart loop.

```python
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
```

---

## 5. And the check that takes down the whole fleet

Now make the probe strict enough to fail during a brief dependency wobble. Every
server fails at once, the balancer removes every server, and a five-second
database hiccup becomes a total outage.

The defence is **fail-open** (sometimes called panic mode): if more than some
fraction of the fleet is marked unhealthy, assume the *probe* is wrong and keep
routing to everyone. A degraded service beats no service.

```python
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
```

---

## 6. Predict before you run

Requests alternate between cheap (1 unit) and expensive (10 units), and you
have two servers behind round robin. Does each server get half the *requests*?
Does each get half the *work*?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Round robin with uneven request costs is the most common load balancing
mistake, and it hides well: your dashboard shows requests-per-server as
perfectly even while one machine sits at 95% CPU and the other at 15%.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

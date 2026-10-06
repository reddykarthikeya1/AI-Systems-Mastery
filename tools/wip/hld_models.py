"""WIP, NOT VERIFIED: draft runnable models for HLD systems 04-10 (appended as section 11 when run).
Known problem: the system 04 lease-queue block hangs (infinite loop in the poison-job section); fix it first.
Run from this folder: python hld_models.py (it writes into 03-High-Level-Design/systems, then runs each block).
"""
import pathlib, re, subprocess, sys, os

R = pathlib.Path(r"C:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\03-High-Level-Design\systems")
S = {}

S["04-distributed-task-scheduler.md"] = r'''

---

## 11. Runnable Model: A Lease Queue with Fencing

The heart of a reliable scheduler is a claim that expires. A worker takes a **lease** on a job; if it dies or stalls, the lease runs out and another worker takes over; if the first worker later wakes up, its stale completion must be refused.

```python
import threading

class LeaseQueue:
    def __init__(self, clock, lease_s=30.0, max_attempts=3):
        self.clock, self.lease_s, self.max_attempts = clock, lease_s, max_attempts
        self.jobs, self.order, self.dead, self.done = {}, [], [], []
        self._lock = threading.Lock()

    def enqueue(self, job_id):
        with self._lock:
            self.jobs[job_id] = {"attempts": 0, "lease_until": 0.0, "token": 0}
            self.order.append(job_id)

    def claim(self, worker):
        with self._lock:
            now = self.clock()
            for job_id in self.order:
                job = self.jobs[job_id]
                if job["lease_until"] > now:
                    continue                                   # leased by a live worker
                if job["attempts"] >= self.max_attempts:       # kept failing: park it instead of retrying forever
                    self.order.remove(job_id); self.dead.append(job_id); del self.jobs[job_id]
                    return self.claim(worker)
                job["attempts"] += 1
                job["token"] += 1                              # the fencing token: higher on every new lease
                job["lease_until"] = now + self.lease_s
                return job_id, job["token"]
            return None

    def heartbeat(self, job_id, token):
        with self._lock:
            job = self.jobs.get(job_id)
            if job is None or job["token"] != token or job["lease_until"] <= self.clock():
                return False
            job["lease_until"] = self.clock() + self.lease_s
            return True

    def complete(self, job_id, token):
        with self._lock:
            job = self.jobs.get(job_id)
            if job is None or job["token"] != token:
                return False                                   # a stale worker: someone else owns the job now
            del self.jobs[job_id]; self.order.remove(job_id); self.done.append(job_id)
            return True

now = [0.0]
q = LeaseQueue(clock=lambda: now[0], lease_s=30, max_attempts=3)
q.enqueue("j1")
a = q.claim("A")
assert a == ("j1", 1) and q.claim("B") is None                      # leased: nobody else can take it

now[0] = 31.0                                                       # A stalled past its lease
b = q.claim("B")
assert b == ("j1", 2)                                               # B takes over with a higher token
assert q.complete(*a) is False                                      # A wakes up late: refused
assert q.complete(*b) is True and q.done == ["j1"]

q.enqueue("j2")
t1 = q.claim("A")
now[0] = 50.0
assert q.heartbeat(*t1) is True                                     # a live worker keeps its lease alive
now[0] = 75.0
assert q.claim("B") is None                                         # still protected: lease runs until 80
assert q.heartbeat("j2", 999) is False                              # a wrong token cannot extend it

q.enqueue("poison")
for _ in range(3):                                                  # three workers die one after another
    now[0] += 31.0
    while (c := q.claim("W")) is not None and c[0] != "poison":
        q.complete(*c)
now[0] += 31.0
assert q.claim("W") is None or q.dead == ["poison"] or "poison" not in q.jobs

q2 = LeaseQueue(clock=lambda: now[0])
for i in range(100):
    q2.enqueue(f"k{i}")
claimed, lock = [], threading.Lock()
def worker():
    while (c := q2.claim("w")) is not None:
        with lock:
            claimed.append(c[0])
threads = [threading.Thread(target=worker) for _ in range(4)]
[t.start() for t in threads]; [t.join() for t in threads]
assert sorted(claimed) == sorted(f"k{i}" for i in range(100))      # four racing workers, every job claimed exactly once
```

What a production scheduler adds: durable storage (the claim becomes `UPDATE ... WHERE lease_until < now() ... RETURNING`, or `SELECT ... FOR UPDATE SKIP LOCKED`), a delay index for scheduled jobs, per-queue priorities, and metrics on queue age. The invariants in this model (one live lease per job, a rising token, stale completions refused, bounded attempts) are the ones to protect.
'''

S["05-video-streaming-youtube.md"] = r'''

---

## 11. Runnable Model: Adaptive Bitrate Selection

The player, not the server, chooses which rendition to fetch for each 4-second segment. A rule based only on the last measured throughput is easily fooled; a rule based on how full the buffer is avoids stalls.

```python
LADDER = [300, 750, 1500, 3000]          # kbit/s renditions
SEGMENT_S = 4

def simulate(choose, throughput_kbps):
    """Play len(throughput) segments. Returns (stall_seconds, average_bitrate)."""
    buffer_s, stall, picked, last_tp = 0.0, 0.0, [], throughput_kbps[0]
    for i, tp in enumerate(throughput_kbps):
        bitrate = choose(buffer_s, last_tp)
        download_s = bitrate * SEGMENT_S / tp                        # kbit divided by kbit/s
        if i > 0:                                                    # playback only drains the buffer after the first segment
            stall += max(0.0, download_s - buffer_s)
            buffer_s = max(0.0, buffer_s - download_s)
        buffer_s += SEGMENT_S
        last_tp = tp
        picked.append(bitrate)
    return round(stall, 2), sum(picked) / len(picked)

highest = lambda buf, tp: LADDER[-1]
rate_based = lambda buf, tp: max([b for b in LADDER if b <= tp * 0.9] or [LADDER[0]])      # last throughput, 10% safety margin
def buffer_based(buf, tp):
    if buf < 8:
        return LADDER[0]                                             # nearly empty: be safe
    if buf < 16:
        return LADDER[1]
    return rate_based(buf, tp) if buf < 24 else LADDER[-1]

trace = [4000] * 6 + [400] * 8 + [4000] * 10                         # a network dip in the middle
stall_hi, avg_hi = simulate(highest, trace)
stall_rate, avg_rate = simulate(rate_based, trace)
stall_buf, avg_buf = simulate(buffer_based, trace)

assert stall_hi > stall_buf                                          # always asking for the best rendition stalls during the dip
assert stall_buf <= stall_rate                                       # the buffer-aware rule never stalls more than the rate-only rule
assert avg_hi > avg_buf                                              # and the price is some quality
assert simulate(buffer_based, [4000] * 20)[0] == 0.0                 # on a steady link nothing stalls
print(stall_hi, stall_rate, stall_buf)
```

The point to make in an interview is the trade-off the numbers show: **maximising quality** (always the top rendition) causes stalls when the network dips, **reacting to throughput alone** is jumpy, and **using buffer level** trades a little quality for far fewer stalls. Real players (BOLA, MPC, Pensieve-style learned policies) refine the same idea, and the server's job is to make it possible: many renditions, short segments, and a CDN close to the viewer.
'''

S["06-ecommerce-platform.md"] = r'''

---

## 11. Runnable Model: Stock Reservation Without Overselling

Checkout needs stock to be **held** while the customer pays, **released** if they leave, and **never sold twice**.

```python
import threading

class Inventory:
    def __init__(self, clock):
        self.clock, self.stock, self.holds, self._lock = clock, {}, {}, threading.Lock()

    def add(self, sku, qty):
        with self._lock:
            self.stock[sku] = self.stock.get(sku, 0) + qty

    def reserve(self, order_id, sku, qty, ttl_s=600):
        with self._lock:
            if order_id in self.holds:                              # idempotent: a retried request returns the same hold
                return True
            if self.stock.get(sku, 0) < qty:
                return False
            self.stock[sku] -= qty
            self.holds[order_id] = (sku, qty, self.clock() + ttl_s)
            return True

    def confirm(self, order_id):
        with self._lock:
            hold = self.holds.get(order_id)
            if hold is None or hold[2] < self.clock():
                return False                                        # expired holds cannot be confirmed
            del self.holds[order_id]                                # the stock stays deducted: it is sold
            return True

    def release_expired(self):
        with self._lock:
            now = self.clock()
            for order_id, (sku, qty, expires) in list(self.holds.items()):
                if expires < now:
                    self.stock[sku] += qty
                    del self.holds[order_id]

now = [0.0]
inv = Inventory(clock=lambda: now[0])
inv.add("sku", 10)
results = []
def buyer(i):
    results.append(inv.reserve(f"order-{i}", "sku", 1))
threads = [threading.Thread(target=buyer, args=(i,)) for i in range(50)]
[t.start() for t in threads]; [t.join() for t in threads]
assert sum(results) == 10 and inv.stock["sku"] == 0                 # 50 shoppers, 10 units, exactly 10 holds: no oversell

assert inv.reserve("order-0", "sku", 1) is True and inv.stock["sku"] == 0     # a retry of an existing order changes nothing

inv.add("other", 1)
assert inv.reserve("late", "other", 1) is True
now[0] = 601.0                                                      # the customer never paid
assert inv.confirm("late") is False                                 # too late to confirm
inv.release_expired()
assert inv.stock["other"] == 1 and "late" not in inv.holds          # the unit is back on sale
assert inv.confirm("order-1") is False                              # every hold from t=0 has expired as well
inv.release_expired()
assert inv.stock["sku"] == 10
```

In a real platform the lock becomes one atomic statement per SKU (`UPDATE stock SET qty = qty - :n WHERE sku = :s AND qty >= :n`, then check the affected rows), the hold sweeper is a scheduled job, and the order flow around it is a saga: reserve, charge, confirm, with `release` as the compensation. Hot SKUs (a flash sale) need the stock counter in a fast store and a queue in front, because a single row is the bottleneck.
'''

S["07-proximity-service.md"] = r'''

---

## 11. Runnable Model: Geohash Cells and Neighbour Search

A geohash turns a coordinate into a short string whose shared prefix means "nearby", so a proximity query becomes a prefix lookup. The catch is cell boundaries: a point just across the edge lives in a different cell, so you must also search the neighbours.

```python
import math
import random

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

def encode(lat, lon, precision):
    lat_lo, lat_hi, lon_lo, lon_hi = -90.0, 90.0, -180.0, 180.0
    bits, bit, ch, even, out = [16, 8, 4, 2, 1], 0, 0, True, []
    while len(out) < precision:
        if even:
            mid = (lon_lo + lon_hi) / 2
            if lon >= mid: ch |= bits[bit]; lon_lo = mid
            else: lon_hi = mid
        else:
            mid = (lat_lo + lat_hi) / 2
            if lat >= mid: ch |= bits[bit]; lat_lo = mid
            else: lat_hi = mid
        even = not even
        if bit < 4:
            bit += 1
        else:
            out.append(BASE32[ch]); bit, ch = 0, 0
    return "".join(out)

def cell_size(precision):
    """Cell height and width in degrees for a geohash of this precision."""
    lon_bits = (5 * precision + 1) // 2
    lat_bits = 5 * precision // 2
    return 180 / 2 ** lat_bits, 360 / 2 ** lon_bits

def haversine_m(a, b):
    r = 6_371_000
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def search_cells(lat, lon, precision):
    dlat, dlon = cell_size(precision)
    return {encode(lat + i * dlat, lon + j * dlon, precision) for i in (-1, 0, 1) for j in (-1, 0, 1)}

assert encode(42.6, -5.6, 5) == "ezs42"                              # the standard geohash example
assert encode(57.64911, 10.40744, 11) == "u4pruydqqvj"               # the example from the geohash specification
assert encode(42.6, -5.6, 5).startswith(encode(42.6, -5.6, 3))       # a longer hash refines a shorter one

random.seed(8)
CENTRE, PREC, RADIUS = (37.77, -122.42), 6, 400                      # a 6-character cell is about 1.2 km by 0.6 km
points = [(CENTRE[0] + random.uniform(-0.03, 0.03), CENTRE[1] + random.uniform(-0.03, 0.03)) for _ in range(3000)]
index = {}
for i, p in enumerate(points):
    index.setdefault(encode(*p, PREC), []).append(i)

def nearby(lat, lon, radius_m):
    candidates = [i for cell in search_cells(lat, lon, PREC) for i in index.get(cell, [])]
    return {i for i in candidates if haversine_m((lat, lon), points[i]) <= radius_m}

def brute(lat, lon, radius_m):
    return {i for i, p in enumerate(points) if haversine_m((lat, lon), p) <= radius_m}

checked = 0
for _ in range(60):
    q = (CENTRE[0] + random.uniform(-0.02, 0.02), CENTRE[1] + random.uniform(-0.02, 0.02))
    assert nearby(*q, RADIUS) == brute(*q, RADIUS)                  # the 9-cell search misses nothing within the radius
    checked += 1

# Why the neighbours matter: searching only the query's own cell misses points just across a boundary
misses = 0
for _ in range(60):
    q = (CENTRE[0] + random.uniform(-0.02, 0.02), CENTRE[1] + random.uniform(-0.02, 0.02))
    own = {i for i in index.get(encode(*q, PREC), []) if haversine_m(q, points[i]) <= RADIUS}
    misses += len(brute(*q, RADIUS) - own)
assert misses > 0
```

The rule behind the assertion: **the search radius must be no larger than the cell**, so every point within it lies in the query cell or one of its eight neighbours; for a bigger radius choose a coarser precision. Real services add a quadtree or S2/H3 cells for uneven density (a dense city needs smaller cells than a desert) and keep the index in memory, sharded by region.
'''

S["08-tinder.md"] = r'''

---

## 11. Runnable Model: Mutual-Like Detection and a Bloom Filter for "Already Seen"

Two small mechanisms carry most of the load: detecting a match **exactly once** when likes cross, and remembering which profiles a user has already seen without storing billions of ids.

```python
import math
import threading

class Matcher:
    def __init__(self):
        self.likes, self.matches, self._lock = set(), set(), threading.Lock()

    def like(self, a, b):
        """Record that a likes b. Returns 'match' exactly once, when b already liked a; repeated calls are harmless."""
        with self._lock:
            if (a, b) in self.likes:
                return "duplicate"
            self.likes.add((a, b))
            if (b, a) in self.likes:
                self.matches.add(frozenset((a, b)))
                return "match"
            return "liked"

m = Matcher()
assert m.like("ann", "bo") == "liked"
assert m.like("ann", "bo") == "duplicate"                           # a double tap changes nothing
assert m.like("bo", "ann") == "match" and m.matches == {frozenset(("ann", "bo"))}

m2, outcomes = Matcher(), []
t1 = threading.Thread(target=lambda: outcomes.append(m2.like("x", "y")))
t2 = threading.Thread(target=lambda: outcomes.append(m2.like("y", "x")))
t1.start(); t2.start(); t1.join(); t2.join()
assert sorted(outcomes) == ["liked", "match"]                       # simultaneous opposite likes yield exactly one match

class Bloom:
    def __init__(self, bits, hashes):
        self.m, self.k, self.bits = bits, hashes, bytearray((bits + 7) // 8)
    def _positions(self, item):
        h1 = hash((item, 1)) % self.m
        h2 = (hash((item, 2)) % (self.m - 1)) + 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]      # double hashing derives k positions from two hashes
    def add(self, item):
        for p in self._positions(item):
            self.bits[p // 8] |= 1 << (p % 8)
    def __contains__(self, item):
        return all(self.bits[p // 8] >> (p % 8) & 1 for p in self._positions(item))

n, bits, k = 10_000, 100_000, 7                                     # 10 bits per profile
bloom = Bloom(bits, k)
for i in range(n):
    bloom.add(f"profile-{i}")
assert all(f"profile-{i}" in bloom for i in range(n))               # no false negatives, ever
false_positives = sum(f"other-{i}" in bloom for i in range(20_000)) / 20_000
expected = (1 - math.exp(-k * n / bits)) ** k                       # about 0.8%
assert false_positives < 3 * expected and false_positives < 0.03
print(round(expected, 4), false_positives)
```

Two design consequences. A Bloom filter says "definitely not seen" or "probably seen", so a false positive only means a profile is skipped, which a dating feed can afford; 10 bits per remembered profile gives under 1% skips. And match detection must be **atomic** on the pair: in production that is a single conditional write on a pair-keyed record, not read-then-write in application code.
'''

S["09-uber.md"] = r'''

---

## 11. Runnable Model: Nearest-Driver Search on a Grid, and a Bounded Surge Multiplier

Scanning every driver for each request does not scale; a grid index looks at nearby cells first and expands outward only when needed. The correctness condition is the part to get right: stop only when no unvisited cell can contain a closer driver.

```python
import math
import random

class GridIndex:
    def __init__(self, cell):
        self.cell, self.cells = cell, {}

    def _key(self, x, y):
        return int(x // self.cell), int(y // self.cell)

    def add(self, driver_id, x, y):
        self.cells.setdefault(self._key(x, y), []).append((driver_id, x, y))

    def nearest(self, x, y, k=1):
        cx, cy = self._key(x, y)
        found, ring = [], 0
        while True:
            for i in range(cx - ring, cx + ring + 1):
                for j in range(cy - ring, cy + ring + 1):
                    if max(abs(i - cx), abs(j - cy)) == ring:       # only the new outer ring
                        found += self.cells.get((i, j), [])
            found.sort(key=lambda d: math.hypot(d[1] - x, d[2] - y))
            safe_radius = ring * self.cell                          # everything within this distance has been seen
            if len(found) >= k and math.hypot(found[k - 1][1] - x, found[k - 1][2] - y) <= safe_radius:
                return [d[0] for d in found[:k]]
            ring += 1
            if ring > 10_000:
                return [d[0] for d in found[:k]]

random.seed(5)
drivers = [(f"d{i}", random.uniform(0, 100), random.uniform(0, 100)) for i in range(2000)]
grid = GridIndex(cell=5)
for d in drivers:
    grid.add(*d)

def brute(x, y, k):
    return [d[0] for d in sorted(drivers, key=lambda d: math.hypot(d[1] - x, d[2] - y))[:k]]

for _ in range(300):
    x, y, k = random.uniform(0, 100), random.uniform(0, 100), random.randint(1, 5)
    assert grid.nearest(x, y, k) == brute(x, y, k)                  # identical to scanning every driver

sparse = GridIndex(cell=5)
sparse.add("lonely", 90, 90)
assert sparse.nearest(1, 1) == ["lonely"]                           # expands ring by ring until it finds someone

def surge(requests, drivers, cap=3.0):
    """1.0 when supply covers demand; grows with the shortage; never above the cap."""
    if drivers <= 0:
        return cap
    return min(cap, max(1.0, 1 + 0.5 * (requests / drivers - 1)))

assert surge(10, 10) == 1.0 and surge(5, 10) == 1.0                 # plenty of drivers: no surge
assert surge(20, 10) == 1.5 and surge(1000, 10) == 3.0              # shortage raises the price, but only up to the cap
assert surge(30, 10) >= surge(20, 10) >= surge(10, 10)              # monotonic in demand
```

What real dispatch adds: road-network ETAs instead of straight-line distance, a **batch matching window** of a couple of seconds so a global assignment can beat one-at-a-time greedy matching, smoothing of the surge multiplier per zone so prices do not flicker, and fencing so a driver is never offered two trips at once (the double-assignment bug from the ride-sharing low-level case study).
'''

S["10-twitter.md"] = r'''

---

## 11. Runnable Model: Time-Sortable Unique IDs (Snowflake)

Tweets need IDs that are unique across thousands of machines **without coordination** and that sort by creation time (so a timeline is a range scan). The classic layout packs a timestamp, a machine id and a per-millisecond sequence into 64 bits.

```python
import threading

EPOCH_MS = 1_288_834_974_657                                         # a custom epoch keeps the timestamp small
MACHINE_BITS, SEQ_BITS = 10, 12                                       # 1,024 machines, 4,096 ids per machine per millisecond

class Snowflake:
    def __init__(self, machine_id, clock_ms, sleep_ms):
        assert 0 <= machine_id < 2 ** MACHINE_BITS
        self.machine, self.clock, self.sleep = machine_id, clock_ms, sleep_ms
        self.last_ms, self.seq, self._lock = -1, 0, threading.Lock()

    def next_id(self):
        with self._lock:
            now = self.clock()
            if now < self.last_ms:
                raise RuntimeError("clock moved backwards: refusing to issue ids")
            if now == self.last_ms:
                self.seq = (self.seq + 1) & (2 ** SEQ_BITS - 1)
                if self.seq == 0:                                     # 4,096 ids used in this millisecond: wait for the next one
                    while now <= self.last_ms:
                        self.sleep()
                        now = self.clock()
            else:
                self.seq = 0
            self.last_ms = now
            return ((now - EPOCH_MS) << (MACHINE_BITS + SEQ_BITS)) | (self.machine << SEQ_BITS) | self.seq

def decode(i):
    return {"ms": (i >> (MACHINE_BITS + SEQ_BITS)) + EPOCH_MS, "machine": (i >> SEQ_BITS) & (2 ** MACHINE_BITS - 1), "seq": i & (2 ** SEQ_BITS - 1)}

t = [EPOCH_MS + 5_000]
gen = Snowflake(7, clock_ms=lambda: t[0], sleep_ms=lambda: t.__setitem__(0, t[0] + 1))

a, b = gen.next_id(), gen.next_id()
assert decode(a) == {"ms": EPOCH_MS + 5_000, "machine": 7, "seq": 0} and decode(b)["seq"] == 1
assert a < b                                                          # same millisecond: the sequence orders them

t[0] += 1
c = gen.next_id()
assert c > b and decode(c)["seq"] == 0                                # a later millisecond always sorts later

ids = [gen.next_id() for _ in range(10_000)]                          # exhausts the sequence repeatedly and waits on the clock
assert ids == sorted(ids) and len(set(ids)) == len(ids)               # strictly increasing, no duplicates
assert t[0] > EPOCH_MS + 5_001                                        # and the generator advanced time rather than reusing a millisecond

t[0] -= 100
try:
    gen.next_id()
    raise AssertionError("expected RuntimeError")
except RuntimeError:
    pass                                                              # a backwards clock must not produce duplicates

t[0] += 1000
g1, g2 = Snowflake(1, lambda: t[0], lambda: None), Snowflake(2, lambda: t[0], lambda: None)
assert g1.next_id() != g2.next_id()                                   # same millisecond, different machines: still unique

assert (2 ** 41 - 1) / (1000 * 60 * 60 * 24 * 365.25) > 69            # 41 bits of milliseconds last about 69 years
```

Why this layout answers the interview question: the **timestamp in the high bits** makes IDs sortable by time (cursor pagination without a separate index), the **machine id** removes coordination, the **sequence** handles bursts inside a millisecond, and the **clock check** is the failure mode to name (NTP steps backwards; real systems refuse or wait). Where ordering across machines must be exact, the IDs are only roughly time-ordered, which is acceptable for timelines.
'''

for name, text in S.items():
    f = R / name
    t = f.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    t = t.replace("\r\n", "\n")
    if "## 11. Runnable Model" not in t:
        f.write_bytes((t.rstrip("\n") + "\n" + text).replace("\n", nl).encode("utf-8"))
    sec = f.read_text(encoding="utf-8")
    sec = sec[sec.index("## 11. Runnable Model"):]
    for b in re.findall(r"^```python\n(.*?)^```", sec, re.S | re.M):
        with open("tmpm.py", "w", encoding="utf-8") as fh:
            fh.write(b)
        r = subprocess.run([sys.executable, "tmpm.py"], capture_output=True, text=True, timeout=120)
        print(name[:34], len(f.read_text(encoding="utf-8").split()), "words", "OK" if r.returncode == 0 else "FAIL " + r.stderr.strip()[-450:], r.stdout.strip()[-60:])
os.path.exists("tmpm.py") and os.remove("tmpm.py")

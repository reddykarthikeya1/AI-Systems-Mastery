# Beginner Playground - The Physics of Scalability and Capacity Math

> *"A coffee shop at 99% busy is not 1% worse than one at 90% busy. The queue is ten times longer, and everybody in it feels it."*


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

## 1. The numbers worth memorising

Every design decision is really a bet about which of these you are paying.

| Operation | Time | Relative |
| :--- | ---: | ---: |
| L1 cache reference | 1 ns | 1 |
| Main memory reference | 100 ns | 100 |
| SSD random read | 100,000 ns | 100,000 |
| Round trip within a datacentre | 500,000 ns | 500,000 |
| Round trip across the Atlantic | 150,000,000 ns | 150,000,000 |

The last row is the one that matters most: it is set by the speed of light and no
amount of engineering will reduce it. Distance is a design constraint.

```python
NANOSECOND = 1e-9
timings_ns = {
    "l1_cache": 1,
    "memory": 100,
    "ssd_read": 100_000,
    "datacentre_rtt": 500_000,
    "atlantic_rtt": 150_000_000,
}

for name, ns in timings_ns.items():
    print(f"  {name:<16} {ns * NANOSECOND * 1000:>10.3f} ms")

assert timings_ns["atlantic_rtt"] / timings_ns["memory"] == 1_500_000
print("One Atlantic round trip costs as much as 1.5 million memory reads.")
```

---

## 2. Little's Law: the only queueing formula you must know

**L = lambda x W.** Items in the system = arrival rate x time each one spends there.

It needs no assumptions about the distribution of anything, which is why it always
holds. Use it to answer "how many concurrent requests am I actually handling" -
and therefore how many threads, connections or containers you need.

```python
arrival_rate = 500          # requests per second
time_in_system = 0.2        # seconds each

concurrent = arrival_rate * time_in_system
print(f"{arrival_rate} req/s x {time_in_system}s each = {concurrent:.0f} in flight")
assert concurrent == 100

# Same law, rearranged: a thread pool of 50 caps you at a known throughput.
pool_size = 50
max_throughput = pool_size / time_in_system
print(f"a pool of {pool_size} threads can sustain {max_throughput:.0f} req/s, no more")
assert max_throughput == 250
print("Beyond that the queue grows without limit. This is arithmetic, not tuning.")
```

---

## 3. Why 99% utilisation is a different planet from 90%

For a single queue, average time in the system is `1 / (service_rate - arrival_rate)`.

Look at the denominator. As arrivals approach capacity it goes to zero, and the
waiting time goes to infinity. There is no gentle slope at the end - it is a wall.

```python
service_rate = 100          # requests per second the server can complete


def time_in_system_at(load):
    return 1 / (service_rate - load)


print(f"{'load':>6} {'utilisation':>12} {'latency':>12}")
for load in (50, 80, 90, 95, 99):
    print(f"{load:>6} {load / service_rate:>11.0%} "
          f"{time_in_system_at(load) * 1000:>10.0f} ms")

at_90 = time_in_system_at(90)
at_99 = time_in_system_at(99)
print(f"\n10% more traffic, {at_99 / at_90:.0f}x the latency")
assert round(at_99 / at_90) == 10
print("Plan for 60-70% utilisation. The headroom IS the design.")
```

---

## 4. Amdahl's Law: the part you cannot parallelise

If 5% of a job must run serially, then even with infinite machines you cannot go
more than 20x faster. The serial fraction sets a ceiling that no amount of
hardware can lift.

Which is why "just add more servers" stops working, and why finding the serial
part - a single database, a global lock, one leader - is usually the whole job.

```python
def speedup(serial_fraction, workers):
    return 1 / (serial_fraction + (1 - serial_fraction) / workers)


for workers in (1, 10, 100, 1_000, 1_000_000):
    print(f"  {workers:>9,} workers -> {speedup(0.05, workers):>6.1f}x faster")

ceiling = 1 / 0.05
print(f"ceiling with 5% serial work: {ceiling:.0f}x, no matter what you spend")
assert speedup(0.05, 1_000_000) < ceiling
assert speedup(0.05, 1_000) > speedup(0.05, 100)
assert speedup(0.05, 1_000_000) - speedup(0.05, 1_000) < 1, "the last 999,000 add nothing"
```

---

## 5. Predict before you run

A server handles 100 requests a second at full tilt. Traffic rises from 90
to 99 requests a second - a 10% increase. Does the waiting time rise by 10%,
by 100%, or by something else entirely?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

This is why systems fall over suddenly rather than gradually. Everything is
fine at 85% utilisation, and then a small traffic bump takes the latency from
100 ms to several seconds with no code change and no error in any log.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).

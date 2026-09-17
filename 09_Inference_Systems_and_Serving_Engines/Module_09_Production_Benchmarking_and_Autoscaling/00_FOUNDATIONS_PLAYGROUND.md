# 🐣 Interactive Foundations Playground: Production Benchmarking & Autoscaling

> *"Little's Law is the immutable equation of servers: Concurrent Users = Arrival Rate x Latency."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Little's Law for LLM Serving

If arrival rate is $\lambda = 20$ requests/sec and average request latency is $W = 1.5$ seconds, exactly $L = \lambda W = 30$ concurrent requests are in flight.

```python
arrival_rate = 20.0     # req/sec
avg_latency_sec = 1.5   # seconds
concurrent_in_flight = arrival_rate * avg_latency_sec

assert concurrent_in_flight == 30.0
print(f"System requires support for {concurrent_in_flight:.0f} concurrent requests.")
```

---

## 2. Queue Delay Knee Point

As utilization approaches 100%, M/M/1 queuing delay explodes hyperbolically: $T_q = \frac{\rho}{\mu(1 - \rho)}$.

```python
def queue_delay(utilization, service_rate=10.0):
    return utilization / (service_rate * (1.0 - utilization))

q_70 = queue_delay(0.70)
q_95 = queue_delay(0.95)
q_ratio = q_95 / q_70

assert q_ratio > 7.0
assert round(q_ratio, 1) == 8.1
print(f"Queue delay explodes {q_ratio:.1f}x when utilization goes from 70% to 95%.")
```

---

## 3. Autoscaling Target Utilization Policy

Production autoscalers target 65-75% GPU utilization to absorb traffic surges without violating SLA latency budgets.

```python
target_utilization = 0.70
current_requests = 140
capacity_per_replica = 20
required_replicas = math.ceil(current_requests / (capacity_per_replica * target_utilization))

assert required_replicas == 10
assert required_replicas * capacity_per_replica * target_utilization >= current_requests
print(f"Autoscaler provisioned {required_replicas} GPU replicas to maintain 70% utilization target.")
```

---

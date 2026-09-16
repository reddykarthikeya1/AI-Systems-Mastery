# Module 20: Troubleshooting, Caching Traps & Stampede Failures

This reference guide details the three most critical caching vulnerabilities in distributed systems: **Cache Penetration**, **Cache Avalanche**, and **Cache Stampede**.

---

## 1. Cache Stampede (Thundering Herd)

### The Problem
A hot cache key (e.g. homepage banner) expires. In the next 100 milliseconds, 5,000 concurrent requests all experience a Cache Miss simultaneously and hammer the database with 5,000 identical heavy queries.

### The Fix
Use **Distributed Mutex Locking** or **Probabilistic Early Re-computation (XFetch)** so only 1 worker queries the database while others wait or serve slightly stale data.

---

## 2. Cache Avalanche (Simultaneous Expirations)

### The Problem
All 100,000 cached products were set with `TTL = 3600s` during deployment. At $t = 3600s$, all 100,000 keys expire at the exact same millisecond, crashing the database.

### The Fix
Always inject random jitter into TTL:
$$\text{TTL} = \text{base\_ttl} + \text{random.randint}(0, 300)$$

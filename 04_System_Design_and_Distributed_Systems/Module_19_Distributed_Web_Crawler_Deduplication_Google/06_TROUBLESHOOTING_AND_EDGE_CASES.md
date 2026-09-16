# Module Troubleshooting & Production Edge Cases: Module_19_Distributed_Web_Crawler_Deduplication_Google

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. DNS Resolver Exhaustion Under Massive Host Crawling

### 🚨 The Bug & Symptoms
Billions of requests to unique web domains overload internal DNS caching infrastructure.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Implement a dedicated asynchronous DNS caching resolver pool with custom TTL caching.

---

## 2. Robots.txt Ignoring Violates Legal Compliance

### 🚨 The Bug & Symptoms
Crawlers hammering private administrative paths cause legal notices and IP bans.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Parse and cache `robots.txt` per host; evaluate rules before enqueueing any URL.

---

## 3. Near-Duplicate Document Ingestion

### 🚨 The Bug & Symptoms
Websites with identical text but different tracking query parameters (`?utm_source=xyz`) duplicate index storage.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Calculate 64-bit SimHash of page text; drop pages whose Hamming distance is <= 3.

---


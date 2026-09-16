# Module Troubleshooting & Production Edge Cases: Module_14_Distributed_URL_Shortener_TinyURL

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. HTTP 301 vs. 302 Redirect Semantic Confusion

### 🚨 The Bug & Symptoms
Using HTTP 301 (Permanent) prevents server from collecting analytics because browsers cache the destination URL locally.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use HTTP 302 (Found) or 307 (Temporary Redirect) if real-time click tracking and analytics are required.

---

## 2. KGS Token Starvation During Worker Crash

### 🚨 The Bug & Symptoms
A worker node pre-allocates 100,000 tokens from Key Generation Service and crashes, leaving gaps in token sequence.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Pre-allocate smaller batches (e.g. 1,000 tokens) and log uncommitted token blocks.

---

## 3. Database Read Bottleneck Under Viral Redirect Spikes

### 🚨 The Bug & Symptoms
A viral short link receives 50,000 clicks/second, bypassing database read replicas and causing connection pool exhaustion.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Cache top 20% viral links in Redis LRU cache with active replication.

---


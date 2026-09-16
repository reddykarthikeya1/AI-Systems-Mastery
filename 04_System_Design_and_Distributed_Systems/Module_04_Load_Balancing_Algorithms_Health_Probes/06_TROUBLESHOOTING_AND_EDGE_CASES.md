# Module Troubleshooting & Production Edge Cases: Module_04_Load_Balancing_Algorithms_Health_Probes

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Sticky Session Hotspotting

### 🚨 The Bug & Symptoms
IP Hashing routes all traffic from a large corporate proxy or university NAT gateway (thousands of users) to a single backend node.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Hash on session cookie or token rather than raw client IP address.

---

## 2. Weighted Round Robin Integer Modulo Bias

### 🚨 The Bug & Symptoms
Naive weighted round robin sends all requests for the heaviest server consecutively (e.g. 5 to A, 1 to B), causing burst queuing on A.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use Smooth Weighted Round Robin (Nginx algorithm) to interleave server selections evenly.

---

## 3. Connection Draining Premature Termination

### 🚨 The Bug & Symptoms
Terminating worker containers during rolling deployment immediately drops in-flight database transactions and long-lived client uploads.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Implement graceful connection draining: stop routing new requests, allow 30–60 seconds for active requests to complete.

---


# Module Troubleshooting & Production Edge Cases: Module_20_Flash_Sale_Inventory_Reservation_Amazon

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Unpaid Reservation Stock Leakage

### 🚨 The Bug & Symptoms
User reserves stock during checkout but abandons cart; stock remains locked indefinitely.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Enforce strict 15-minute lease TTL; run background reaper to roll back expired reservations.

---

## 2. Database Primary Key Lock Contention

### 🚨 The Bug & Symptoms
50,000 threads trying to update the exact same inventory row in MySQL results in lock deadlocks and timeouts.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Manage inventory in Redis memory; batch-commit decrements to SQL database asynchronously.

---

## 3. Duplicate Purchase via Webhook Replay

### 🚨 The Bug & Symptoms
A slow network causes payment gateway to send duplicate webhook confirmations, decrementing inventory twice.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Store payment idempotency key; ignore webhooks for already-completed orders.

---


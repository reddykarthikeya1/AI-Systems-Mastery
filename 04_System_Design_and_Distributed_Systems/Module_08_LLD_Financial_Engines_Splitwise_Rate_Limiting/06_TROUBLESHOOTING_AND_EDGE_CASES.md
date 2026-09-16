# Module Troubleshooting & Production Edge Cases: Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Debt Simplification Cyclic Deadlock

### 🚨 The Bug & Symptoms
Greedy debt simplification that does not compute net balances first gets trapped in cyclic debtor-creditor loops.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Always collapse transactions into net balances ($net = credits - debits$) before running greedy settlement.

---

## 2. Rate Limiter Time-Drift Under Monotonic Clock Reset

### 🚨 The Bug & Symptoms
Using `time.time()` (wall-clock) instead of `time.monotonic()` causes token refill calculations to fail during NTP adjustments.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Always use `time.monotonic()` for interval and rate limiting calculations.

---

## 3. Negative Debt Settlement Injection

### 🚨 The Bug & Symptoms
Failing to validate that split amounts are strictly positive allows users to inject negative expenses, stealing money from group members.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Enforce validation: `assert amount_cents > 0` on every split.

---


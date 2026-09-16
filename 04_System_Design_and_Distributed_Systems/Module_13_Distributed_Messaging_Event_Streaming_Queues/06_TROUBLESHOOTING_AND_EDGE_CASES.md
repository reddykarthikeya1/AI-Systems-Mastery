# Module Troubleshooting & Production Edge Cases: Module_13_Distributed_Messaging_Event_Streaming_Queues

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Consumer Group Rebalance Storm

### 🚨 The Bug & Symptoms
A slow consumer taking longer than `max.poll.interval.ms` to process a batch is marked dead by broker, triggering repeated cluster-wide rebalances.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Offload heavy processing to asynchronous pools or increase `max.poll.interval.ms`.

---

## 2. Duplicate Delivery on Consumer Crash Before Commit

### 🚨 The Bug & Symptoms
Consumer finishes database write but crashes before committing offset to broker. On restart, messages are re-processed.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Design consumers to be strictly idempotent using unique message deduplication IDs.

---

## 3. Poison Pill Deadlock

### 🚨 The Bug & Symptoms
A malformed message crashes the consumer parser. The consumer restarts, reads the same offset, and crashes in an infinite boot loop.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Implement Dead Letter Queues (DLQ): route poisoned messages to DLQ after $N$ failures and commit offset.

---


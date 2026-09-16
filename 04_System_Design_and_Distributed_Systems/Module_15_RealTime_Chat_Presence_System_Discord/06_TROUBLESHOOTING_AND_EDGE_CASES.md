# Module Troubleshooting & Production Edge Cases: Module_15_RealTime_Chat_Presence_System_Discord

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. WebSocket Ephemeral Connection Leaks

### 🚨 The Bug & Symptoms
Clients closing laptops without TCP FIN handshake leave phantom connections open on the server indefinitely.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Enforce periodic bidirectional ping/pong heartbeats; reap connections missing 2 consecutive pings.

---

## 2. Cross-Gateway Message Routing Misses

### 🚨 The Bug & Symptoms
User A sends a message to User B, but User B is connected to Gateway 3 while User A is on Gateway 1.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use a distributed Pub/Sub message bus (Redis Pub/Sub, Kafka) where each Gateway subscribes to user-session channels.

---

## 3. Offline Message Buffer Exhaustion

### 🚨 The Bug & Symptoms
Storing millions of offline messages for inactive users in fast RAM exhausts memory.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Spool offline messages into persistent disk storage (Cassandra/DynamoDB) and fetch on reconnect.

---


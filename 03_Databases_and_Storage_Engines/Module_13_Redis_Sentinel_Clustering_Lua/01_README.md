# Module 13: Redis Sentinel, Clustering, Lua Scripting & Streams

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

---

## 🛡️ 1. Redis Sentinel & High Availability

A standalone Redis instance represents a single point of failure (SPOF). Redis Sentinel provides automated monitoring, failure detection, notification, and master-replica failover without human intervention.

```
                  ┌──────────────────────┐
                  │ Client Application   │
                  └──────────┬───────────┘
                             │ 1. Ask: "Who is current Master?"
                             ▼
             ┌────────────────────────────────┐
             │   Sentinel Quorum (e.g. 3)     │
             │ [Sentinel 1] [Sentinel 2] [...]│
             └──────────────┬─────────────────┘
                            │ 2. Heartbeat (PING), SDOWN/ODOWN detection
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
    ┌───────────┐    Replication Stream  ┌───────────┐
    │  Master   │ ═════════════════════► │  Replica  │
    │  (Port)   │                        │  (Port)   │
    └───────────┘                        └───────────┘
```

### Replication Mechanics: Replication ID & Offset
Replication between master and replica is asynchronous:
- The master and replica each track a **Replication ID** and a 64-bit byte counter called **Replication Offset** (`master_repl_offset`).
- Every byte written to the master increments the master offset. Replicas ack their received offset periodically (`REPLCONF ACK <offset>`).
- **Replication Backlog Buffer**: An in-memory ring buffer (default 1MB) on the master storing recent write bytes.
- **Partial Resync (`PSYNC`)**: When a disconnected replica reconnects, if its offset is still within the backlog buffer, the master streams only the missing delta bytes. If the replica fell too far behind, a **Full Resync** occurs (master forks, writes `dump.rdb`, transfers file over socket, replica wipes memory and reloads).

### Failure Detection: SDOWN vs. ODOWN
1. **Subjective Down (`sdown`)**: A single Sentinel fails to receive a `PONG` response to its `PING` within `down-after-milliseconds` (e.g., 5000ms).
2. **Objective Down (`odown`)**: The Sentinel queries its peers via `SENTINEL is-master-down-by-addr`. Once a configured **quorum** (e.g., 2 out of 3 sentinels) confirm the master is down, the state escalates to `odown`.

### Failover & Leader Election
1. Sentinels initiate a Raft-inspired leader election with incrementing epochs.
2. The Sentinel that wins the election becomes the failover leader.
3. The leader chooses the best replica to promote based on:
   - **Lowest `slave-priority`** (0 means never promote).
   - **Highest `replication offset`** (most up-to-date data, minimizing data loss).
   - **Lowest Run ID** (deterministic tie-breaker).
4. Leader executes `SLAVEOF NO ONE` on the chosen replica and reconfigures the remaining replicas via `SLAVEOF <new_master_ip> <port>`.
5. Publishes notifications over Redis Pub/Sub (`+switch-master`), notifying clients to reconnect to the new master.

---

## 🌐 2. Redis Cluster: 16,384 Hash Slots & Sharding

When data exceeds the RAM of a single physical server (e.g., > 100 GB) or write throughput exceeds one CPU core (~100k ops/sec), you need horizontal scale-out. **Redis Cluster** provides multi-master sharding with automated routing and master-replica failover.

### The 16,384 Hash Slot Topology
Redis Cluster does not use consistent hashing. Instead, the keyspace is statically divided into **exactly 16,384 Hash Slots** (numbered `0` to `16383`):
$$\text{Slot} = \text{CRC16}(\text{key}) \pmod{16384}$$

In a 3-master cluster:
- **Master A**: Serves slots `0 – 5460`
- **Master B**: Serves slots `5461 – 10922`
- **Master C**: Serves slots `10923 – 16383`

```
Key: "user:100" ──► CRC16("user:100") = 23941 ──► 23941 % 16384 = 7557 ──► Routed to Master B!
```

### Hash Tags `{...}` for Multi-Key Operations
By default, Redis Cluster forbids multi-key operations (like `MGET`, transactions, or Lua scripts) if the keys reside on different nodes (`CROSSSLOT Keys in request don't hash to the same slot`).
- **Solution — Hash Tags**: If a key contains `{...}`, only the text inside curly braces is hashed!
  - `user:{100}:profile` $\implies$ hashes `{100}` $\implies$ Slot 4120
  - `user:{100}:orders` $\implies$ hashes `{100}` $\implies$ Slot 4120
  - Both keys are guaranteed to reside on the same cluster node, enabling atomic multi-key transactions!

### Client Redirection: `-MOVED` vs `-ASK`
Clients cache the slot-to-node routing table locally. When the topology changes:
1. **`-MOVED <slot> <ip:port>`**: The key's slot has permanently migrated to a new node. The client updates its local routing cache and re-executes the command on the new node.
2. **`-ASK <slot> <ip:port>`**: The slot is currently in the middle of being migrated between nodes. The client sends an `ASKING` command followed by the query to the target node, but **does not** update its local routing cache.

---

## 📜 3. Lua Scripting & Atomic Transactions

In standard Redis, executing multiple commands (`GET`, followed by conditional logic in Python, followed by `SET`) requires optimistic locking via `WATCH` / `MULTI` / `EXEC`. Under high concurrency, `WATCH` frequently aborts, forcing expensive application retries.

### Why Lua Scripts Win
1. **True ACID Atomicity**: Redis executes an entire Lua script atomically inside the core single-threaded event loop. No other command or script can execute while a Lua script runs.
2. **Eliminates Race Conditions**: You can read a value, evaluate business logic, and update keys without locks or abort retries.
3. **Reduced Network Round-Trips**: Multiple dependent queries execute locally on the Redis server in 1 network round-trip.
4. **SHA1 Caching (`EVALSHA`)**: Redis caches the compiled bytecode of scripts. Clients pass the 40-character SHA1 hash instead of the entire script body, conserving bandwidth.

### Canonical Use Case: Atomic Token Bucket Rate Limiter
```lua
-- KEYS[1]: rate limit key
-- ARGV[1]: capacity, ARGV[2]: refill_rate_per_sec, ARGV[3]: requested_tokens, ARGV[4]: current_time
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local requested = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

local state = redis.call('HMGET', key, 'tokens', 'last_updated')
local tokens = tonumber(state[1]) or capacity
local last_updated = tonumber(state[2]) or now

-- Compute refilled tokens based on elapsed time
local elapsed = math.max(0, now - last_updated)
tokens = math.min(capacity, tokens + (elapsed * refill_rate))

if tokens >= requested then
    tokens = tokens - requested
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', now)
    return 1 -- Allowed
else
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', now)
    return 0 -- Rejected (Rate limited)
end
```

---

## 🌊 4. Redis Streams & Consumer Groups

Redis Streams (`XADD`, `XREAD`) is an append-only log data structure modeled after Apache Kafka, designed for high-throughput event sourcing and task queues.

### Stream Architecture
- **Entry ID**: Composed of `<millisecondsTime>-<sequenceNumber>` (e.g. `1693000000000-0`), guaranteeing strict chronological ordering.
- **Radix Tree Internals**: Streams are backed by a Radix Tree (Rax) holding compact listpack chunks, achieving incredible memory efficiency (~100 bytes per event).

### Consumer Groups (`XGROUP`, `XREADGROUP`)
Consumer groups allow multiple workers to cooperatively consume a stream with load balancing:
```
                    ┌─────────────────────────┐
                    │  Stream: "orders_log"   │
                    │  [E1] [E2] [E3] [E4]... │
                    └───────────┬─────────────┘
                                │
                   ┌────────────┴────────────┐
                   ▼ Consumer Group: "orders"▼
            ┌──────────────┐         ┌──────────────┐
            │  Worker-1    │         │  Worker-2    │
            │ (Assigned E1)│         │ (Assigned E2)│
            └──────┬───────┘         └──────┬───────┘
                   │                        │
                   ▼                        ▼
        Pending Entries List (PEL) [Unacknowledged Events]
```
1. **Load Balancing**: Each consumer in the group receives a distinct subset of messages (`>`).
2. **Pending Entries List (PEL)**: When a message is delivered to a consumer, it is recorded in the PEL along with the consumer ID and idle delivery timestamp.
3. **Acknowledgment (`XACK`)**: Once processed, the consumer sends `XACK`. Redis removes the message from the PEL.
4. **Dead Consumer Reclamation (`XAUTOCLAIM` / `XCLAIM`)**: If a worker crashes while processing, other workers inspect the PEL for messages idle longer than `min-idle-time` and claim ownership, guaranteeing **At-Least-Once Delivery**.

---

## 🛠️ 5. Hands-On Lab: Building Sentinel, Cluster & Stream Orchestrator

In this lab, you will implement:
1. **CRC16 Hash Slot & Hash Tag Engine**: Calculate 16,384 cluster slots with `{tag}` extraction and `-MOVED` redirection routing.
2. **Sentinel Quorum & Failover State Machine**: Detect `sdown`, reach `odown` consensus, elect leader, and promote replica by highest replication offset.
3. **Atomic Lua Simulation Engine**: Execute atomic check-and-mutate rate-limiting and compare-and-swap scripts.
4. **Redis Stream & Consumer Group with PEL**: Implement `xadd`, `xreadgroup`, `xack`, and `xclaim` for crash recovery.

---

## 📂 Project Structure
```
Module_13_Redis_Sentinel_Clustering_Lua/
├── README.md
├── 01_sentinel_clustering_streams_demo.py
├── starter/
│   └── sentinel_cluster_streams.py
└── project_solution/
    ├── sentinel_cluster_streams.py
    └── test_sentinel_cluster_streams.py
```

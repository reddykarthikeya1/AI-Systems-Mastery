# Module 13 Redis Sentinel Clustering Lua: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Redis High Availability: Sentinel, Clustering & Lua Scripting** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **How does Redis Sentinel achieve automated master failover?** How does Redis Sentinel achieve automated master failover?
2. **How many Hash Slots exist in a Redis Cluster, and how are keys mapped to them?** How many Hash Slots exist in a Redis Cluster, and how are keys mapped to them?
3. **What is a Redis Hash Tag, and why is it essential for multi-key cluster operations?** What is a Redis Hash Tag, and why is it essential for multi-key cluster operations?
4. **What happens when a client sends a query for a key to the wrong Redis Cluster node?** What happens when a client sends a query for a key to the wrong Redis Cluster node?
5. **Why are Lua scripts atomic in Redis?** Why are Lua scripts atomic in Redis?
6. **What is the difference between MOVED and ASK redirection in Redis Cluster?** What is the difference between MOVED and ASK redirection in Redis Cluster?
7. **What does SCRIPT LOAD and EVALSHA do?** What does SCRIPT LOAD and EVALSHA do?
8. **How does min-replicas-to-write prevent split-brain data loss in Redis Sentinel?** How does min-replicas-to-write prevent split-brain data loss in Redis Sentinel?
9. **Can Redis Cluster automatically rebalance hash slots when adding a new node?** Can Redis Cluster automatically rebalance hash slots when adding a new node?
10. **What is the maximum execution timeout for Lua scripts before Redis allows SCRIPT KILL?** What is the maximum execution timeout for Lua scripts before Redis allows SCRIPT KILL?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Sentinels monitor master nodes via heartbeat pings; when a quorum agrees master is down (ODOWN), a sentinel is elected to promote a replica.

#### Answer 2:
16,384 hash slots. Keys are mapped using `CRC16(key) mod 16384`.

#### Answer 3:
Wrapping part of a key in braces `{user:101}` forces Redis Cluster to hash only the braced substring, placing related keys in the same slot.

#### Answer 4:
The node responds with a `-MOVED <slot> <ip:port>` redirection error instructing the client where to route the request.

#### Answer 5:
Redis executes the entire Lua script without interleaving any other command in its single-threaded event loop.

#### Answer 6:
MOVED indicates a slot migration is permanent; ASK indicates a slot is currently in the process of migrating to another node.

#### Answer 7:
SCRIPT LOAD pre-compiles a Lua script on the Redis server returning a SHA1 digest; EVALSHA executes it by digest, saving bandwidth.

#### Answer 8:
It halts writes on the master if fewer than the specified number of replicas acknowledge heartbeat within a maximum lag window.

#### Answer 9:
Yes, via `redis-cli --cluster reshard` which migrates slot allocations and keys online.

#### Answer 10:
Configured by `lua-time-limit` (default 5,000 ms). After this, Redis accepts `SCRIPT KILL` (read-only) or `SHUTDOWN NOSAVE`.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement an atomic multi-resource reservation engine in Lua that validates inventory and deducts balances atomically.

### 🚀 Challenge 2: Architect Stretch Problem
Build a Redis Sentinel failover client listener that reconnects transparently during master promotion.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. CROSSSLOT Keys in Request Don't Hash to the Same Slot

```python
# Redis Cluster Python Client
import rediscluster

rc = rediscluster.RedisCluster(host="redis-cluster.internal", port=7000)

def transfer_points(from_user: str, to_user: str, amount: int):
    # Multi-key pipeline to transfer loyalty points
    pipe = rc.pipeline()
    pipe.decrby(f"user:{from_user}:balance", amount)
    pipe.incrby(f"user:{to_user}:balance", amount)
    pipe.execute()

transfer_points("alice_99", "bob_102", 50)
```

**Observed symptom:** redis.exceptions.RedisClusterException: CROSSSLOT Keys in request don't hash to the same slot when executing pipeline.

**(a)** Why does Redis Cluster reject multi-key commands or pipelines containing keys from different users?

**(b)** How does Redis Cluster compute key-to-slot mapping, and how can you check which slot each key maps to?

**(c)** How do hash tags (`{...}`) solve this issue, and what is the trade-off of clustering keys into the same hash slot?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Redis Cluster partitions its 16,384 hash slots across primary nodes. Multi-key operations (transactions, MGET/MSET, or transactional pipelines) are strictly constrained to keys that map to the exact same hash slot on the exact same primary node. `user:alice_99:balance` hashes to CRC16("user:alice_99:balance") % 16384, whereas `user:bob_102:balance` hashes to a completely different slot located on a different master node.

**Diagnostic Commands:**
1. In `redis-cli`:
   ```bash
   CLUSTER KEYSLOT "user:alice_99:balance"   # e.g. slot 11422 (Node A)
   CLUSTER KEYSLOT "user:bob_102:balance"     # e.g. slot 4819 (Node B)
   ```
2. Verify node slot assignments:
   ```bash
   CLUSTER NODES
   ```

**Production Fix:**
- **Approach 1 (Hash Tags):** If two keys must reside on the same slot, enclose the common grouping token in braces `{...}`:
  ```python
  # Both keys will hash based ONLY on the string inside '{tenant_42}'
  key1 = "{tenant_42}:user:alice:balance"
  key2 = "{tenant_42}:user:bob:balance"
  ```
- **Approach 2 (Distributed Workflows):** If keys naturally belong to separate entities across the cluster, do not execute multi-key single-node pipelines. Instead, use a two-phase application workflow, or execute two separate single-key calls with idempotency keys and compensating transactions (Saga pattern). Beware that overusing hash tags can create hot shards if too many keys hash to one node.

</details>

---

### D2. Redis Sentinel Split-Brain and Dual-Master Write Loss

```python
# redis.conf on Primary (Node 1)
bind 0.0.0.0
port 6379
# min-replicas-to-write commented out (default 0)
# min-replicas-max-lag commented out (default 10)

# Sentinel configuration on 3 nodes
sentinel monitor mymaster 10.0.1.10 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 15000
```

**Observed symptom:** During a 20-second network partition between datacenter rack A and B, Node 1 continued accepting writes from client partition A. Sentinel in partition B elected Node 2 as new master. Once network healed, 15,000 writes sent to Node 1 vanished completely.

**(a)** What caused the silent loss of 15,000 committed writes when the network partition healed?

**(b)** What command and log entries on Node 1 confirm that it underwent full resynchronization and discarded its dataset?

**(c)** How do `min-replicas-to-write` and `min-replicas-max-lag` guard against split-brain write loss?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Redis replication is asynchronous. During the partition, Node 1 was isolated from Sentinels and replicas in partition B, but still reachable by local clients in partition A. Sentinel formed a quorum in partition B and promoted Node 2. When the partition healed, Sentinels reconfigured Node 1 to become a replica of Node 2. When a replica connects to a new master, it empties its entire local database (`FLUSHALL`) and performs a full resync (RDB snapshot load) from Node 2, completely erasing all writes committed to Node 1 during the partition.

**Diagnostic Commands:**
1. Check Redis logs on Node 1:
   ```text
   [Sentinel] +convert-to-slave master mymaster 10.0.1.10 6379 ...
   [Replication] Connecting to MASTER 10.0.2.20:6379
   [Replication] MASTER <-> REPLICA sync: Flush old data from memory
   ```
2. Check replication lag on replica:
   ```bash
   redis-cli -h node1 INFO replication
   ```

**Production Fix:**
Enforce write fencing using replica acknowledgments in `redis.conf`:
```conf
# Reject writes if fewer than 1 healthy replica acknowledge lag <= 10s
min-replicas-to-write 1
min-replicas-max-lag 10
```
When Node 1 loses connection to all replicas, it immediately responds with `(error) NOREPLICAS Not enough good replicas to write` to local clients, preventing writes to the partitioned master.

</details>

---

### D3. Lua Script Blocking Redis Single-Thread Event Loop

```sql
-- Lua script executed via EVALSHA
local keys = redis.call('KEYS', 'session:user:*')
local expired = 0
for i, k in ipairs(keys) do
    local ttl = redis.call('TTL', k)
    if ttl == -1 then
        redis.call('DEL', k)
        expired = expired + 1
    end
end
return expired
```

**Observed symptom:** All incoming Redis client requests across all microservices time out with connection drops. Redis latency spikes from 0.8ms to 15,000ms. Clients attempting to connect receive '(error) BUSY Redis is busy running a script'.

**(a)** Why does this Lua script freeze all other Redis commands on the server?

**(b)** How can you detect running scripts and safely kill or inspect a frozen Lua script?

**(c)** How should this key-cleanup routine be refactored using SCAN and batched execution?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Redis is fundamentally single-threaded for command execution. Lua scripts in Redis execute atomically and exclusively: while a script is running, no other client command or event loop iteration can proceed. Running `redis.call('KEYS', ...)` on millions of keys scans the entire keyspace in $O(N)$ time in memory inside the Lua VM, blocking all other connections. After `lua-time-limit` (default 5s), Redis starts replying with `BUSY`.

**Diagnostic Commands:**
1. Check slowlog:
   ```bash
   redis-cli SLOWLOG GET 10
   ```
2. Check if a script is currently running:
   ```bash
   redis-cli SCRIPT KILL    # Only succeeds if script has not issued write commands
   # If write commands have been issued, redis requires:
   redis-cli SHUTDOWN NOSAVE
   ```

**Production Fix:**
1. Never run `KEYS` inside Lua or production.
2. Perform cursor-based iteration outside of Lua using `SCAN` in Python in batches of 500:
   ```python
   cursor = 0
   while True:
       cursor, keys = r.scan(cursor=cursor, match="session:user:*", count=500)
       if keys:
           # Check TTL or delete in small pipelines
           pipe = r.pipeline(transaction=False)
           for k in keys:
               pipe.ttl(k)
           ttls = pipe.execute()
           to_del = [k for k, ttl in zip(keys, ttls) if ttl == -1]
           if to_del:
               r.delete(*to_del)
       if cursor == 0:
           break
   ```

</details>

---

### D4. Redis Cluster Slot Migration MOVED vs ASK Loop

```python
import redis
# Using standard redis-py instead of redis-py-cluster / redis.cluster
client = redis.Redis(host="node1.cluster.internal", port=7000)

# Resharding slot 5460 from Node 1 to Node 2 is 40% complete
response = client.get("account:user_8821")
```

**Observed symptom:** Client throws redis.exceptions.ResponseError: ASK 5460 10.0.1.12:7000 and crashes instead of returning the requested user data.

**(a)** What is the difference between a `MOVED` redirection and an `ASK` redirection in Redis Cluster?

**(b)** What exact two-step sequence must a client execute upon receiving an `ASK` redirection?

**(c)** Why did using a non-cluster-aware client library cause this error, and how should it be resolved?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
During online resharding / slot migration in Redis Cluster:
- `MOVED 5460 10.0.1.12:7000` means slot 5460 permanently belongs to Node 2. The client must update its internal slot routing table.
- `ASK 5460 10.0.1.12:7000` is transient: slot 5460 is currently migrating. Some keys are still on Node 1, but the requested key has already been moved to Node 2. The client must query Node 2 *for this request only* without updating its permanent slot routing map.
A non-cluster-aware client does not parse cluster redirections and raises `ResponseError`.

**Diagnostic Commands:**
1. Check migration state in `redis-cli`:
   ```bash
   CLUSTER NODES | grep -E "importing|migrating"
   ```
2. Check key location:
   ```bash
   redis-cli -h 10.0.1.11 -p 7000 CLUSTER KEYSLOT account:user_8821
   ```

**Production Fix:**
1. Switch to a cluster-aware client (`redis.cluster.RedisCluster` in `redis-py >= 4.1`):
   ```python
   from redis.cluster import RedisCluster
   rc = RedisCluster(host="node1.cluster.internal", port=7000)
   val = rc.get("account:user_8821")  # Transparently handles MOVED and ASK
   ```
2. The protocol handshake executed automatically by cluster clients on `ASK`:
   - Connect to target node (`10.0.1.12:7000`)
   - Send `ASKING` command
   - Send the target command: `GET account:user_8821`

</details>

---

### D5. Pub/Sub Slow Consumer Client Output Buffer Overflow

```python
# redis.conf
client-output-buffer-limit pubsub 32mb 8mb 60
# hard limit 32MB, soft limit 8MB for 60 seconds

# Python subscriber running data analysis
sub = r.pubsub()
sub.subscribe("market_ticks_high_frequency")
for message in sub.listen():
    time.sleep(0.05)  # Heavy NumPy processing per tick (20 msgs/sec throughput)
    # Publisher emits 2,000 ticks/sec
```

**Observed symptom:** The subscriber process abruptly disconnects after ~45 seconds with ConnectionResetError: [Errno 104] Connection reset by peer. Redis server logs: 'Client id=4821 scheduled to be closed ASAP for overcoming of output buffer limits'.

**(a)** Why does Redis forcefully terminate the connection of this subscriber?

**(b)** Which Redis commands allow monitoring of client buffer consumption and identifying slow consumers?

**(c)** What architectural pattern should replace Pub/Sub when message consumers require processing time or backpressure?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Redis Pub/Sub has no server-side persistence or backpressure. Published messages are immediately queued into each subscriber's client output buffer in Redis memory. When publisher rate (2,000 msgs/sec) drastically outpaces consumer processing (20 msgs/sec), the subscriber's outbound buffer balloons. Once it breaches the hard limit (32MB) or soft limit (8MB continuously for 60s), Redis disconnects the subscriber to protect itself from Out-Of-Memory (OOM) crashes.

**Diagnostic Commands:**
1. Check client list in `redis-cli`:
   ```bash
   redis-cli CLIENT LIST
   # Look for high 'omem' (output memory) and 'obl' / 'oll' (output buffer/list length)
   ```
2. Check memory usage by clients:
   ```bash
   redis-cli INFO memory | grep mem_clients_normal
   ```

**Production Fix:**
1. Migrate from Pub/Sub to **Redis Streams** (`XADD`, `XREADGROUP`, `XACK`). Redis Streams store messages in a bounded stream (`MAXLEN ~ 100000`) with consumer groups, enabling worker scaling, offset tracking, and consumer backpressure.
2. If Pub/Sub must be used, decouple listening from processing using an in-memory queue (`asyncio.Queue` or Python worker pool) so the network socket is read at line speed without blocking on compute.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.

# Phase Checkpoint: Distributed Core Primitives & Storage Mechanics

> **Phase Scope:** Modules 09–13 (Consistent Hashing, Snowflake IDs, Caching & Stampede, Probabilistic Structs, Commit Logs)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Architect a High-Throughput Distributed Key-Value Store with LSM Replication and Cache-Aside Shielding

### Executive Scenario
You are the Lead Systems Engineer designing the distributed storage core for a real-time event analytics platform.
The system ingests 1,000,000 events/sec, partitions data across 100 storage nodes, provides sub-millisecond point lookups for active keys, and logs all state mutations to a durable append-only commit log.
You must design the partitioning ring, unique ID generation, probabilistic query pre-filtering, cache stampede protection, and consumer partition rebalancing.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

                     [ Ingestion API Workers (1,000,000 writes/sec) ]
                                            |
                            Snowflake 64-bit ID Generation
                                            v
               +---------------------------------------------------------+
               |              Consistent Hash Ring Router                |
               | (150 Virtual Nodes/Server, MD5/Murmur3 Token Ring)      |
               +---------------------------------------------------------+
                        |                          |
       Preference List: Node A (Primary)   Preference List: Node B (Replica)
                        v                          v
               +-------------------+      +-------------------+
               |  Storage Node A   |      |  Storage Node B   |
               |                   |      |                   |
               |  [SingleFlight]   |      |  [SingleFlight]   |
               |         |         |      |         |         |
               |         v         |      |         v         |
               |  [Redis L1 Cache] |      |  [Redis L1 Cache] |
               |         |         |      |         |         |
               |   (Cache Miss)    |      |   (Cache Miss)    |
               |         v         |      |         v         |
               |  [Bloom Filter]   |      |  [Bloom Filter]   |
               |         |         |      |         |         |
               |  [Commit Log WAL] |      |  [Commit Log WAL] |
               |         |         |      |         |         |
               |  [LSM MemTable]   |      |  [LSM MemTable]   |
               +-------------------+      +-------------------+

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Consistent Partitioning:** Distribute keys across storage nodes using Consistent Hashing with 150 virtual nodes per server.
- **64-Bit Globally Unique IDs:** Generate monotonic, time-sortable 64-bit Snowflake IDs supporting 4,096 IDs/ms per worker node.
- **Cache Stampede Prevention:** Shield backend storage from hot-key cache expirations using SingleFlight request coalescing and XFetch probabilistic early expiration.
- **Probabilistic Membership:** Filter disk reads using Bloom Filters to reject non-existent key lookups before hitting storage files.
- **Partitioned Event Streaming:** Provide an append-only commit log with consumer group offset tracking and automatic partition rebalancing.

### 2. Non-Functional & Scale Metrics
- **Write Throughput:** 1,000,000 writes/sec sustained; peak 2,500,000 writes/sec.
- **Key Migration Upper Bound:** Adding a node to an $N$-node cluster must migrate strictly $\le 1/(N+1)$ of total keys.
- **Clock Drift Tolerance:** Snowflake ID generator must detect backward clock jumps and prevent duplicate ID issuance.
- **Memory Footprint:** Probabilistic filters must operate within strict RAM budgets (HyperLogLog $\le 1.5$ KB per cardinality counter).

---

## 🧮 Quantitative Physics & Mathematical Formulations

### Distributed Primitives Mathematical Formulations
1. **Bloom Filter Bit Size Formula:**
   $$m = -\frac{n \ln p}{(\ln 2)^2} \approx -1.44 \cdot n \log_2 p$$
   For $n = 10,000,000$ keys with false positive rate $p = 0.01$ (1%):
   $$m = -\frac{10^7 \cdot \ln(0.01)}{0.48045} \approx 95,850,583 \text{ bits} \approx 11.42 \text{ MB RAM}.$$
2. **Optimal Hash Functions Count:**
   $$k = \frac{m}{n} \ln 2 = \frac{95,850,583}{10,000,000} \cdot 0.69315 \approx 6.64 \implies 7 \text{ hash functions}.$$
3. **Snowflake ID Bit Allocation:**
   - 1 bit sign | 41 bits timestamp ($2^{41} \text{ ms} \approx 69.7 \text{ years}$) | 10 bits worker ID ($1024 \text{ nodes}$) | 12 bits sequence ($4096 \text{ IDs/ms}$).
4. **XFetch Probabilistic Early Expiry Formula:**
   $$\Delta - \beta \cdot \delta \cdot \ln(\text{rand}()) < 0$$
   Where $\Delta$ is remaining TTL, $\delta$ is computation time, and $\beta > 0$ is aggressiveness multiplier.

---

### 💥 Distributed Failure & Partition Scenarios
1. **NTP Leap Second / Backward Step:** The host NTP client adjusts local time backwards by 40ms during peak ID generation. The Snowflake generator must either spin-wait or reject calls rather than producing duplicate 64-bit keys.
2. **Hot Partition Avalanche:** 40% of all writes target a single celebrity tenant key. Naive consistent hashing concentrates this entirely on Node 14. Your architecture must apply bounded-load consistent hashing to divert overflow keys to alternative nodes.
3. **Cache Expiration Avalanche:** 50,000 cached records expire at the exact same second. SingleFlight mutex groups must collapse concurrent queries into 1 backend read per unique key, eliminating the database thundering herd.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Consistent Hashing & vnodes** | Ring implementation, bisect binary search, preference list replication, and minimal key migration proof | 20 pts |
| **Snowflake ID Bitwise Mechanics** | Correct bit-packing, 41-bit custom epoch, sequence overflow spinning, and NTP clock skew safety | 20 pts |
| **Cache Stampede & SingleFlight** | Mutex request coalescing, negative caching for penetration defense, and TTL jitter | 20 pts |
| **Probabilistic Data Structures** | Bloom Filter, Count-Min Sketch, and HyperLogLog mathematically sized and verified | 20 pts |
| **Commit Log & Stream Semantics** | Monotonic sequential offsets, consumer group rebalancing, and at-least-once replay guarantees | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why does modulo hashing ($hash(k) \pmod N$) trigger a catastrophic full-cluster cache flush when a single server dies, while consistent hashing isolates migration?**
2. **What happens if an operating system's NTP daemon steps the hardware clock backwards by 500ms while a Snowflake generator is running under high load?**
3. **How does SingleFlight (request coalescing) differentiate from simple cache locks in terms of waiting thread resource consumption?**
4. **Why can a standard Bloom Filter never yield a false negative, and under what operational condition does its false positive rate degrade to 100%?**
5. **Explain how Apache Kafka achieves high write throughput despite storing data on mechanical hard drives or standard cloud block storage.**

---

## 🚦 Pre-Flight Submission & Quality Checklist

Before submitting your phase architecture for certification, verify:
- [ ] All quantitative capacity math equations use explicit powers of 10 and real-world hardware latencies.
- [ ] API endpoints specify HTTP verbs, status codes, request bodies, and idempotency headers.
- [ ] Data models define primary keys, partition keys, sharding strategies, and secondary indexes.
- [ ] No single point of failure (SPOF) exists in either the control plane or the data path.
- [ ] Failure modes (split-brain, clock skew, thundering herds, cascading timeouts) have explicit mitigations.
- [ ] All starter exercises and unit tests in this phase pass with a 100% success rate (`pytest`).


---

## 🚦 Pre-Flight Gate: Verify Before You Start

**Do not start until all of this is green.** Sitting a timed exam on a broken
checkout means spending the clock on setup instead of on architecture.

```bash
# From the course root.
pytest Module_09_Consistent_Hashing_Distributed_Partitioning \n      Module_10_Unique_Distributed_ID_Generation_Snowflake \n      Module_11_Distributed_Caching_Stampede_Prevention \n      Module_12_Probabilistic_Data_Structures \n      Module_13_Distributed_Messaging_Event_Streaming_Queues       -q

python tools/check_links.py --quiet
ruff check .
```

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer for the duration above. When it ends, stop and score what exists. |
| **No solution exists** | There is deliberately no reference answer for this exam. The rubric *is* the specification. |
| **Modules are open-book** | Re-read any README, notebook or troubleshooting guide. That is what the job looks like. |
| **`project_solution/` is closed-book** | Do not open the module solutions during the exam. Copying them measures nothing. |
| **Numbers or it did not happen** | Every capacity claim needs arithmetic you can show. "It scales" scores zero. |
| **Name your tradeoffs** | A design with no stated downside is an unexamined design, and the rubric penalises it. |

---

## 🔬 Self-Verification Harness

Produce this evidence before scoring yourself. The rubric grades **evidence**,
not intent.

```bash
# 1. Your design's code runs at all
python -m your_design               # must not traceback

# 2. Your own tests pass
pytest your_tests.py -v             # paste the summary line

# 3. It is clean
ruff check .

# 4. Your capacity numbers are reproducible
python your_capacity_math.py        # prints QPS, bandwidth, storage, cache size
```

A design document with no runnable artefact caps at the analysis criteria only.

---

## ⏱️ If You Run Out of Time

1. **Submit the working subset.** Comment out anything that does not run - a
   broken import forfeits every point in the file.
2. **Write down what is missing**, one line per requirement. Naming your own gap
   accurately is a senior skill and earns analysis credit.
3. **Keep your numbers.** Capacity math for the parts you finished outscores
   hand-waving about the parts you did not.

---

## 🔁 If You Score Below the Threshold

1. Identify the **rubric row** you lost the most points on.
2. Re-read: **Module 09's ring mechanics and Module 11's stampede material**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can pick the right distributed primitive and say what it costs**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.

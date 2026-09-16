# Phase Checkpoint: High-Level System Design Case Studies & Real-World Architectures

> **Phase Scope:** Modules 14–20 (TinyURL, Real-Time Chat, Newsfeed & Recommendations, Geospatial Uber, Video Netflix, Web Crawler, Flash Sale)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Comprehensive System Design Defense: Architect a Multi-Modal Global Mobility & Delivery Platform

### Executive Scenario
You are presenting a 45-minute Staff/Principal System Design whiteboard presentation for a global super-app (combining ride-hailing, real-time messaging, video stories, and flash delivery).
The system handles 100M Daily Active Users, 2M active drivers reporting location every 4 seconds, 100,000 flash sale product drops with extreme concurrent contention, and real-time chat between riders and couriers.
You must formulate and defend the end-to-end architecture across all tiers.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

                    [ Mobile Apps (Riders, Drivers, Shoppers) ]
                                        |
                            Layer 7 API Gateway & WAF
                                        |
       +--------------------+-----------+--------------------+--------------------+
       |                    |                                |                    |
       v                    v                                v                    v
 [Geospatial Dispatch] [Real-Time Chat]              [Flash Sale Store]   [Newsfeed Engine]
       |                    |                                |                    |
       | Lat/Lon updates    | WebSocket Sessions             | Atomic DECR        | Two-Tower Recs
       v                    v                                v                    v
 [Redis Geo Index]     [Redis Pub/Sub Mesh]          [Redis Stock Tokens] [Redis Timelines]
       |                    |                                |                    |
       | Periodic Snapshot  | Persistent History             | Async Batch Write  | Async Aggregator
       v                    v                                v                    v
 [PostGIS Spatial DB]  [Cassandra / ScyllaDB]        [Postgres Ledger DB] [Document Store]

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Geospatial Proximity Dispatch:** Match riders to the nearest available driver within a 3km radius in < 500ms using Geohashes or H3 hexagons.
- **Atomic Inventory Flash Sales:** Process limited-edition merchant promotions (e.g. 50 items contested by 100,000 buyers) with zero overselling.
- **Real-Time Presence & Chat:** Provide ephemeral user presence (`ONLINE`, `IDLE`, `OFFLINE`) and instant WebSocket messaging between riders and couriers.
- **Hybrid Timeline Feed:** Serve user social updates and promotional video clips using hybrid Fan-out (Push for normal users, Pull for celebrities).
- **Video Ingestion & ABR Delivery:** Ingest short video stories via multipart upload, transcode to 720p/480p, and generate HLS `.m3u8` manifests.

### 2. Non-Functional & Scale Metrics
- **Driver GPS Ingestion:** $2,000,000 \text{ drivers} / 4 \text{ s} = 500,000 \text{ location writes/sec}$.
- **Flash Sale Concurrency:** 100,000 concurrent checkout attempts on 50 inventory units; zero double-booking tolerance.
- **WebSocket Gateway Concurrency:** 15,000,000 concurrent persistent TCP/WebSocket connections.
- **P99 Read Latency:** Feed loading < 200ms; dispatch matching < 500ms; short URL redirection < 15ms.

---

## 🧮 Quantitative Physics & Mathematical Formulations

### Multi-Tier Scale Computations
1. **Geospatial GPS Ingestion Bandwidth:**
   $$500,000 \text{ updates/sec} \times 64 \text{ bytes} = 32 \text{ MB/s} = 256 \text{ Mbps}.$$
   Stored in Redis Geo (in-memory sorted sets / geohashes) requiring:
   $$2,000,000 \text{ drivers} \times 128 \text{ bytes overhead} \approx 256 \text{ MB RAM} \implies \text{Fits easily in single Redis instance!}$$
2. **Flash Sale Inventory Lock Contention:**
   - 50 units in stock. 100,000 requests in first 500ms.
   - Relational database row locking (`SELECT FOR UPDATE`) causes 100,000 transactions to queue on a single row, exhausting database connection pool within 200ms.
   - Mitigation: In-memory atomic decrements (`DECR` in Redis with Lua token allocation) serving 100k ops in < 40ms.
3. **Newsfeed Storage Retention Math (500M DAU):**
   - 500M users $	imes$ 800 post IDs in timeline cache $	imes$ 8 bytes (64-bit ID) $= 3.2 \text{ TB RAM}$ across Redis cluster.

---

### 💥 Real-World Outage Scenarios
1. **The 'Lady Gaga' Write Amplification Collapse:** A celebrity with 70M followers posts a flash sale link. If pure Fan-out-on-Write is used, the message broker is injected with 70,000,000 write tasks, stalling all user chat messages for 4 hours. Your design must demonstrate real-time hybrid fanout isolation.
2. **Driver GPS Boundary Blindspot:** A rider standing 10 meters inside cell `9q8yy` is matched with an idle driver 4km away because the driver 50 meters away is across the border in `9q8yz`. Your dispatch algorithm must expand to all 8 adjacent neighbor cells before ranking.
3. **Abandoned Flash Cart Inventory Lock:** 50,000 shoppers reserve flash inventory tokens but close their browser without completing payment. Your background lease-reaper must systematically release unconfirmed stock back to available inventory without overselling.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Geospatial Indexing & Dispatch** | Geohash/H3 encoding, 8-neighbor bounding box expansion, and atomic driver reservation | 20 pts |
| **High-Concurrency Inventory** | Overselling prevention via atomic tokens, 15-minute lease TTLs, and reaper rollbacks | 20 pts |
| **Real-Time Presence & WebSockets** | Heartbeat tracking, connection-state gateway affinity, and cross-gateway Pub/Sub routing | 20 pts |
| **Feed Fanout & Recommendation** | Hybrid push/pull architecture (Lady Gaga problem mitigation) and Two-Tower candidate retrieval | 20 pts |
| **Video Pipeline & ABR Packaging** | Multipart upload reassembly, asynchronous DAG transcoding, and HLS manifest generation | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why does querying only the rider's immediate Geohash cell cause the 'boundary blindspot' problem, and how does querying 8 adjacent neighbor cells resolve it?**
2. **How do you prevent the 'thundering herd' and 'lost update' anomalies when 100,000 users click 'Buy Now' on 10 concert tickets simultaneously?**
3. **Why is Fan-out-on-Write (Push) disastrous for accounts with 50M followers, and what are the trade-offs of the hybrid push/pull solution?**
4. **How do you structure the database schema for chat messages to support fast bidirectional pagination while guaranteeing strict monotonic ordering?**
5. **What happens if an uncompressed 4K video chunk upload fails halfway through a 10GB transfer, and how does multipart chunking protect against restarting from byte 0?**

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
pytest Module_14_Distributed_URL_Shortener_TinyURL \n      Module_15_RealTime_Chat_Presence_System_Discord \n      Module_16_Social_Media_Newsfeed_Recommendation_TwoTower \n      Module_17_Geospatial_Ride_Sharing_Dispatch_Uber \n      Module_18_Video_Ingestion_Streaming_YouTube_Netflix \n      Module_19_Distributed_Web_Crawler_Deduplication_Google \n      Module_20_Flash_Sale_Inventory_Reservation_Amazon       -q

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
2. Re-read: **the case study you scored lowest on, then its debug_lab**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can assemble the primitives into a named product under time pressure**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.

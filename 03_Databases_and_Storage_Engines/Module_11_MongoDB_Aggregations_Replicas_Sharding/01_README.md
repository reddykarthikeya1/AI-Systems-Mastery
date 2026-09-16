# Module 11: MongoDB Aggregations, Replica Sets & Sharding

> **Brand new to this topic?** Start with [`00_W3_BEGINNER_PLAYGROUND.md`](00_W3_BEGINNER_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 11**. In this module, you will master the analytical computation engine of MongoDB (**The Aggregation Pipeline**), explore fault-tolerant consensus across **Replica Sets**, and master distributed horizontal scaling via **Sharding**.

---

## 🔄 1. The Aggregation Pipeline Architecture

While relational databases use SQL clauses (`SELECT ... FROM ... WHERE ... GROUP BY ...`), MongoDB transforms data using an **assembly line of sequential pipeline stages**:

```
[Raw Collection (1M Docs)]
         │
         ▼
┌──────────────────┐
│     $match       │ ── Filters active orders only (Uses index!) -> 100k docs
└────────┬─────────┘
         ▼
┌──────────────────┐
│     $unwind      │ ── Deconstructs 'items' array into individual docs -> 300k items
└────────┬─────────┘
         ▼
┌──────────────────┐
│     $group       │ ── Groups by 'category', computes total_revenue, avg_price -> 50 docs
└────────┬─────────┘
         ▼
┌──────────────────┐
│     $sort        │ ── Orders by total_revenue descending
└────────┬─────────┘
         ▼
┌──────────────────┐
│     $limit       │ ── Returns Top 10 High-Earning Categories
└────────┬─────────┘
         ▼
[Final Response Array (10 Docs)]
```

### Essential Pipeline Stages
- **`$match`**: Filters documents. When placed as the first stage, it can leverage B-Tree indexes!
- **`$project`**: Reshapes documents, computes new derived fields, includes/excludes keys.
- **`$unwind`**: Explodes an array field. If a document has an array of 5 items, `$unwind` produces 5 separate documents.
- **`$group`**: Groups documents by an `_id` key and applies accumulators (`$sum`, `$avg`, `$min`, `$max`, `$push`, `$addToSet`).
- **`$lookup`**: Performs a relational left outer join against an unsharded target collection.
- **`$facet`**: Executes multiple independent parallel sub-pipelines over the same input stream (e.g. faceted search).

---

## 🛡️ 2. Replica Set Consensus & Write Concerns

A MongoDB Replica Set consists of a **Primary** (accepts all writes) and multiple **Secondaries** (replicate the Primary's Oplog).

### The Oplog (`local.oplog.rs`)
The **Operations Log** is a special capped collection that stores idempotent change descriptions:
- Even if the master executed an increment: `{$inc: {views: 1}}`
- The Oplog logs the deterministic absolute state: `{$set: {views: 42}}`
- This ensures secondaries replaying the Oplog produce identical state even under network retries.

### Write Concern vs. Read Concern
```javascript
db.orders.insertOne(orderData, { 
    writeConcern: { w: "majority", j: true, wtimeout: 5000 } 
});
```
- **`w: 1`**: Acknowledges write once written to Primary RAM (Vulnerable to data loss if Primary crashes before replication).
- **`w: "majority"`**: Acknowledges write only after a quorum ($> 50\%$) of voting nodes write it to disk.
- **`j: true`**: Confirms write has been flushed to the on-disk journal file (zero crash loss).

---

## 🌐 3. Horizontal Scaling: Sharded Cluster Architecture

When a single server cannot hold the dataset or process the write volume, MongoDB shards data across multiple independent replica sets.

```
                         [Client Application]
                                   │
                                   ▼
                         [mongos Query Router]
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       ▼ (Reads Routing Metadata)  ▼                           ▼
[Config Server Replica Set] [Shard 1 (Replica Set)] [Shard 2 (Replica Set)]
 (Stores Chunk Ranges)       (Chunk [0 .. 10,000])   (Chunk [10,001 .. Max])
```

### Targeted Queries vs. Scatter-Gather Queries
- **Targeted Query**: The query includes the **Shard Key**. `mongos` inspects the Config Server chunk table and routes the request **directly to the single specific shard holding that data**.
- **Scatter-Gather Query**: The query **does NOT include the Shard Key**. `mongos` must broadcast the query to **EVERY shard in the cluster**, wait for all to respond, merge results in RAM, and return them. This destroys scalability!

### Choosing a Shard Key: Range vs. Hashed
1. **Range Shard Key**: Good for range queries (`BETWEEN a AND b`), but monotonically increasing keys (e.g. `_id` or `timestamp`) create a **Hotspot** where 100% of inserts hit the highest shard!
2. **Hashed Shard Key**: Computes an MD5 hash of the key, scattering writes evenly across all shards (eliminates hotspots), but forces scatter-gather on range queries.

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/mongo_aggregation_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | mongo_aggregation_engine.py (Pipeline stages & shard router) | mongo_scale_live.py (pymongo aggregation pipeline, $facet, $lookup) |
| **Verification** | `project_solution/test_mongo_aggregation_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. 100MB Pipeline RAM Limit: In-memory $group and $sort operations crash unless allowDiskUse is enabled.
2. Scatter-Gather Sharding Penalty: Queries lacking shard keys broadcast to all cluster shards, destroying throughput.
3. Stale Secondary Reads: Using secondaryPreferred with readConcern local reading uncommitted or lagging oplog states.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT choose low-cardinality shard keys (e.g. status or country) which create un-splittable jumbo chunks and extreme hot partition bottlenecks.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_11_MongoDB_Aggregations_Replicas_Sharding -v

# Operational Diagnostics & Health Verification
mongosh mongodb://localhost:27017/coursedb --eval "sh.status()"
mongosh mongodb://localhost:27017/coursedb --eval "rs.status()"
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_mongo_aggregation.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.


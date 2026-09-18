# Module 15: LSM-Trees, Compaction & AWS DynamoDB

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

---

## 🌲 1. The B-Tree vs. LSM-Tree Paradigm Shift

For decades, relational databases relied almost exclusively on B-Trees and $B^+$ Trees. However, modern high-scale distributed workloads (sensor streams, time-series metrics, clickstreams, social messaging) exposed fundamental hardware limitations of B-Trees:

```
[B-Tree Architecture: In-Place Random Writes]
Page 421 ──► [Disk Seek / Random 8KB Page Overwrite] ──► Disk I/O Bottleneck & Write Amplification

[LSM-Tree Architecture: Sequential Append-Only]
Memory (MemTable) ──► Fast In-Memory Sort ──► Flushed to Sequential On-Disk SSTable!
```

### Why LSM-Trees Dominate Write Workloads
1. **Random I/O vs. Sequential I/O**:
   - On spinning HDDs, sequential writes are 100x faster than random writes because the physical disk arm does not seek.
   - On NVMe SSDs, random in-place overwrites trigger flash **Write Amplification** (pages cannot be overwritten directly; entire 2MB–8MB NAND flash blocks must be read, erased, and rewritten).
   - LSM-Trees convert **100% of incoming random writes into sequential appends**, maximizing storage device throughput.
2. **Immutable Storage**:
   - Once written to disk, an SSTable file is never modified in place. It is append-only and read-only.
   - Immutability eliminates complex page-level concurrency locks, simplifies snapshot isolation, and allows fearless caching.

---

## 🏛️ 2. The Four Pillars of the LSM-Tree Architecture

An LSM-Tree engine coordinates four complementary storage components:

```
                   ┌─────────────────────────────┐
                   │ Client Write: PUT(key, val) │
                   └──────────────┬──────────────┘
                                  │
            ┌─────────────────────┴─────────────────────┐
            ▼                                           ▼
   ┌─────────────────┐                        ┌───────────────────┐
   │ Write-Ahead Log │ (Sequential Disk Sync) │     MemTable      │ (In-Memory Sorted
   │     (WAL)       │                        │ (SkipList/RBTree) │  Buffer, e.g. 64MB)
   └─────────────────┘                        └─────────┬─────────┘
                                                        │ When Full
                                                        ▼ (Sequential Flush)
                                              ┌───────────────────┐
                                              │      SSTable      │ (Level 0 Disk File)
                                              │  ┌─────────────┐  │
                                              │  │ Bloom Filter│  │
                                              │  ├─────────────┤  │
                                              │  │ Sparse Index│  │
                                              │  ├─────────────┤  │
                                              │  │ Data Blocks │  │
                                              │  └─────────────┘  │
                                              └───────────────────┘
```

### 1. Write-Ahead Log (WAL)
Every mutation is immediately appended to an on-disk sequential log before being acknowledged to the client. If the server loses power, the volatile in-memory buffer is reconstructed by replaying the WAL during startup.

### 2. MemTable
An in-memory, sorted concurrent data structure (typically a SkipList or Red-Black Tree).
- Writes insert keys in sorted order in $O(\log N)$ time.
- When the MemTable exceeds a configured memory threshold (e.g. 64 MB), it is frozen into a read-only immutable MemTable, a fresh active MemTable is opened, and a background thread flushes the immutable buffer sequentially to disk.

### 3. Sorted String Table (SSTable)
An immutable, sorted file format on disk consisting of three sections:
- **Data Blocks**: Key-value pairs stored sequentially in lexicographical key order.
- **Sparse Index**: Stores the physical file byte offset for every $N$-th key (e.g., every 128th key). Instead of indexing every key, the engine uses the sparse index to binary search the approximate file block, then scans locally.
- **Bloom Filter**: A space-efficient probabilistic filter embedded in the SSTable header.

### 4. Bloom Filters: Eliminating Point-Read Penalties
Because an LSM-Tree may accumulate dozens of SSTable files across multiple disk levels, searching for a non-existent key could require reading every single SSTable file from disk (catastrophic Read Amplification).
- A **Bloom Filter** uses a bit array of $m$ bits and $k$ independent hash functions:
  $$\text{Bit Positions} = h_1(\text{key}) \pmod m, \quad h_2(\text{key}) \pmod m, \quad \dots \quad h_k(\text{key}) \pmod m$$
- **Mathematical Guarantee**:
  - **Zero False Negatives**: If the Bloom filter returns `False`, the key is **100% guaranteed not to exist** in that SSTable. The engine completely skips reading the file from disk!
  - **Configurable False Positive Rate ($p$)**:
    $$m = -\frac{n \ln p}{(\ln 2)^2}, \quad k = \frac{m}{n} \ln 2$$
    With ~10 bits per key ($m/n = 10$), the false positive rate drops to **1%**, eliminating 99% of unnecessary disk lookups.

---

## 🔄 3. Compaction Strategies: Size-Tiered vs. Leveled

Over time, disk fills with obsolete versions of updated keys and deleted keys (marked by tombstones). **Compaction** is the background merge process that purges tombstones, discards superseded versions, and maintains read performance.

| Metric / Dimension | Size-Tiered Compaction (STCS) | Leveled Compaction (LCS) |
| :--- | :--- | :--- |
| **Strategy** | Merges SSTables of similar file size | Organizes SSTables into hierarchical levels ($L_0, L_1, L_2 \dots$) |
| **Key Overlap** | High (keys can exist across all files) | Zero overlap within any level $L_1+$ |
| **Read Amplification** | Higher (must check multiple files) | Bounded (at most 1 SSTable per level) |
| **Space Amplification**| High (~50% free disk required) | Low (~10% free disk required) |
| **Write Amplification**| Low | Higher (repeated multi-pass merges) |
| **Best For** | High-throughput write-only / append logs | Read-heavy / update-heavy workloads |

### Leveled Compaction Mechanics
- **Level 0 ($L_0$)**: Directly receives flushed MemTables. Key ranges across $L_0$ files can overlap.
- **Level 1 ($L_1$)**: Target capacity 10 MB. SSTables have strictly non-overlapping key ranges.
- **Level $i+1$**: Target capacity $10 \times \text{Level } i$ ($L_2 = 100 \text{ MB}$, $L_3 = 1 \text{ GB}$, $L_4 = 10 \text{ GB}$).
- When Level $i$ exceeds its byte quota, the engine picks an SSTable from Level $i$, finds all overlapping SSTables in Level $i+1$, performs a multi-way merge sort, and writes out fresh non-overlapping SSTables into Level $i+1$.

---

## ⚡ 4. Amazon DynamoDB: Single-Table Architecture & Capacity Units

Amazon DynamoDB is a proprietary, serverless distributed key-value and document database built on SSD-backed partition storage and automated Paxos replication.

### Primary Keys & Single-Table Design
- **Partition Key (`PK`)**: Hashed to determine the physical partition node hosting the item.
- **Sort Key (`SK`)**: Sorts items lexicographically within the physical partition.
- **Single-Table Design (The Rick Houlihan Pattern)**:
  Instead of creating 10 different tables for Users, Orders, Products, and Invoices, advanced DynamoDB architects store all entity types in a **single table** using generic keys:
  - `PK: "USER#1001"`, `SK: "PROFILE"` $\implies$ User profile data
  - `PK: "USER#1001"`, `SK: "ORDER#2026-001"` $\implies$ User order item
  - `PK: "ORDER#2026-001"`, `SK: "ITEM#PROD_99"` $\implies$ Order line item
  This pattern enables fetching a user profile AND their recent orders in a **single round-trip query** (`WHERE PK = 'USER#1001' AND SK BEGINS_WITH 'ORDER#'`) with zero joins!

### Global Secondary Indexes (GSI) vs. Local Secondary Indexes (LSI)
- **Local Secondary Index (LSI)**: Shares the base table's partition key, but specifies a different sort key. Strictly consistent, limited to 10 GB per partition.
- **Global Secondary Index (GSI)**: Defines completely new `PK` and `SK`. Can span the entire table. Asynchronously replicated (eventually consistent).

### Provisioned vs. On-Demand Capacity Units
1. **Read Capacity Unit (RCU)**:
   - 1 RCU = One **Strongly Consistent Read** per second for items up to 4 KB.
   - 1 RCU = Two **Eventually Consistent Reads** per second (up to 4 KB each).
   - 1 Transactional Read = 2 RCUs.
2. **Write Capacity Unit (WCU)**:
   - 1 WCU = One write per second for items up to 1 KB.
   - 1 Transactional Write (`TransactWriteItems`) = 2 WCUs.

---

## 🛠️ 5. Hands-On Lab: Building an LSM-Tree Engine with Bloom Filters

In this lab, you will implement:
1. **Bloom Filter**: Bit-array probabilistic filter with multiple hash functions and zero false negatives.
2. **MemTable**: Sorted in-memory write buffer with size-triggered flush threshold.
3. **SSTable**: Immutable on-disk representation with embedded Bloom filter, sparse index, and sorted data blocks.
4. **Leveled Compaction Merger**: Multi-way merge sort collapsing multiple SSTables into a compacted level, purging tombstones and keeping only newest versions.
5. **Single-Table DynamoDB Interface**: Partition key hashing, sort key prefix queries, and RCU/WCU calculation.

---

## 📂 Project Structure
```
Module_15_LSM_Trees_Compaction_DynamoDB/
├── README.md
├── 01_lsm_tree_and_bloom_filter_demo.py
├── starter/
│   └── lsm_dynamo_engine.py
└── project_solution/
    ├── lsm_dynamo_engine.py
    └── test_lsm_dynamo_engine.py
```

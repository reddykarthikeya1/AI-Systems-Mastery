# Master Syllabus: Production-Grade System Design Mastery (HLD + LLD + AI/ML)

Welcome to the **System Design Mastery Course** — the definitive zero-to-100 curriculum bridging **Low-Level Design (LLD / Machine Coding)**, **High-Level Distributed System Design (HLD)**, and **Modern AI/ML Systems Engineering**.

---

---

## 📚 Scope: what this course deliberately does not cover

This course builds distributed-systems mechanisms from scratch and imports
nothing outside the standard library. Four adjacent topic areas are **out of
scope here by design**, because they belong to the database layer and are
covered as full modules in the companion **Databases** course rather than
summarised badly in this one:

| Topic | Where it is actually taught |
| :--- | :--- |
| **Data modelling & SQL** — normal forms, joins, window functions, CTEs, `EXPLAIN` | Databases Modules 01, 02, 04, 05 |
| **Storage engines** — B+ trees, LSM trees, SSTables, compaction, WAL, MVCC, buffer pools, write amplification | Databases Modules 21, 15, 03, 05 |
| **Lexical search** — inverted indexes, tokenisation, BM25, Lucene segments, faceting, typeahead | Databases Module 19 |
| **Analytics engineering** — columnar/OLAP engines, star schemas, SCD2, materialised aggregates, pipelines | Databases Modules 17, 18 |

Module 09 (consistent hashing), Module 12 (probabilistic structures) and
Module 21 (vector indexes) touch the *distribution* and *indexing* side of these
topics. They do not teach the storage engines underneath, and they do not
pretend to.

Stating this explicitly matters: a system-design curriculum that quietly omits
storage engines while claiming to be complete is misleading in a way that a
curriculum which names its boundaries is not.

## 🗺️ Course Structure: 6 Progressive Phases (27 Modules)

```
========================================================================================================================
                                     SYSTEM DESIGN MASTERY CURRICULUM ROADMAP
========================================================================================================================
[Phase I: Foundations & Math]  ──► [Phase II: LLD & Clean Code]  ──► [Phase III: Distributed Primitives]
  • Mod 00: Fundamentals & Interview • Mod 05: SOLID & DDD            • Mod 09: Consistent Hashing
  • Mod 01: Physics & Capacity       • Mod 06: GoF Design Patterns    • Mod 10: Distributed ID Gen
  • Mod 02: Network & Protocols      • Mod 07: LLD Elevator/Parking   • Mod 11: Distributed Caching
  • Mod 03: Edge, DNS, Proxies       • Mod 08: LLD Splitwise/Limiter  • Mod 12: Probabilistic Structs
  • Mod 04: Load Balancing                                            • Mod 13: Queues & Streaming
                                                                                     │
                                                                                     ▼
[Phase VI: Consensus, SRE & Capstone] ◄── [Phase V: AI/ML Systems] ◄── [Phase IV: Real-World HLD Architectures]
  • Mod 23: Distributed Sagas & Outbox    • Mod 21: Vector DB & HNSW     • Mod 14: TinyURL Shortener
  • Mod 24: Raft Consensus & Clocks      • Mod 22: LLM Serving/vLLM     • Mod 15: WhatsApp/Discord Chat
  • Mod 25: Observability & SRE                                          • Mod 16: Two-Tower RecSys / Feed
  • Mod 26: Capstone: Payment & AI Fraud                                 • Mod 17: Uber Geospatial Dispatch
                                                                         • Mod 18: YouTube Video Ingestion
                                                                         • Mod 19: Google Web Crawler
                                                                         • Mod 20: Amazon Flash Sale
========================================================================================================================
```

---

## Phase I: Foundations, Capacity Math & Networking
- **[Module 00](Module_00_System_Design_Fundamentals_Interview_Playbook/01_README.md)**: System Design Fundamentals & Interview Navigation Playbook (45-min framework, capacity mental math, C4 diagrams)
- **[Module 01](Module_01_Physics_of_Scalability_Capacity_Math/01_README.md)**: The Physics of Scalability & Latency Numbers Every Engineer Must Know
- **[Module 02](Module_02_Network_Protocols_Transport_API_Paradigms/01_README.md)**: Network Protocols, Transport Layers & API Paradigms (HTTP/1-3, gRPC, WebSockets)
- **[Module 03](Module_03_Edge_Infrastructure_Reverse_Proxies/01_README.md)**: Edge Infrastructure, DNS, CDNs & Reverse Proxies (Nginx, Envoy)
- **[Module 04](Module_04_Load_Balancing_Algorithms_Health_Probes/01_README.md)**: Load Balancing Algorithms & Health Probes (Round-Robin, Weighted RR, LeastConn, Draining)

---

## Phase II: Low-Level Design (LLD) & Machine Coding
- **Module 05**: SOLID Principles & Clean Architecture in Practice (E-Commerce Checkout Aggregate)
- **Module 06**: Essential Gang of Four (GoF) Design Patterns (Multi-Channel Notification Pipeline)
- **Module 07**: LLD Classic Case Studies I – State Machines & Scheduling (Elevator LOOK Algorithm & Parking Lot)
- **Module 08**: LLD Classic Case Studies II – Financial & Collaborative Engines (Splitwise & Token Bucket Rate Limiter)

---

## Phase III: Distributed Systems Core Primitives
- **Module 09**: Consistent Hashing & Distributed Partitioning (Virtual Nodes, Bisect Routing)
- **Module 10**: Unique Distributed ID Generation (Twitter Snowflake 64-bit Layout, Clock Skew Guard)
- **Module 11**: Distributed Caching Architectures & Stampede Prevention (Single-Flight, XFetch, Negative Caching)
- **Module 12**: Probabilistic Data Structures (Bloom Filter, Count-Min Sketch, HyperLogLog)
- **Module 13**: Distributed Messaging, Event Streaming & Task Queues (Partitioned Append-Only Commit Log)

---

## Phase IV: High-Level System Design (HLD) Real-World Case Studies
- **Module 14**: Design a Globally Distributed URL Shortener (TinyURL, Base62, KGS, Cache-Aside)
- **Module 15**: Design a Real-Time Distributed Chat & Presence System (WhatsApp/Discord, WebSocket Gateway)
- **Module 16**: Design a Social Media Newsfeed & Personalized Recommendation Engine (Two-Tower Deep Retrieval & Ranking, Real-time Feature Store, Redis Timeline Caching)
- **Module 17**: Design a Geospatial Ride-Sharing Dispatch Platform (Uber/Lyft, Geohash / H3 Grid, Driver Matching)
- **Module 18**: Design a Large-Scale Video Ingestion & Streaming Platform (YouTube/Netflix, Transcoding DAG, HLS)
- **Module 19**: Design a Distributed Web Crawler & Deduplication Engine (Google/Bing, Politeness Frontier, SimHash)
- **Module 20**: Design an E-Commerce Flash Sale & Inventory Reservation System (Amazon/Ticketmaster, Redlock, 2-Phase Reservation)

---

## Phase V: Modern AI/ML Systems & Distributed Inference Engineering
- **Module 21**: Design a High-Scale Vector Database & Approximate Nearest Neighbor (ANN) Indexing Engine (Milvus / Pinecone / Faiss Architecture, HNSW Proximity Graphs, Vector Quantization, Metadata Filtering)
- **Module 22**: Design a High-Throughput Distributed LLM Serving & Inference Platform (vLLM / Triton Architecture, Continuous Batching, PagedAttention / KV-Cache Memory Management, Model Parallelism)

---

## Phase VI: Advanced Reliability, Consensus & Enterprise Capstone
- **Module 23**: Distributed Transactions, Sagas & Outbox Pattern (Orchestrator, Compensations, CDC)
- **Module 24**: Distributed Consensus & Replication (Raft Leader Election, Quorum Writes, Vector Clocks)
- **Module 25**: Observability, Distributed Tracing & Site Reliability Engineering (OpenTelemetry Spans, Prometheus, Circuit Breakers with Full Jitter)
- **Module 26**: Master Enterprise Capstone: Multi-Region Payment Gateway with Real-Time AI Fraud Detection Pipeline (Double-Entry Ledger, Idempotency Tokens, Streaming Feature Scoring)

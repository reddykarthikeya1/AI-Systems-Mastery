# Study Plans & Pacing Guide: System Design Mastery

Whether you are preparing for an imminent Big Tech System Design interview, modernizing your enterprise architecture, or aiming for foundational mastery, select the roadmap that matches your timeline.

---

## ?? Track A: 10-Day Intensive Sprint (Interview Preparation)

Designed for senior engineers who need to master the universal 4-step interview framework, core distributed primitives, and high-frequency case studies in under two weeks.

*Daily Commitment: ~4�5 hours/day*

| Day | Focus Modules | Key Deliverables & Hands-on Practice |
| :--- | :--- | :--- |
| **Day 1** | **Mod 01 & Mod 02** | Master back-of-the-envelope capacity estimation. Practice QPS, storage, and network math. Compare HTTP/2, HTTP/3, and WebSockets. |
| **Day 2** | **Mod 03 & Mod 04** | Edge infrastructure, DNS routing, CDNs. Understand L4 vs L7 load balancing algorithms and failover probes. |
| **Day 3** | **Mod 05 & Mod 06** | Low-Level Design (LLD): SOLID principles in code, Domain-Driven Design, and essential GoF patterns (Factory, Strategy, Observer). |
| **Day 4** | **Mod 07 & Mod 08** | LLD Machine Coding: Implement the Elevator Dispatcher, Parking Lot, and Concurrency-Safe Rate Limiter. |
| **Day 5** | **Mod 09 & Mod 10** | Consistent Hashing Ring with virtual nodes. Snowflake 64-bit unique distributed ID generator. |
| **Day 6** | **Mod 11 & Mod 12** | Distributed Caching (Cache-Aside, Write-Back). Cache stampede prevention. Probabilistic filters (Bloom Filters & HyperLogLog). |
| **Day 7** | **Mod 13 & Mod 14** | Message Queues & Kafka event logs. Design **TinyURL** from scratch with Base62 encoding and Key Generation Service. |
| **Day 8** | **Mod 15 & Mod 16** | Design **WhatsApp/Discord** (WebSocket gateways + presence cluster) and **Twitter Newsfeed** (Fan-out write vs read). |
| **Day 9** | **Mod 17 & Mod 20** | Design **Uber Dispatch** (Geohash / H3 hexagonal indexing) and **Amazon Flash Sale** (Redlock + optimistic stock reservations). |
| **Day 10**| **Mod 21 & Mod 24** | Distributed Transactions (Sagas & Outbox pattern). Walk through Capstone: Stripe-Scale Payment Gateway. |

---

## ?? Track B: 30-Day Working Professional Track (Recommended)

The balanced path for software engineers seeking comprehensive depth while managing full-time work commitments.

*Daily Commitment: ~1.5�2 hours/day*

- **Week 1 (Days 1�7): Foundations, Networking & LLD Architecture**
  - Days 1�2: Modules 01 & 02 (Scale, Latency numbers, Capacity math, TCP/HTTP/QUIC/gRPC).
  - Days 3�4: Modules 03 & 04 (DNS, CDNs, Reverse Proxies, L4/L7 Load Balancing).
  - Days 5�7: Modules 05 & 06 (SOLID principles, DDD, GoF patterns in production Python).
- **Week 2 (Days 8�14): LLD Machine Coding & Distributed Primitives**
  - Days 8�10: Modules 07 & 08 (Elevator system, Parking Lot, Splitwise, Rate Limiter).
  - Days 11�12: Modules 09 & 10 (Consistent Hashing Ring, Snowflake ID generator).
  - Days 13�14: Modules 11 & 12 (Distributed Caching topologies, Stampede guards, Bloom Filters).
- **Week 3 (Days 15�21): Messaging & High-Frequency Case Studies (HLD I)**
  - Days 15�16: Module 13 (RabbitMQ vs Apache Kafka, consumer groups, partition offsets).
  - Days 17�18: Modules 14 & 15 (TinyURL URL Shortener, Real-time Chat & Presence).
  - Days 19�21: Modules 16 & 17 (Twitter Newsfeed, Uber Geospatial Dispatch).
- **Week 4 (Days 22�30): Media, Scale, Consensus & Enterprise Capstone (HLD II & SRE)**
  - Days 22�24: Modules 18, 19 & 20 (YouTube video ingestion, Web Crawler, Flash Sale).
  - Days 25�27: Modules 21 & 22 (Distributed Sagas, Outbox CDC, Raft consensus, Vector clocks).
  - Days 28�29: Module 23 (Observability, OpenTelemetry, Circuit Breakers, SRE error budgets).
  - Day 30: Module 24 (Capstone: Double-Entry Payment Gateway with idempotent webhooks).

---

## ?? Track C: 60-Day Deep Architectural Immersion (Principal / Staff Path)

For architects and senior developers aiming for exhaustive 100% mastery, including writing custom distributed algorithms from scratch and running production fault-injection simulations.

- **Phase 1 (Days 1�12)**: Physical hardware limits, networking protocols, edge caching, and L4/L7 load balancers.
- **Phase 2 (Days 13�24)**: Low-level design, GoF patterns, concurrency safety, and building full LLD machine coding platforms.
- **Phase 3 (Days 25�36)**: Distributed primitives: Consistent hashing, Snowflake IDs, distributed locks, Bloom filters, and stream partitioning.
- **Phase 4 (Days 37�48)**: Exhaustive High-Level Designs (TinyURL, WhatsApp, Twitter, Uber, Netflix, Google Crawler, Amazon Flash Sale).
- **Phase 5 (Days 49�60)**: Advanced consensus, Raft implementations, Sagas, Chaos engineering, and the Enterprise Capstone Payment Gateway.

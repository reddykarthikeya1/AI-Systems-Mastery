# Textbook Exercise → Python Solution Map

This index is the companion to `HLD_Python_Master_Textbook_Final.pdf`. Start with the chapter in the textbook, attempt the exercise, then open the referenced solution and run the matching pytest test. The tests are executable examples: they show expected behaviour and important edge cases.

> **Scope note:** Some chapters have dedicated implementations; the remaining chapters use intentionally small reference models in `chapter_reference_solutions.py`. These are learning aids, not production implementations. The PDF itself was not regenerated in this patch bundle; this map is the ready-to-add companion appendix for the next textbook export.

## Run the exercises

From `High Level Design/HLD_Python_Labs`:

```bash
python -m pip install -r requirements.txt
pytest -q
```

Run one chapter's tests with `pytest tests/test_<module>.py -v`, or run the shared reference exercises with:

```bash
pytest tests/test_chapter_reference_solutions.py -v
```

No Docker, database server, message broker, Kubernetes, or deployment setup is required for the default test suite. A few modules contain optional Redis integration paths; their in-memory test doubles are sufficient for the core exercises.

## Chapters

| Textbook chapter | Exercise focus | Solution script | Verification |
|---|---|---|---|
| 01 – Scalability | Bound concurrent work and reason about queueing/load | `ch01_scalability/concurrency_limiter.py` | `tests/test_concurrency_limiter.py` |
| 02 – Load balancing | Compare round-robin distribution across backends | `chapter_reference_solutions.py` – `RoundRobinBalancer` | `tests/test_chapter_reference_solutions.py::test_round_robin_load_balancing` |
| 03 – Caching | Cache-aside, single-flight, version and invalidation fencing | `ch03_caching/cache_aside_versioned.py` | `tests/test_cache_aside_versioned.py` |
| 04 – CDN | Model edge TTL, cache hits, expiry and invalidation | `chapter_reference_solutions.py` – `CDNCache` | `tests/test_chapter_reference_solutions.py::test_cdn_cache_ttl_and_invalidation` |
| 05 – Sharding | Route stable keys to shards | `chapter_reference_solutions.py` – `HashShardRouter` | `tests/test_chapter_reference_solutions.py::test_hash_shard_routing_is_stable` |
| 06 – Replication | Simulate replica lag, read-your-writes and read repair | `chapter_reference_solutions.py` – `ReplicaGroup` | `tests/test_chapter_reference_solutions.py::test_replication_lag_read_your_writes_and_read_repair` |
| 07 – Consistent hashing | Place keys on a virtual-node hash ring | `ch07_consistent_hashing/hash_ring.py` | `tests/test_hash_ring.py` |
| 08 – CAP | Choose availability or consistency during a partition | `chapter_reference_solutions.py` – `cap_choice` | `tests/test_chapter_reference_solutions.py::test_cap_and_pacelc_decisions` |
| 09 – PACELC | Compare partition-mode and normal-mode preferences | `chapter_reference_solutions.py` – `pacelc_choice` | `tests/test_chapter_reference_solutions.py::test_cap_and_pacelc_decisions` |
| 10 – Consistency models | Compare vector clocks and detect concurrent updates | `chapter_reference_solutions.py` – `VectorClock` | `tests/test_chapter_reference_solutions.py::test_vector_clock_causal_order_and_concurrency` |
| 11 – Kafka / queues | Partition an append-only log and commit group offsets | `chapter_reference_solutions.py` – `PartitionedLog` | `tests/test_chapter_reference_solutions.py::test_partitioned_log_offsets_and_consumer_groups` |
| 12 – Event-driven architecture | Write events to an outbox and poll safely | `ch12_event_driven/transactional_outbox.py` | `tests/test_transactional_outbox.py` |
| 13 – Microservices | Register, resolve and deregister service instances | `chapter_reference_solutions.py` – `ServiceRegistry` | `tests/test_chapter_reference_solutions.py::test_service_discovery_registration` |
| 14 – API gateway | Route requests and enforce an authentication boundary | `chapter_reference_solutions.py` – `ApiGateway` | `tests/test_chapter_reference_solutions.py::test_api_gateway_authentication_boundary` |
| 15 – Rate limiting | Enforce request/token budgets | `ch15_rate_limiter/dual_token_bucket.py` | `tests/test_dual_token_bucket.py` |
| 16 – Bloom filters | Membership checks, counting-filter hazards, MinHash and LSH | `ch16_bloom_filter/bloom_and_minhash.py` | `tests/test_bloom_and_minhash.py` |
| 17 – Circuit breaker | Open/half-open/closed transitions and timeout handling | `ch17_circuit_breaker/circuit_breaker.py` | `tests/test_circuit_breaker.py` |
| 18 – Saga | Execute steps and compensate in reverse order | `ch18_saga_orchestrator/saga_orchestrator.py` | `tests/test_saga_orchestrator.py` |
| 19 – Blob storage | Upload ordered parts and validate checksums | `chapter_reference_solutions.py` – `MultipartObjectStore` | `tests/test_chapter_reference_solutions.py::test_multipart_object_upload_integrity_and_order` and `::test_multipart_rejects_checksum_mismatch` |
| 20 – Estimation | Convert DAU, requests/user and peak factor into capacity estimates | `chapter_reference_solutions.py` – `estimate_capacity` | `tests/test_chapter_reference_solutions.py::test_back_of_envelope_capacity_estimates` |
| 21 – Distributed search | BM25, dense ranking and reciprocal-rank fusion | `ch21_distributed_search/bm25_and_rrf.py` | `tests/test_bm25_and_rrf.py` |
| 22 – Raft | Require a majority and one vote per node per term | `chapter_reference_solutions.py` – `RaftElection` | `tests/test_chapter_reference_solutions.py::test_raft_election_requires_majority_and_one_vote_per_term` |
| 23 – Stream processing | Aggregate event-time windows and handle late data | `chapter_reference_solutions.py` – `TumblingWindowAggregator` | `tests/test_chapter_reference_solutions.py::test_event_time_windows_close_on_watermark` |
| 24 – Zanzibar / ReBAC | Evaluate relationship tuples and transitive access | `ch24_zanzibar_rebac/zanzibar_rebac.py` | `tests/test_zanzibar_rebac.py` |
| 25 – LSM vs B-tree | Demonstrate memtable flush, reads and compaction | `chapter_reference_solutions.py` – `LSMStore` | `tests/test_chapter_reference_solutions.py::test_lsm_flush_and_compaction_preserve_latest_value` |

## End-to-end workshops

| Workshop | Exercise focus | Solution script | Verification |
|---|---|---|---|
| A – E-commerce / flash sale | Reserve, confirm, expire and reconcile inventory | `workshop_ecommerce/flash_sale_inventory.py` | `tests/test_flash_sale_inventory.py` |
| B – Distributed chat | Track presence using heartbeat TTLs | `chapter_reference_solutions.py` – `PresenceRegistry` | `tests/test_chapter_reference_solutions.py::test_chat_presence_ttl` |
| C – Video streaming | Combine resumable multipart upload with edge caching | `chapter_reference_solutions.py` – `MultipartObjectStore` and `CDNCache` | multipart and CDN tests in `tests/test_chapter_reference_solutions.py` |
| D – Ride-hailing | Find driver candidates using coarse geospatial cells | `chapter_reference_solutions.py` – `DriverCellIndex` | `tests/test_chapter_reference_solutions.py::test_ride_hailing_driver_cell_candidates` |
| E – LLM serving | Allocate KV-cache blocks and model copy-on-write behaviour | `workshop_llm_serving/paged_attention_simulator.py` | `tests/test_paged_attention_simulator.py` |
| F – Multi-tenant RAG / agents | Combine retrieval, authorization and safe tool execution | `workshop_rag_agents/agent_rag_engine.py` | `tests/test_agent_rag_engine.py` |

## How every new textbook task should be written

Give each task a stable identifier, such as `CH03-E01` or `WE-E02`. Under the exercise, include a short **Solution in repository** line with the exact script and test path from this index. Keep the solution out of the textbook body; learners should attempt the problem first, then use the repository to check their work.

For future additions, do not mark a textbook exercise complete until all three exist: (1) the task in the PDF source, (2) an executable solution in the lab folder, and (3) a test that checks the task's expected behaviour and at least one important edge case.

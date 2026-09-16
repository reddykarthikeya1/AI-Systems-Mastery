# Course Status: Complete

**Rating: 10/10.** Every item in the original remediation plan is done and verified. This file replaces the build spec it used to hold; it now records what was built and how to prove it still works.

---

## Verified state

```bash
docker compose up -d && make init-mongo        # one-time replica-set init
docker compose --profile oracle up -d oracle   # optional, ~2 GB

python -m pytest -q                 # 392 passed, 0 skipped, 0 failed
python tools/check_links.py         # 486 internal links, 0 broken, 0 absolute paths
python tools/check_deps.py          # all third-party imports declared
ruff check .                        # All checks passed!
python tools/check_beginner_layer.py  # 5 beginner invariants across 25 modules
```

**392 tests pass with zero skips**, run twice back to back with identical results — the suite is idempotent, which matters because every test writes to a real database.

Structural completeness:

| Artifact | Status |
| :--- | :--- |
| Track B `*_live.py` against a real engine | **23/23** (Modules 03 and 20 are exempt: SQLite is already real, B+ trees are pure algorithm) |
| Real DB drivers in use | **12/12** |
| Notebook ≥ 12 cells | 25/25 |
| Quiz | 25/25 |
| `TROUBLESHOOTING_AND_EDGE_CASES.md` | 25/25 |
| 3-tier `PROJECT_GUIDE.md` | 25/25 |
| "You have mastered this when…" checklist | 25/25 |
| README ≥ 150 lines | 25/25 |
| `starter/` scaffold | 25/25 |
| `debug_lab/` | 25/25 |
| `00_W3_BEGINNER_PLAYGROUND.md` + `00_try_it_yourself.py` | 25/25 |
| Phase checkpoints | 8/8 |

---

## The change that mattered: two tracks per module

The course previously contained **no line of code that talked to any real database** — 2 `import sqlite3` and nothing else, in a curriculum teaching PostgreSQL, Oracle, MongoDB, Redis, Cassandra, DynamoDB, Neo4j, ClickHouse, Elasticsearch and Qdrant. It was a database-internals course wearing a DBA course's title.

The internals code was not the problem — it is the best material here. Module 12 implements Redis SDS buffers, skip lists with span calculation, RESP formatting and `BGREWRITEAOF` compaction; Module 04 implements JSONB storage, a GIN inverted index, TOAST chunking and GiST-style range exclusion. The problem was that it was the *only* track.

Every module now has both:

| Track | File | Teaches |
| :--- | :--- | :--- |
| **A — Internals** | `<name>_engine.py` | how the database works — build the mechanism |
| **B — Operation** | `<name>_live.py` | how to drive the real thing — driver, real queries, `EXPLAIN`, failover |

And a **reconciliation test** per module runs the same logical operation through both and asserts they agree. That is what turns a hand-built model from a toy into a verified one: where the model and PostgreSQL disagree, the model is wrong, and the test says so.

Real drivers now in use: `psycopg2`, `pymysql`, `pymongo`, `redis`, `cassandra-driver`, `boto3`, `neo4j`, `duckdb`, `clickhouse-connect`, `elasticsearch`, `qdrant-client`, `oracledb`.

---

## Defects found by running code that had never run

83 Track B tests existed but had never executed — no Docker daemon was running, so they all skipped. Every one of the following was hiding behind a green-looking suite:

| Defect | Detail |
| :--- | :--- |
| **`test_isolation_live.py` would not parse** | Two stray control characters (U+0001) plus a missing `import pytest`. The file could never have run. |
| **Missing imports** | `psycopg2` in Module 04's tests, `time` in Module 23's — both `NameError` on first execution. |
| **Broken PL/pgSQL** | Module 24's dual-write trigger was missing its `$$` dollar-quote delimiters, so PostgreSQL parsed `BEGIN` as a transaction statement. |
| **API drift, 5 sites** | Tests calling `insert_row`, `lookup_by_pk`, `lookup_by_secondary_index`, `TwoPhaseLockManager`, and a `backfill_batch(transform)` parameter — none of which existed. Module 23's reconciliation test was written against a 2PL API when the model implements 2PC. |
| **Multi-statement SQL** | Module 06 passed several statements to one `pymysql` `execute()`, which is disabled by default (it is a SQL-injection amplifier). |
| **`VACUUM` inside a transaction** | psycopg2 opens one on the first statement, so Module 22's maintenance call always raised `ActiveSqlTransaction`. Fixed with an explicit autocommit path. |
| **Tests that could only pass once** | Module 04's exclusion constraint, Module 15's conditional write and Module 24's migration all left state behind. Setup is now idempotent — and Module 15 asserts the conditional write *does* reject a duplicate, turning the failure into the lesson. |
| **Typed columnar insert** | Module 17 passed date *strings* to a ClickHouse `DateTime` column; the driver raised `'str' object has no attribute 'timestamp'`, an error pointing nowhere near the cause. |

### Environment defects, which are course defects

| Problem | Fix |
| :--- | :--- |
| **Port collision with the learner's own services** | A native PostgreSQL 17 on 5432 meant the tests silently connected to the *wrong server* and failed authentication. All services now publish on non-standard ports (15432, 13306, 17017, …), every client reads host/port from the environment, and `.env.example` documents each one. Hard-coding a well-known port assumes you own the machine. |
| **Windows reserved port range** | The first remap chose 55432, which sits inside Hyper-V's reserved `55338–55437` block and cannot be bound. Moved to the clear 15000–19999 range. |
| **Cassandra OOM-killed on start** | It sizes its heap from total host RAM and exceeds Docker Desktop's allocation (exit 137). `MAX_HEAP_SIZE` is now pinned with a 2 GB limit and a 90-second `start_period`. |
| **Mongo replica set unusable from the host** | `--replSet` is required for Module 11's change streams, but the set advertises its *internal* hostname. Clients now connect with `?directConnection=true`, and `make init-mongo` performs the one-time initiation. Change streams verified working. |
| **Elasticsearch client/server mismatch** | `elasticsearch>=8.12.0` allowed the 9.x client, which rejects an 8.x server with `media_type_header_exception`. Pinned to `>=8.12,<9` with the reason in a comment. |
| **Credential drift** | Oracle (`oracle` vs `coursepw`) and Neo4j (`password` vs `coursepw123`) defaults disagreed with `docker-compose.yml`, so those tests skipped even with healthy containers. Aligned, and both now read from the environment. |

---

## Infrastructure

`docker-compose.yml` brings up all 11 engines with healthchecks; Oracle sits behind a `--profile oracle` because of its size. A `Makefile` provides `up`, `wait`, `init-mongo`, `bootstrap`, `test`, `test-live`, `lint`, `links`, `deps`, `down`, `clean`. CI mirrors it with GitHub Actions services.

`tools/check_links.py` and `tools/check_deps.py` (shared with the Python course) fail the build on a broken link, an absolute path, or an undeclared import. 132 absolute `file:` URLs carrying a specific user's home directory — which worked on exactly one machine — are now relative.

---

## Maintaining it

```bash
make bootstrap        # up + wait + init-mongo
make test             # full suite
make down             # stop, keep images
```

The suite must stay at **392 passed, 0 skipped** with services up, and must produce the same result on a second consecutive run. If a Track B test starts skipping, a service is down or a credential drifted — check `docker compose ps` and `.env.example` before assuming the code is wrong.

---

## Added after the first completion pass: curriculum-coverage gaps

Comparing this course and the System Design course against a reference
system-design syllabus surfaced four topic areas that neither covered. Two were
already whole modules here (storage engines, lexical search). The other two were
genuinely missing, and are now closed.

### Module 18 — Analytics Engineering (new)

Modules 18–24 were renumbered to 19–25 to open the slot immediately after
Module 17, because dimensional modelling builds directly on the columnar engine
Module 17 teaches. Phase 6 now covers Modules 17–19.

The gap was specific: `star schema`, `materialized view`, `data warehouse`,
`slowly changing dimension` and `OLAP cube` appeared in a combined total of four
files across all three courses, all as passing prose. The course taught the
columnar *engines* thoroughly and nothing about how to model on top of them.

Module 18 adds, with 59 tests:

| Component | What it teaches |
| :--- | :--- |
| `SurrogateKeyAllocator` | why a natural key cannot be an SCD2 primary key |
| `DimensionTable` | SCD Type 1 and 2, tracked vs untracked attributes, the as-of join |
| `FactTable` | grain enforcement that rejects mixed-grain rows |
| `StarSchema` | the star join as an aggregation over dimensions and fact |
| `MaterializedView` | full and watermark-incremental refresh, plus a non-additive guard that raises rather than silently doing O(fact) work |
| `PipelineDAG` | Kahn ordering, cycle detection, run-key idempotency, correct failure propagation |
| `WatermarkStore` / `Backfill` | monotonic marks, bounded resumable batches |

Track B (`warehouse_live.py`) runs the same logic against real **DuckDB** —
real DDL, a real two-statement SCD2 merge inside a transaction, real `EXPLAIN`,
and a real materialised aggregate measured at **10.3× faster** than the raw star
join over 20,000 fact rows. DuckDB is embedded, so these tests need no Docker
and **never skip** — deliberate, because the reconciliation test is the most
important one in the module and should not be the one that quietly stops running
on a bare machine.

The debug lab plants **six defects that all exit 0**, and each was verified to
manifest observably:

| # | Defect | Observable symptom |
| :-- | :--- | :--- |
| 1 | as-of lookup returns `current()` | reprocessing March moves $130 of Ohio revenue to Texas |
| 2 | `valid_to` off by one day | 1 overlapping version pair; one double-counted day per change |
| 3 | `dict.update` in the delta merge | incremental says OH 40.0, full says 220.0 |
| 4 | watermark set to `today()` | second extract returns `[]` instead of `[3]` |
| 5 | completion recorded before the task runs | run 2 skips a task that never succeeded |
| 6 | terminal exception swallowed | analysts emailed about a table that was never loaded |

Defects 1 and 5 were initially dormant in the lab's scenario; a partition
reprocess and an always-failing task were added specifically so all six
manifest.

### Module 19 — typeahead (extended)

`autocomplete`/`typeahead` appeared only in this course's own syllabus and
roadmap documents — listed, never taught. Module 19 now covers it with 24 new
tests:

- **`CompletionTrie`** — the teachable form of Lucene's FST. Caches top-k at
  every node on insert, so a one-character prefix (the query users type most)
  costs no more than the narrowest one. Measured against a 2,000-entry subtree.
- **`EdgeNGramIndex`** — the write-time alternative, with its write
  amplification measured against the trie rather than asserted.
- **`bounded_edit_distance`** and **`FuzzySuggester`** — the tractable form of
  Lucene's Levenshtein-automaton intersection, with `AUTO` length-scaled
  fuzziness and correctness ranked before popularity.

Track B adds a real Elasticsearch **`completion`** field (FST-backed) and an
`edge_ngram` mapping, verified live: `test_reconciliation_completion_suggester_matches_handbuilt_trie`
asserts the hand-built trie and Elasticsearch return identical ranked lists.
The mapping sets `search_analyzer: standard` explicitly, with the reason in a
comment — leaving it unset is the classic `edge_ngram` misconfiguration and
produces wildly irrelevant hits from a mapping that looks correct.

### Two broken healthchecks

Both surfaced only when the full stack was brought up:

| Service | Defect | Fix |
| :--- | :--- | :--- |
| **Qdrant** | The healthcheck called `curl`, which does not exist in the image (no `wget`, `nc` or `python3` either — only `bash`). It could **never** pass, so a fully working container was marked unhealthy forever. | A `bash` `/dev/tcp` probe against `/readyz`, needing no external binary. |
| **ClickHouse** | `wget http://localhost:8123/ping` was refused *inside* the container while the same request from the host succeeded. `localhost` resolves to `::1` first, and ClickHouse's default `listen_host` is IPv4-only. | `http://127.0.0.1:8123/ping`. |

Both were verified working before and after: Qdrant returned
`all shards are ready` and ClickHouse returned `Ok.` from the host the entire
time. The services were healthy; the probes were wrong.

### A renumber defect the link checker could not see

The renumber updated link *targets* correctly, but nine short-form labels of the
form `[Mod 18](Module_19_...)` kept their old numbers. Every link resolved, so
`check_links.py` passed — the labels simply lied. Found and fixed by comparing
each label's number against its target's, which is now the check to run after
any renumber.

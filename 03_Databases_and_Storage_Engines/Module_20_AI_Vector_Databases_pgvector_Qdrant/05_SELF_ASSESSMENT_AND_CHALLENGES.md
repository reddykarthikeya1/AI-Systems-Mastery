# Module 20 AI Vector Databases pgvector Qdrant: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **AI Vector Databases: pgvector & Qdrant HNSW Similarity** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the difference between Cosine Distance, Euclidean ($L_2$) Distance, and Dot Product?** What is the difference between Cosine Distance, Euclidean ($L_2$) Distance, and Dot Product?
2. **How does the Hierarchical Navigable Small World (HNSW) graph index work?** How does the Hierarchical Navigable Small World (HNSW) graph index work?
3. **What is Approximate Nearest Neighbor (ANN) search vs Flat (Exact) k-NN?** What is Approximate Nearest Neighbor (ANN) search vs Flat (Exact) k-NN?
4. **What does the `ef_search` parameter control in HNSW graph traversal?** What does the `ef_search` parameter control in HNSW graph traversal?
5. **How does pgvector integrate vector similarity search into PostgreSQL?** How does pgvector integrate vector similarity search into PostgreSQL?
6. **What is the difference between Pre-Filtering and Post-Filtering in vector databases?** What is the difference between Pre-Filtering and Post-Filtering in vector databases?
7. **Why must vectors be unit-normalized when using Dot Product for cosine similarity?** Why must vectors be unit-normalized when using Dot Product for cosine similarity?
8. **What is the IVFFlat index in vector databases?** What is the IVFFlat index in vector databases?
9. **What is Recall@K in vector search benchmarking?** What is Recall@K in vector search benchmarking?
10. **How does Qdrant achieve sub-millisecond vector search with complex metadata filtering?** How does Qdrant achieve sub-millisecond vector search with complex metadata filtering?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Cosine measures angle regardless of magnitude; Euclidean measures geometric distance; Dot product combines angle and magnitude.

#### Answer 2:
It organizes vectors into multi-layer skip-list graphs; upper layers perform long-distance routing; bottom layers perform fine-grained local search.

#### Answer 3:
Flat compares query against every vector ($O(N)$); ANN traverses graph or clusters in sub-linear time ($O(\log N)$) with slight recall trade-off.

#### Answer 4:
The size of the dynamic priority queue during search: higher `ef_search` yields higher accuracy (recall) at the cost of latency.

#### Answer 5:
As a native C extension providing a `vector` type, operators (`<->` L2, `<=>` Cosine), and IVFFlat / HNSW index access methods.

#### Answer 6:
Pre-filtering filters metadata before vector traversal; post-filtering searches vectors first and then discards non-matching metadata (risking returning fewer than K items).

#### Answer 7:
For unit vectors, the dot product is mathematically identical to cosine similarity: $\vec{u} \cdot \vec{v} = \cos(\theta)$.

#### Answer 8:
Inverted File Flat: vectors are clustered into Voronoi cells around centroids; queries search only the nearest centroids.

#### Answer 9:
The percentage of true nearest neighbors (from exact brute force) retrieved by an ANN algorithm in its top-K results.

#### Answer 10:
It builds combined payload indices and integrates filter evaluation directly into the HNSW graph traversal loop.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Benchmark ANN Recall@10 of an HNSW index against exact brute-force search across 10,000 vectors.

### 🚀 Challenge 2: Architect Stretch Problem
Build a hybrid search engine combining vector embeddings with dense scalar filters in Qdrant.

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

### D1. HNSW Recall Cliff from Undersized ef_search with Filtering

```sql
-- pgvector table with HNSW index
CREATE TABLE document_embeddings (
    doc_id uuid PRIMARY KEY,
    category_id int,
    embedding vector(1536)
);

CREATE INDEX idx_docs_hnsw ON document_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

-- Query executed by semantic search API:
SET hnsw.ef_search = 20;

SELECT doc_id, embedding <=> $query_vector AS distance
FROM document_embeddings
WHERE category_id = 42
ORDER BY distance
LIMIT 10;
```

**Observed symptom:** Semantic search returns only 2 documents instead of requested 10, or returns documents with cosine distance 0.85 when documents with cosine distance 0.12 exist in category 42.

**(a)** Why does combining a restrictive `WHERE` filter with small `ef_search` cause an HNSW recall cliff?

**(b)** What is the difference between pre-filtering, post-filtering, and single-stage iterative HNSW index traversal?

**(c)** How should `ef_search` be tuned, or how does modern iterative index scanning resolve this issue?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In early vector search engines (and unoptimized HNSW implementations), post-filtering traverses the graph nearest-neighbor candidates first (bounded by `ef_search = 20`) and then filters out candidates that do not meet `category_id = 42`. If only 10% of total documents belong to category 42, an `ef_search` of 20 explores only 20 global nearest nodes, of which only 1 or 2 happen to match category 42, causing recall to collapse to near zero.

**Diagnostic Commands:**
1. Check execution plan in Postgres:
   ```sql
   EXPLAIN ANALYZE
   SELECT doc_id FROM document_embeddings
   WHERE category_id = 42
   ORDER BY embedding <=> $query_vector LIMIT 10;
   ```
2. Observe whether pgvector used an index scan or filtered bitmap scan, and note the ratio of visited to returned nodes.

**Production Fix:**
1. **Increase `ef_search` dynamically for filtered queries:**
   ```sql
   SET hnsw.ef_search = 100;  -- or higher depending on filter selectivity
   ```
2. **Use pgvector 0.7.0+ Iterative Index Scan:** pgvector 0.7+ supports iterative index scans that dynamically continue traversing HNSW until the `LIMIT` is satisfied:
   ```sql
   SET hnsw.iterative_scan = 'relaxed';
   ```
3. **Payload Indexing in Qdrant:** In dedicated vector databases like Qdrant, build payload indexes on `category_id` so the HNSW traversal is restricted exclusively to nodes with `category_id = 42` during the graph traversal itself.

</details>

---

### D2. Vector Normalization Mismatch in Cosine vs Inner Product Metric

```sql
-- OpenAI text-embedding-3-small generates unit-normalized vectors (norm = 1.0)
-- Custom BERT model generates unnormalized vectors (norm between 3.2 and 15.8)

CREATE TABLE product_embeddings (
    id serial PRIMARY KEY,
    embedding vector(768)
);

-- Index built using Inner Product (<#>) for speed
CREATE INDEX idx_products_ip ON product_embeddings 
USING ivfflat (embedding vector_ip_ops) WITH (lists = 100);

-- Query using inner product:
SELECT id FROM product_embeddings 
ORDER BY embedding <#> $query_vector LIMIT 5;
```

**Observed symptom:** Search returns completely irrelevant long documents first. Shorter, semantically identical product descriptions are ranked far down the list.

**(a)** Why does Inner Product (`<#>`) return erroneous rankings when vectors are not unit-normalized?

**(b)** What is the mathematical relationship between Dot Product, Cosine Similarity, and Euclidean Distance for normalized vectors?

**(c)** How can you normalize vectors in SQL/Python or configure pgvector with native cosine distance (`<=>`)?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Inner product (dot product) between vectors $\mathbf{u}$ and $\mathbf{v}$ is defined as $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos(	heta)$. If vectors are not unit-normalized ($\|\mathbf{u}\| 
eq 1$), the metric is dominated by the vector magnitudes rather than the angle $	heta$. In embedding models, longer texts or documents with repeated terms often have larger $L_2$ norms, causing inner product to favor large-magnitude vectors over genuine semantic similarity.

**Mathematical Proof:**
Only when $\|\mathbf{u}\| = 1$ and $\|\mathbf{v}\| = 1$ does:
$$\mathbf{u} \cdot \mathbf{v} = \cos(	heta) = 1 - rac{1}{2} \|\mathbf{u} - \mathbf{v}\|^2$$

**Production Fix:**
1. **Option A: Use Cosine Distance (`<=>`) Index:**
   ```sql
   DROP INDEX idx_products_ip;
   CREATE INDEX idx_products_cosine ON product_embeddings 
   USING hnsw (embedding vector_cosine_ops);
   
   SELECT id FROM product_embeddings ORDER BY embedding <=> $query_vector LIMIT 5;
   ```
2. **Option B: Normalize Vectors in Python Before Ingestion:**
   ```python
   import numpy as np
   norm = np.linalg.norm(vec)
   if norm > 0:
       vec = vec / norm
   # With unit-normalized vectors, inner product matches cosine similarity and is faster.
   ```

</details>

---

### D3. Uncompressed Flat Vector Index RAM Exhaustion

```python
# Ingesting 10,000,000 vectors of dimension 1536 (Float32) into Qdrant/pgvector
# Server RAM: 64 GB

# pgvector table:
CREATE TABLE large_corpus (
    id bigint PRIMARY KEY,
    vector vector(1536)
);
-- 10 million vectors inserted
CREATE INDEX idx_large_hnsw ON large_corpus 
USING hnsw (vector vector_cosine_ops) WITH (m = 32, ef_construction = 128);
```

**Observed symptom:** Postgres index build terminates after 3 hours with: out of memory. System OOM killer kills postgres process. In Qdrant, process crashes during index construction when memory exceeds 64GB.

**(a)** How much RAM do 10 million 1536-dimensional Float32 vectors consume in raw storage plus HNSW graph edges?

**(b)** What is Scalar Quantization (SQ) and Product Quantization (PQ), and what compression ratios do they achieve?

**(c)** How can halfvec (Float16) or Product Quantization be enabled in pgvector / Qdrant to fit within RAM?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Let us calculate the memory requirement:
1. **Raw Vectors:** $10,000,000 	imes 1536 	imes 4	ext{ bytes} pprox 61.44	ext{ GB}$.
2. **HNSW Graph Edges:** With $M = 32$, each node stores 32 neighbor pointers ($32 	imes 8	ext{ bytes} = 256	ext{ bytes}$ per vector) plus index metadata $pprox 10	ext{ to }15	ext{ GB}$.
Total memory required is over $75	ext{ GB}$, exceeding the 64GB physical RAM limit. The system runs out of memory and crashes.

**Production Fix:**
1. **Scalar Quantization (SQ) / Float16 (`halfvec`):**
   In `pgvector` 0.7+, use `halfvec` to cut vector storage by 50% (from 4 bytes to 2 bytes per float) with virtually zero recall loss:
   ```sql
   ALTER TABLE large_corpus ALTER COLUMN vector TYPE halfvec(1536);
   -- Raw vectors drop from 61.4 GB to 30.7 GB
   ```
2. **Product Quantization (PQ) in Qdrant:**
   Quantize 1536 floats into 96 or 192 byte codes (32x compression), storing quantized vectors in RAM and keeping original vectors on NVMe disk:
   ```json
   {
     "quantization_config": {
       "scalar": {
         "type": "int8",
         "quantile": 0.99,
         "always_ram": true
       }
     }
   }
   ```
   Memory drops from 75GB to ~12GB with 98%+ recall.

</details>

---

### D4. Post-Filtering vs Single-Stage Filtered Vector Search Latency

```sql
-- Hybrid query: find documents by author and semantic similarity
SELECT doc_id, title
FROM articles
WHERE author_id = 'auth_10928'
ORDER BY embedding <=> $search_vector
LIMIT 5;

-- articles contains 20,000,000 rows. author_id 'auth_10928' has only 8 articles.
```

**Observed symptom:** Query takes 14,200ms to execute. EXPLAIN ANALYZE shows an HNSW index scan visited 500,000 nodes before finding 5 matching the author filter.

**(a)** Why does an HNSW index scan struggle when the relational filter matches a tiny fraction (<0.01%) of rows?

**(b)** When should the database optimizer choose a B-Tree index scan over a Vector index scan?

**(c)** How can you structure the index or query so Postgres uses the B-Tree index on `author_id` and exact distance calculation?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
When a filter is highly selective (e.g. author 10928 has only 8 rows out of 20,000,000, or 0.00004%), searching through the global HNSW graph requires traversing hundreds of thousands of unrelated nodes just to stumble upon one belonging to that author. The CBO miscalculated costs and chose the HNSW index scan instead of a simple B-Tree index scan on `author_id` followed by an exact top-K distance sort on the 8 matching rows.

**Diagnostic Commands:**
1. Run `EXPLAIN (ANALYZE, BUFFERS)`:
   ```sql
   EXPLAIN (ANALYZE, BUFFERS)
   SELECT doc_id FROM articles WHERE author_id = 'auth_10928'
   ORDER BY embedding <=> $search_vector LIMIT 5;
   ```
2. Notice `HNSW index scan: loops=1, rows=5, time=14180ms`.

**Production Fix:**
1. Create a composite B-Tree index on `author_id`:
   ```sql
   CREATE INDEX idx_articles_author ON articles(author_id);
   ```
2. For highly selective filters, force the optimizer or write a CTE that isolates the small filtered candidate set first:
   ```sql
   WITH author_docs AS (
       SELECT doc_id, embedding
       FROM articles
       WHERE author_id = 'auth_10928'  -- Uses B-Tree, fetches 8 rows in 0.1ms
   )
   SELECT doc_id
   FROM author_docs
   ORDER BY embedding <=> $search_vector
   LIMIT 5;  -- Exact distance calculation on 8 rows takes 0.02ms
   ```
   Query latency drops from 14,000ms to **0.3ms**.

</details>

---

### D5. Postgres WAL Amplification During HNSW Index Build

```sql
-- Building HNSW index on 2 million 768-dim vectors
CREATE INDEX idx_hnsw_embed ON items USING hnsw (embedding vector_cosine_ops);
```

**Observed symptom:** During index creation, disk space drops by 85 GB. Postgres replica falls 45 minutes behind. WAL archive directory fills up, causing database to stall all write transactions.

**(a)** Why does building an HNSW or IVFFlat index generate enormous volumes of Write-Ahead Log (WAL)?

**(b)** What postgresql.conf settings (`wal_level`, `max_wal_size`, `maintenance_work_mem`) influence index build WAL generation?

**(c)** How can you build large vector indexes safely without saturating WAL archives or replicas?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In PostgreSQL, every page modification during index construction must be logged to WAL to guarantee crash recovery and replica replication. For HNSW, inserting millions of vectors requires building bi-directional graph links across multiple layers, dirtying thousands of index pages repeatedly. If `maintenance_work_mem` is low, Postgres must write temporary spill pages to disk and emit full-page WAL images, resulting in 50GB–100GB of WAL generation for a 10GB dataset.

**Diagnostic Commands:**
1. Check WAL generation rate:
   ```bash
   SELECT pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/00000000'));
   ```
2. Check replication lag on replica:
   ```sql
   SELECT client_addr, pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) AS write_lag_bytes FROM pg_stat_replication;
   ```

**Production Fix:**
1. **Increase `maintenance_work_mem`:**
   ```sql
   SET maintenance_work_mem = '8GB';  -- Keep HNSW build graph in memory
   ```
2. **Increase `max_parallel_maintenance_workers`:**
   ```sql
   SET max_parallel_maintenance_workers = 4;
   ```
3. **If Populating a New Table:** Build the index *before* streaming WAL to replicas, or populate data with `UNLOGGED` table mode, build the index, and then convert to logged (`ALTER TABLE items SET LOGGED;`).
4. **Tune WAL Checkpoint:** Increase `max_wal_size = 32GB` and `checkpoint_completion_target = 0.9` during large bulk index migrations.

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

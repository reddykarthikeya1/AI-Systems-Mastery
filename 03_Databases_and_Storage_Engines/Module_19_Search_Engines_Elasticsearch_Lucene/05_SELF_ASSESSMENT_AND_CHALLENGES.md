# Module 19 Search Engines Elasticsearch Lucene: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Search Engines: Elasticsearch, Lucene & Inverted Indexes** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is an Inverted Index in information retrieval?** What is an Inverted Index in information retrieval?
2. **Explain the components of Okapi BM25 ranking function.?** Explain the components of Okapi BM25 ranking function.
3. **What are the stages of an Elasticsearch Text Analyzer?** What are the stages of an Elasticsearch Text Analyzer?
4. **How does a compound Bool Query combine must, should, and filter clauses?** How does a compound Bool Query combine must, should, and filter clauses?
5. **What is Fuzzy Search in Elasticsearch, and how does Levenshtein distance work?** What is Fuzzy Search in Elasticsearch, and how does Levenshtein distance work?
6. **What is the difference between a `text` field and a `keyword` field in Elasticsearch?** What is the difference between a `text` field and a `keyword` field in Elasticsearch?
7. **What is the Two-Phase Query-Then-Fetch distributed search execution model?** What is the Two-Phase Query-Then-Fetch distributed search execution model?
8. **What is Mapping Explosion, and how is it prevented?** What is Mapping Explosion, and how is it prevented?
9. **How do Term Bucket Aggregations compute top categories?** How do Term Bucket Aggregations compute top categories?
10. **Why should deep pagination avoid high `from` offsets in Elasticsearch?** Why should deep pagination avoid high `from` offsets in Elasticsearch?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
A mapping from unique terms (words) to postings lists containing document IDs and token positions where the terms occur.

#### Answer 2:
Term Frequency (TF) with saturation ($k_1$), Document Frequency (IDF), and Document Length normalization ($b$) relative to average document length.

#### Answer 3:
Character Filters (strip HTML) $\rightarrow$ Tokenizer (split into terms) $\rightarrow$ Token Filters (lowercasing, stopwords, stemming).

#### Answer 4:
`must`: must match, contributes to score; `should`: optional, boosts score; `filter`: must match, cached, does NOT contribute to score.

#### Answer 5:
It matches terms within $N$ character edits (insertions, deletions, substitutions) using finite state transducers (FSTs).

#### Answer 6:
`text` is analyzed and tokenized for full-text search; `keyword` is stored exact and un-tokenized for exact matching, sorting, and aggregations.

#### Answer 7:
Phase 1: Coordinator queries all shards for matching document IDs and scores. Phase 2: Coordinator fetches full document sources only for top-K results.

#### Answer 8:
Too many distinct fields in an index exhausting cluster state memory; prevented by setting `"dynamic": "strict"`.

#### Answer 9:
By building doc-value hash tables counting occurrences of exact keyword values across matching documents.

#### Answer 10:
High offsets force all shards to score and return thousands of documents to the coordinator; use `search_after` instead.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Build an inverted index with TF-IDF / BM25 scoring in Python matching Lucene formula.

### 🚀 Challenge 2: Architect Stretch Problem
Create an Elasticsearch index with custom stemmer and synonym filters and verify multi-field search.

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

### D1. Lucene TooManyClauses Boolean Query Expansion Exception

```json
POST /products/_search
{
  "query": {
    "wildcard": {
      "sku_code": {
        "value": "*AB*"
      }
    }
  }
}
```

**Observed symptom:** Elasticsearch returns HTTP 500: SearchPhaseExecutionException: all shards failed; nested: TooManyClauses[maxClauseCount is set to 1024]; nested: BooleanQuery$TooManyClauses.

**(a)** Why does a leading wildcard query (`*AB*`) trigger Lucene's `TooManyClauses` exception?

**(b)** How does Lucene's inverted index structure make leading wildcard queries inefficient?

**(c)** What indexing strategies (`wildcard` field type, n-grams, or reverse token filters) solve substring searches efficiently?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Lucene's inverted index stores terms sorted lexicographically (e.g. `aa`, `ab`, `ac`). Prefix queries (`AB*`) perform a fast binary search to find the start term and scan until the prefix changes. However, a leading wildcard query (`*AB*`) cannot use binary search; it must iterate through *every term in the entire inverted index* dictionary for that field. Lucene rewrites this into a giant `BooleanQuery` consisting of an `OR` of every matching term. If matching terms exceed `indices.query.bool.max_clause_count` (default 1,024), Lucene aborts the query.

**Diagnostic Commands:**
1. Check Lucene terms on the shard:
   ```bash
   GET /products/_validate/query?explain=true
   { "query": { "wildcard": { "sku_code": "*AB*" } } }
   ```
2. Observe `rewrite` method and clause counts.

**Production Fix:**
1. **Use `wildcard` field type (Elasticsearch 7.9+):**
   ```json
   PUT /products
   {
     "mappings": {
       "properties": {
         "sku_code": { "type": "wildcard" }
       }
     }
   }
   ```
   The `wildcard` field type indexes n-grams and character n-gram automata internally, allowing arbitrary wildcard searches without BooleanQuery expansion.
2. **N-Gram Tokenizer:** Index the field with an `ngram` or `edge_ngram` tokenizer so substrings are indexed as distinct tokens at ingest time.

</details>

---

### D2. Deep Pagination OOM via 'from' + 'size' > 10,000

```python
# E-commerce export service
page_number = 1500
page_size = 50

response = es.search(
    index="orders",
    body={
        "from": page_number * page_size,  # from = 75,000
        "size": page_size,                 # size = 50
        "sort": [{"order_date": "desc"}]
    }
)
```

**Observed symptom:** Elasticsearch rejects request with: Result window is too large, from + size must be less than or equal to: [10000] but was [75050]. See the scroll api or search_after for more information.

**(a)** Why does paginating with `from + size` across distributed shards scale with $O(N \times \text{shards})$ memory and CPU overhead?

**(b)** What setting controls the maximum result window, and why is increasing it a trap?

**(c)** How does `search_after` with Point-in-Time (PIT) solve deep pagination efficiently?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In a distributed index with $S$ primary shards, when a client requests `from: 75000, size: 50`, every shard must compute its local top $75,050$ matching documents and serialize their sort values back to the coordinating node. The coordinating node must deserialize and sort $S 	imes 75,050$ records in memory (e.g. across 5 shards = 375,250 records) before discarding 375,200 and returning the final 50. For deep pages, this causes severe heap memory pressure and coordinator crashes. Elasticsearch caps `index.max_result_window` at 10,000.

**Diagnostic Commands:**
1. Check current index settings:
   ```bash
   GET /orders/_settings?filter_path=*.settings.index.max_result_window
   ```

**Production Fix:**
Use **Point In Time (PIT)** and **`search_after`**:
```python
# 1. Open Point in Time
pit = es.open_point_in_time(index="orders", keep_alive="2m")
pit_id = pit["id"]

# 2. Paginate using sort cursor
response = es.search(body={
    "size": 50,
    "query": {"match_all": {}},
    "pit": {"id": pit_id, "keep_alive": "2m"},
    "sort": [{"order_date": "desc"}, {"_shard_doc": "asc"}],
    "search_after": last_sort_values  # Cursor from previous page
})

# 3. Close PIT when done
es.close_point_in_time(body={"id": pit_id})
```
`search_after` has $O(	ext{size})$ complexity per page and constant memory overhead.

</details>

---

### D3. Mapping Explosion from Dynamic JSON Keys

```python
# Ingesting raw webhook JSON payloads directly
def ingest_webhook(payload: dict):
    # Payload contains dynamic UUID keys:
    # {"user_attributes": {"550e8400-e29b-41d4-a716-446655440000": "active", ...}}
    es.index(
        index="webhook_events",
        document=payload
    )
```

**Observed symptom:** Elasticsearch cluster state turns RED. Master node logs: 'Limit of total fields [1000] in index [webhook_events] has been exceeded'. Master CPU reaches 100% propagating cluster state updates.

**(a)** What is a 'mapping explosion' in Elasticsearch, and why are dynamic JSON keys hazardous?

**(b)** What cluster-wide metadata must the master node synchronize on every new mapping field addition?

**(c)** How should dynamic key-value pairs be modeled using the `nested` or `flattened` data types?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
By default, Elasticsearch uses **dynamic mapping**: whenever a new JSON key appears in an indexed document, Elasticsearch adds that field to the index mapping schema. Each field mapping is stored in the cluster state metadata. When documents contain unique keys (such as UUIDs, email addresses, or user IDs as keys), thousands of new fields are created daily. The cluster state balloons to hundreds of megabytes. Every mapping update must be serialized and acknowledged across every node in the cluster by the master node, causing master timeouts and cluster lockups.

**Diagnostic Commands:**
1. Inspect field count:
   ```bash
   GET /webhook_events/_mapping
   ```
2. Check cluster state size:
   ```bash
   GET /_cluster/state/metadata?filter_path=metadata.indices.webhook_events.mappings
   ```

**Production Fix:**
1. **Use the `flattened` Field Type:** The `flattened` type indexes entire JSON objects as a single Lucene field without creating individual column mappings for each leaf key:
   ```json
   PUT /webhook_events
   {
     "mappings": {
       "properties": {
         "user_attributes": { "type": "flattened" }
       }
     }
   }
   ```
2. **Key-Value Nested Array Pattern:** Restructure the data model:
   ```json
   "user_attributes": [
       {"key": "uuid_123", "value": "active"}
   ]
   ```
3. Disable dynamic mapping (`"dynamic": "strict"` or `"dynamic": "runtime"`).

</details>

---

### D4. Stopword and Stemming Collisions on Exact Part Number Searches

```json
PUT /catalog
{
  "settings": {
    "analysis": {
      "analyzer": {
        "standard_english": {
          "type": "standard",
          "stopwords": "_english_"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "model_number": { "type": "text", "analyzer": "standard_english" }
    }
  }
}

-- Documents indexed: "Model IT-100", "Part A-OR-B", "Unit IN-55"
-- Search for "IT-100":
GET /catalog/_search
{
  "query": { "match": { "model_number": "IT-100" } }
}
```

**Observed symptom:** Searching for 'IT-100' matches hundreds of irrelevant items containing '100', '200', '300', but fails to boost the exact 'IT-100' model. Searching for 'IN-55' returns 0 results.

**(a)** Why did the search for 'IN-55' fail and 'IT-100' lose precision under the English analyzer?

**(b)** Which Elasticsearch API allows testing how a string is tokenized and filtered by an analyzer?

**(c)** How should part numbers and technical identifiers be modeled using multi-fields (`keyword` + custom tokenizers)?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
The standard English analyzer applies tokenization and stopword removal:
1. `IT` and `IN` are recognized as English stop words (`it`, `in`) and are completely dropped by the stopword filter.
2. The standard tokenizer splits on punctuation, tokenizing `IT-100` into `[it, 100]`. Since `it` is removed, only `100` is indexed.
3. Searching for `IT-100` removes `IT` from the query tokens as well, reducing the query to a search for the token `100`, matching every item with `100`. Searching for `IN-55` where `55` doesn't match returns nothing.

**Diagnostic Commands:**
Use the `_analyze` API to test tokenization:
```json
POST /_analyze
{
  "analyzer": "standard_english",
  "text": "Unit IN-55"
}
// Response: only token "unit" and "55" are generated; "IN" is discarded.
```

**Production Fix:**
Use multi-fields with a raw `keyword` normalizer or a custom code analyzer:
```json
PUT /catalog
{
  "mappings": {
    "properties": {
      "model_number": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "exact": {
            "type": "keyword",
            "normalizer": "lowercase_normalizer"
          }
        }
      }
    }
  }
}
```
Query using `term` or `multi_match` with a boost on `model_number.exact`:
```json
GET /catalog/_search
{
  "query": {
    "multi_match": {
      "query": "IT-100",
      "fields": ["model_number", "model_number.exact^10"]
    }
  }
}
```

</details>

---

### D5. Oversharding Primary Shard Imbalance and Latency Degradation

```python
# Index template creating 10 primary shards per daily index
PUT /_index_template/daily_logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 10,
      "number_of_replicas": 1
    }
  }
}
# Daily index size: 500MB total per day.
# After 180 days: 180 indices * 10 shards * 2 = 3,600 shards on a 3-node cluster.
```

**Observed symptom:** Search queries across last 30 days take 12,000ms. Heap memory on all 3 nodes is pegged at 95%. Elasticsearch crashes with frequent garbage collection pauses exceeding 10 seconds.

**(a)** What is 'oversharding', and what memory overhead does each Lucene shard consume on the Java heap?

**(b)** What is the official Elasticsearch recommendation for shard size and shards per GB of heap?

**(c)** How do you remediate existing small shards using the Shrink API and Index Lifecycle Management (ILM)?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Each Lucene shard is an independent search engine with its own Lucene segment files, terms dictionaries, norms, and memory buffers. Even an empty or tiny shard consumes 4MB to 30MB of Java heap memory just to keep metadata and file handles open. With 3,600 shards on a 3-node cluster with 16GB heap per node, over 50% of the entire heap is consumed exclusively by shard overhead. When a query touches 30 daily indices ($30 	imes 10 = 300$ shards), it spawns 300 search tasks, saturating thread pools.

**Diagnostic Commands:**
1. Check shard count and heap overhead:
   ```bash
   GET /_cat/allocation?v
   GET /_cat/shards?v&s=store:desc
   ```
2. Count total shards:
   ```bash
   GET /_cluster/health
   ```

**Production Fix:**
1. **Elasticsearch Shard Sizing Rules:**
   - Shard size should be between **20GB and 50GB**.
   - Maintain fewer than **20 shards per GB of configured heap**. A node with 16GB heap should host at most 300 shards.
2. **Index Lifecycle Management (ILM) Rollover:**
   Instead of daily calendar indices, roll over based on size:
   ```json
   PUT /_ilm/policy/logs_policy
   {
     "policy": {
       "phases": {
         "hot": {
           "actions": {
             "rollover": { "max_primary_shard_size": "30gb", "max_age": "30d" }
           }
         }
       }
     }
   }
   ```
3. **Shrink and Merge Existing Shards:** Use the Shrink API (`POST /logs-2026-01-01/_shrink/logs-2026-01-01-shrunk`) to reduce 10 shards down to 1 shard for historical indices.

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

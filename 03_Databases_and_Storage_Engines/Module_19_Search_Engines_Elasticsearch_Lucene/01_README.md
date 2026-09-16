# Module 19: Search Engines — Apache Lucene, Elasticsearch & BM25 Relevance

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 19**. In this module, you will master **Search Engines, Apache Lucene, and Elasticsearch** — the technology powering full-text search, distributed log analysis (ELK Stack / OpenSearch), e-commerce product catalogs, and semantic text retrieval.

---

## 🔍 1. The Relational Full-Text Failure vs. The Inverted Index

In relational databases, querying freeform text using substring matching:
```sql
SELECT * FROM articles WHERE content LIKE '%distributed systems%';
```
- **B-Trees cannot be used**: B-Tree indexes only support prefix lookups (`LIKE 'distributed%'`), not leading wildcard searches (`'%...'`).
- **Full Table Scan**: Every disk page must be scanned and scanned byte-by-byte for every query.
- **No Relevance Ranking**: A document mentioning the query phrase once by accident is ranked identically to a document whose primary subject is that phrase.
- **No Linguistic Understanding**: Cannot handle morphological variations ("database", "databases", "databased"), synonyms, or typos.

### The Inverted Index: The Core of Search
Instead of mapping `Document -> Words` (Forward Index), search engines invert the relationship into `Word -> Documents` (**Inverted Index**):

```
Forward Index (Normal Storage):
Doc 1 ──► ["distributed", "consensus", "raft", "databases"]
Doc 2 ──► ["relational", "databases", "acid", "sql"]
Doc 3 ──► ["distributed", "databases", "sharding", "acid"]

Inverted Index (Lucene / Elasticsearch):
"acid"        ──► [Doc 2, Doc 3]
"consensus"   ──► [Doc 1]
"databases"   ──► [Doc 1, Doc 2, Doc 3]
"distributed" ──► [Doc 1, Doc 3]
"raft"        ──► [Doc 1]
"relational"  ──► [Doc 2]
"sharding"    ──► [Doc 3]
"sql"         ──► [Doc 2]
```

### The Postings List
For every term in the **Term Dictionary** (stored as an immutable Finite State Transducer / FST in memory), the index maintains an ordered **Postings List**:
- Document ID
- Term Frequency ($TF$) within that document
- Term Positions (byte offsets and word positions for exact phrase matching `"distributed consensus"`)
- Postings lists are sorted by Document ID and compressed using bit-packing (Frame of Reference / Roaring Bitmaps), allowing multi-term boolean queries (`distributed AND databases`) to execute via linear two-pointer list intersections in microseconds.

---

## ⚙️ 2. The Text Analysis Pipeline

Before text is indexed into an inverted index, it must pass through a 3-stage **Analysis Pipeline**:

```
Raw Text: "<p>The 3 QUICKEST databases are running fast!</p>"
   │
   ▼ 1. Character Filter (HTML Strip)
"The 3 QUICKEST databases are running fast!"
   │
   ▼ 2. Tokenizer (Standard Word Boundary Tokenizer)
["The", "3", "QUICKEST", "databases", "are", "running", "fast"]
   │
   ▼ 3. Token Filters:
       - Lowercase Filter      ──► ["the", "3", "quickest", "databases", "are", "running", "fast"]
       - Stopword Removal Filter ──► ["3", "quickest", "databases", "running", "fast"] (removed "the", "are")
       - Stemming Filter (Porter)──► ["3", "quick", "databas", "run", "fast"]
```

- **Stemming (Porter / Snowball)**: Reduces inflected words to their root base form ("running", "runs", "ran" $\implies$ "run"). A user searching for "running databases" immediately matches documents containing "run database".

---

## 📐 3. The BM25 (Best Matching 25) Relevance Formula

Lucene and Elasticsearch use **Okapi BM25** as their default relevance scoring algorithm. BM25 calculates the relevance score of document $D$ for query $Q = \{q_1, q_2, \dots, q_n\}$:

$$\text{Score}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

### Deconstructing the Formula
1. **Inverse Document Frequency ($\text{IDF}$)**:
   $$\text{IDF}(q_i) = \ln\left(1 + \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5}\right)$$
   - $N$ = Total documents in index.
   - $n(q_i)$ = Number of documents containing term $q_i$.
   - Rare terms (e.g. "Paxos", "Quorum") receive high IDF weights; ubiquitous terms (e.g. "data", "system") receive near-zero weights.
2. **Term Frequency Saturation ($k_1$, default 1.2)**:
   - In basic TF-IDF, repeating a term 100 times makes the document 100x more relevant (vulnerable to keyword stuffing).
   - In BM25, the impact of additional term occurrences asymptotes toward $(k_1 + 1)$. A document with 20 occurrences is barely scored higher than one with 5 occurrences.
3. **Document Length Normalization ($b$, default 0.75)**:
   - $|D|$ = Length of current document (word count).
   - $\text{avgdl}$ = Average document length across the entire index.
   - A short document that mentions the keyword once is considered more focused and relevant than a 500-page book that happens to mention it once.

---

## 🌐 4. Elasticsearch Distributed Architecture

Elasticsearch wraps Apache Lucene instances in a distributed, auto-sharding cluster:

```
                          ┌──────────────────────┐
                          │ Client Search Query  │
                          └──────────┬───────────┘
                                     │
                                     ▼
                        ┌──────────────────────────┐
                        │ Coordinating Node        │
                        └────────────┬─────────────┘
                Broadcast Query      │
         ┌───────────────────────────┼───────────────────────────┐
         ▼ Phase 1: Query Phase      ▼                           ▼
  ┌─────────────┐             ┌─────────────┐             ┌─────────────┐
  │   Shard 0   │             │   Shard 1   │             │   Shard 2   │
  │ (Lucene Core│             │ (Lucene Core│             │ (Lucene Core│
  │ Returns Top │             │ Returns Top │             │ Returns Top │
  │ 10 (ID,BM25)│             │ 10 (ID,BM25)│             │ 10 (ID,BM25)│
  └──────┬──────┘             └──────┬──────┘             └──────┬──────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                        ┌──────────────────────────┐
                        │ Coordinating Node        │
                        │ Merges Top 10 Best Scores│
                        └────────────┬─────────────┘
                                     │ Phase 2: Fetch Phase (Fetches _source only for 10 winners)
                                     ▼
                          ┌──────────────────────┐
                          │ Client Final Result  │
                          └──────────────────────┘
```

### The Query-Then-Fetch Two-Phase Execution
1. **Query Phase**: The coordinating node broadcasts the search query to a primary or replica of every shard in the index. Each shard executes BM25 scoring locally and returns only a priority queue of document IDs and scores (e.g., top 10).
2. **Fetch Phase**: The coordinating node merges the results into a global top 10 list, then requests the full document `_source` JSON only from the specific shards hosting those 10 winning documents. This prevents transferring gigabytes of raw JSON across internal network nodes during large searches.

---

## ⌨️ 5. Typeahead: Search-As-You-Type Is A Different Problem

Autocomplete looks like search with a wildcard on the end. It is not, and
treating it as one is the standard mistake. Three things differ:

| | Search | Typeahead |
| :--- | :--- | :--- |
| Latency budget | ~200 ms (a query) | **~50 ms (a keystroke)** |
| Input | analyzed terms | a raw **prefix** |
| Ranking signal | relevance to a document | **popularity** — there is no document yet |
| Queries per intent | 1 | one per character typed |

The keystroke budget is the constraint that drives everything. If a response
arrives after the user has typed the next character, the result is discarded —
so a slow suggester is not merely slow, it produces work that is thrown away.

And an inverted index cannot answer this directly. It is keyed on whole analyzed
terms, so "starts with `lapt`" requires scanning the term dictionary.
`LIKE 'lapt%'` on a relational table gets you a working demo and a full index
scan **per keystroke**.

### Mechanism 1 — the FST / prefix trie

Walk the prefix, read the answers. Lucene stores this as an **FST** (a minimised
automaton that shares suffixes as well as prefixes, so `laptop` and `desktop`
share their tail); Elasticsearch's `completion` field type builds a separate
in-memory FST, which is why it hits the keystroke budget and why it costs heap in
proportion to the vocabulary.

`CompletionTrie` in this module is the teachable form — same lookup shape,
without suffix minimisation. **The design decision that matters is where the
ranking happens.** A naive trie walks the prefix and then enumerates the whole
subtree to sort candidates by weight, which makes a one-character prefix — the
query users type *most* — the slowest possible query. Caching the top-k at every
node during insert moves that cost to write time, where there is budget for it,
and makes lookup `O(len(prefix) + k)` regardless of subtree size.

`test_trie_lookup_cost_is_independent_of_subtree_size` measures exactly that,
with a 2,000-entry subtree against a 1-entry one.

### Mechanism 2 — edge n-grams

Index every prefix as a term at write time. `laptop` becomes
`l, la, lap, lapt, lapto, laptop`, so a prefix query becomes an ordinary exact
term lookup needing no traversal at all — and it reuses the inverted index you
already have, which is the whole appeal.

The cost is **write amplification**: a term of length *L* produces *L* index
entries.

| | `CompletionTrie` (FST) | `EdgeNGramIndex` |
| :--- | :--- | :--- |
| Lookup | `O(len(prefix) + k)` | `O(1)` hash lookup |
| Index size | one node per *shared* character | one entry per *prefix* |
| Reuses the inverted index | no, separate structure | **yes** |
| Rebuild cost | cheap | proportional to total characters |
| Infix ("middle of a word") | no | no |

Neither handles matching inside a word. For that you need a full n-gram
tokenizer, whose index grows quadratically in term length — which is why nobody
enables it on a large corpus without measuring first.

> ⚠️ **The classic `edge_ngram` misconfiguration.** Set the index analyzer to
> `edge_ngram` and leave `search_analyzer` unset, and Elasticsearch analyses the
> *query* with edge n-grams too — matching every prefix of the query against
> every prefix of every term. The results are wildly irrelevant and the mapping
> looks correct. Set `search_analyzer: standard` explicitly. The mapping in
> `project_solution/elastic_live.py` does, with the reason in a comment.

### Typo tolerance

Users misspell. `laptp` must still find `laptop`, and a strict prefix query
returns nothing for it — verified in
`test_fuzzy_completion_tolerates_a_typo`.

Lucene compiles the query term into a **Levenshtein automaton** and intersects it
with the term dictionary, so a candidate outside the edit-distance bound is never
considered at all. `bounded_edit_distance` is the tractable form of the same
idea: abandon the DP the moment the distance provably exceeds the bound. Two
early exits do most of the work — a length difference above the bound rules a
pair out with no DP, and a completed row whose minimum already exceeds the bound
can never come back down.

**The bound must scale with term length.** Lucene's `AUTO` fuzziness is 2 for
terms of 6+ characters, 1 for 3–5, and 0 below that — because at three
characters an edit distance of 2 matches most of the dictionary.
`FuzzySuggester.for_term` implements that rule and
`test_fuzzy_short_term_does_not_match_everything` asserts the consequence.

One ranking detail worth stating: `FuzzySuggester` sorts by
`(edit_distance, -weight, phrase)` — **correctness before popularity**. Rank by
popularity first and a very common term outranks an exact match, which users read
as the search box ignoring what they typed.

### Reconciliation

Both mechanisms are checked against each other and against the real thing:

- `test_trie_and_edge_ngram_agree_on_suggestions` — the two hand-built
  mechanisms must return identical ranked lists for the same vocabulary.
- `test_reconciliation_completion_suggester_matches_handbuilt_trie` — the
  hand-built trie and **real Elasticsearch's FST-backed `completion` field**
  must agree. Where they disagree, the model here is lying about how a real
  suggester behaves.

---

## 🛠️ 6. Hands-On Lab: Building a Lucene-Style Inverted Index & BM25 Engine

In this lab, you will implement:
1. **Text Analysis Pipeline**: Lowercasing, punctuation stripping, stopword removal, and prefix-suffix stemmer.
2. **Inverted Index & Postings**: Build term dictionaries with document IDs, term frequencies, and positional offsets.
3. **Boolean Query Engine**: Multi-term `AND` and `OR` postings intersections.
4. **Exact BM25 Relevance Scorer**: Compute corpus-wide IDF, document length normalization ($b=0.75$), and TF saturation ($k_1=1.2$).
5. **Two-Phase Query-Then-Fetch Distributed Simulator**: Partition documents across shards and aggregate top-K relevance results.
6. **CompletionTrie**: Prefix trie with per-node cached top-k, so the broadest prefix costs no more than the narrowest.
7. **EdgeNGramIndex**: The write-time alternative, with its write amplification measured against the trie's node count.
8. **Bounded Levenshtein & FuzzySuggester**: Typo tolerance with a length-scaled distance bound, ranking correctness before popularity.

---

## 📂 Project Structure
```
Module_19_Search_Engines_Elasticsearch_Lucene/
├── README.md
├── 01_inverted_index_and_bm25_demo.py
├── starter/
│   └── search_engine.py
└── project_solution/
    ├── search_engine.py
    └── test_search_engine.py
```

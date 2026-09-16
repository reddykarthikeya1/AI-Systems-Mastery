# Module 04: Beginner Playground - Hybrid Search & Reciprocal Rank Fusion (RRF)

Welcome to **Hybrid Search & RRF**!
If you build a search system with ONLY vector embeddings or ONLY keyword search, your users will quickly encounter catastrophic failures:
- **Vector Search Only**: A user searches for: *"Invoice #INV-2024-9981"*. Vector search has no idea what that string of numbers means, and returns an invoice for office supplies from 2021!
- **Keyword Search Only**: A user searches for: *"How to fix a dripping bathroom faucet"*. A document titled *"Repairing Leaky Plumbing Pipes"* is completely ignored because none of the words match!

How do we combine the brilliance of **Dense Vector Semantic Understanding** with the precision of **Sparse BM25 Keyword Matching**?

---

## 1. The Score Normalization Problem

Suppose Document A gets:
- Vector Cosine Similarity: **$0.82$** (scale is $0.0$ to $1.0$)
- BM25 Score: **$14.5$** (scale is unbounded, $0.0$ to $\infty$)

How can you add $0.82$ and $14.5$? You can't! It's like adding 2 apples and 50 miles per hour!
If you normalize them naively, one query has BM25 scores maxing out at 5.0, while another query maxes out at 40.0!

---

## 2. The Genius of Reciprocal Rank Fusion (RRF)

RRF throws away the arbitrary scores and looks **ONLY at the RANK** ($1^{\text{st}}$ place, $2^{\text{nd}}$ place, $3^{\text{rd}}$ place...):

$$RRF(d) = \sum_{m \in \{\text{Dense}, \text{Sparse}\}} \frac{1}{k + \text{rank}_m(d)}$$

Where $k = 60$ is a standard smoothing constant.
- If Document A is #1 in Vector search and #1 in BM25:
  $$RRF = \frac{1}{60 + 1} + \frac{1}{60 + 1} = \frac{2}{61} \approx 0.0328$$
- If Document B is #1 in Vector search but not even in the top 100 for BM25:
  $$RRF = \frac{1}{60 + 1} + 0 = 0.0164$$

Documents that perform well across **both channels** rocket to the top, giving you bulletproof search quality!

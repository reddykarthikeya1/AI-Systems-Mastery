# Module Troubleshooting & Production Edge Cases: Module_16_Social_Media_Newsfeed_Recommendation_TwoTower

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Pagination Duplication on Fast-Moving Feeds

### 🚨 The Bug & Symptoms
Offset-based pagination (`OFFSET 20 LIMIT 10`) skips or duplicates posts when new posts are published while user scrolls.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use cursor-based pagination (`WHERE post_id < last_seen_post_id LIMIT 10`).

---

## 2. Two-Tower Embedding Drift

### 🚨 The Bug & Symptoms
Serving user recommendations using model embeddings that have not been re-normalized causes dot-product scores to distort.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Normalize feature vectors to unit length ($\|v\| = 1$) so dot product equals cosine similarity.

---

## 3. Timeline Cache Memory Exhaustion

### 🚨 The Bug & Symptoms
Caching entire infinite feeds for all registered users wastes expensive RAM on dormant accounts.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Only cache the top 800 post IDs for Daily Active Users (DAU); evict inactive users after 3 days.

---


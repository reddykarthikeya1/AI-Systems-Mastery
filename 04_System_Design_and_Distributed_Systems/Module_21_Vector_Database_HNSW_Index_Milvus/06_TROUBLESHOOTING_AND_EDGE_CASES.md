# Module Troubleshooting & Production Edge Cases: Module_21_Vector_Database_HNSW_Index_Milvus

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Dimensionality Mismatch in Cosine Distance

### 🚨 The Bug & Symptoms
Comparing a 768-dim query embedding with 1536-dim indexed vectors causes shape errors or garbage similarity scores.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Validate `len(vec_a) == len(vec_b)` on every vector ingestion and query.

---

## 2. Scalar Quantization (SQ8) Overflow

### 🚨 The Bug & Symptoms
Normalizing vectors with extreme outliers causes non-outlier coordinates to compress into the same integer bin, destroying precision.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use percentile-based clipping (e.g. 1st and 99th percentiles) rather than absolute min/max.

---

## 3. Graph Traversal efSearch Undersizing

### 🚨 The Bug & Symptoms
Setting `efSearch` too low (e.g. `ef=10`) gives blazing fast latency but recall drops below 70%.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Benchmark recall vs latency curves; tune `efSearch` dynamically based on application requirements.

---


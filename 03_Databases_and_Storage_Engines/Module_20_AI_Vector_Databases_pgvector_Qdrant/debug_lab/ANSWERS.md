# Debug Lab: Forensic Analysis & Solution

## Incident: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors

### 🔍 Root Cause Analysis
Embeddings inserted with arbitrary magnitudes while index was configured for Dot Product, causing vectors with huge norms to dominate similarity scores regardless of direction.

### 🛠️ The Fix
Normalize all vector embeddings to unit length ($L_2$ norm = 1.0) before insertion: `v = v / np.linalg.norm(v)`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.

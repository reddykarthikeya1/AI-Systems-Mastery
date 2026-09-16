# Module 03: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Memory Budgeting for 100 Million Vectors (1536-dim)
**Question**: Calculate the physical RAM required to host an HNSW index of 100,000,000 vectors of dimension $D=1,536$ in FP32 with $M=32$ edges per node. How does Product Quantization (PQ) alter this budget?

**Solution**:
1. **Raw Vector Memory**:
   $$\text{Vector RAM} = 10^8 \times 1536 \times 4 \text{ bytes} = 6.144 \times 10^{11} \text{ bytes} = 614.4 \text{ GB}$$
2. **HNSW Graph Topology Overhead**:
   Each node stores on average $M=32$ edges. In 64-bit integer IDs ($8 \text{ bytes}$ per pointer):
   $$\text{Graph RAM} = 10^8 \times 32 \times 8 \text{ bytes} = 25.6 \times 10^{10} \text{ bytes} = 256 \text{ GB}$$
   $$\text{Total Unquantized Memory} = 614.4 + 256 \approx 870 \text{ GB}$$
3. **With Product Quantization (PQ64)**:
   Compress 1536-dim vector into 64 bytes (using 64 sub-vectors with 8-bit codebooks):
   $$\text{Quantized Vector RAM} = 10^8 \times 64 \text{ bytes} = 6.4 \text{ GB}$$
   Total RAM with graph drops to $\approx 262 \text{ GB}$ (a $3.3\times$ reduction)!

---

### Scenario 2: Index Degradation Under Streaming Deletions
**Question**: Why do soft deletions (tombstones) degrade HNSW recall over time, and what maintenance operation is required?

**Solution**:
HNSW routing depends on graph connectivity. When nodes are tombstoned without edge reconstruction, navigation paths are severed, stranding subgraphs into unreachable islands.
To maintain $> 95\%$ recall, the database must trigger periodic background graph consolidation (edge rewiring) or rebuild the index.

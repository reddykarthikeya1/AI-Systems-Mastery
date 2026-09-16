# Module 08: Beginner Playground - 3D Parallelism Integration

Welcome to **3D Parallelism**!
You now possess the three master keys to distributed AI:
1. **DP (Data Parallelism)**: Replicate model, shard data.
2. **TP (Tensor Parallelism)**: Shard layers inside a single GPU server over NVLink.
3. **PP (Pipeline Parallelism)**: Shard layers across servers in a pipeline line over InfiniBand.

When you assemble all three, you create a **3D Parallelism Grid** capable of training trillions of parameters across thousands of GPUs!

---

## 1. The 3D Coordinate Grid

Think of a cluster of 64 GPUs as a 3D Rubik's cube:
- **TP dimension**: $TP = 4$
- **PP dimension**: $PP = 2$
- **DP dimension**: $DP = 8$
$$\text{Total GPUs} = TP \times PP \times DP = 4 \times 2 \times 8 = 64 \text{ GPUs}$$

Every single GPU has a unique 3D coordinate $(r_{\text{tp}}, r_{\text{pp}}, r_{\text{dp}})$.

### The Golden Rule of Hardware Placement
- **Tensor Parallel (TP)**: Must ALWAYS sit on the **fastest, ultra-low latency NVLink wires** ($TP \le 8$ inside 1 node).
- **Pipeline Parallel (PP)**: Can cross node boundaries because it only transmits small activation tensors between adjacent stages.
- **Data Parallel (DP)**: Can scale across the entire data center!

---

## 2. Interactive Calculator: Where Does the Memory Go?

For a 175B model (like GPT-3):
- Total static memory $\approx 2,800 \text{ GB}$.
- With $TP=8$ and $PP=8$, the model is partitioned into $8 \times 8 = 64$ pieces!
- Each GPU stores only $\frac{2800}{64} = 43.75 \text{ GB}$!
- It fits comfortably on an 80 GB A100/H100 with plenty of room for activations!

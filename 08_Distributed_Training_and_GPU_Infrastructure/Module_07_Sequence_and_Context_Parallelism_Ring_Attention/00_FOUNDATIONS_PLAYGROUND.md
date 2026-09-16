# Module 07: Beginner Playground - Sequence & Context Parallelism (Ring Attention)


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Sequence & Context Parallelism**!
Modern LLMs are expected to read entire books, codebases, or hours of video in a single prompt (128,000 to 1,000,000+ tokens).
Why is this mathematically brutal on GPUs, and how does **Ring Attention** conquer it?

---

## 1. The Million-Token Quadratic Disaster

Standard Self-Attention computes:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V$$

If your sequence length $S = 1,000,000$ tokens:
- $Q K^T$ is a matrix of size $1,000,000 \times 1,000,000 = 10^{12}$ values!
- In FP16 ($2$ bytes), this single attention matrix requires **2 Terabytes of VRAM** for just 1 head!

Even with FlashAttention (which computes attention in small tiles inside fast SRAM without materializing the $S \times S$ matrix in HBM), what happens when **$Q, K, V$ themselves exceed GPU memory**?
A sequence of 1M tokens with hidden size 8192 takes $\approx 16 \text{ GB}$ just to store the token embeddings!

---

## 2. The Ring Attention Round-Robin Analogy

Suppose 4 students (GPUs 0, 1, 2, 3) sit in a circle.
A 128,000-word book is cut into 4 equal quarters of 32,000 words:
- Student 0 holds Words $0 - 32\text{k}$ ($Q_0, K_0, V_0$)
- Student 1 holds Words $32\text{k} - 64\text{k}$ ($Q_1, K_1, V_1$)
- Student 2 holds Words $64\text{k} - 96\text{k}$ ($Q_2, K_2, V_2$)
- Student 3 holds Words $96\text{k} - 128\text{k}$ ($Q_3, K_3, V_3$)

How can Student 0 compare their questions ($Q_0$) with all words in the book without moving everything to one student?

```
Step 0: Each student computes attention with their OWN K and V.
Student 0: Q0 vs (K0, V0)
Student 1: Q1 vs (K1, V1)
Student 2: Q2 vs (K2, V2)
Student 3: Q3 vs (K3, V3)

Step 1: Pass K and V to neighbor on the right!
Student 0: Q0 vs (K3, V3)  [received from Student 3]
Student 1: Q1 vs (K0, V0)  [received from Student 0]
Student 2: Q2 vs (K1, V1)  [received from Student 1]
Student 3: Q3 vs (K2, V2)  [received from Student 2]

Step 2 & 3: Keep passing around the ring until full circle!
```

### The Secret Superpower: 100% Compute & Communication Overlap!
While Student 0 is multiplying $Q_0$ by $K_3$, in the background the GPU's copy engine is **already receiving $K_2$ from Student 3**!
Because the attention computation takes milliseconds, the network transmission completes completely in the background!
**Communication overhead is effectively ZERO!**

---

## 3. DeepSpeed Ulysses vs. Ring Attention

| Feature | DeepSpeed Ulysses | Ring Attention |
| :--- | :--- | :--- |
| **Mechanism** | All-to-All sequence/head transpose | Circular P2P Ring communication |
| **Max Sequence Parallel Size** | Limited by number of Attention Heads ($H$) | **Virtually unlimited** (can exceed $H$) |
| **Network Sensitivity** | Requires high All-to-All bisection bandwidth | High latency tolerance (P2P overlap) |
| **Best Used For** | Sequences up to $64\text{k}-128\text{k}$ intra-cluster | Extreme contexts ($512\text{k}$ to $10\text{M}+$ tokens) |

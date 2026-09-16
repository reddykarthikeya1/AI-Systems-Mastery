# Module 01: Beginner Playground - Inference Latency & Throughput Trade-offs

Welcome to **LLM Inference Systems**!
Training a model happens once, but **inference happens billions of times a day**.
Serving Large Language Models is fundamentally different from serving traditional web APIs or standard convolutional networks.

Let's understand why LLMs behave so strangely during generation!

---

## 1. The Restaurant Waiting Analogy: TTFT vs. TPOT

When you visit a restaurant:
1. **Time-to-First-Token (TTFT)**: The time between placing your order and the waiter bringing you warm bread.
   - If this takes 10 seconds, you get impatient and think the kitchen is broken.
   - In AI: This is the **Prefill Phase** where the model processes your entire prompt.
2. **Time-Per-Output-Token (TPOT)**: The pace at which subsequent courses arrive.
   - If courses arrive at a steady, enjoyable pace, the experience is great.
   - In AI: This is the **Decode Phase** where the model generates words one by one. Humans read at $\approx 5$ words per second. If TPOT is $\le 25\text{ ms}$ ($40$ tokens/sec), the text streams faster than you can read!

---

## 2. The Two Faces of LLM Serving

An LLM request consists of two completely different computational worlds:

```
+-------------------------------------------------------------------------------+
| PHASE 1: PREFILL (Prompt Processing)                                          |
| - All prompt tokens processed AT ONCE                                         |
| - Matrix-Matrix Multiplications (GEMM)                                        |
| - COMPUTE-BOUND: Saturates GPU Tensor Cores (TFLOPs)                          |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2: DECODE (Token Generation)                                            |
| - One token generated AT A TIME                                               |
| - Matrix-Vector Multiplications (GEMV)                                        |
| - MEMORY-BANDWIDTH BOUND: GPU sits idle waiting for memory transfer (TB/s)   |
+-------------------------------------------------------------------------------+
```

---

## 3. Why GPUs Run at < 1% Efficiency During Decoding

When generating a single token for a 70B parameter model:
- The GPU must load **all 140 Gigabytes of model weights** from HBM (High Bandwidth Memory) into the processor cores just to generate **ONE single token**!
- On an NVIDIA H100 with $3.35 \text{ TB/s}$ memory bandwidth:
  $$\text{Min Time to Stream Weights} = \frac{140 \text{ GB}}{3,350 \text{ GB/s}} \approx 41.8 \text{ ms}$$
  $$\text{Max Generation Speed} \approx \frac{1}{0.0418} \approx 24 \text{ tokens/second}$$
- Notice that this speed limit has **nothing to do with the 989 TFLOPs tensor cores**! The compute units are literally sitting idle 99% of the time, waiting for weights to travel over the memory bus.

To fix this, we must **batch requests together** so that loading 140 GB serves 32 or 64 tokens at once!

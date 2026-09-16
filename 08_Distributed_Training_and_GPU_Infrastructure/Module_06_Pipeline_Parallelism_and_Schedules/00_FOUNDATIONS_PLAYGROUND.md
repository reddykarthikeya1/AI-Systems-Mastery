# Module 06: Beginner Playground - Pipeline Parallelism & Schedules

Welcome to **Pipeline Parallelism (PP)**!
If your model has **96 layers** (like GPT-3 175B), even with Tensor Parallelism across 8 GPUs on one machine, the model is still too massive.
How do you split a model **across different machines**?

---

## 1. The Car Assembly Line Analogy

Imagine building a car requires 4 sequential steps:
1. **Station 0**: Chassis Assembly
2. **Station 1**: Engine Installation
3. **Station 2**: Painting
4. **Station 3**: Wheels & Inspection

### The Naive Mistake (Batch Execution)
If you bring a batch of 8 cars to Station 0, build all 8 chassis, then move them to Station 1...
While Station 1 installs engines, **Station 0, 2, and 3 are sitting completely idle!**
When Station 3 puts on wheels, Stations 0, 1, and 2 are idle!
This idle time is called the **Pipeline Bubble ($F_{\text{bubble}}$)**.

### The Pipeline Solution: Micro-batches!
Instead of processing all 8 cars at once, process **1 car at a time**!
- As soon as Car 1 moves from Chassis to Engine, Station 0 immediately starts on Car 2!
- In steady state, **all 4 stations are working on different cars simultaneously**!

---

## 2. GPipe vs. 1F1B (One Forward, One Backward)

```
GPipe Schedule (All Forwards, Then All Backwards):
GPU 0: [F1][F2][F3][F4]                [B4][B3][B2][B1]
GPU 1:     [F1][F2][F3][F4]        [B4][B3][B2][B1]
GPU 2:         [F1][F2][F3][F4][B4][B3][B2][B1]
   Time ----------------------------------------->
```

### The Problem with GPipe: Peak Memory Explosion!
In GPipe, GPU 0 must hold the activation memory for **all micro-batches** (F1, F2, F3, F4) in VRAM until B1 finally arrives! If you have 32 micro-batches, your GPU crashes with OOM.

### The 1F1B Schedule Solution:
In **1F1B** (used by DeepSpeed and Megatron-LM), once the pipeline warms up, each GPU executes **one forward micro-batch, followed by one backward micro-batch**:
```
1F1B Schedule:
GPU 0: [F1][F2][F3][F4][B1][F5][B2][F6][B3]...
```
Peak memory on GPU 0 is capped at **$p$ micro-batches** (number of pipeline stages), no matter how many total micro-batches you run!

---

## 3. The Math of the Pipeline Bubble

Let $p$ be the number of pipeline stages (GPUs), and $m$ be the number of micro-batches.
The fraction of time GPUs spend idle is:
$$F_{\text{bubble}} = \frac{p - 1}{m + p - 1}$$

- If $p = 8$ and $m = 8$: $F_{\text{bubble}} = \frac{7}{15} \approx 46.7\%$ wasted time!
- If $p = 8$ and $m = 64$: $F_{\text{bubble}} = \frac{7}{71} \approx 9.8\%$ wasted time!

To keep bubble overhead $< 10\%$, you must set $m \ge 4p$.

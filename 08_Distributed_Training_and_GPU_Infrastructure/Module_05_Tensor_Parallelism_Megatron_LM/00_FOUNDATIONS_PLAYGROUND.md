# Module 05: Beginner Playground - Tensor Parallelism (Megatron-LM)


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Tensor Parallelism (TP)**!
In the previous module, we learned that ZeRO-3 and FSDP partition static weights across GPUs.
But what if a **single individual layer or matrix multiplication** is so giant that it doesn't fit in GPU memory during execution, or what if we want to run inference/training with ultra-low latency?

Enter **Megatron-LM Tensor Parallelism**!

---

## 1. What is Tensor Parallelism?

In Data Parallelism, we split the **batch** (different GPUs process different sentences).
In Tensor Parallelism, we split the **weights of a single layer across GPUs** (different GPUs compute different parts of the same matrix multiplication for the **same sentence**)!

### The Matrix Multiplication Problem: $Y = X \cdot W$
Suppose $X$ has dimension $[B, H]$ and weight matrix $W$ has dimension $[H, 4H]$ (standard MLP expansion layer).
How can we split $W$ across 2 GPUs?

There are two fundamental ways to split a matrix:
1. **Column Parallel**: Split $W$ vertically into $[W_1, W_2]$
2. **Row Parallel**: Split $W$ horizontally into $\begin{bmatrix} W_1 \\ W_2 \end{bmatrix}$

---

## 2. Megatron-LM's Genius Insight: Column + Row

In a standard Transformer MLP, we have two linear layers with a GeLU activation in between:
$$Y = \text{GeLU}(X \cdot W_1) \cdot W_2$$

If we do this naively, we'd need expensive communication between every operation.
Megatron-LM pairs **Column Parallel** with **Row Parallel**:

```
Input X
   |-----------------------------|
   | (Broadcast X to both GPUs)  |
   v                             v
[GPU 0: W1_col1]             [GPU 1: W1_col2]   <-- Column Parallel (No comms!)
   |                             |
 GeLU                          GeLU
   |                             |
[GPU 0: W2_row1]             [GPU 1: W2_row2]   <-- Row Parallel
   |-----------------------------|
                 v
            [All-Reduce]                        <-- ONLY ONE COMMUNICATION!
                 v
              Output Y
```

### Why is this brilliant?
- **Column Parallel Linear**: $X$ is multiplied by each column slice independently. Because GeLU is element-wise, $\text{GeLU}([Y_1, Y_2]) = [\text{GeLU}(Y_1), \text{GeLU}(Y_2)]$. **Zero communication needed!**
- **Row Parallel Linear**: Each GPU multiplies its GeLU output with its row slice of $W_2$. The partial sums are summed across ranks via **one single `All-Reduce`**!
- In an entire MLP block, there is **only ONE `All-Reduce` in the forward pass** and **only ONE `All-Reduce` in the backward pass**!

---

## 3. When Should You Use Tensor Parallelism?

> [!WARNING]
> Tensor Parallelism requires communication on **every single layer** of the neural network.
> Because communication happens thousands of times per forward pass, it requires **microsecond latency**.
> **Rule of Thumb**: TP degree ($TP$) should almost always be $\le 8$ and contained within a **single physical node connected by NVLink/NVSwitch**! Never run TP across standard Ethernet!

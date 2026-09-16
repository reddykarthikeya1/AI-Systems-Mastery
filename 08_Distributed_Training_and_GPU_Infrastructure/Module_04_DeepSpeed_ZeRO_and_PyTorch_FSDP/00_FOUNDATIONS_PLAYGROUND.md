# Module 04: Beginner Playground - DeepSpeed ZeRO & PyTorch FSDP


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **ZeRO** (Zero Redundancy Optimizer) and **FSDP** (Fully Sharded Data Parallel)! If you've ever tried training a modern Large Language Model (LLM) and hit the dreaded `torch.cuda.OutOfMemoryError: CUDA out of memory`, this module is your cure.

---

## 1. The Real-World Memory Crisis

Imagine you have a **70 Billion parameter** model.
In half-precision (FP16 or BF16), each parameter takes **2 bytes**.
So just the weights take:
$$70 \times 10^9 \times 2 \text{ bytes} = 140 \text{ GB}$$

Can you train this on an NVIDIA A100 (80 GB GPU)?
You might think: *"If I get two 80 GB GPUs ($2 \times 80 = 160 \text{ GB}$), can I train it?"*
**NO! You cannot even train a 14B model on one 80 GB GPU!**

Why? Because training requires **far more than just model weights**:
1. **Model Weights (FP16)**: $2\Phi$ bytes ($140$ GB)
2. **Gradients (FP16)**: $2\Phi$ bytes ($140$ GB)
3. **Adam Optimizer States (FP32)**:
   - FP32 copy of weights (master weights): $4\Phi$ bytes ($280$ GB)
   - Momentum (first moment): $4\Phi$ bytes ($280$ GB)
   - Variance (second moment): $4\Phi$ bytes ($280$ GB)
   - **Total Optimizer State = $12\Phi$ bytes ($840$ GB)!**

$$\text{Total Static Memory} = 2\Phi + 2\Phi + 12\Phi = 16\Phi \text{ bytes} = 1,120 \text{ GB}!$$

In traditional DDP (Distributed Data Parallel), **every single GPU stores all 1,120 GB**. That is $100\%$ redundancy!

---

## 2. The Library Analogy: What is ZeRO?

Imagine 8 students are studying for a giant exam using an encyclopedia of 8 volumes ($1,120$ pages total).

- **Standard DDP (Replication)**: Every student buys their own copy of all 8 volumes. They need huge bookshelves. Redundancy is $8\times$.
- **ZeRO Stage 1 (Partition Optimizer States)**:
  Student 0 tracks the study notes (optimizer states) for Volume 1.
  Student 1 tracks notes for Volume 2...
  Memory drops by $4\times$ to $8\times$! No communication overhead during forward or backward pass!
- **ZeRO Stage 2 (Partition Optimizer States + Gradients)**:
  Students also share gradient tracking. As soon as Student 0 computes a gradient for Volume 2, they hand it to Student 1 and forget it!
- **ZeRO Stage 3 / PyTorch FSDP (Partition Weights + Gradients + Optimizer)**:
  Nobody keeps the full encyclopedia on their desk.
  Each student keeps only 1 volume.
  When Student 0 needs to read Volume 2 to solve a question:
  1. Student 0 asks Student 1 for Volume 2 (`All-Gather`).
  2. Student 0 does the math.
  3. Student 0 **shreds** Volume 2 immediately (`Discard`)!
  Static memory per GPU drops by an exact factor of $N$ (world size)!

---

## 3. Interactive Comparison Matrix

| Feature | Standard DDP | ZeRO-1 | ZeRO-2 | ZeRO-3 / PyTorch FSDP |
| :--- | :--- | :--- | :--- | :--- |
| **Optimizer States** | Replicated on all GPUs | Sharded ($1/N$) | Sharded ($1/N$) | Sharded ($1/N$) |
| **Gradients** | Replicated on all GPUs | Replicated | Sharded ($1/N$) | Sharded ($1/N$) |
| **Model Weights** | Replicated on all GPUs | Replicated | Replicated | Sharded ($1/N$) |
| **Communication Volume** | $2\Phi$ (All-Reduce) | $2\Phi$ (All-Reduce) | $2\Phi$ (Reduce-Scatter) | $3\Phi$ ($1.5\times$ DDP) |
| **Max Model on 8x 80GB** | ~13B params | ~20B params | ~30B params | **120B+ params** |

---

## 4. PyTorch FSDP in 5 Lines of Code

PyTorch provides native ZeRO-3 via `FullyShardedDataParallel` (FSDP):

```python
import torch
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.fully_sharded_data_parallel import ShardingStrategy

# Wrap model with FSDP
model = MyTransformerModel().cuda()
sharded_model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD, # ZeRO-3
    auto_wrap_policy=my_transformer_layer_wrap_policy, # Shard layer by layer
)

# Standard training loop remains identical!
optimizer = torch.optim.AdamW(sharded_model.parameters(), lr=1e-4)
out = sharded_model(inputs)
loss = criterion(out, targets)
loss.backward()
optimizer.step()
```

Let's dive into the production implementation and exact mathematical derivation in the next chapters!

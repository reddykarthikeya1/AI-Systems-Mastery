# Module 06: Pipeline Parallelism & Schedules (GPipe, 1F1B, Interleaved, Zero-Bubble)

> **Architectural Scope**: Layer partitioning across stages, micro-batching, the pipeline bubble, GPipe vs 1F1B schedules, interleaved virtual stages, zero-bubble ideas, and point-to-point communication.

---

## Why this module matters

Tensor parallelism (Module 05) is bandwidth-hungry and confined to a node. To go beyond a node, you need a way to split a model that only sends small amounts of data across the slower network. **Pipeline parallelism (PP)** splits the model **by layers**: GPU group 1 holds layers 1 to 8, group 2 holds layers 9 to 16, and so on. Only the **activations at stage boundaries** cross the wire, one point-to-point message per micro-batch. The price is the **pipeline bubble**: idle time while the pipeline fills and drains. Understanding the schedule (GPipe, 1F1B, interleaved, zero-bubble) is understanding how to keep that price low.

## Mental model: an assembly line for micro-batches

A car factory with 4 stations. If you send one car through, three stations are idle at any time. Send a stream of cars and every station is busy once the line is full. Pipeline parallelism cuts the batch into **micro-batches** (the cars) so all stages work at the same time on different micro-batches.

```mermaid
flowchart LR
    MB["Global batch cut into m micro-batches"] --> S1["Stage 1: layers 1-8"]
    S1 -->|"activations (b x s x h)"| S2["Stage 2: layers 9-16"]
    S2 -->|"activations"| S3["Stage 3: layers 17-24"]
    S3 -->|"activations"| S4["Stage 4: layers 25-32 + loss"]
    S4 -.->|"gradients flow back the same way"| S3
```

## 1. The bubble

Let `p` = number of stages, `m` = micro-batches per step, and assume equal forward and backward times per stage. The pipeline needs `p - 1` time slots to fill and `p - 1` to drain, so

- **Idle ("bubble") fraction of total time** `= (p - 1) / (m + p - 1)`.
- **Extra time relative to ideal compute** `= (p - 1) / m`.

| `p` | `m` | Bubble fraction of total | Extra vs ideal |
|---|---|---|---|
| 4 | 4 | 3/7 = 43% | 75% |
| 4 | 8 | 3/11 = 27% | 37.5% |
| 4 | 32 | 3/35 = 8.6% | 9.4% |
| 8 | 64 | 7/71 = 9.9% | 10.9% |

Rule of thumb: use `m >= 4p` micro-batches. But more micro-batches means a smaller micro-batch size (lower GPU efficiency) or a larger global batch (which may hurt convergence). That tension drives schedule design.

## 2. GPipe: all forwards, then all backwards

GPipe runs the forward pass of **all** `m` micro-batches through the pipeline, then all backward passes. Simple, and the bubble is the formula above. But each stage must **keep the activations of all `m` micro-batches** until backward starts: memory grows with `m`. Activation checkpointing (recompute per stage) reduces this at a ~33% compute cost.

## 3. 1F1B: one forward, one backward

The **1F1B** schedule (PipeDream-Flush, used by Megatron-LM) has three phases per stage:

1. **Warm-up:** stage `i` runs forwards for `p - i` micro-batches to fill the pipeline.
2. **Steady state:** each stage alternates **one forward, one backward**, so as soon as a micro-batch's backward is done, its activations are freed.
3. **Cool-down:** the remaining backwards drain.

The **bubble is the same** as GPipe, but peak activation memory is bounded by about `p` micro-batches (not `m`), so you can increase `m` to shrink the bubble without running out of memory. This is why 1F1B is the standard default.

```
Stage 1: F1 F2 F3 F4 B1 F5 B2 F6 B3 F7 B4 F8 B5 .. B8
Stage 2:    F1 F2 F3 B1 F4 B2 F5 B3 F6 B4 F7 B5 ..  B8
Stage 3:       F1 F2 B1 F3 B2 F4 B3 F5 B4 F6 ..     B8
Stage 4:          F1 B1 F2 B2 F3 B3 F4 B4 ..        B8
```

## 4. Interleaved 1F1B (virtual stages)

Instead of giving each GPU one contiguous block of layers, give it `v` smaller non-contiguous chunks (for example GPU 0 gets layers 1 to 2 and 9 to 10). The pipeline now has `p x v` *virtual* stages and each micro-batch visits each GPU `v` times. The bubble shrinks by a factor of `v`:

`extra vs ideal = (p - 1) / (v x m)`

With `p = 4`, `m = 8`, `v = 2`: `3 / 16 = 18.75%` instead of 37.5%. The cost is **`v` times more point-to-point communication** (activations cross GPU boundaries `v` times as often) and more complex scheduling, so it is attractive when the network is fast relative to compute and `m` cannot grow.

## 5. Zero-bubble and bidirectional schedules

The backward pass has two independent parts: **B** (gradient with respect to *activations*, needed by the previous stage right away) and **W** (gradient with respect to *weights*, needed only before the optimizer step). **Zero-bubble pipeline parallelism** (Qi et al., 2023) splits them and schedules W into what would be bubble time (variants ZB-H1, ZB-H2, ZB-V), approaching zero bubble at the cost of extra activation memory and scheduling complexity. **DualPipe** (DeepSeek-V3) feeds micro-batches from both ends of the pipeline simultaneously to overlap communication with computation, particularly useful with MoE all-to-alls. These are advanced; know the idea: *fill the bubbles with work that has no dependency.*

## 6. Practicalities

- **Partitioning must balance stage time**, not layer count. The embedding and the LM head/loss are heavy, so first and last stages usually get fewer transformer layers. Profile and rebalance; the slowest stage sets the pace.
- **Communication** is point-to-point (`send`/`recv`, NCCL P2P) of a tensor `b x s x h` per micro-batch per boundary: for `h = 8192`, 8,192 tokens, BF16 that is 128 MiB, about 2.7 ms over a 50 GB/s link, which overlaps with other micro-batches' compute. Compare with TP's critical-path all-reduces.
- **Memory:** weights per stage are `1/p` of the model; activation memory depends on the schedule (GPipe `~m`, 1F1B `~p` micro-batches).
- **Batch norm and cross-micro-batch state** need care (use LayerNorm/RMSNorm; transformers are fine).
- **Tooling:** `torch.distributed.pipelining` (PyTorch), Megatron-Core, DeepSpeed's `PipelineModule`, and schedule classes such as `ScheduleGPipe` and `Schedule1F1B`.

## Worked example: choosing `m`

A 70B model over `p = 8` stages (across 8 nodes). Global batch 1,024 sequences. With data-parallel degree 4, each pipeline sees 256 sequences per step. Micro-batch size 2 gives `m = 128`. Extra vs ideal `= 7 / 128 = 5.5%` for 1F1B: acceptable. If memory forced a micro-batch of 8 (`m = 32`), the extra would be `7 / 32 = 22%`, and interleaving with `v = 2` would reduce it to about 11%, at twice the P2P messages. Meanwhile 1F1B keeps at most about 8 micro-batches of activations alive per stage, versus 128 under GPipe.

## Common pitfalls

1. **Too few micro-batches** (`m < p`): the bubble dominates.
2. **Unbalanced stages**: one slow stage (often the last, with loss and LM head) stalls everyone.
3. **Treating the bubble formula as exact**: real forward/backward times differ and communication adds skew.
4. **Putting PP inside a node and TP across nodes**, the reverse of the efficient arrangement.
5. **Deadlocks from mismatched send/recv ordering** between stages.
6. **Forgetting that the loss lives on the last stage** (and any tied embeddings need a gradient sync between the first and last stage).

## How this connects

- **Module 05** (TP within node) and **Module 04** (sharding across DP) combine with PP in **Module 08**.
- **Module 01**: PP is the strategy whose traffic suits the slower inter-node fabric.
- **Course 09**: pipeline stages also appear in multi-node inference, with micro-batching of requests.

## Go further

- roadmap.sh: *Inference Engineering* nodes **pipeline parallelism**, **model parallelism**.
- Huang et al., *GPipe* (2019); Narayanan et al., *PipeDream* (2019) and *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM* (2021, interleaved 1F1B); Qi et al., *Zero Bubble Pipeline Parallelism* (2023).
- PyTorch `torch.distributed.pipelining` documentation; DeepSpeed pipeline tutorial.

---

## Module Study Progression
1. **Beginner Playground**: Read [00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).

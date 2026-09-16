# Module 09: Beginner Playground - Distributed Checkpointing (DCP)

Welcome to **Distributed Checkpointing (DCP)**!
When you train an AI model across 4,096 GPUs for several weeks, things **will** break:
- GPUs suffer hardware ECC memory faults.
- Cables get loose.
- Power supplies surge.
- Mean Time Between Failures (MTBF) on huge clusters can be **under 24 hours**!

If your checkpointing system is slow or clumsy, you will lose weeks of training progress and hundreds of thousands of dollars!

---

## 1. Why `torch.save(model.state_dict())` Fails Horribly

If you have an 800 GB model and do standard PyTorch saving:
1. **Rank 0 Host OOM**: All 800 GB must be gathered into Rank 0's CPU memory. The host crashes instantly with Out-Of-Memory.
2. **Network Bottleneck**: Rank 0 sends 800 GB over a single network card. It takes 45 minutes! During those 45 minutes, all 4,096 GPUs sit idle!

---

## 2. The DCP Breakthrough: Parallel Direct I/O

In **Distributed Checkpointing (PyTorch DCP)**:
- **Every GPU writes its own chunk in parallel** directly to distributed file storage (Lustre / GPFS / Ceph / S3).
- 4,096 GPUs write concurrently $\implies$ Checkpointing finishes in **15 seconds**!
- Only a tiny metadata manifest file is written to describe the global layout.

---

## 3. The Superpower: Arbitrary Resharding!

What if you saved a model on **8 GPUs ($TP=8$)**, but now you want to load it for inference on **2 GPUs ($TP=2$)** or **1 GPU**?

With traditional checkpoints, you would have to write custom concatenation scripts.
With **DCP**, PyTorch automatically reads the global tensor metadata, calculates which chunks belong to which target GPUs, and **reshards the weights automatically on the fly**!

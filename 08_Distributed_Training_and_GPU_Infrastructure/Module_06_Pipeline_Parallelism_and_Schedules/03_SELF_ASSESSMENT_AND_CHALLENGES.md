# Module 06: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Point-to-Point NCCL Deadlock
**Question**: An engineer writes custom P2P communication logic for Pipeline Parallelism:
```python
if rank < world_size - 1:
    dist.send(activation, dst=rank + 1)
if rank > 0:
    dist.recv(activation, src=rank - 1)
```
When running on 4 nodes, all processes freeze instantly on step 0. Explain why this code deadlocks and write the exact deadlock-free communication pattern.

**Solution**:
1. **Root Cause**: In NCCL and standard MPI, `dist.send` is blocking when transfer buffers exceed the internal eager protocol threshold. Rank 0 calls `dist.send` to Rank 1 and blocks waiting for Rank 1 to issue a matching receive. However, Rank 1 begins by executing `if rank < world_size - 1: dist.send(..., dst=2)`! Rank 1 blocks attempting to send to Rank 2 before ever reaching its `recv` call. Every rank in the pipeline is blocked waiting for its downstream peer to receive, creating a circular wait deadlock.
2. **Deadlock-Free Implementation**:
   - Use non-blocking P2P collectives: `dist.isend()` and `dist.irecv()`, followed by `torch.cuda.current_stream().wait_stream(...)`.
   - Alternatively, alternate even/odd ranks or use combined `dist.send_recv()`:
   ```python
   # Deadlock-free P2P exchange
   reqs = []
   if rank % 2 == 0:
       if rank < world_size - 1:
           reqs.append(dist.isend(send_tensor, dst=rank + 1))
       if rank > 0:
           reqs.append(dist.irecv(recv_tensor, src=rank - 1))
   else:
       if rank > 0:
           reqs.append(dist.irecv(recv_tensor, src=rank - 1))
       if rank < world_size - 1:
           reqs.append(dist.isend(send_tensor, dst=rank + 1))
   for req in reqs:
       req.wait()
   ```

---

### Scenario 2: Pipeline Stage Stragglers & Load Imbalance
**Question**: In an 8-stage pipeline running a 70B model, telemetry shows GPU 0 running at 94% memory utilization and taking 120 ms per forward step, while GPUs 1–6 take 85 ms, and GPU 7 takes 135 ms. Why are the boundary stages stragglers, and how should layers be repartitioned?

**Solution**:
1. **Root Cause**:
   - **Stage 0** holds the input token embedding table ($V \times H$). For modern vocabularies ($V=128\text{k}, H=8192$), the embedding weights consume substantial memory and compute.
   - **Stage 7** hosts the final LayerNorm, the output classification head (`lm_head`, another $128\text{k} \times 8192$ matrix), and computes Cross-Entropy loss.
   - Intermediate stages 1–6 only compute standard transformer layers. Allocating an equal number of transformer layers ($L/p$) to all stages causes severe load imbalance; the entire pipeline is throttled to the speed of Stage 7.
2. **Remedy**:
   - Apply **non-uniform layer partitioning**: Allocate fewer transformer layers to Stage 0 and Stage 7. For instance, if $L=32$, assign 3 layers to Stage 0, 4 layers to Stages 1–6, and 3 layers to Stage 7.

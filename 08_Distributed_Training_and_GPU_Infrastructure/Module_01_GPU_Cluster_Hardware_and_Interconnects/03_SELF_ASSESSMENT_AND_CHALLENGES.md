# Self-Assessment & Staff Interview Challenges: Cluster Hardware & Interconnects

## Architectural Interview Scenarios

### Question 1: Rail-Optimized Routing vs Random Oversubscription
**Scenario**: You deploy an 8-way Tensor Parallelism model across 8 nodes (1 GPU per node) instead of placing all 8 Tensor Parallel ranks within a single node. What happens to training throughput?

**Staff-Level Solution**:
Tensor Parallelism requires **2 AllReduce operations per Transformer layer** (one in Attention, one in MLP).
In a 70B parameter model, AllReduce is called thousands of times per forward-backward pass.
- Inside a node over NVLink: Bandwidth is $900 \text{ GB/s}$, latency $\approx 100 \text{ ns}$.
- Across nodes over InfiniBand: Bandwidth is $50 \text{ GB/s}$ ($18\times$ slower), latency $\approx 1.5 \; \mu\text{s}$ ($15\times$ slower).
Placing TP across nodes causes the GPUs to spend **>80% of their time stalled waiting for inter-node network packets**.
Training throughput drops by $5\times$ to $10\times$!
**Architectural Invariant**: Tensor Parallelism dimension must **never exceed the intra-node GPU count** ($TP \le 8$).

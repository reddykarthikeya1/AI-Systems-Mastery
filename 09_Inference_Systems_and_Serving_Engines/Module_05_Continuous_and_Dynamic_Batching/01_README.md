# Module 05: Continuous & Dynamic Iteration-Level Batching

## 1. Algorithmic Principles of Iteration-Level Scheduling

Classical static batching operates at request granularity: a batch of $B$ requests enters execution concurrently and holds GPU resources until the longest request in the batch completes generation.

### 1.1 The Inefficiency of Static Batching
Let sequence length of request $i \in \{1, \dots, B\}$ be $S_i$.
$$\text{Total Wasted Execution Slots} = \sum_{i=1}^B (\max_j S_j - S_i)$$
Because generation length in production exhibits high variance (e.g. short greetings vs full code solutions), static batching achieves $< 40\%$ compute utilization.

### 1.2 Iteration-Level Scheduling (Orca / vLLM)
Iteration-level scheduling executes at step granularity:
1. At step $t$, the execution engine runs one decode forward pass for the active batch $\mathcal{B}_t$.
2. For every sequence $i \in \mathcal{B}_t$:
   - If token $y_{i,t} == \langle\text{eos}\rangle$ or reached $\text{max\_tokens}$, retire sequence $i$ and deallocate physical blocks.
3. The scheduler checks the waiting queue $\mathcal{Q}$:
   - If available KV cache capacity $\ge S_{\text{prompt}}$ for candidate $k \in \mathcal{Q}$, admit candidate $k$ into $\mathcal{B}_{t+1}$.
4. Advance to step $t+1$.

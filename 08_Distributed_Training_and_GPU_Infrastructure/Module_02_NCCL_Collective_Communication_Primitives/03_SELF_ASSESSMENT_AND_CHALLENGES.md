# Self-Assessment & Staff Interview Challenges: Collective Communications

## Architectural Interview Scenarios

### Question 1: Deriving Ring AllReduce Optimality
**Scenario**: Prove why Ring AllReduce transfers $2 \frac{N-1}{N} S$ bytes and why no AllReduce algorithm can transfer fewer bytes on a ring network.

**Staff-Level Solution**:
- In AllReduce, each of the $N$ ranks contributes $S/N$ data that must be combined with data from all other $N-1$ ranks.
- During Scatter-Reduce: Each rank sends $S/N$ bytes in each of $N-1$ steps. Total data sent = $(N-1)(S/N) = \frac{N-1}{N} S$.
- During AllGather: Each rank sends its reduced $S/N$ slice in each of $N-1$ steps. Total data sent = $\frac{N-1}{N} S$.
- Total sent per rank = $2 \frac{N-1}{N} S$.
Because each rank must receive $N-1$ external chunks to complete the reduction, $\frac{N-1}{N} S$ is the information-theoretic lower bound for both reduction and dissemination.

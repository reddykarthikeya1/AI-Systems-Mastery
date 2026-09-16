# Self-Assessment & Staff Interview Challenges: Parallel Reduction & Prefix Sum

## Architectural Interview Scenarios

### Question 1: Block Reduction with Grid-Stride Loop
**Scenario**: You have an array of 100 million elements. How do you design a scalable 2-pass parallel reduction kernel without running out of SM resources?

**Staff-Level Solution**:
1. **Pass 1 (Grid-Stride Block Reduction)**:
   - Launch a fixed grid of blocks (e.g. 512 blocks of 256 threads).
   - Each thread performs a grid-stride loop, accumulating multiple elements into its register (`val += data[idx]`).
   - Intra-block reduction: Threads use sequential addressing in shared memory down to 32 threads, then use `__shfl_down_sync` within warp 0.
   - Thread 0 of each block writes the block partial sum to a global buffer of size 512.
2. **Pass 2 (Final Single-Block Reduction)**:
   - Launch 1 block of 512 threads to reduce the 512 partial sums into the final single scalar.

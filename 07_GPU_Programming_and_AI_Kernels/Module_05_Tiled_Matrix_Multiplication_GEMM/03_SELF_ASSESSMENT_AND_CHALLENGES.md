# Self-Assessment & Staff Interview Challenges: Tiled GEMM

## Architectural Interview Scenarios

### Question 1: Bank Conflicts in Shared Memory Matrix B
**Scenario**: In a tiled GEMM kernel, threads load `sB[k][col]` where `col = threadIdx.x`. Does this cause a bank conflict?

**Staff-Level Solution**:
No! When `col = threadIdx.x` and `threadIdx.x` ranges from 0 to 31 in warp 0:
Thread $i$ accesses `sB[k][i]`.
The 32-bit words are located at consecutive addresses: `base + (k * stride + i) * 4`.
Because consecutive words map to consecutive banks ($0, 1, 2, \dots, 31$), all 32 threads hit **32 distinct banks**.
This access is **100% conflict-free**.
However, transposing $A$ inside shared memory or accessing column-major structures can cause severe conflicts unless padded.

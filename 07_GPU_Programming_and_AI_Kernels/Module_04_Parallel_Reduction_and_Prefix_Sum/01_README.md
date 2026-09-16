# Module 04: Parallel Reduction & Warp Primitives

> **Architectural Scope**: Parallel Tree Reductions, Warp Shuffle Instructions (`__shfl_down_sync`), Blelloch Work-Efficient Parallel Prefix Sum.

---

## 1. Tree-Based Parallel Reduction

Computing the sum, maximum, or norm of an array of $N$ numbers is a fundamental building block of Softmax, LayerNorm, and Loss computations.
On sequential CPUs: $O(N)$ steps.
On parallel GPUs: $O(\log N)$ depth.

```
+---------------------------------------------------------------------------------------------------+
| PARALLEL TREE REDUCTION ACROSS 8 THREADS                                                          |
+---------------------------------------------------------------------------------------------------+
| Input:    [ 3 ]   [ 1 ]   [ 7 ]   [ 0 ]   [ 4 ]   [ 1 ]   [ 6 ]   [ 3 ]                           |
| Step 1:     \      /       \      /       \      /       \      /      (Stride = 4)             |
|           [ 3+4=7 ]       [ 1+1=2 ]       [ 7+6=13]       [ 0+3=3 ]                               |
| Step 2:       \              /               \              /            (Stride = 2)             |
|               [ 7+13=20 ]                     [ 2+3=5 ]                                           |
| Step 3:             \                            /                        (Stride = 1)             |
|                                [ 20+5=25 ]                                                        |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Warp-Level Shuffles (`__shfl_down_sync`)

Before Kepler GPUs, passing data between threads required storing to Shared Memory, followed by a hardware barrier `__syncthreads()`.
The **Warp Shuffle** instruction allows threads in a warp to read registers directly from other threads:

```cpp
template <typename T>
__device__ inline T warp_reduce_sum(T val) {
    #pragma unroll
    for (int offset = 16; offset > 0; offset /= 2) {
        val += __shfl_down_sync(0xFFFFFFFF, val, offset);
    }
    return val; // Thread 0 holds the warp sum
}
```

- **0 bytes of Shared Memory used**.
- **0 clock cycles spent at barriers**.
- **Executed in 1 instruction cycle** per step.

---

## 3. Work-Efficient Parallel Prefix Sum (Blelloch Scan)

A naive parallel scan (Hillis-Steele) requires $O(N \log N)$ operations.
The **Blelloch Algorithm** performs scan in $O(N)$ operations:

1. **Up-Sweep (Reduce Phase)**:
   - Build a binary tree of partial sums from leaves to root.
   - Root becomes the total sum of the array.
2. **Down-Sweep (Distribute Phase)**:
   - Set the root value to 0.
   - At each step down the tree:
     - The left child gets the parent's value.
     - The right child gets the `left_child + parent's_value`.

---

## 4. Module Study Progression
1. **Beginner Playground**: Read [00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).

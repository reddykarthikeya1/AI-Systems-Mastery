# 🐣 W3Schools-Style Playground: Parallel Reduction & Prefix Sum

> *"Adding 1,000 numbers on a CPU takes 1,000 sequential clock ticks. On a GPU, it takes 10 ticks—because 512 pairs of numbers are added at the exact same moment in Round 1, 256 pairs in Round 2, until one champion emerges."*

---

## 1. The Tournament Bracket (Parallel Tree Reduction)

Think of the single-elimination NCAA basketball tournament:
- In Round 1, 64 teams play simultaneously across 32 courts $\to$ 32 winners.
- In Round 2, 32 teams play simultaneously across 16 courts $\to$ 16 winners.
- In Round 6, the final 2 teams play $\to$ 1 champion!
- **Span (Latency)**: $\log_2(64) = 6$ rounds!

---

## 2. Warp Divergence in Reductions & The Sequential Addressing Fix

### The Novice Mistake (Branch Divergence)
```cpp
// BAD: Thread 0, 2, 4, 6 work; Thread 1, 3, 5, 7 sit idle!
// Extreme warp divergence inside every single warp!
for (int s = 1; s < blockDim.x; s *= 2) {
    if (threadIdx.x % (2 * s) == 0) {
        sdata[threadIdx.x] += sdata[threadIdx.x + s];
    }
    __syncthreads();
}
```

### The Senior Engineer Fix (Sequential Addressing)
```cpp
// BRILLIANT: Threads 0 to (s - 1) work; Threads s to 255 idle!
// Consecutive warps execute. Zero divergence until stride < 32!
for (int s = blockDim.x / 2; s > 0; s >>= 1) {
    if (threadIdx.x < s) {
        sdata[threadIdx.x] += sdata[threadIdx.x + s];
    }
    __syncthreads();
}
```

---

## 3. Warp Shuffle (`__shfl_down_sync`): Zero Shared Memory, Zero Barriers!

When your tree reduction reaches the last 32 threads (1 single warp), you can stop using shared memory and `__syncthreads()` entirely!
Modern NVIDIA GPUs have **Warp Shuffle** hardware instructions:
```cpp
// Thread i directly reads register from Thread (i + offset)!
val += __shfl_down_sync(0xFFFFFFFF, val, 16);
val += __shfl_down_sync(0xFFFFFFFF, val, 8);
val += __shfl_down_sync(0xFFFFFFFF, val, 4);
val += __shfl_down_sync(0xFFFFFFFF, val, 2);
val += __shfl_down_sync(0xFFFFFFFF, val, 1);
// Now Thread 0 holds the total sum of all 32 threads in its register!
```
- **Latency**: ~1 clock cycle!
- **SRAM Footprint**: 0 bytes of shared memory used!

---

## 4. Parallel Scan (Prefix Sum): Blelloch Work-Efficient Algorithm

Given array `[3, 1, 7, 0, 4, 1, 6, 3]`:
- **Inclusive Scan**: `[3, 4, 11, 11, 15, 16, 22, 25]`
- **Exclusive Scan**: `[0, 3, 4, 11, 11, 15, 16, 22]`

### Blelloch 2-Pass Tree:
1. **Up-Sweep (Reduce)**: Build partial sums up the binary tree. Root becomes sum.
2. **Down-Sweep (Distribute)**: Set root to 0. At each node, pass left child to right, and right child gets `left + old_parent`.
- Total Work: $O(N)$ operations (work-efficient)!
- Depth: $2 \log_2 N$ steps!

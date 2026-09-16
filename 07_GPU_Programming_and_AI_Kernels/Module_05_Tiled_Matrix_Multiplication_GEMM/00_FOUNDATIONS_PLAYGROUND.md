# 🐣 Interactive Foundations Playground: Tiled Matrix Multiplication (GEMM)

> *"In naive matrix multiplication, computing a $4096 \times 4096$ matrix reads 68 billion numbers from slow DRAM. Tiling loads small square blocks into fast shared memory, letting threads reuse each number 32 times—turning a slow crawl into blistering speed."*

---

## 1. The Naive GEMM Memory Bottleneck

To compute $C = A \times B$ for $N \times N$ matrices:
$$C_{ij} = \sum_{k=0}^{N-1} A_{ik} B_{kj}$$
- **Total Math**: $2 N^3$ FLOPs (1 multiply + 1 add per element).
- **Total Global Memory Loads**: Each of the $N^2$ elements of $C$ reads $N$ elements from $A$ and $N$ elements from $B$ $\to 2 N^3$ loads!
- **Arithmetic Intensity**:
  $$I_{naive} = \frac{2 N^3 \text{ FLOPs}}{2 N^3 \times 4 \text{ Bytes}} = 0.25 \text{ FLOPs/Byte}$$
On an NVIDIA A100 (which needs $I \ge 30$ to saturate compute), naive GEMM achieves **less than 1% of the GPU's potential**!

---

## 2. Shared Memory Tiling ($B \times B$)

Instead of reading from global memory for every multiply-add:
1. Divide matrix $A$ and $B$ into square tiles of size $B \times B$ (e.g., $32 \times 32$).
2. In Phase 0: All threads in a thread block collaborate to load Tile 0 of $A$ and Tile 0 of $B$ into **Shared Memory (SRAM)**:
   ```cpp
   __shared__ float sA[TILE_SIZE][TILE_SIZE];
   __shared__ float sB[TILE_SIZE][TILE_SIZE];
   sA[ty][tx] = A[row * K + (phase * TILE_SIZE + tx)];
   sB[ty][tx] = B[(phase * TILE_SIZE + ty) * N + col];
   __syncthreads(); // Wait until entire tile is loaded!
   ```
3. Multiply the tiles in ultra-fast SRAM.
4. Advance to Phase 1: Load next tile, accumulate partial sums!
5. **Memory Traffic Reduction**: Global memory loads drop by a factor of $B$!
   $$I_{tiled} = \frac{B}{4} \text{ FLOPs/Byte} \quad \implies \text{For } B=32, \; I = 8.0 \text{ FLOPs/Byte (32x improvement!)}$$

---

## 3. Register Micro-Tiling & Double Buffering

Elite GPU engineers (Cutlass / cuBLAS) take this two steps further:
1. **Register Micro-Tiling**: Each thread computes a small $m_m \times n_n$ matrix (e.g. $8 \times 8$) in its own private registers. This reuses shared memory loads an additional $8\times$!
2. **Double Buffering (Ping-Pong Pipelining)**:
   - Buffer 0: Calculating math on registers/SRAM for step $k$.
   - Buffer 1: Simultaneously issuing asynchronous DRAM loads for step $k+1$.
   The math completely hides the memory transfer latency!

# 🐣 Interactive Foundations Playground: FlashAttention-3 & Hopper/Blackwell Features

> *"Ampere (A100) forced CPU-like threads to do manual labor copying memory. Hopper (H100) introduced hardware conveyor belts (TMA) and 128-thread super-units (WGMMA), letting memory move asynchronously without wasting a single compute cycle."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. Tensor Memory Accelerator (TMA): The Conveyor Belt

On an A100 GPU:
- Threads had to load data from Global Memory into registers, and then store it into Shared Memory.
- Every load instruction tied up valuable thread registers and ALU cycles!

On Hopper (H100) & Blackwell (B200):
- **TMA** is a dedicated 2D/3D hardware copy engine.
- A thread issues **one single TMA instruction descriptor**: *"TMA, copy a $64 \times 128$ tile from tensor $X$ into shared memory."*
- The thread goes back to doing matrix math! TMA copies the entire multi-dimensional tile into SRAM in the background with **0 register overhead**!

---

## 2. Asynchronous Barriers (`mbarrier`)

How do compute threads know when TMA has finished copying?
In CUDA, `__syncthreads()` halts all threads until everyone arrives.
Hopper uses hardware **Transaction Barriers (`mbarrier`)**:
```cpp
// Initialize barrier for 8192 expected bytes
mbarrier.init(&bar, num_threads, 8192);
// Issue TMA transfer
tma_load(sram_ptr, global_ptr, &bar);
// Compute threads wait asynchronously
mbarrier.wait(&bar, phase);
```

---

## 3. Warp Group Matrix Multiply & Accumulate (WGMMA)

On Ampere, Tensor Core instructions operate on a single Warp (32 threads).
On Hopper, **WGMMA** merges **4 Warps (128 threads)** into a single coordinated unit!
- WGMMA reads matrix operands directly from **Shared Memory** without loading them into registers first!
- Freeing registers allows each thread to hold much larger matrix accumulators.

---

## 4. Ping-Pong Double Buffering

FlashAttention-3 achieves ~75% of H100 hardware theoretical peak using **Ping-Pong scheduling**:
- **Warpgroup 0**: Executes WGMMA on Tile $k$.
- **Warpgroup 1**: Issues TMA loads and barrier waits for Tile $k+1$.
- In the next phase, they swap roles! The memory latency is **100% hidden behind compute**.

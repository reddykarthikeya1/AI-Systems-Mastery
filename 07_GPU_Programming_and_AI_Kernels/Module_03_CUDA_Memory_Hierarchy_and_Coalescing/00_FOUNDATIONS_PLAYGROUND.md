# 🐣 Interactive Foundations Playground: CUDA Memory Hierarchy & Coalescing

> *"In GPU programming, arithmetic is free; memory traffic is bankruptingly expensive. A matrix multiplication kernel that spends 99% of its time waiting for memory is not a compute kernel—it is an overpriced memory copier."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Grocery Store Checkout (Memory Hierarchy)

- **Registers**: Your pocket. Latency: **0 cycles**. Capacity: tiny (~64K 32-bit registers per SM). Private to each individual thread.
- **Shared Memory (SRAM)**: Your shopping cart. Latency: **~20 cycles**. Capacity: ~100-228 KB per SM. Shared by all threads in the thread block. Ultra-fast!
- **L2 Cache**: The store checkout counter. Latency: **~200 cycles**. Capacity: ~40-60 MB on the entire GPU chip.
- **Global Memory (HBM3e / GDDR6)**: The central warehouse across town. Latency: **~400-800 cycles**. Capacity: 80-141 GB.

---

## 2. Memory Coalescing: The 128-Byte Box Trick

Global memory is read in hardware transactions of **32-byte, 64-byte, or 128-byte aligned cache lines**.
When a warp of 32 threads accesses memory:
- **Scenario A (Coalesced)**: Thread 0 reads float 0, Thread 1 reads float 1, ..., Thread 31 reads float 31.
  - $32 \times 4 \text{ bytes} = 128 \text{ bytes}$ of contiguous, aligned memory.
  - **Result**: The GPU memory controller issues **1 single 128-byte transaction**. 100% bus utilization!
- **Scenario B (Strided Access - Stride 32)**: Thread 0 reads float 0, Thread 1 reads float 32, ..., Thread 31 reads float 992.
  - Each thread hits a completely different 128-byte cache line.
  - **Result**: The memory controller must issue **32 separate 128-byte transactions** ($32 \times 128 = 4096 \text{ bytes}$ transferred to use only 128 bytes!).
  - **Bandwidth Waste**: **96.875% of your GPU memory bandwidth is thrown in the trash!**

---

## 3. Shared Memory Banks & The Bank Conflict Disaster

Shared memory is physically partitioned into **32 independent memory banks** (Bank 0 to Bank 31).
Each bank has a bandwidth of 32 bits (4 bytes) per clock cycle.
The bank mapping formula:
$$\text{Bank ID} = \left(\frac{\text{Byte Address}}{4}\right) \pmod{32}$$

- **Conflict-Free**: 32 threads in a warp access 32 different banks simultaneously $\to$ **1 cycle**.
- **Broadcast**: All 32 threads read the exact same address $\to$ **1 cycle** (multicast).
- **$k$-Way Bank Conflict**: $k$ threads in a warp access *different addresses that fall into the same bank*.
  - The hardware must **serialize** the requests into $k$ separate passes.
  - A 32-way bank conflict makes shared memory **32 times slower**!

### The Legendary Shared Memory Padding Trick
When loading a $32 \times 32$ float matrix into shared memory:
```cpp
__shared__ float tile[32][32]; // BAD: column access tile[threadIdx.x][0] hits Bank 0 for ALL 32 threads!
__shared__ float tile[32][33]; // BRILLIANT: 1 float pad shifts row strides so Bank = (row * 33 + col) % 32 -> 0 conflicts!
```

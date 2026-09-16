# Module 03: CUDA Memory Hierarchy & Coalescing

> **Architectural Scope**: 128-Byte Coalescing Rules, Shared Memory 32-Bank Structure, Bank Conflicts, Padding Mechanics, and Cache Bypass with `__ldg()`.

---

## 1. Global Memory Coalescing Rules

NVIDIA GPU memory controllers do not read individual 4-byte floating-point numbers.
They read memory in aligned **32-byte, 64-byte, or 128-byte DRAM cache lines**.

```
+---------------------------------------------------------------------------------------------------+
| CASE 1: COALESCED ACCESS (100% Bus Efficiency)                                                    |
| Thread:      T0   T1   T2   T3   ...  T31                                                         |
| Byte Addr:    0    4    8   12   ...  124                                                         |
| Hardware:    --> Read aligned 128-Byte Cache Line [0..127] in 1 SINGLE TRANSACTION                |
+---------------------------------------------------------------------------------------------------+
| CASE 2: STRIDED ACCESS - Stride 32 (3.125% Bus Efficiency)                                        |
| Thread:      T0   T1   T2   T3   ...  T31                                                         |
| Byte Addr:    0  128  256  384   ... 3968                                                         |
| Hardware:    --> 32 INDEPENDENT 128-Byte Transactions (4,096 Bytes transferred to use 128 Bytes!) |
+---------------------------------------------------------------------------------------------------+
```

### The Vectorized Load Trick (`float4`)
To maximize memory bus throughput, modern CUDA kernels use 128-bit vector types (`float4`, `uint4`):
```cpp
// Load 4 consecutive floats in a single instruction per thread
float4 val = *reinterpret_cast<const float4*>(&input[idx * 4]);
```
This reduces instruction issue overhead by $4\times$ and guarantees memory coalescing.

---

## 2. Shared Memory 32-Bank Architecture

Shared memory (SRAM) is organized into **32 memory banks** (Bank 0 to 31).
Each bank has a word size of 32 bits (4 bytes).
Successive 32-bit words are assigned to successive banks:
$$\text{Bank ID} = \left(\frac{\text{Byte Address}}{4}\right) \pmod{32}$$

- **Conflict-Free**: All 32 threads in a warp access different banks $\to$ 1 clock cycle.
- **Broadcast**: Multiple threads access the *exact same address* $\to$ 1 clock cycle (hardware multicast).
- **$k$-Way Bank Conflict**: Multiple threads access *different addresses within the same bank*. The requests are serialized, taking $k$ clock cycles.

---

## 3. The Classic Matrix Transpose Shared Memory Padding Trick

When transposing a $32 \times 32$ matrix in shared memory:
```cpp
// UNPADDED: BAD!
__shared__ float tile[32][32];
// Row write: tile[threadIdx.y][threadIdx.x] -> Coalesced, conflict-free!
// Column read: tile[threadIdx.x][threadIdx.y] -> ALL 32 threads hit Bank (threadIdx.x * 32) % 32 = Bank 0!
// 32-WAY BANK CONFLICT! Throughput drops by 32x!
```

### The Fix: Add 1 Column of Padding
```cpp
// PADDED: ELEGANT!
__shared__ float tile[32][33];
// Column read: Address = threadIdx.x * 33 + threadIdx.y
// Bank = (threadIdx.x * 33 + threadIdx.y) % 32 = (threadIdx.x + threadIdx.y) % 32
// Every thread in the warp hits a UNIQUE bank! 1-WAY (ZERO CONFLICTS)!
```

---

## 4. Module Study Progression
1. **Beginner Playground**: Read [00_W3_BEGINNER_PLAYGROUND.md](00_W3_BEGINNER_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).

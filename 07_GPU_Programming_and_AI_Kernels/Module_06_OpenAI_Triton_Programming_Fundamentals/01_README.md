# Module 06: OpenAI Triton Programming Fundamentals

> **Architectural Scope**: Block-Level Programming Model, Block Pointers, Strided Memory Access, Masked Loads/Stores, and the Triton JIT Compiler Pipeline.

---

## 1. The Block-Level Programming Paradigm

CUDA operates at the **scalar thread level**: the developer writes code for 1 thread and manually orchestrates warps, memory coalescing, and shared memory allocations.
OpenAI Triton operates at the **Block level**: the developer writes Python code operating on small multi-dimensional arrays (Blocks) of shape `(BLOCK_M, BLOCK_N)`.

```
+-----------------------------------------------------------------------------------------------+
| TRITON JIT COMPILER LOWERING PIPELINE                                                         |
+-----------------------------------------------------------------------------------------------+
| Python AST (@triton.jit)                                                                      |
|    |                                                                                          |
|    v                                                                                          |
| Triton-IR (Block-level dataflow graph)                                                        |
|    |                                                                                          |
|    v                                                                                          |
| TritonGPU-IR (Hardware mapping: allocates shared memory, assigns warps, generates coalescing) |
|    |                                                                                          |
|    v                                                                                          |
| LLVM-IR  -->  PTX Assembly  -->  Cubin Machine Code                                           |
+-----------------------------------------------------------------------------------------------+
```

---

## 2. Core Triton Primitives

### 1. `tl.arange(0, BLOCK_SIZE)`
Generates a 1D tensor of consecutive integer indices in registers.

### 2. `tl.load(pointer + offsets, mask=offsets < boundary, other=0.0)`
Performs a vectorized memory read from DRAM. The compiler automatically aligns transactions to 128-byte cache lines. The `mask` parameter guards against segmentation faults at boundaries.

### 3. `tl.store(pointer + offsets, values, mask=offsets < boundary)`
Performs guarded vectorized memory writes.

### 4. `tl.dot(block_a, block_b)`
Directly targets NVIDIA Tensor Cores (MMA instructions) to execute hardware matrix multiplication.

---

## 3. Triton Fused Softmax Implementation

```python
import triton
import triton.language as tl

@triton.jit
def softmax_kernel(output_ptr, input_ptr, input_row_stride, output_row_stride, n_cols, BLOCK_SIZE: tl.constexpr):
    row_idx = tl.program_id(0)
    row_start_ptr = input_ptr + row_idx * input_row_stride
    col_offsets = tl.arange(0, BLOCK_SIZE)
    input_ptrs = row_start_ptr + col_offsets
    mask = col_offsets < n_cols

    # 1. Load row with boundary mask
    row = tl.load(input_ptrs, mask=mask, other=-float('inf'))

    # 2. Stable subtraction of row max
    row_max = tl.max(row, axis=0)
    numerator = tl.exp(row - row_max)

    # 3. Denominator sum
    denominator = tl.sum(numerator, axis=0)
    softmax_output = numerator / denominator

    # 4. Store back to DRAM
    output_row_start_ptr = output_ptr + row_idx * output_row_stride
    tl.store(output_row_start_ptr + col_offsets, softmax_output, mask=mask)
```

---

## 4. Module Study Progression
1. **Beginner Playground**: Read [00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).

# 🐣 Interactive Foundations Playground: OpenAI Triton Programming Fundamentals

> *"Writing CUDA is like laying bricks by hand—you control every single trowel stroke and mortar drop. Triton is like 3D printing a house—you specify block operations, and the compiler figures out how to lay the bricks without making mistakes."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Block Paradigm Shift

In CUDA, you write a function executed by a **single thread**:
```cpp
// CUDA: Thread-level
__global__ void add(float *x, float *y, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) y[idx] += x[idx];
}
```

In Triton, you write a function executed by an entire **Block of threads**:
```python
# Triton: Block-level
@triton.jit
def add_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)  # Which block are we?
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)  # Vector of offsets!
    mask = offsets < n_elements  # Protect against out-of-bounds memory!
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    tl.store(y_ptr + offsets, x + y, mask=mask)
```

Notice the power:
1. `tl.arange(0, BLOCK_SIZE)` creates a **NumPy-like vector** of indices.
2. `mask` automatically prevents illegal memory segmentation faults without thread divergence.
3. The Triton compiler generates memory coalescing, register allocations, and warp shuffle instructions automatically!

---

## 2. Block Pointers: Strided Multi-Dimensional Memory

For 2D matrices, Triton provides **Block Pointers** (`tl.make_block_ptr`):
- **Base**: Pointer to matrix start.
- **Shape**: `(M, N)` total dimensions.
- **Strides**: `(stride_m, stride_n)` memory layout strides.
- **Offsets**: `(block_m * BLOCK_M, block_n * BLOCK_N)` current block origin.
- **Block Shape**: `(BLOCK_M, BLOCK_N)` size of block to load.
- **Order**: `(1, 0)` row-major order.

Triton advances pointers across iterations with a single line:
```python
ptr = tl.advance(ptr, (0, BLOCK_K))
```

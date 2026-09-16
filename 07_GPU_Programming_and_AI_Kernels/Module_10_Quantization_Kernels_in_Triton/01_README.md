# Module 10: Quantization Kernels in Triton (FP8 & INT4)

> **Architectural Scope**: Sub-Byte Bitwise Packing, On-the-Fly Register Dequantization, AWQ Outlier Protection, and Grouped Quantized GEMMs.

---

## 1. The VRAM Capacity & Bandwidth Challenge

Large Language Models (LLMs) are constrained by memory capacity and memory bandwidth:
- A **70 Billion parameter model** in FP16 ($2 \text{ bytes per weight}$) requires:
  $$70 \times 10^9 \times 2 \text{ bytes} = 140 \text{ Gigabytes}$$
  It requires at least two 80GB A100/H100 GPUs just to load into VRAM.
- In **4-Bit Quantization (INT4)** ($0.5 \text{ bytes per weight}$):
  $$70 \times 10^9 \times 0.5 \text{ bytes} = 35 \text{ Gigabytes}$$
  The entire 70B model fits on a single consumer GPU (e.g. RTX 4090 or single A100)!

---

## 2. Sub-Byte Bitwise Packing Mechanics

Computer DRAM cannot address individual 4-bit nibbles.
Therefore, two INT4 values are packed into a single 8-bit `uint8` byte:
```python
# Packing two 4-bit values (v0, v1) into 1 byte:
packed_byte = (v0 & 0x0F) | ((v1 & 0x0F) << 4)

# Unpacking on GPU:
v0 = packed_byte & 0x0F
v1 = (packed_byte >> 4) & 0x0F
```

---

## 3. On-The-Fly Register Dequantization

**Crucial Engineering Principle**: Never dequantize packed weights into global memory before matrix multiplication!
If you dequantize into DRAM, you write 140 GB back to memory, completely destroying your memory bandwidth advantage.

### The Correct Kernel Architecture:
1. Load packed `uint8` bytes from HBM into thread **Registers**.
2. Unpack two 4-bit numbers inside ALU registers.
3. Multiply by floating-point scale factor $s$ and subtract zero-point $z$:
   $$W_{\text{FP16}} = (W_{\text{INT4}} - z) \times s$$
4. Pass directly to Tensor Cores!
5. **Result**: Memory traffic across the memory bus is reduced by **$4\times$**, providing massive speedups for memory-bound token generation.

---

## 4. Activation-Aware Weight Quantization (AWQ)

Uniform weight quantization degrades model perplexity.
Research by Lin et al. (2023) discovered:
- Only $\approx 0.1\%$ to $1\%$ of channels contain salient outlier activations that dictate model intelligence.
- **AWQ Algorithm**:
  1. Observe activation magnitudes $S_X = \text{mean}(|X|, \text{dim}=0)$.
  2. Find per-channel protection scales $s = S_X^\alpha$.
  3. Scale up salient weight channels: $W' = W \times s$.
  4. Scale down corresponding input activations: $X' = X / s$.
  5. Quantize $W'$ without clipping errors!

---

## 5. FP8 Formats (E4M3 vs E5M2) & Tensor Core Scaling

Modern GPU architectures (NVIDIA Ada Lovelace, Hopper H100, Blackwell B200) feature dedicated 8-bit floating-point Tensor Cores providing **$2\times$ the FLOPS** of FP16.

### The Two IEEE/OCP FP8 Standards:
| Format | Sign | Exponent | Mantissa | Max Value | Primary Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **E4M3** | 1 bit | 4 bits | 3 bits | $\pm 448$ | Forward pass weights & activations (higher numerical precision) |
| **E5M2** | 1 bit | 5 bits | 2 bits | $\pm 57,344$ | Backward pass gradients (wider dynamic range prevents underflow) |

### Delayed Scaling Factor Updates:
Because FP8 has limited dynamic range, tensors must be dynamically scaled:
$$X_{\text{FP8}} = \text{clip}\left(\text{round}\left(X \times s\right), -\text{max\_fp8}, \text{max\_fp8}\right)$$
To avoid costly full-tensor reductions during the forward pass, production serving engines employ **delayed scaling**: the maximum absolute value from iteration $t-1$ determines the scale factor $s_t$ for iteration $t$. Accumulation inside Tensor Cores is always performed in high-precision **FP32**.

---

## 6. CUTLASS 3.x and NVIDIA CuTe Layout Abstractions

For bare-metal CUDA C++ developers, NVIDIA provides **CUTLASS 3.x** and its core abstraction library **CuTe**:

1. **CuTe Layout Algebra**:
   - Expresses multidimensional coordinate tensors as a tuple of `(Shape, Stride)`.
   - Decouples mathematical coordinate iteration from physical memory arrangement (row-major, column-major, or swizzled shared memory banking).

2. **Tensor Memory Accelerator (TMA) Support**:
   - On Hopper and Blackwell architectures, TMA executes multi-dimensional asynchronous bulk copies between global memory (HBM) and shared memory (SRAM) without consuming SM ALU cycles.

3. **Warp-Specialized GEMM Pipelines**:
   - Divides warps into dedicated roles: *Producer warps* manage TMA memory traffic into shared memory, while *Consumer warps* execute `wgmma.mma_async` instructions on Tensor Cores.

---

## 7. Module Study Progression
1. **Beginner Playground**: Read [00_W3_BEGINNER_PLAYGROUND.md](00_W3_BEGINNER_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).


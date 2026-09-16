# 🐣 Interactive Foundations Playground: Quantization Kernels (FP8 & INT4)

> *"A 70B parameter model in FP16 weighs 140 Gigabytes and demands $30,000 server GPUs. Quantizing weights to 4-bit shrinks the entire model to 35 Gigabytes, letting it run on a single workstation without losing its intelligence."*

---

## 1. Bitwise Packing: Squeezing 2 Numbers into 1 Byte

An integer from 0 to 15 (or -8 to +7) fits into **4 bits (a nibble)**.
Because computer memory cannot address individual bits, we pack **two 4-bit numbers** into a single 8-bit `uint8` byte:
```python
# Packing:
packed_byte = (val1 & 0x0F) | ((val2 & 0x0F) << 4)

# Unpacking:
val1 = packed_byte & 0x0F
val2 = (packed_byte >> 4) & 0x0F
```

---

## 2. Dequantization On-the-Fly in Registers

**The Rookie Blunder**: Unpacking INT4 weights into an FP16 matrix in GPU memory before doing matrix multiplication.
- Result: You still transfer 140 GB across the slow memory bus! You saved disk space but gained zero speedup!

**The Kernel Engineer Solution**:
- Keep weights packed as INT4 in slow Global Memory (HBM).
- In the inner loop of your matrix multiply kernel, load 1 byte from HBM into a thread register.
- Unpack into 2 registers, multiply by scale $s$, add zero-point $z$:
  $$w_{fp} = (w_{int4} - z) \times s$$
- Feed directly into Tensor Cores!
- **Memory Bandwidth Reduction**: $4\times$ less HBM traffic!

---

## 3. FP8 (E4M3 vs E5M2)

Hopper & Blackwell GPUs support native **FP8 (8-bit floating point)**:
1. **E4M3** (1 sign, 4 exponent, 3 mantissa bits):
   - Higher precision, narrower range (max $\approx 448$).
   - Standard for neural network weights and forward activations.
2. **E5M2** (1 sign, 5 exponent, 2 mantissa bits):
   - Same dynamic range as FP16 (max $\approx 57{,}344$), lower precision.
   - Standard for backward pass gradients where dynamic range is wide.

---

## 4. Activation-Aware Weight Quantization (AWQ)

Research shows not all weights are equal:
- $\approx 0.1\%$ to $1\%$ of channels contain salient outlier activations that dictate model intelligence.
- If you quantize those outliers uniformly, perplexity explodes!
- **AWQ (Lin et al.)**: Protects salient channels by multiplying weight channels by per-channel scales, keeping quantization error minimal without mixed-precision overhead!

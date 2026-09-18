# Debug Lab: INT8 Per-Tensor Quantization Kernel Clips Its Outliers
# Course 07 - Module 10 Quantization Kernels in Triton

def compute_scale(tensor, qmax=127):
    avg_abs = sum(abs(v) for v in tensor) / len(tensor)
    return avg_abs / qmax


def quantize_int8(tensor, qmax=127):
    scale = compute_scale(tensor, qmax)
    q = [max(-qmax - 1, min(qmax, round(v / scale))) for v in tensor]
    return q, scale


def dequantize_int8(q, scale):
    return [v * scale for v in q]


if __name__ == "__main__":
    activations = [0.1, -0.2, 0.15, 0.05, -0.1, 8.5, 0.2, -0.05]  # one large outlier

    q, scale = quantize_int8(activations)
    recovered = dequantize_int8(q, scale)

    print(f"Original activations: {activations}")
    print(f"Per-tensor scale used: {scale:.6f}")
    print(f"Quantized int8 levels: {q}")
    print(f"Dequantized round-trip: {[round(v, 4) for v in recovered]}")

    errors = [abs(o - r) for o, r in zip(activations, recovered)]
    print(f"Per-element absolute error: {[round(e, 4) for e in errors]}")
    print(f"Max absolute error: {max(errors):.4f}")

# Debug Lab: Asymmetric INT8 Dequantization Drops the Zero-Point
# Course 09 - Module 08 Quantization for Serving

QINT8_MIN, QINT8_MAX = 0, 255  # unsigned 8-bit quantized range


def compute_scale_and_zero_point(values):
    """Asymmetric quantization: map [min(values), max(values)] onto
    [0, 255]. The zero_point is the quantized code that represents real
    value 0.0, needed whenever the real range isn't symmetric around zero."""
    lo, hi = min(values), max(values)
    scale = (hi - lo) / (QINT8_MAX - QINT8_MIN)
    zero_point = round(QINT8_MIN - lo / scale)
    return scale, zero_point


def quantize(values, scale, zero_point):
    return [max(QINT8_MIN, min(QINT8_MAX, round(v / scale) + zero_point)) for v in values]


def dequantize(qvalues, scale, zero_point):
    # Reconstructing the real value from a quantized code must undo BOTH the
    # scaling and the zero-point shift that quantize() applied.
    return [q * scale for q in qvalues]


if __name__ == "__main__":
    weights = [-2.0, -1.0, 0.0, 1.0, 5.0]  # not symmetric around zero

    scale, zero_point = compute_scale_and_zero_point(weights)
    quantized = quantize(weights, scale, zero_point)
    recovered = dequantize(quantized, scale, zero_point)

    error = [round(r - w, 4) for r, w in zip(recovered, weights)]

    print(f"Original FP32 weights: {weights}")
    print(f"scale={scale:.4f}, zero_point={zero_point}")
    print(f"Quantized INT8 codes:  {quantized}")
    print(f"Expected dequantized weights (should closely match the originals): {weights}")
    print(f"Actual dequantized weights: {[round(v, 4) for v in recovered]}")
    print(f"Per-element error (actual - expected): {error}")

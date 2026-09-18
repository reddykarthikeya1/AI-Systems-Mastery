# Debug Lab: Fused LayerNorm Kernel Produces Wrong Variance Off-Center Data
# Course 07 - Module 07 Fused Activations and Normalization

def reference_layernorm(x, eps=1e-5):
    n = len(x)
    mean = sum(x) / n
    var = sum((v - mean) ** 2 for v in x) / n
    denom = (var + eps) ** 0.5
    return [(v - mean) / denom for v in x]


def fused_layernorm(x, eps=1e-5):
    # Single-pass "fused" statistics: accumulate sum(x) and sum(x*x) together
    # in one loop instead of a second pass over the data.
    n = len(x)
    sum_x = 0.0
    sum_x2 = 0.0
    for v in x:
        sum_x += v
        sum_x2 += v * v
    mean = sum_x / n
    var = sum_x2 / n
    denom = (var + eps) ** 0.5
    return [(v - mean) / denom for v in x]


if __name__ == "__main__":
    row = [10.0, 11.0, 12.0, 13.0, 14.0]  # mean = 12, not centered at 0

    expected = reference_layernorm(row)
    actual = fused_layernorm(row)
    mismatches = sum(1 for e, a in zip(expected, actual) if abs(e - a) > 1e-6)

    print(f"Input row: {row}")
    print(f"reference_layernorm: {[round(v, 4) for v in expected]}")
    print(f"fused_layernorm:     {[round(v, 4) for v in actual]}")
    print(f"Mismatched entries: {mismatches} of {len(row)}")

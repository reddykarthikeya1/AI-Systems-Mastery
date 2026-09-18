# Debug Lab: FA3-Style FP8 Block-Scaled Accumulation Shrinks the Output
# Course 07 - Module 09 FlashAttention 3 and Hopper/Blackwell Features

def quantize_block(block, qmax=127):
    """Per-block FP8-style symmetric quantization (the 'block scale' of FA3's
    two-level scaling: one scale per K/V tile, plus an outer tensor scale)."""
    block_scale = max(abs(v) for v in block) / qmax
    q = [round(v / block_scale) for v in block]
    return q, block_scale


def dequantize_block(q, block_scale):
    return [v * block_scale for v in q]


def fp8_accumulate(blocks, tensor_scale=1.0):
    """Merge each quantized K/V block's dequantized contribution into the
    fp32 output accumulator, then apply the outer tensor-level scale once."""
    width = len(blocks[0])
    acc = [0.0] * width
    for block in blocks:
        q, block_scale = quantize_block(block)
        dequantized = dequantize_block(q, block_scale)
        for i, v in enumerate(dequantized):
            acc[i] += v * block_scale
    return [v * tensor_scale for v in acc]


if __name__ == "__main__":
    blocks = [
        [1.0, -2.0, 3.0, 4.0],
        [0.5, 5.0, -1.5, 2.0],
        [3.0, 1.0, 2.5, -4.0],
    ]
    reference = [sum(block[i] for block in blocks) for i in range(len(blocks[0]))]
    actual = fp8_accumulate(blocks, tensor_scale=1.0)

    print(f"K/V blocks: {blocks}")
    print(f"Reference (exact) sum:          {[round(v, 4) for v in reference]}")
    print(f"FP8 block-scaled accumulation:  {[round(v, 4) for v in actual]}")
    mismatches = sum(1 for e, a in zip(reference, actual) if abs(e - a) > 0.05)
    print(f"Entries off by more than 0.05: {mismatches} of {len(reference)}")

# Debug Lab: FlashAttention Online Softmax Diverges From Full Softmax Output
# Course 07 - Module 08 FlashAttention 1 and 2 Internals

import math


def reference_attention(scores, values):
    m = max(scores)
    weights = [math.exp(s - m) for s in scores]
    denom = sum(weights)
    return sum(w * v for w, v in zip(weights, values)) / denom


def flash_attention_blocked(score_blocks, value_blocks):
    running_max = -math.inf
    running_sum = 0.0
    acc = 0.0
    for scores, values in zip(score_blocks, value_blocks):
        block_max = max(scores)
        new_max = max(running_max, block_max)
        alpha = math.exp(running_max - new_max) if running_max != -math.inf else 0.0

        block_weights = [math.exp(s - new_max) for s in scores]
        block_sum = sum(block_weights)

        running_sum = running_sum * alpha + block_sum
        acc = acc + sum(w * v for w, v in zip(block_weights, values))

        running_max = new_max
    return acc / running_sum


if __name__ == "__main__":
    scores = [1.0, 2.0, 3.0, 0.5, 4.0, 1.5]
    values = [10.0, 20.0, 30.0, 5.0, 40.0, 15.0]
    score_blocks = [scores[0:2], scores[2:4], scores[4:6]]
    value_blocks = [values[0:2], values[2:4], values[4:6]]

    expected = reference_attention(scores, values)
    actual = flash_attention_blocked(score_blocks, value_blocks)

    print(f"Scores: {scores}")
    print(f"Full-softmax reference output:  {expected:.6f}")
    print(f"Blocked online-softmax output:  {actual:.6f}")
    print(f"Absolute difference: {abs(expected - actual):.6f}")

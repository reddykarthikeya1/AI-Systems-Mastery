# Debug Lab: Attention Weights Do Not Sum To One
# Course 06 - Module 06 Transformers

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def softmax_over_scores(scores):
    exps = [[math.exp(v) for v in row] for row in scores]
    col_sums = [sum(exps[r][c] for r in range(len(exps))) for c in range(len(exps[0]))]
    return [[exps[r][c] / col_sums[c] for c in range(len(exps[0]))] for r in range(len(exps))]


def self_attention(queries, keys, values):
    scores = [[dot(q, k) / math.sqrt(len(q)) for k in keys] for q in queries]
    weights = softmax_over_scores(scores)
    outputs = []
    for row in weights:
        out = [0.0] * len(values[0])
        for w, v in zip(row, values):
            out = [o + w * vi for o, vi in zip(out, v)]
        outputs.append(out)
    return weights, outputs


if __name__ == "__main__":
    tokens = ["the", "cat", "sat"]
    queries = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    keys = [[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]]
    values = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]

    weights, outputs = self_attention(queries, keys, values)

    print("Attention weight matrix (each row is one token's distribution over all keys):")
    for token, row in zip(tokens, weights):
        row_sum = sum(row)
        print(f"  '{token}': {[round(w, 3) for w in row]}  row_sum={row_sum:.3f}")

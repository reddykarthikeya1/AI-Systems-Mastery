# Debug Lab: Row-Parallel Linear Layer Under-Reports Its Output Magnitude
# Course 08 - Module 05 Tensor Parallelism (Megatron-LM)

def reference_linear(x, weight_rows):
    """A single, un-sharded linear layer: out = sum_k x[k] * weight_rows[k]."""
    width = len(weight_rows[0])
    out = [0.0] * width
    for k, row in enumerate(weight_rows):
        for j in range(width):
            out[j] += x[k] * row[j]
    return out


def row_parallel_partial(x_shard, weight_shard):
    """Each tensor-parallel rank holds a contiguous shard of input features
    and the matching rows of the weight matrix, and computes its own
    partial sum over just its shard of the reduction (input-feature)
    dimension."""
    width = len(weight_shard[0])
    partial = [0.0] * width
    for k, row in enumerate(weight_shard):
        for j in range(width):
            partial[j] += x_shard[k] * row[j]
    return partial


def row_parallel_combine(rank_partials):
    """Combine every TP rank's partial output into the final layer output."""
    tp_size = len(rank_partials)
    width = len(rank_partials[0])
    return [sum(rank_partials[r][j] for r in range(tp_size)) / tp_size for j in range(width)]


if __name__ == "__main__":
    tp_size = 2
    x = [1.0, 2.0, 3.0, 4.0]
    weight_rows = [[1.0, 0.5], [2.0, 1.0], [0.5, 1.5], [1.0, 2.0]]

    expected = reference_linear(x, weight_rows)

    x_shards = [x[0:2], x[2:4]]
    weight_shards = [weight_rows[0:2], weight_rows[2:4]]
    rank_partials = [row_parallel_partial(xs, ws) for xs, ws in zip(x_shards, weight_shards)]
    actual = row_parallel_combine(rank_partials)

    print(f"tp_size={tp_size}, per-rank partial outputs: {rank_partials}")
    print(f"Un-sharded reference output: {[round(v, 4) for v in expected]}")
    print(f"Row-parallel combined output: {[round(v, 4) for v in actual]}")

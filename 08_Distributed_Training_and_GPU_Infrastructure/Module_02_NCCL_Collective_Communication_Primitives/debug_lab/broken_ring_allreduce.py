# Debug Lab: Ring All-Reduce Averaged Gradient Is Too Small By a Factor of World Size
# Course 08 - Module 02 NCCL Collective Communication Primitives

def reduce_scatter_sum(rank_buffers):
    """Simulates the reduce-scatter phase of a ring all-reduce: after N-1
    ring steps, each rank ends up holding one chunk reduced across all N
    ranks' contributions."""
    world_size = len(rank_buffers)
    chunk_count = len(rank_buffers[0])
    summed_chunks = []
    for c in range(chunk_count):
        total = sum(rank_buffers[r][c] for r in range(world_size))
        summed_chunks.append(total / world_size)
    return summed_chunks


def ring_allreduce_mean(rank_buffers):
    """Reduce-scatter + all-gather ring all-reduce, averaging the gradient
    across all ranks."""
    world_size = len(rank_buffers)
    reduced = reduce_scatter_sum(rank_buffers)
    return [v / world_size for v in reduced]


if __name__ == "__main__":
    world_size = 4
    # Each rank's local gradient for a 3-element parameter tensor.
    rank_buffers = [
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 4.0, 5.0],
        [4.0, 5.0, 6.0],
    ]

    expected_mean = [
        sum(rank_buffers[r][c] for r in range(world_size)) / world_size
        for c in range(len(rank_buffers[0]))
    ]
    actual_mean = ring_allreduce_mean(rank_buffers)

    print(f"world_size={world_size}, per-rank gradients: {rank_buffers}")
    print(f"Expected all-reduced mean gradient: {[round(v, 4) for v in expected_mean]}")
    print(f"ring_allreduce_mean() output:       {[round(v, 4) for v in actual_mean]}")
    ratio = actual_mean[0] / expected_mean[0]
    print(f"Ratio actual/expected on element 0: {ratio:.4f} (should be 1.0)")

# Debug Lab: Kernel Leaves Most of the Output Array Untouched
# Course 07 - Module 02 CUDA C++ Programming Fundamentals

def compute_global_index(block_idx, thread_idx, block_dim):
    return block_idx + thread_idx


def run_kernel(num_blocks, block_dim, n):
    output = [None] * n
    for block_idx in range(num_blocks):
        for thread_idx in range(block_dim):
            idx = compute_global_index(block_idx, thread_idx, block_dim) % n
            output[idx] = block_idx * block_dim + thread_idx
    return output


if __name__ == "__main__":
    num_blocks, block_dim = 4, 8
    n = num_blocks * block_dim

    result = run_kernel(num_blocks, block_dim, n)
    untouched = [i for i, v in enumerate(result) if v is None]

    print(f"Kernel launched with {num_blocks} blocks x {block_dim} threads for {n} output elements.")
    print(f"Output array: {result}")
    print(f"Elements never written by any thread: {len(untouched)} of {n} -> indices {untouched}")

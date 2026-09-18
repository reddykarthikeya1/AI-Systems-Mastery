# Debug Lab: Vector-Add "Kernel" Produces the Wrong Length Output
# Course 07 - Module 06 OpenAI Triton Programming Fundamentals

BLOCK_SIZE = 4


def vector_add_kernel(a, b, n):
    out = [None] * n
    num_blocks = (n + BLOCK_SIZE - 1) // BLOCK_SIZE
    for pid in range(num_blocks):
        block_start = pid * (BLOCK_SIZE - 1)
        for offset in range(BLOCK_SIZE):
            idx = block_start + offset
            if idx < n:
                out[idx] = a[idx] + b[idx]
    return out


if __name__ == "__main__":
    n = 12
    a = list(range(n))
    b = list(range(100, 100 + n))

    result = vector_add_kernel(a, b, n)
    expected = [x + y for x, y in zip(a, b)]
    mismatches = [i for i in range(n) if result[i] != expected[i]]

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"kernel output   = {result}")
    print(f"expected output = {expected}")
    print(f"mismatched positions: {mismatches}")

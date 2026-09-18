# Debug Lab: Tree Reduction Silently Drops the Tail of a Non-Power-of-2 Array
# Course 07 - Module 04 Parallel Reduction and Prefix Sum

def tree_reduce_sum(values):
    buf = list(values)
    n = len(buf)
    stride = 1
    while stride < n:
        i = 0
        while i + stride < n:
            buf[i] += buf[i + stride]
            i += stride * 2
        stride *= 2
    return buf[0]


if __name__ == "__main__":
    data = [3, 1, 4, 1, 5, 9]  # length 6, not a power of two

    reduced = tree_reduce_sum(data)
    reference = sum(data)

    print(f"Input array: {data}")
    print(f"Tree-reduction result: {reduced}")
    print(f"sum(data) reference:   {reference}")

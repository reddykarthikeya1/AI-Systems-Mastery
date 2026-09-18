# Debug Lab: "Contiguous" Row Read Requires Far Too Many Memory Transactions
# Course 07 - Module 03 CUDA Memory Hierarchy and Coalescing

def compute_address(row, col, cols, dtype_size=4):
    return (col * cols + row) * dtype_size


def warp_access_pattern(cols, dtype_size=4):
    row = 0
    return [compute_address(row, lane, cols, dtype_size) for lane in range(cols)]


def count_transactions(addresses, segment_size=32):
    segments = sorted(set(addr // segment_size for addr in addresses))
    return len(segments), segments


if __name__ == "__main__":
    cols = 32
    addresses = warp_access_pattern(cols)
    tx_count, segments = count_transactions(addresses)

    print(f"Warp of {cols} threads reading row 0 of a {cols}x{cols} row-major float32 matrix.")
    print(f"Byte addresses touched by lanes 0-7: {addresses[:8]}")
    print(f"Memory transactions required: {tx_count} (32-byte segments touched: {segments[:8]}{'...' if len(segments) > 8 else ''})")
    print(f"Ideal contiguous {cols}-lane row read should need only a handful of transactions, not {tx_count}.")

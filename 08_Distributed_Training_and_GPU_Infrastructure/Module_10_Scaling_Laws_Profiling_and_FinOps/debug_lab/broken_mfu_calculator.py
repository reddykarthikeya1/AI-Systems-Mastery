"""Broken Model Flops Utilization (MFU) Calculator."""
def calculate_mfu(num_params: int, tokens_per_sec: float, peak_tflops: float) -> float:
    # BUG: Uses 2 * N * tokens for forward only, but compares against total training time
    # Full forward + backward pass requires 6 * N * tokens per step (2 FWD + 4 BWD)
    # The divisor also forgot factor of 1e12 for TFLOPS
    flops_per_sec = 2.0 * num_params * tokens_per_sec  # BUG
    mfu = (flops_per_sec / (peak_tflops * 1e12)) * 100.0
    return mfu

if __name__ == '__main__':
    print("Calculated MFU:", calculate_mfu(70_000_000_000, 2500, 989.0))

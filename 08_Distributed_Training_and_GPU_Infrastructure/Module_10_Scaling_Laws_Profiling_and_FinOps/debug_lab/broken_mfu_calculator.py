"""Broken Model Flops Utilization (MFU) Calculator."""
def calculate_mfu(num_params: int, tokens_per_sec: float, peak_tflops: float) -> float:
    # Full forward + backward pass requires 6 * N * tokens per step (2 FWD + 4 BWD)
    flops_per_sec = 2.0 * num_params * tokens_per_sec
    mfu = (flops_per_sec / (peak_tflops * 1e12)) * 100.0
    return mfu

if __name__ == '__main__':
    print("Calculated MFU:", calculate_mfu(70_000_000_000, 2500, 989.0))

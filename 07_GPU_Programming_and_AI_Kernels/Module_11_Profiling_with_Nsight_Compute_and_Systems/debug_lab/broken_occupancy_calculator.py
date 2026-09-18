# Debug Lab: Theoretical Occupancy Calculator Ignores the Register-Limited Bound
# Course 07 - Module 11 Profiling with Nsight Compute and Systems

WARP_SIZE = 32
MAX_THREADS_PER_SM = 2048
MAX_WARPS_PER_SM = MAX_THREADS_PER_SM // WARP_SIZE  # 64
MAX_REGS_PER_SM = 65536
MAX_BLOCKS_PER_SM_HW = 32


def blocks_per_sm_limits(threads_per_block, regs_per_thread):
    thread_limit = MAX_THREADS_PER_SM // threads_per_block
    reg_limit = MAX_REGS_PER_SM // (regs_per_thread * threads_per_block)
    return thread_limit, reg_limit, MAX_BLOCKS_PER_SM_HW


def theoretical_occupancy(threads_per_block, regs_per_thread):
    thread_limit, reg_limit, hw_limit = blocks_per_sm_limits(threads_per_block, regs_per_thread)
    resident_blocks = min(thread_limit, hw_limit)
    warps_per_block = threads_per_block // WARP_SIZE
    resident_warps = resident_blocks * warps_per_block
    return resident_warps / MAX_WARPS_PER_SM


if __name__ == "__main__":
    threads_per_block = 256
    regs_per_thread = 96  # a register-hungry fused kernel

    thread_limit, reg_limit, hw_limit = blocks_per_sm_limits(threads_per_block, regs_per_thread)
    true_resident_blocks = min(thread_limit, reg_limit, hw_limit)
    true_occupancy = (true_resident_blocks * (threads_per_block // WARP_SIZE)) / MAX_WARPS_PER_SM

    reported_occupancy = theoretical_occupancy(threads_per_block, regs_per_thread)

    print(f"threads_per_block={threads_per_block}, regs_per_thread={regs_per_thread}")
    print(f"Per-limiter resident blocks/SM -> thread: {thread_limit}, register: {reg_limit}, hw: {hw_limit}")
    print(f"Nsight-style achieved occupancy (binding limiter): {true_occupancy:.2%}")
    print(f"Calculator-reported theoretical occupancy:         {reported_occupancy:.2%}")

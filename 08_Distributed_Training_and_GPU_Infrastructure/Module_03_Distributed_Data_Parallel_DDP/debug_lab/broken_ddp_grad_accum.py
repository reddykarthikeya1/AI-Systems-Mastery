# Debug Lab: DDP Gradient Accumulation Produces an Oversized Effective Gradient
# Course 08 - Module 03 Distributed Data Parallel (DDP)

def local_accumulated_grad(microbatch_grads):
    """Sums a rank's per-microbatch gradients over one accumulation window,
    mirroring how DDP buckets gradients locally between sync points."""
    total = [0.0] * len(microbatch_grads[0])
    for g in microbatch_grads:
        for i, v in enumerate(g):
            total[i] += v
    return total


def allreduce_average(rank_grads):
    """DDP's cross-rank gradient sync: average the (already locally
    accumulated) gradient across all ranks."""
    world_size = len(rank_grads)
    width = len(rank_grads[0])
    return [sum(rank_grads[r][i] for r in range(world_size)) / world_size for i in range(width)]


def ddp_step_gradient(per_rank_microbatch_grads):
    accumulated = [local_accumulated_grad(mb) for mb in per_rank_microbatch_grads]
    return allreduce_average(accumulated)


if __name__ == "__main__":
    accumulation_steps = 4
    world_size = 2
    # Each rank ran `accumulation_steps` microbatches before syncing; every
    # microbatch on every rank happens to have gradient [1.0, 2.0] here.
    per_rank_microbatch_grads = [
        [[1.0, 2.0] for _ in range(accumulation_steps)] for _ in range(world_size)
    ]

    effective_grad = ddp_step_gradient(per_rank_microbatch_grads)
    single_microbatch_grad = [1.0, 2.0]

    print(f"world_size={world_size}, accumulation_steps={accumulation_steps}")
    print(f"Single-microbatch gradient (reference): {single_microbatch_grad}")
    print(f"DDP step's effective gradient:           {effective_grad}")
    print(f"Ratio to reference: {[round(a / b, 4) for a, b in zip(effective_grad, single_microbatch_grad)]}")

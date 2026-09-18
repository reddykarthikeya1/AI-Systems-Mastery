# Debug Lab: ZeRO Parameter Partitioning Silently Strands a Tail of Parameters
# Course 08 - Module 04 DeepSpeed ZeRO and PyTorch FSDP

def partition_ranges(num_params, world_size):
    """Returns a contiguous [start, end) shard range per rank, ZeRO-style:
    each rank owns and updates exactly one shard of the flattened parameters."""
    shard_size = num_params // world_size
    ranges = []
    start = 0
    for _ in range(world_size):
        ranges.append((start, start + shard_size))
        start += shard_size
    return ranges


def optimizer_update(param_ids, shard_ranges):
    """Simulates one optimizer step: each rank updates only the parameter
    indices that fall inside its own shard."""
    updated = set()
    for (lo, hi) in shard_ranges:
        for pid in param_ids:
            if lo <= pid < hi:
                updated.add(pid)
    return updated


if __name__ == "__main__":
    num_params = 10
    world_size = 4
    param_ids = list(range(num_params))

    shard_ranges = partition_ranges(num_params, world_size)
    updated = optimizer_update(param_ids, shard_ranges)
    expected = set(param_ids)
    missing = sorted(expected - updated)

    print(f"num_params={num_params}, world_size={world_size}")
    print(f"Shard ranges per rank: {shard_ranges}")
    print(f"Parameters updated by some rank:  {sorted(updated)}")
    print(f"Parameters that should be updated: {sorted(expected)}")
    print(f"Never-updated (stale) parameter indices: {missing}")

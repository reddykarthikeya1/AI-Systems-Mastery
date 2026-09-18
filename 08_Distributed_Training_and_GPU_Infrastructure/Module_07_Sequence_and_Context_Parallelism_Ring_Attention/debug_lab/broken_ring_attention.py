"""Broken Ring Attention Circular Shift Simulation."""
def ring_shift(kv_blocks: list[int], step: int, rank: int, world_size: int) -> int:
    source_rank = (rank - step)
    return kv_blocks[source_rank]

if __name__ == '__main__':
    world_size = 4
    blocks = [10, 20, 30, 40]
    # Rank 1 step 2 should get block from (1 - 2) % 4 = 3 (block 40)
    res = ring_shift(blocks, step=2, rank=1, world_size=world_size)
    print("Received block:", res)

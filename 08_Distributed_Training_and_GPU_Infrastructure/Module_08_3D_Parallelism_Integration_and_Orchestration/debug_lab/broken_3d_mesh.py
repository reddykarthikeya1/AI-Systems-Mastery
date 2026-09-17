"""Broken 3D Parallelism Rank Coordinate Decomposition."""
def get_3d_coordinates(global_rank: int, dp_size: int, pp_size: int, tp_size: int):
    # BUG: Incorrect rank layout assumes TP is the outermost dimension
    # Standard Megatron 3D layout: rank = pp * (tp * dp) + dp_id * tp + tp_id
    tp_id = global_rank % tp_size
    pp_id = (global_rank // tp_size) % pp_size  # BUG: Swapped with DP
    dp_id = global_rank // (tp_size * pp_size)
    return (dp_id, pp_id, tp_id)

if __name__ == '__main__':
    coords = [get_3d_coordinates(r, 2, 2, 4) for r in range(16)]
    print("Rank 4 coords:", coords[4])

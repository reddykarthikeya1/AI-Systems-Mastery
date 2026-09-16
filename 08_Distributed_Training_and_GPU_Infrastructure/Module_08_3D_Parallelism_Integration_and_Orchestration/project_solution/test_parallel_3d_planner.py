from __future__ import annotations

import pytest
from parallel_3d_planner import ClusterConfigPlanner, Parallel3DGrid


def test_3d_grid_coordinate_bijectivity():
    grid = Parallel3DGrid(tp=4, pp=2, dp=8)
    assert grid.world_size == 64

    for r in range(grid.world_size):
        coord = grid.get_coordinate(r)
        reconstructed_rank = grid.get_rank(coord.tp, coord.pp, coord.dp)
        assert reconstructed_rank == r


def test_orthogonal_communicator_groups():
    grid = Parallel3DGrid(tp=4, pp=2, dp=8)
    rank = 15
    # Rank 15 coordinate: tp=3, pp=1, dp=1
    coord = grid.get_coordinate(rank)
    assert coord.tp == 3 and coord.pp == 1 and coord.dp == 1

    tp_group = grid.get_tp_group(rank)
    assert len(tp_group) == 4
    assert rank in tp_group

    pp_group = grid.get_pp_group(rank)
    assert len(pp_group) == 2
    assert rank in pp_group

    dp_group = grid.get_dp_group(rank)
    assert len(dp_group) == 8
    assert rank in dp_group


def test_cluster_config_planner_evaluation():
    # 530B model on 80GB GPUs with TP=8, PP=8, DP=32
    plan_no_zero = ClusterConfigPlanner.evaluate_config(
        params_b=530.0, gpu_vram_gb=80.0, tp=8, pp=8, dp=32, use_zero1=False
    )
    # Should not fit without ZeRO (> 80GB static VRAM)
    assert plan_no_zero["feasible"] is False

    plan_zero = ClusterConfigPlanner.evaluate_config(
        params_b=530.0, gpu_vram_gb=80.0, tp=8, pp=8, dp=32, use_zero1=True
    )
    # Should fit with ZeRO-1 (~36GB static VRAM)
    assert plan_zero["feasible"] is True
    assert plan_zero["static_vram_per_gpu_gb"] < 40.0


def test_invalid_grid_initialization():
    with pytest.raises(ValueError, match="must be >= 1"):
        Parallel3DGrid(tp=0, pp=2, dp=4)

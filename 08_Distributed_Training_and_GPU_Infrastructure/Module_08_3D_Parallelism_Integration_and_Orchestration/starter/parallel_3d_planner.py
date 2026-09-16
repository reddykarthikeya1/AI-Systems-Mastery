from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class GridCoordinate:
    tp: int
    pp: int
    dp: int
    rank: int


class Parallel3DGrid:
    def __init__(self, tp: int, pp: int, dp: int):
        raise NotImplementedError("Implement Parallel3DGrid")

    def get_coordinate(self, rank: int) -> GridCoordinate:
        raise NotImplementedError("Implement get_coordinate")

    def get_rank(self, tp: int, pp: int, dp: int) -> int:
        raise NotImplementedError("Implement get_rank")

    def get_tp_group(self, rank: int) -> list[int]:
        raise NotImplementedError("Implement get_tp_group")

    def get_pp_group(self, rank: int) -> list[int]:
        raise NotImplementedError("Implement get_pp_group")

    def get_dp_group(self, rank: int) -> list[int]:
        raise NotImplementedError("Implement get_dp_group")


class ClusterConfigPlanner:
    @staticmethod
    def evaluate_config(
        params_b: float,
        gpu_vram_gb: float,
        tp: int,
        pp: int,
        dp: int,
        use_zero1: bool = False,
    ) -> dict[str, float | bool]:
        raise NotImplementedError("Implement evaluate_config")

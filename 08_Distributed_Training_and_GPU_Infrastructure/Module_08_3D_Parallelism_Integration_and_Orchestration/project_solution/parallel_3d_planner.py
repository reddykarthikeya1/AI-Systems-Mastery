from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class GridCoordinate:
    tp: int
    pp: int
    dp: int
    rank: int


class Parallel3DGrid:
    """Manages 3D Cartesian Grid coordinates and orthogonal communication groups."""

    def __init__(self, tp: int, pp: int, dp: int):
        if tp < 1 or pp < 1 or dp < 1:
            raise ValueError("All parallel degrees must be >= 1")
        self.tp = tp
        self.pp = pp
        self.dp = dp
        self.world_size = tp * pp * dp

    def get_coordinate(self, rank: int) -> GridCoordinate:
        if rank < 0 or rank >= self.world_size:
            raise ValueError(f"Rank {rank} out of bounds for world size {self.world_size}")
        r_tp = rank % self.tp
        r_pp = (rank // self.tp) % self.pp
        r_dp = rank // (self.tp * self.pp)
        return GridCoordinate(tp=r_tp, pp=r_pp, dp=r_dp, rank=rank)

    def get_rank(self, tp: int, pp: int, dp: int) -> int:
        if not (0 <= tp < self.tp and 0 <= pp < self.pp and 0 <= dp < self.dp):
            raise ValueError("Coordinate components out of bounds")
        return tp + pp * self.tp + dp * (self.tp * self.pp)

    def get_tp_group(self, rank: int) -> list[int]:
        """Ranks sharing identical PP and DP coordinates."""
        coord = self.get_coordinate(rank)
        return [self.get_rank(t, coord.pp, coord.dp) for t in range(self.tp)]

    def get_pp_group(self, rank: int) -> list[int]:
        """Ranks sharing identical TP and DP coordinates."""
        coord = self.get_coordinate(rank)
        return [self.get_rank(coord.tp, p, coord.dp) for p in range(self.pp)]

    def get_dp_group(self, rank: int) -> list[int]:
        """Ranks sharing identical TP and PP coordinates."""
        coord = self.get_coordinate(rank)
        return [self.get_rank(coord.tp, coord.pp, d) for d in range(self.dp)]


class ClusterConfigPlanner:
    """Validates memory and configuration feasibility for 3D parallel clusters."""

    @staticmethod
    def evaluate_config(
        params_b: float,
        gpu_vram_gb: float,
        tp: int,
        pp: int,
        dp: int,
        use_zero1: bool = False,
    ) -> dict[str, float | bool]:
        phi = params_b * 1e9
        model_states_gb = (16.0 * phi) / (1024**3)

        mp_size = tp * pp
        if not use_zero1:
            static_vram_per_gpu = model_states_gb / mp_size
        else:
            # ZeRO-1 shards the 12 bytes of optimizer state across DP
            weights_grads_gb = (4.0 * phi) / (1024**3 * mp_size)
            opt_gb = (12.0 * phi) / (1024**3 * mp_size * dp)
            static_vram_per_gpu = weights_grads_gb + opt_gb

        fits = static_vram_per_gpu < (gpu_vram_gb * 0.7)  # Leave 30% for activations
        return {
            "total_gpus": tp * pp * dp,
            "static_vram_per_gpu_gb": round(static_vram_per_gpu, 2),
            "feasible": fits,
        }

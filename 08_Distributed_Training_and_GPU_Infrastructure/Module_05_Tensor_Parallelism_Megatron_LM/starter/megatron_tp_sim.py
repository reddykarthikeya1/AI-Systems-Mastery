from __future__ import annotations

import numpy as np


class ColumnParallelLinearSim:
    def __init__(self, in_features: int, out_features: int, tp_size: int):
        raise NotImplementedError("Implement ColumnParallelLinearSim")

    def forward(self, x: np.ndarray, rank: int) -> np.ndarray:
        raise NotImplementedError("Implement forward")


class RowParallelLinearSim:
    def __init__(self, in_features: int, out_features: int, tp_size: int):
        raise NotImplementedError("Implement RowParallelLinearSim")

    def forward_local(self, x_slice: np.ndarray, rank: int) -> np.ndarray:
        raise NotImplementedError("Implement forward_local")

    def all_reduce_sum(self, partial_outputs: list[np.ndarray]) -> np.ndarray:
        raise NotImplementedError("Implement all_reduce_sum")


class MegatronMLPBlockSim:
    def __init__(self, hidden_dim: int, ffn_dim: int, tp_size: int):
        raise NotImplementedError("Implement MegatronMLPBlockSim")

    def forward_tp(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Implement forward_tp")

    def forward_monolithic(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Implement forward_monolithic")

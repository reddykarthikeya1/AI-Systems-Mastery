from __future__ import annotations

import numpy as np


class ColumnParallelLinearSim:
    """Simulates Megatron Column Parallel Linear Layer:

    Y_i = X * W_i
    Splits output features along columns.
    """

    def __init__(self, in_features: int, out_features: int, tp_size: int):
        if out_features % tp_size != 0:
            raise ValueError(f"out_features ({out_features}) must be divisible by tp_size ({tp_size})")
        self.in_features = in_features
        self.out_features = out_features
        self.tp_size = tp_size
        self.split_out = out_features // tp_size

        # Create reference monolithic weight and split columns
        self.master_weight = np.random.randn(in_features, out_features).astype(np.float32) * 0.02
        self.sharded_weights = [
            self.master_weight[:, r * self.split_out : (r + 1) * self.split_out]
            for r in range(tp_size)
        ]

    def forward(self, x: np.ndarray, rank: int) -> np.ndarray:
        """Each rank multiplies replicated X by its column slice W_i."""
        return np.matmul(x, self.sharded_weights[rank])


class RowParallelLinearSim:
    """Simulates Megatron Row Parallel Linear Layer:

    Y = sum(X_i * W_i) via All-Reduce.
    Splits input features along rows.
    """

    def __init__(self, in_features: int, out_features: int, tp_size: int):
        if in_features % tp_size != 0:
            raise ValueError(f"in_features ({in_features}) must be divisible by tp_size ({tp_size})")
        self.in_features = in_features
        self.out_features = out_features
        self.tp_size = tp_size
        self.split_in = in_features // tp_size

        self.master_weight = np.random.randn(in_features, out_features).astype(np.float32) * 0.02
        self.sharded_weights = [
            self.master_weight[r * self.split_in : (r + 1) * self.split_in, :]
            for r in range(tp_size)
        ]

    def forward_local(self, x_slice: np.ndarray, rank: int) -> np.ndarray:
        """Multiplies column-split activation by row-split weight."""
        return np.matmul(x_slice, self.sharded_weights[rank])

    def all_reduce_sum(self, partial_outputs: list[np.ndarray]) -> np.ndarray:
        """Simulates NCCL All-Reduce sum across all TP ranks."""
        return sum(partial_outputs)


class MegatronMLPBlockSim:
    """End-to-End Megatron-LM MLP block simulation:

    X -> ColumnParallelLinear -> GeLU -> RowParallelLinear -> All-Reduce -> Y
    """

    def __init__(self, hidden_dim: int, ffn_dim: int, tp_size: int):
        self.tp_size = tp_size
        self.col_layer = ColumnParallelLinearSim(hidden_dim, ffn_dim, tp_size)
        self.row_layer = RowParallelLinearSim(ffn_dim, hidden_dim, tp_size)

    @staticmethod
    def gelu(x: np.ndarray) -> np.ndarray:
        return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * np.power(x, 3))))

    def forward_tp(self, x: np.ndarray) -> np.ndarray:
        """Simulates distributed TP forward across all ranks."""
        # Step 1: Each rank computes column projection and GeLU
        partial_row_inputs = []
        for r in range(self.tp_size):
            y_col = self.col_layer.forward(x, rank=r)
            y_act = self.gelu(y_col)
            # Step 2: Each rank computes row projection
            y_partial = self.row_layer.forward_local(y_act, rank=r)
            partial_row_inputs.append(y_partial)

        # Step 3: Single All-Reduce Sum
        return self.row_layer.all_reduce_sum(partial_row_inputs)

    def forward_monolithic(self, x: np.ndarray) -> np.ndarray:
        """Reference monolithic single-GPU computation."""
        h1 = np.matmul(x, self.col_layer.master_weight)
        act = self.gelu(h1)
        return np.matmul(act, self.row_layer.master_weight)

from __future__ import annotations

import numpy as np


class ModelMemoryProfile:
    def __init__(self, params_b: float, world_size: int, precision_bytes: int = 2):
        raise NotImplementedError("Implement ModelMemoryProfile")

    def calculate_memory_gb(self) -> dict[str, float]:
        raise NotImplementedError("Implement calculate_memory_gb")


class ShardedParameterSimulator:
    def __init__(self, full_weights: list[np.ndarray], world_size: int):
        raise NotImplementedError("Implement ShardedParameterSimulator")

    def simulate_forward_layer(self, layer_idx: int, rank: int) -> np.ndarray:
        raise NotImplementedError("Implement simulate_forward_layer")

    def simulate_backward_layer(self, layer_idx: int, grad_full: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Implement simulate_backward_layer")

from __future__ import annotations

import dataclasses
import numpy as np


@dataclasses.dataclass
class ModelMemoryProfile:
    params_b: float  # Billion parameters
    world_size: int
    precision_bytes: int = 2  # 2 for FP16/BF16
    optimizer_precision_bytes: int = 4  # 4 for FP32 master + moments

    def calculate_memory_gb(self) -> dict[str, float]:
        phi = self.params_b * 1e9
        weight_bytes = phi * self.precision_bytes
        grad_bytes = phi * self.precision_bytes
        # Master weight (4) + Momentum (4) + Variance (4) = 12 bytes/param
        opt_bytes = phi * (3 * self.optimizer_precision_bytes)

        gb = 1024**3
        total_static_ddp = (weight_bytes + grad_bytes + opt_bytes) / gb
        zero_1 = (weight_bytes + grad_bytes + (opt_bytes / self.world_size)) / gb
        zero_2 = (weight_bytes + ((grad_bytes + opt_bytes) / self.world_size)) / gb
        zero_3 = (weight_bytes + grad_bytes + opt_bytes) / (self.world_size * gb)

        return {
            "DDP_Static_GB": round(total_static_ddp, 2),
            "ZeRO_1_GB": round(zero_1, 2),
            "ZeRO_2_GB": round(zero_2, 2),
            "ZeRO_3_FSDP_GB": round(zero_3, 2),
            "Communication_Overhead_Factor": {
                "DDP": 1.0,
                "ZeRO_1": 1.0,
                "ZeRO_2": 1.0,
                "ZeRO_3": 1.5,
            },
        }


class ShardedParameterSimulator:
    """Simulates ZeRO-3 / FSDP parameter sharding, All-Gather, and Discard lifecycle."""

    def __init__(self, full_weights: list[np.ndarray], world_size: int):
        self.world_size = world_size
        self.num_layers = len(full_weights)
        self.sharded_weights: list[list[np.ndarray]] = []

        # Shard each layer evenly across ranks
        for layer in full_weights:
            flat = layer.ravel()
            # Pad if needed
            pad_len = (world_size - (flat.size % world_size)) % world_size
            if pad_len > 0:
                flat = np.pad(flat, (0, pad_len))
            chunk_size = flat.size // world_size
            chunks = [flat[r * chunk_size : (r + 1) * chunk_size] for r in range(world_size)]
            self.sharded_weights.append(chunks)

    def simulate_forward_layer(self, layer_idx: int, rank: int) -> np.ndarray:
        """Simulates All-Gather for layer_idx, reconstructs full weights on rank, returns full array."""
        chunks = self.sharded_weights[layer_idx]
        # Simulates NCCL All-Gather
        gathered_full = np.concatenate(chunks)
        return gathered_full

    def simulate_backward_layer(self, layer_idx: int, grad_full: np.ndarray) -> np.ndarray:
        """Simulates Reduce-Scatter of gradients for layer_idx, returning local gradient chunk for rank."""
        flat_grad = grad_full.ravel()
        pad_len = (self.world_size - (flat_grad.size % self.world_size)) % self.world_size
        if pad_len > 0:
            flat_grad = np.pad(flat_grad, (0, pad_len))
        chunk_size = flat_grad.size // self.world_size
        # Each rank receives its slice of gradients
        return flat_grad[:chunk_size]

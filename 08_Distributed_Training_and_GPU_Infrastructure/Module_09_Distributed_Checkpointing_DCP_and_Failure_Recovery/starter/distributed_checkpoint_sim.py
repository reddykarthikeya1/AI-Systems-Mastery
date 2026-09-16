from __future__ import annotations

from pathlib import Path
import numpy as np


class DistributedCheckpointSim:
    def __init__(self, storage_dir: Path):
        raise NotImplementedError("Implement DistributedCheckpointSim")

    def save_sharded_checkpoint(
        self,
        step: int,
        tensor_name: str,
        rank_slices: list[np.ndarray],
    ) -> Path:
        raise NotImplementedError("Implement save_sharded_checkpoint")

    def load_resharded_checkpoint(
        self,
        ckpt_path: Path,
        target_num_ranks: int,
    ) -> list[np.ndarray]:
        raise NotImplementedError("Implement load_resharded_checkpoint")

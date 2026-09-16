from __future__ import annotations

import hashlib
import json
from pathlib import Path
import numpy as np


class DistributedCheckpointSim:
    """Simulates Distributed Checkpointing (DCP) parallel saving and dynamic resharding."""

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def compute_sha256(array: np.ndarray) -> str:
        return hashlib.sha256(array.tobytes()).hexdigest()

    def save_sharded_checkpoint(
        self,
        step: int,
        tensor_name: str,
        rank_slices: list[np.ndarray],
    ) -> Path:
        """Simulates parallel rank write of tensor chunks and metadata manifest."""
        ckpt_path = self.storage_dir / f"step_{step}"
        ckpt_path.mkdir(parents=True, exist_ok=True)

        manifest = {
            "step": step,
            "tensor_name": tensor_name,
            "total_ranks": len(rank_slices),
            "chunks": [],
        }

        # Each rank writes its chunk
        for r, chunk in enumerate(rank_slices):
            shard_filename = f"shard_{r}.npy"
            shard_file = ckpt_path / shard_filename
            np.save(shard_file, chunk)

            chunk_meta = {
                "rank": r,
                "shape": list(chunk.shape),
                "size": chunk.size,
                "file": shard_filename,
                "sha256": self.compute_sha256(chunk),
            }
            manifest["chunks"].append(chunk_meta)

        # Write manifest file
        manifest_file = ckpt_path / "metadata.json"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return ckpt_path

    def load_resharded_checkpoint(
        self,
        ckpt_path: Path,
        target_num_ranks: int,
    ) -> list[np.ndarray]:
        """Simulates loading and dynamically resharding to a different number of ranks."""
        manifest_file = ckpt_path / "metadata.json"
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Load and verify all saved chunks
        saved_chunks = []
        for chunk_meta in manifest["chunks"]:
            shard_file = ckpt_path / chunk_meta["file"]
            chunk_data = np.load(shard_file)
            # Verify checksum
            if self.compute_sha256(chunk_data) != chunk_meta["sha256"]:
                raise ValueError(f"Checksum mismatch on {shard_file}")
            saved_chunks.append(chunk_data)

        # Reconstruct logical global tensor
        global_tensor = np.concatenate(saved_chunks, axis=0)

        # Reshard across target_num_ranks
        if global_tensor.shape[0] % target_num_ranks != 0:
            raise ValueError(
                f"Global dimension {global_tensor.shape[0]} not divisible by target ranks {target_num_ranks}"
            )

        new_chunk_size = global_tensor.shape[0] // target_num_ranks
        target_slices = [
            global_tensor[r * new_chunk_size : (r + 1) * new_chunk_size]
            for r in range(target_num_ranks)
        ]
        return target_slices

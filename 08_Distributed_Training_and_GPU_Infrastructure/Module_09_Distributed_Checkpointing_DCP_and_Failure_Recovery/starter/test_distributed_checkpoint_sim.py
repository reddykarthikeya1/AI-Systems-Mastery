from __future__ import annotations

from pathlib import Path
import numpy as np
import pytest
from distributed_checkpoint_sim import DistributedCheckpointSim


def test_dcp_save_and_reshard_loading(tmp_path: Path):
    sim = DistributedCheckpointSim(storage_dir=tmp_path)

    # Master tensor partitioned across 4 ranks (TP=4)
    original_weights = np.arange(128, dtype=np.float32).reshape(16, 8)
    # 4 slices of shape (4, 8)
    rank_slices = [original_weights[r * 4 : (r + 1) * 4] for r in range(4)]

    ckpt_path = sim.save_sharded_checkpoint(
        step=100,
        tensor_name="transformer.layers.0.weight",
        rank_slices=rank_slices,
    )
    assert (ckpt_path / "metadata.json").exists()

    # Reshard to 2 ranks (TP=2) -> should produce 2 slices of shape (8, 8)
    resharded_2 = sim.load_resharded_checkpoint(ckpt_path, target_num_ranks=2)
    assert len(resharded_2) == 2
    assert resharded_2[0].shape == (8, 8)
    np.testing.assert_allclose(np.concatenate(resharded_2, axis=0), original_weights)


def test_dcp_checksum_tamper_detection(tmp_path: Path):
    sim = DistributedCheckpointSim(storage_dir=tmp_path)
    rank_slices = [np.ones((4, 4), dtype=np.float32) for _ in range(2)]
    ckpt_path = sim.save_sharded_checkpoint(
        step=200, tensor_name="weight", rank_slices=rank_slices
    )

    # Tamper with shard_0.npy
    shard_file = ckpt_path / "shard_0.npy"
    tampered_data = np.zeros((4, 4), dtype=np.float32)
    np.save(shard_file, tampered_data)

    # Must raise checksum error
    with pytest.raises(ValueError, match="Checksum mismatch"):
        sim.load_resharded_checkpoint(ckpt_path, target_num_ranks=2)

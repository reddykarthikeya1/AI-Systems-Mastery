from __future__ import annotations

import numpy as np
from zero_fsdp_engine import ModelMemoryProfile, ShardedParameterSimulator


def test_zero_memory_scaling():
    # 70B parameter model on 8 GPUs
    profile = ModelMemoryProfile(params_b=70.0, world_size=8)
    mem = profile.calculate_memory_gb()

    # DDP should be 16 * 70 GB = ~1120 GB per GPU in static state
    assert mem["DDP_Static_GB"] > 1000.0
    # ZeRO-3 should shard by world size 8: ~1120 / 8 = ~130-140 GB
    assert mem["ZeRO_3_FSDP_GB"] < 150.0
    assert mem["ZeRO_3_FSDP_GB"] < mem["ZeRO_1_GB"]
    assert mem["Communication_Overhead_Factor"]["ZeRO_3"] == 1.5


def test_sharded_parameter_simulation():
    # 3 layers of weights
    w1 = np.ones((64, 64), dtype=np.float32) * 1.5
    w2 = np.ones((64, 128), dtype=np.float32) * 2.5
    full_weights = [w1, w2]

    sim = ShardedParameterSimulator(full_weights, world_size=4)

    # Simulate forward pass on rank 2 for layer 0
    reconstructed = sim.simulate_forward_layer(layer_idx=0, rank=2)
    assert reconstructed.size == w1.size
    np.testing.assert_allclose(reconstructed, w1.ravel())

    # Simulate backward pass reduce-scatter
    grad_full = np.ones_like(w1) * 3.0
    local_grad = sim.simulate_backward_layer(layer_idx=0, grad_full=grad_full)
    assert local_grad.size == w1.size // 4

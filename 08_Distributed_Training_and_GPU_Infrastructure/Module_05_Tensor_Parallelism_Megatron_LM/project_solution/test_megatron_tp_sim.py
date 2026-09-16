from __future__ import annotations

import numpy as np
import pytest
from megatron_tp_sim import ColumnParallelLinearSim, MegatronMLPBlockSim


def test_megatron_mlp_mathematical_equivalence():
    np.random.seed(42)
    b, s, h, ffn = 2, 8, 32, 128
    tp_size = 4

    mlp = MegatronMLPBlockSim(hidden_dim=h, ffn_dim=ffn, tp_size=tp_size)
    x = np.random.randn(b, s, h).astype(np.float32)

    y_tp = mlp.forward_tp(x)
    y_ref = mlp.forward_monolithic(x)

    # Must match reference monolithic computation within floating point tolerance
    np.testing.assert_allclose(y_tp, y_ref, rtol=1e-5, atol=1e-5)


def test_tp_divisibility_validation():
    with pytest.raises(ValueError, match="divisible by tp_size"):
        ColumnParallelLinearSim(in_features=32, out_features=35, tp_size=4)

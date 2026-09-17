from __future__ import annotations

import numpy as np
from quantization_serving_sim import UniformQuantizer


def test_int8_quantization_and_reconstruction():
    np.random.seed(42)
    x = np.random.randn(64, 64).astype(np.float32)
    res = UniformQuantizer.quantize_symmetric(x, bits=8)

    assert res.compression_ratio == 4.0  # 32 / 8 = 4x
    assert res.mse_error < 0.001
    np.testing.assert_allclose(res.reconstructed, x, atol=0.05)


def test_smoothquant_mathematical_invariance():
    np.random.seed(42)
    b, h, out_dim = 4, 32, 64
    x = np.random.randn(b, h).astype(np.float32)
    w = np.random.randn(h, out_dim).astype(np.float32)

    # Reference unscaled product
    y_ref = np.matmul(x, w)

    # SmoothQuant transformed product
    x_smooth, w_smooth = UniformQuantizer.apply_smoothquant_transform(x, w, alpha=0.5)
    y_smooth = np.matmul(x_smooth, w_smooth)

    # Must be mathematically identical down to floating point precision
    np.testing.assert_allclose(y_smooth, y_ref, rtol=1e-5, atol=1e-5)

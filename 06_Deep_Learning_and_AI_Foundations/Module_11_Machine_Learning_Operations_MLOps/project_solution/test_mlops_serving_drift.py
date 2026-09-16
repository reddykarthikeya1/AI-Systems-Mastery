"""Unit tests for DynamicBatchingQueue and DataDriftDetector."""
from __future__ import annotations

import numpy as np
from mlops_serving_drift import DataDriftDetector, DynamicBatchingQueue


def test_dynamic_batching_packing():
    queue = DynamicBatchingQueue(max_batch_size=4)
    items = [np.ones(10) * i for i in range(6)]

    batch, lengths = queue.pack_batch(items)
    # Must cap at max_batch_size = 4
    assert batch.shape == (4, 10)
    assert len(lengths) == 4
    assert np.all(batch[2] == 2.0)


def test_data_drift_detector():
    np.random.seed(42)
    # Identical distributions should have low KS statistic
    baseline = np.random.normal(0.0, 1.0, size=500)
    normal_prod = np.random.normal(0.0, 1.0, size=500)
    ks_low = DataDriftDetector.compute_ks_statistic(baseline, normal_prod)
    assert ks_low < 0.15

    # Drifting distribution (shifted mean) must have high KS statistic
    drifted_prod = np.random.normal(3.0, 1.0, size=500)
    ks_high = DataDriftDetector.compute_ks_statistic(baseline, drifted_prod)
    assert ks_high > 0.8

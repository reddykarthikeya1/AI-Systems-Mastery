# Troubleshooting & Edge Cases: Distributed Data Parallel

## Production Traps & Silent Failure Modes

### 1. Desynchronized Batch Normalization
- **Symptom**: Model accuracy degrades when scaling from 8 GPUs to 128 GPUs.
- **Root Cause**: Standard BatchNorm computes mean and variance locally per GPU. When batch size per GPU shrinks to 2 samples, batch statistics become noisy and diverge across ranks.
- **Fix**: Replace BatchNorm with GroupNorm/LayerNorm, or convert to `torch.nn.SyncBatchNorm`.

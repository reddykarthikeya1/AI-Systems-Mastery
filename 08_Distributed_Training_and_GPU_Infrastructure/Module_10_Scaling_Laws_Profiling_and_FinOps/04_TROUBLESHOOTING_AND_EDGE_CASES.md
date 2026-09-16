# Module 10: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Profiling & FinOps

### Bug 1: SwiGLU MFU Over-estimation
- **Symptom**: Telemetry reports impossible MFU (> 70%) on Llama-2/3 models.
- **Root Cause**: Using standard $6\Phi$ FLOP formula while neglecting that SwiGLU has 3 linear matrices in the MLP rather than 2, under-counting true model FLOPs.
- **Fix**: Account for gated MLP expansion factor in analytical FLOP counters.

### Bug 2: PyTorch Profiler Memory Leak
- **Symptom**: Enabling `torch.profiler` triggers GPU OOM within 5 steps.
- **Root Cause**: Leaving profiler active for hundreds of steps accumulates millions of CUDA activity records in host RAM and VRAM.
- **Fix**: Use `schedule=torch.profiler.schedule(wait=2, warmup=2, active=3, repeat=1)` to capture a small window.

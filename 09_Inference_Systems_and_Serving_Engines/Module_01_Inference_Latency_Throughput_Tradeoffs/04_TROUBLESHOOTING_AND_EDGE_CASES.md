# Module 01: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Inference Serving

### Bug 1: Premature Client Disconnection Compute Leak
- **Symptom**: GPU utilization remains at 100%, but server throughput drops; client timeouts spike.
- **Root Cause**: When a client terminates an HTTP connection (e.g. browser tab closed or timeout), the serving engine continues generating tokens until `max_tokens` or `<eos>` is reached if cancellation signals are not propagated to the scheduler.
- **Fix**: Wire HTTP disconnect callbacks (`request.is_disconnected()`) directly to the serving engine queue to cancel active request IDs immediately.

### Bug 2: GPU Frequency Thermal Throttling
- **Symptom**: Steady-state TPOT increases by 25% after 2 hours of peak daytime traffic.
- **Root Cause**: Sustained high-concurrency GEMM kernels cause GPU core temperatures to exceed $83^{\circ}\text{C}$, triggering hardware throttling from $1.98 \text{ GHz}$ down to $1.45 \text{ GHz}$.
- **Fix**: Monitor `nvidia-smi --query-gpu=clocks.current.graphics,temperature.gpu` and configure rack fan curves or reduce batch size concurrency caps.

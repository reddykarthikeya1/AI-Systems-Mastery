# Module 07: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Context Parallelism

### Bug 1: Running Online Softmax Scale Drift in FP16
- **Symptom**: Attention output diverges or generates `NaN` after 16 ring steps when running in native FP16.
- **Root Cause**: When computing $e^{m_{\text{old}} - m_{\text{new}}}$, if $m_{\text{new}} - m_{\text{old}} > 11$, underflow in FP16 collapses running scale to exact 0.
- **Fix**: Always accumulate online softmax running stats ($m, l$) in FP32 precision (`float32`), even when inputs and outputs are FP16 or BF16.

### Bug 2: Double Buffering P2P Stream Race Condition
- **Symptom**: Inconsistent generation or nondeterministic loss spikes.
- **Root Cause**: Reading incoming $K, V$ buffers before the background `dist.irecv` CUDA stream has completed synchronization.
- **Fix**: Use two ping-pong buffers (`buffer_curr` and `buffer_next`) and record CUDA events (`event.record()`, `stream.wait_event(event)`) to enforce hardware ordering.

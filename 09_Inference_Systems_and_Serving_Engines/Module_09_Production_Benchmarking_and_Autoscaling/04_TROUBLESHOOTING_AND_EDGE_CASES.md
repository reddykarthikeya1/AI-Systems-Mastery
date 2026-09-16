# Module 09: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Autoscaling

### Bug 1: Cold Start Connection Timeout
- **Symptom**: When autoscaler spins up a new pod, clients routed to the new pod experience 60-second connection timeouts.
- **Root Cause**: Loading 140 GB weights into VRAM takes 45 seconds. Kubernetes marks the pod as "Ready" before the vLLM engine finishes warm-up initialization.
- **Fix**: Configure a custom HTTP readiness probe pointing to `/health` that returns 200 ONLY after model weights are loaded and warm-up dummy forward passes have succeeded.

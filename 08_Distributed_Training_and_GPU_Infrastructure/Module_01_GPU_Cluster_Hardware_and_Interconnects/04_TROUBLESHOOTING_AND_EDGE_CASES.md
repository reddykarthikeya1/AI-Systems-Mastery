# Troubleshooting & Edge Cases: Cluster Hardware & Interconnects

## Production Traps & Silent Failure Modes

### 1. InfiniBand Cable Degradation & Flapping Links
- **Symptom**: A 1,024-GPU training run exhibits random 30% performance drops without any crash or error logs.
- **Root Cause**: A single degraded optical transceiver on one switch port drops from 400 Gbps (NDR) to 100 Gbps (EDR) or experiences packet retransmissions.
  - Because synchronous Ring AllReduce requires every node to pass data to its neighbor, the entire 1,024-GPU cluster slows down to the speed of the slowest link!
- **Fix**: Run periodic network health sweeps (`ibdiagnet`, `nccl-tests`) and quarantine degraded links automatically.

# Project Guide: Distributed Checkpointing (DCP) & Recovery

## Overview
Implement a resilient, asynchronous Distributed Checkpointing engine with dynamic resharding support.

## Architectural Requirements
1. **Parallel Sharded I/O**: Direct per-rank chunk writing with global metadata manifest generation.
2. **Dynamic Resharding**: Seamlessly load and slice checkpoints across disparate rank counts ($TP_1 \to TP_2$).
3. **Data Integrity & Consensus**: SHA-256 integrity verification to detect bit flips and interrupted writes.

## Workspaces
- `starter/distributed_checkpoint_sim.py`: Starter interfaces and stubs.
- `project_solution/distributed_checkpoint_sim.py`: Production reference implementation.
- `project_solution/test_distributed_checkpoint_sim.py`: Pytest test suite.

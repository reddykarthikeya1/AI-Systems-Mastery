# Project Guide: Scaling Laws, Profiling & FinOps

## Overview
Implement analytical Model FLOPs Utilization (MFU) analyzers and Chinchilla compute-optimal allocation engines.

## Architectural Requirements
1. **Transformer FLOP Math**: Exact $6\Phi$ (standard) and $8\Phi$ (activation checkpointing) forward/backward accounting.
2. **Chinchilla Optimization**: Lagrange multiplier parameter $N$ and token $D$ allocation for fixed FLOP budgets.
3. **Cluster FinOps**: Hourly cost modeling and dollar loss calculation for low-MFU training anomalies.

## Workspaces
- `starter/scaling_laws_finops.py`: Starter interfaces and stubs.
- `project_solution/scaling_laws_finops.py`: Production reference implementation.
- `project_solution/test_scaling_laws_finops.py`: Pytest test suite.

# Project Guide: 3D Parallelism Integration & Orchestration

## Overview
Implement a Cartesian 3D Grid Coordinate Planner for Megatron-DeepSpeed $(TP \times PP \times DP)$ clusters.

## Architectural Requirements
1. **Bijective Mapping**: Guarantee $R \leftrightarrow (r_{\text{tp}}, r_{\text{pp}}, r_{\text{dp}})$ 1-to-1 correspondence.
2. **Orthogonal Communicator Partitioning**: Form deterministic TP, PP, and DP process groups.
3. **FinOps & VRAM Sizing**: Validate static and activation memory feasibility for arbitrary parameter counts.

## Workspaces
- `starter/parallel_3d_planner.py`: Starter interfaces and stubs.
- `project_solution/parallel_3d_planner.py`: Production reference implementation.
- `project_solution/test_parallel_3d_planner.py`: Pytest test suite.

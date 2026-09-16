# Project Guide: Sequence & Context Parallelism (Ring Attention)

## Overview
Implement a high-performance simulation of **Ring Attention with Online Softmax Tracking** across arbitrary context-parallel ranks.

## Architectural Requirements
1. **Online Softmax Invariant**: Maintain numerical stability via running row-max $m_r$ and scale adjustments.
2. **Causal Mask Support**: Support triangular diagonal masking and skipped computation for strictly future blocks.
3. **Equivalence Validation**: Prove bitwise and floating-point equivalence against monolithic full-sequence attention.

## Workspaces
- `starter/ring_attention_sim.py`: Starter interfaces and stubs.
- `project_solution/ring_attention_sim.py`: Production reference implementation.
- `project_solution/test_ring_attention_sim.py`: Pytest test suite.

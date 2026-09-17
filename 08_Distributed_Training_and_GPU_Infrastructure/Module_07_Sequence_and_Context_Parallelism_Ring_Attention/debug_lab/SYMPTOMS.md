# Symptoms: Deadlock and Value Drift in Ring Attention Circular Shift

## Issue Description
During context parallelism over long sequences (64k tokens across 8 GPUs), the ring attention collective deadlocks or produces corrupted attention outputs after the second step of the ring rotation.

## Reproduction
Run `python broken_ring_attention.py`. The circular buffer step skips block index updates, causing rank 0 to consume stale KV blocks.

## Diagnostic Questions
1. How must KV blocks rotate across a circular ring of P processes?
2. What happens if the send-receive buffer pointers are overwritten before the attention calculation finishes?

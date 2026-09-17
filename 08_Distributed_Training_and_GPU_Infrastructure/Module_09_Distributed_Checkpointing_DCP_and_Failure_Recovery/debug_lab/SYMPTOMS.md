# Symptoms: Sharded Checkpoint Key Overwrite & Truncated State

## Issue Description
During distributed checkpointing with PyTorch DCP across 8 ranks, the saved checkpoint directory is corrupted and only contains rank 7's slice because each worker writes to a non-unique shard filename.

## Reproduction
Run `python broken_dcp.py`.

# Module 09: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Distributed Checkpointing

### Bug 1: Partial Write from Dead Rank Corrupts Manifest
- **Symptom**: Checkpoint restore fails with `CorruptedCheckpointError: Incomplete shard`.
- **Root Cause**: If Rank 47 dies mid-write and Rank 0 writes the `.metadata` manifest without checking completion consensus, the checkpoint directory is irreversibly broken.
- **Fix**: Use two-phase commit: All ranks write to temporary directory `ckpt_tmp_step/`. An `All-Reduce` consensus barrier confirms all ranks completed successfully. Rank 0 atomically renames directory to `ckpt_step/`.

### Bug 2: Silent Data Corruption (Bit Flips)
- **Symptom**: Checkpoint loads cleanly, but evaluation loss increases from 1.8 to 8.4 instantly.
- **Root Cause**: Bit-flip in parallel filesystem transit or storage drive bad blocks without checksum verification.
- **Fix**: Store SHA-256 or CRC32 checksums for every chunk in the manifest and verify hashes during read.

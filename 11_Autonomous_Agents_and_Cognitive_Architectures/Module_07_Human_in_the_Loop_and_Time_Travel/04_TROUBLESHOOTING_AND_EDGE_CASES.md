# Troubleshooting & Production Edge Cases

### 1. Checkpoint Deserialization Failures
- **Symptom**: `TypeError: Object of type CustomTool is not JSON serializable` when saving checkpoint.
- **Root Cause**: Non-serializable objects (sockets, class instances) stored in state channels.
- **Fix**: Restrict state variables to JSON-serializable primitives, Pydantic models, or dataclasses.

### 2. Phantom Resumption on Race Conditions
- **Symptom**: Two human reviewers click approve simultaneously, causing double payments.
- **Root Cause**: Lack of optimistic concurrency locking on checkpoint status.
- **Fix**: Use conditional SQL updates: `UPDATE checkpoints SET status='RESUMED' WHERE id=:id AND status='PENDING'`.

# Module 07: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Speculative Decoding

### Bug 1: KV-Cache Rollback Pointer Corruption
- **Symptom**: Model produces repetitious nonsense after the first rejected speculative token.
- **Root Cause**: When speculative tokens are rejected, the engine must roll back the target model's KV cache pointers to erase the rejected tokens. Failing to decrement the sequence length in the block manager leaves phantom tokens in the attention cache.
- **Fix**: Roll back KV cache block slot index to $S_{\text{accepted}}$ immediately upon rejection.

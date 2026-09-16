# Troubleshooting & Edge Cases: Hopper & FlashAttention-3

## Production Traps & Silent Failure Modes

### 1. `mbarrier` Transaction Count Desynchronization
- **Symptom**: Kernel hangs indefinitely (deadlock) on H100 with 0% SM activity.
- **Root Cause**: The transaction count passed to `mbarrier.arrive_and_expect_tx(bytes)` does not match the exact number of bytes transferred by the TMA instruction.
  - The hardware barrier never flips phase, so compute threads wait forever.
- **Fix**: Verify that `expected_bytes == tile_rows * tile_cols * sizeof(element)`.

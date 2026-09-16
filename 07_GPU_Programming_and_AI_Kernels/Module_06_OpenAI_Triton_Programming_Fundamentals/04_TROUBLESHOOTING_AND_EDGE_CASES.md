# Troubleshooting & Edge Cases: OpenAI Triton

## Production Traps & Silent Failure Modes

### 1. Non-Power-of-Two Block Sizes
- **Symptom**: Triton compilation error: `BLOCK_SIZE must be a power of 2`.
- **Root Cause**: Triton's code generator relies on binary power-of-two decompositions to generate efficient SIMD shuffle instructions and memory mask registers.
- **Fix**: Always define `BLOCK_SIZE` as a power of 2 (e.g. 32, 64, 128, 256, 512, 1024) and use boolean masking `offsets < N` to handle arbitrary boundary lengths.

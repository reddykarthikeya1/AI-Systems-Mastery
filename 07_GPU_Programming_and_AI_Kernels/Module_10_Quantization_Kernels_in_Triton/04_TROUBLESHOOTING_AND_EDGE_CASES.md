# Troubleshooting & Edge Cases: Quantization Kernels

## Production Traps & Silent Failure Modes

### 1. Sign Extension Bugs in INT4 Unpacking
- **Symptom**: Negative weights unpack as large positive integers (e.g. -1 becomes 15).
- **Root Cause**: Performing bitwise operations without proper signed two's complement extension:
  `int4_val = (packed >> 4) & 0x0F; // Treats 0x0F as +15 instead of -1!`
- **Fix**: Sign-extend using bit arithmetic:
  `int8_val = (int8_t)(nibble << 4) >> 4; // Preserves sign bit!`

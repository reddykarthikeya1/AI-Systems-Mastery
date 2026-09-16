# Module 08: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Model Quantization

### Bug 1: Dequantization Kernel Register Spilling
- **Symptom**: Custom INT4 kernel runs slower than unquantized FP16 PyTorch baseline.
- **Root Cause**: Uncoalesced bit-unpacking logic causes high register pressure ($> 64$ registers per thread), forcing register spills into local GPU DRAM.
- **Fix**: Use optimized assembly-level packed GEMM kernels (like Marlin or GPTQ-Triton).

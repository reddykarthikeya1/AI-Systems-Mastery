# Self-Assessment & Staff Interview Challenges: OpenAI Triton

## Architectural Interview Scenarios

### Question 1: Triton vs CUDA Performance Parity
**Scenario**: In which workloads does Triton match or exceed hand-tuned CUDA C++, and where does it fall short?

**Staff-Level Solution**:
- **Where Triton Excels**:
  1. Fused elementwise and normalization kernels (LayerNorm, RMSNorm, GeLU, Softmax). Triton matches or beats cuDNN because fusion saves DRAM traffic and Triton's register allocator is state-of-the-art.
  2. FlashAttention and specialized GEMM variants. Triton allows rapid exploration of tile sizes (`BLOCK_M`, `BLOCK_N`) without rewriting complex assembly.
- **Where CUDA C++ / CUTLASS Wins**:
  1. Deeply pipelined Tensor Core GEMMs on Hopper/Blackwell using asynchronous TMA and WGMMA instructions.
  2. Custom warp-specialized architectures where specific warps are pinned to memory loading while other warps are dedicated to math.

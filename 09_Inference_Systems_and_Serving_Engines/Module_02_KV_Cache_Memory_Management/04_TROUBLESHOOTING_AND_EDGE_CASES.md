# Module 02: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in KV Cache Management

### Bug 1: Unexpected OOM on Sequence Length Boundary
- **Symptom**: Server functions normally for 10,000 requests, then crashes with CUDA OOM when a single request reaches token 4,097.
- **Root Cause**: The KV allocator pre-allocated memory in powers-of-two (e.g., buffer sizes 1024, 2048, 4096). When token 4,097 arrived, the allocator attempted to allocate an 8,192-token contiguous chunk, triggering an immediate out-of-memory exception.
- **Fix**: Decouple physical memory allocation from power-of-two doubling by adopting fixed-size block paging (PagedAttention).

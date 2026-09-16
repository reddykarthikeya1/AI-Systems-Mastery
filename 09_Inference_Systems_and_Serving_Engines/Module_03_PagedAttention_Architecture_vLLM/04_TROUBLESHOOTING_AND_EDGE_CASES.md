# Module 03: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in PagedAttention

### Bug 1: Reference Counting Memory Leak
- **Symptom**: GPU memory fills up over 24 hours of operation, even though active concurrent request count is constant.
- **Root Cause**: When aborting an in-flight branched request, the scheduler frees the parent request's block table but fails to decrement `ref_count` on shared prefix blocks, orphaning physical blocks in the allocator.
- **Fix**: Implement an atomic `decref()` cascade on all physical blocks registered in a sequence's block table upon request termination.

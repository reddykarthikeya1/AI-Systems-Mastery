# Module 04: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Prefix Caching

### Bug 1: Cache Eviction Deadlock
- **Symptom**: Server hangs when GPU memory reaches 99%; no new requests are admitted.
- **Root Cause**: All tree nodes have `ref_count > 0` because client requests are paused waiting for memory, creating a circular wait: the allocator waits for requests to finish to evict nodes, but requests wait for the allocator to assign new blocks!
- **Fix**: Implement preemption: abort or swap out the longest running request to break the cycle.

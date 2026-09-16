# Module 04: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Prefix Cache Hit Rate Degradation in Production
**Question**: After deploying SGLang with RadixAttention for a multi-tenant enterprise app, telemetry reports that prefix cache hit rate is only 4%, despite all users sharing an identical 2,500-token prompt template. Investigation shows the developer added dynamic session timestamps (`f"Current time: {datetime.now()}"`) at the very top of the system prompt. Explain the catastrophic impact on RadixAttention and prescribe the architectural fix.

**Solution**:
1. **Root Cause**: Radix trees match strictly from the root ($t_0, t_1, \dots$). Placing dynamic, non-deterministic tokens (like current timestamp or unique request UUID) at token positions $0 \dots 10$ causes the prefix lookup to diverge from the root on token 5. The subsequent 2,490 identical tokens are never matched, forcing a full 2,500-token prefill on every single request.
2. **Remedy**:
   - **Template Canonicalization**: Move all static, invariant prompt text (system instructions, tool schemas, few-shot examples) to the beginning of the prompt.
   - Place all dynamic, request-specific context (timestamps, user query, session IDs) strictly at the suffix.
   - Cache hit rate immediately restores to $> 95\%$.

---

### Scenario 2: Radix Tree Concurrency & Lock Contention
**Question**: Under 5,000 QPS, CPU profiling reveals that worker threads spend 35% of their execution time waiting on the Radix Tree global lock during prefix lookup and insertion. How do you scale prefix tree access to high concurrency?

**Solution**:
1. Use **Read-Copy-Update (RCU)** or fine-grained read-write locks (`pthread_rwlock` / `tbb::concurrent_hash_map` for child edges).
2. Multiple threads can perform simultaneous read-only traversals without locking.
3. Node splitting and leaf eviction acquire write locks localized strictly to the immediate parent and affected child node rather than locking the entire tree.

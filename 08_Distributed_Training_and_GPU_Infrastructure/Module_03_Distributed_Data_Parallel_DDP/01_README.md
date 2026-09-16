# Module 03: Distributed Data Parallel (DDP)

> **Architectural Scope**: PyTorch DDP Architecture, Gradient Bucketing (25 MB), Autograd Backward Hooks, Ring AllReduce Overlap, and Synchronization Invariants.

---

## 1. DDP System Architecture

```
+-----------------------------------------------------------------------------------------------+
| PYTORCH DDP OVERLAPPED BACKWARD PASS EXECUTION TIMELINE                                       |
+-----------------------------------------------------------------------------------------------+
| Time -->                                                                                      |
| Compute (Backward Pass): [ Layer 4 Backprop ] [ Layer 3 Backprop ] [ Layer 2 ] [ Layer 1 ]    |
| Communication (NCCL):                         [ Bucket 1 AllReduce ]   [ Bucket 0 AllReduce ] |
|                                               ^                                               |
|                                               Overlap hides 70-90% of network communication!  |
+-----------------------------------------------------------------------------------------------+
```

---

## 2. Autograd Hook Mechanics
In PyTorch DDP, each parameter tensor registers a `post_accumulate_grad_hook`:
1. When autograd writes `param.grad`, the hook fires.
2. The hook copies the gradient into its pre-allocated 25MB contiguous bucket buffer.
3. Once all parameters in the bucket have fired, DDP issues an asynchronous `dist.all_reduce(bucket)`.

---

## 3. Module Study Progression
1. **Beginner Playground**: Read [00_W3_BEGINNER_PLAYGROUND.md](00_W3_BEGINNER_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).

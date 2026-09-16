# Troubleshooting & Edge Cases: Hash Tables & Collision Resolution

## Common Bugs & Pitfalls
- **Off-By-One Errors**: Fencepost issues on boundary intervals $[0, N-1]$.
- **Null / None Dereferencing**: Accessing `.next` or `.left` without checking if node is `None`.
- **Recursion Depth Exceeded**: Deep trees causing Python `RecursionError` (mitigate via iterative traversal + explicit stack).
- **Memory Leaks**: Cyclic references preventing garbage collection in bidirectional pointers.

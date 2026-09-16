# Troubleshooting & Edge Cases: Memory Hierarchy & Coalescing

## Production Traps & Silent Failure Modes

### 1. Structure of Arrays (SoA) vs Array of Structures (AoS)
- **Symptom**: Custom object kernel runs at 20% of memory bandwidth.
- **Root Cause**: Storing data as `struct Particle { float x, y, z, mass; } particles[N];`.
  - When threads read `particles[i].x`, Thread 0 reads byte 0, Thread 1 reads byte 16, Thread 2 reads byte 32.
  - Stride is 16 bytes, causing uncoalesced memory reads!
- **Fix**: Convert to Structure of Arrays:
  `struct Particles { float *x; float *y; float *z; float *mass; };`
  Now `x[threadIdx.x]` reads contiguous 4-byte floats, achieving 100% coalescing.

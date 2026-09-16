# Troubleshooting & Production Edge Cases

### 1. AST Bypass via String Obfuscation
- **Symptom**: Code executes `getattr(__builtins__, 'ev' + 'al')` and bypasses direct name checks.
- **Root Cause**: The AST visitor checked only `ast.Name` nodes rather than dynamic `ast.Call` on `getattr`.
- **Fix**: Ban `getattr`, `setattr`, and private attribute access (`node.attr.startswith('_')`).

### 2. Fork Bomb Deadlocks in Subprocesses
- **Symptom**: Worker server runs out of PIDs and hangs.
- **Root Cause**: Untrusted code spawned infinite threads or processes (`while True: os.fork()`).
- **Fix**: Enforce OS-level process limits (`ulimit -u` / `RLIMIT_NPROC`) and use cgroups to cap process spawning.

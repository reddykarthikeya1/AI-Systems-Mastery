# Module 09: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Context Optimization

### Bug 1: Accidental Context Pruning of Negation Terms
- **Symptom**: Model answers the opposite of the truth (e.g. asserts a refund is allowed when the policy expressly forbids it).
- **Root Cause**: Heuristic compression algorithms pruned the word `"never"` or `"except"` because it had high frequency in the corpus.
- **Fix**: Never prune tokens from a protected list of semantic modulators (`"not"`, `"no"`, `"never"`, `"except"`, `"unless"`).

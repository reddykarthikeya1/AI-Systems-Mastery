# Troubleshooting & Production Edge Cases

### 1. Recency Decay Overwhelming High-Value Historic Memories
- **Symptom**: The agent forgets a user's name or fundamental preference declared 3 days ago.
- **Root Cause**: Recency decay factor $\lambda$ was too aggressive, reducing the recency component to zero.
- **Fix**: Boost the importance weight $w_i$ for high-importance items ($importance \ge 8$) or store core facts in semantic memory which has zero recency decay.

### 2. Hallucinated Reflections During Memory Consolidation
- **Symptom**: Agent forms incorrect beliefs about the user during the reflection step.
- **Root Cause**: Reflection prompt lacked citation requirements.
- **Fix**: Require the reflection LLM to output source memory IDs for every synthesized insight.

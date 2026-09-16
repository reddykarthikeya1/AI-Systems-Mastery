# Troubleshooting & Production Edge Cases

### 1. Intent Clashing in Colang Flows
- **Symptom**: User asks "How does political risk affect AWS billing?" and gets blocked by the politics rail.
- **Root Cause**: Greedy keyword matching flagged "political" without checking customer service context.
- **Fix**: Require multi-token intent matches or contextual intent classifier with confidence scoring.

### 2. False Positives on Cybersecurity Education
- **Symptom**: User asks "What is a SQL injection vulnerability?" and Llama Guard blocks as S6 Cyberattack.
- **Root Cause**: Dual-use capability confusion.
- **Fix**: Refine safety rubric to distinguish defensive conceptual explanations from actionable exploit code generation.

# Troubleshooting & Production Edge Cases

### 1. Judge False Refusal (Over-Refusal Bias)
- **Symptom**: Red-teaming judge marks benign responses as safety violations.
- **Root Cause**: Safety judge flagged presence of toxic words in the *quote* of user input.
- **Fix**: Direct the safety judge to evaluate only the model's *actionable advice*, not echoed text.

### 2. Mutation Stagnation
- **Symptom**: Attacker LLM generates identical paraphrases across iterations.
- **Root Cause**: Low temperature sampling ($T=0.0$) on attacker LLM.
- **Fix**: Increase attacker temperature to $T=0.8 - 1.0$ and sample top-p.

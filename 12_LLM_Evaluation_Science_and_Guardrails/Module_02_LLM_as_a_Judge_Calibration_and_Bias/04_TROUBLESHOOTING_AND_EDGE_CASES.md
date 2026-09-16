# Troubleshooting & Production Edge Cases

### 1. High Tie Rates Due to Overly Strict Agreement Criteria
- **Symptom**: Swap-pair evaluation outputs 85% Ties.
- **Root Cause**: The judge outputs slight differences in reasoning between runs that cause opposite votes on minor nuances.
- **Fix**: Use numeric scoring rubrics (e.g. 1-10) in both permutations and declare a winner if the average margin exceeds an epsilon threshold $\epsilon = 1.0$.

### 2. Format Inconsistency in Judge Explanations
- **Symptom**: Judge fails to emit `[[A]]` or `[[B]]` winner delimiter.
- **Root Cause**: Judge LLM generates conversational justification without following output schema.
- **Fix**: Enforce structured JSON output via tool calling or constrained grammar decoding.

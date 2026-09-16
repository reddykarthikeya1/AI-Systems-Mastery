# Troubleshooting & Production Edge Cases

### 1. Token F1 Skew on Numeric Strings
- **Symptom**: Model generates `"1,000,000"` but target is `"1000000"`, yielding 0.0 F1 score.
- **Root Cause**: Naive whitespace tokenization splits numbers with commas into separate tokens.
- **Fix**: Normalize numeric strings and remove internal commas before tokenizing.

### 2. Over-Segmentation in Claim Decomposition
- **Symptom**: Claim extractor splits `"Dr. Smith visited New York"` into three fragmented claims.
- **Root Cause**: Splitting on periods without recognizing honorific abbreviations or decimal numbers.
- **Fix**: Use regex with negative lookahead for common abbreviations: `r"(?<!\b(?:Dr|Mr|Mrs|Ms|vs|e\.g|i\.e))\.\s+"`.

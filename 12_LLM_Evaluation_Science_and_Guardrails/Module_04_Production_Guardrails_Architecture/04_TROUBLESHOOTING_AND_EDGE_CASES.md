# Troubleshooting & Production Edge Cases

### 1. Credit Card Luhn Algorithm False Positives
- **Symptom**: 16-digit product serial numbers are masked as credit cards.
- **Root Cause**: Regex only validated digit count without validating the Luhn checksum algorithm.
- **Fix**: Apply Luhn formula validation to candidate 16-digit matches before masking.

### 2. Broken Anonymization Due to Pluralization / Inflection
- **Symptom**: Anonymizer replaces `"Alice"` with `"<PERSON_1>"`, but misses `"Alice's"`.
- **Root Cause**: Exact string match without stemmer or possessive handling.
- **Fix**: Strip possessive suffixes (`'s`) during entity detection and apply mapping to both root and inflected forms.

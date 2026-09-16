# Troubleshooting & Production Edge Cases

### 1. False Positives on Software Engineering Documentation
- **Symptom**: User asking "How do I ignore previous commits in git?" gets flagged as prompt injection.
- **Root Cause**: Substring match on "ignore previous".
- **Fix**: Require exact multi-phrase matches: `ignore (?:all )?previous instructions`.

### 2. High Overhead on Random Base64 False Matches
- **Symptom**: Long URLs with alphanumeric query params trigger hundreds of failed Base64 decodes.
- **Root Cause**: Regex matched arbitrary 8-char strings.
- **Fix**: Enforce valid Base64 padding checks (`len(s) % 4 == 0`) and verify that decoded bytes form valid UTF-8 strings.

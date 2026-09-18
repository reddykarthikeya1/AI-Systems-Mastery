# Debug Lab Incident Report: PII Guardrail Passes Social Security Numbers, Card Numbers, and Emails Straight Through Unredacted

- **Severity:** P0 Data Privacy / Compliance
- **Affected Subsystem:** Module_04_Production_Guardrails_Architecture
- **Reported Impact:** A compliance audit of chat transcripts found that customer SSNs, credit card numbers, and email addresses typed into the chat were logged and forwarded downstream completely unredacted -- the guardrail that was supposed to scrub this data before logging or forwarding had no effect on it whatsoever.

---

## 🚨 Observable Symptoms & Logs
```text
Original message:  My SSN is 219-09-9999 and my card is 4111-1111-1111-1111, reach me at alice@example.com
Sanitized message: My SSN is 219-09-9999 and my card is 4111-1111-1111-1111, reach me at alice@example.com
Output identical to input (nothing redacted): True
SSN still present in sanitized output: True
Credit card number still present in sanitized output: True
Email address still present in sanitized output: True
```
Calling `sanitize()` on a message returns without error, and the returned value looks like a normal string -- there's no exception or obviously malformed output to flag it. Comparing the "sanitized" output to the original input character-for-character shows they are identical: every piece of PII in the message (the SSN, the card number, the email address) is present in the output exactly as it was in the input.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_Production_Guardrails_Architecture/debug_lab
   ```
2. `broken_guardrail.py` only defines `BrokenGuardrail`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_guardrail import BrokenGuardrail

   guardrail = BrokenGuardrail()
   user_message = "My SSN is 219-09-9999 and my card is 4111-1111-1111-1111, reach me at alice@example.com"

   sanitized = guardrail.sanitize(user_message)

   print(f"Original message:  {user_message}")
   print(f"Sanitized message: {sanitized}")
   print(f"Output identical to input (nothing redacted): {sanitized == user_message}")
   print(f"SSN still present in sanitized output: {'219-09-9999' in sanitized}")
   print(f"Credit card number still present in sanitized output: {'4111-1111-1111-1111' in sanitized}")
   print(f"Email address still present in sanitized output: {'alice@example.com' in sanitized}")
   ```
3. Observe that `sanitized == user_message` is `True` -- the guardrail's output is byte-for-byte identical to its input, for a message containing three distinct categories of PII.

---

## 🎯 Your Objective
1. Inspect `sanitize()` -- what transformation, if any, does it apply to `text` before returning it?
2. Run it on a message containing an SSN, a card number, and an email address, and compare input to output character-for-character.
3. Formulate a hypothesis for what pattern-matching or redaction logic is missing, then check `ANSWERS.md`.

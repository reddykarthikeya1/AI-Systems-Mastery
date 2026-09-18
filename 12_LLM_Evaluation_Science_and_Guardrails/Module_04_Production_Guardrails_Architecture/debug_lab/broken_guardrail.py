"""Broken guardrail with zero regex escaping or PII detection."""

class BrokenGuardrail:
    def sanitize(self, text):
        return text


def reproduce_defect():
    print("Sanitizing a message containing an SSN, a card number, and an email address...")
    guardrail = BrokenGuardrail()
    user_message = "My SSN is 219-09-9999 and my card is 4111-1111-1111-1111, reach me at alice@example.com"

    sanitized = guardrail.sanitize(user_message)

    print(f"Original message:  {user_message}")
    print("Expected sanitized message: PII replaced with [REDACTED_*] markers")
    print(f"Actual sanitized message:   {sanitized}")
    print(f"Output identical to input (nothing redacted): {sanitized == user_message}")
    print(f"SSN still present in sanitized output: {'219-09-9999' in sanitized}")
    print(f"Credit card number still present in sanitized output: {'4111-1111-1111-1111' in sanitized}")
    print(f"Email address still present in sanitized output: {'alice@example.com' in sanitized}")


if __name__ == "__main__":
    reproduce_defect()

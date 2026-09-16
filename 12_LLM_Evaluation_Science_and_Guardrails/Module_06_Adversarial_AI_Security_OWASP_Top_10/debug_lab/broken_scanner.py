"""Broken scanner that misses obfuscations."""

class BrokenScanner:
    def scan(self, text):
        # BUG: Only checks one exact string; misses Base64 and regex variations
        if "ignore all previous instructions" in text:
            return False
        return True

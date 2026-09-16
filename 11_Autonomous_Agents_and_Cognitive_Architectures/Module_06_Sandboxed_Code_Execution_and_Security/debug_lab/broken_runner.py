"""Insecure code runner directly calling exec()."""

class BrokenCodeRunner:
    def execute(self, code):
        # VULNERABLE: Direct arbitrary code execution
        exec(code)

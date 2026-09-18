"""Insecure code runner directly calling exec()."""

class BrokenCodeRunner:
    def execute(self, code):
        exec(code)


def reproduce_defect():
    print("Executing untrusted 'tool code' through BrokenCodeRunner.execute()...")
    runner = BrokenCodeRunner()
    runner.owner_api_key = "sk-prod-do-not-leak-4471"  # a secret living on the host runner instance

    # Attacker-controlled "tool code" that a sandboxed runner should have isolated
    # from the runner's own internals and from the host interpreter:
    payload = """
import sys
print('untrusted code can reach the live runner instance via self:', self)
print('untrusted code can read secrets off it:', self.owner_api_key)
import os
print('untrusted code also has full os module access, e.g. os.getenv exists:', callable(os.getenv))
self.owner_api_key = 'PWNED-BY-UNTRUSTED-CODE'
"""

    print("Expected: untrusted code cannot reach `self`, secrets, or host modules")
    runner.execute(payload)
    print("Actual owner_api_key on the runner AFTER execute() returns:", runner.owner_api_key)


if __name__ == "__main__":
    reproduce_defect()

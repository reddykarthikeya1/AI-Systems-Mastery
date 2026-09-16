"""Broken HITL with blocking wait loop."""

class BrokenHITL:
    def run(self, action):
        # BUG: Blocks thread with synchronous input()
        approved = input("Approve? (y/n)")
        return approved == "y"

"""Broken HITL with blocking wait loop."""

class BrokenHITL:
    def run(self, action):
        approved = input("Approve? (y/n)")
        return approved == "y"


def reproduce_defect():
    import io
    import sys

    print("Agent paused for human approval of action: 'delete_staging_database'")
    print("Expected: the approval step durably pauses/resumes instead of crashing when no terminal is attached")

    hitl = BrokenHITL()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO("")  # simulate a non-interactive deployment: no terminal attached
    try:
        approved = hitl.run("delete_staging_database")
        print(f"Actual: Approved: {approved}")
    except EOFError as e:
        print(f"Actual: run() crashed instead of pausing: {type(e).__name__}: {e}")
    finally:
        sys.stdin = old_stdin


if __name__ == "__main__":
    reproduce_defect()

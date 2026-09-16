# Beginner Playground: Human-in-the-Loop & Time Travel

Welcome to Human-in-the-Loop (HITL) and Time Travel! In autonomous systems, high-risk actions (e.g. paying invoices, dropping tables, sending public emails) must pause execution for human verification.

---

## 1. The Core Mental Model: Interrupts and Resumption

```
 [ Node A: Generate Draft ]
             |
             v
   [ Breakpoint / Interrupt ] ---> (Suspends graph; yields control to human)
             |
     (Human Approves / Edits)
             |
             v
 [ Node B: Send Email ]
```

- **Interrupt Before**: Pause before executing a specific node.
- **Payload Editing**: The human can edit the draft before resuming.
- **Time Travel**: Rewind the entire graph to an earlier checkpoint, change an input, and branch out a new future.

---

## 2. Interactive Pure-Python Experiment: Zero-Dependency HITL Graph

```python
class HITLStateGraph:
    def __init__(self):
        self.state = {}
        self.paused_action = None

    def execute_until_approval(self, email_draft: str):
        self.state["draft"] = email_draft
        self.paused_action = {"type": "send_email", "payload": email_draft}
        print(f"[*] Execution SUSPENDED at approval gate.")
        print(f"Pending Action: {self.paused_action}")
        return "WAITING_FOR_HUMAN"

    def resume(self, human_approval: bool, edited_draft: str = None):
        if not human_approval:
            self.state["status"] = "REJECTED"
            print("[x] Action Rejected by Human.")
            return self.state

        final_text = edited_draft or self.state["draft"]
        self.state["sent_content"] = final_text
        self.state["status"] = "SENT"
        print(f"[+] Action Approved! Email sent: '{final_text}'")
        return self.state

graph = HITLStateGraph()
graph.execute_until_approval("Dear Customer, here is your $10,000 refund.")
# Human intervenes and corrects amount
graph.resume(human_approval=True, edited_draft="Dear Customer, here is your $100 refund.")
```

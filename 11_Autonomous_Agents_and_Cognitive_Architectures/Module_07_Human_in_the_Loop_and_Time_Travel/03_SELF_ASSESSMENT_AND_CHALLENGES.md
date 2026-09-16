# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is pausing an async asyncio task with `await input()` anti-pattern in production agents?
   - *Answer*: It holds memory and thread resources hostage, breaks on server restarts or deployments, and cannot scale across distributed worker nodes. Checkpoint persistence is mandatory.
2. What is the difference between `interrupt_before` and `interrupt_after`?
   - *Answer*: `interrupt_before` pauses before the node runs (to approve/edit inputs), while `interrupt_after` pauses after the node finishes (to inspect/edit outputs before routing).
3. How does state branching maintain auditability in regulated environments?
   - *Answer*: Historical checkpoints are immutable append-only logs; branches create new DAG paths with parent pointers, preserving the full audit trail.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Volume HITL Queue for Financial Transactions
**Context**: An AI accounts-payable agent processes 20,000 vendor invoices daily. 5% exceed $50,000 and trigger human review. Invoices sit in the human queue for up to 3 days.
**Question**: Architect the durable suspension and resumption engine.
**Solution**:
1. Serialize the full graph state to a durable database (e.g. Postgres JSONB).
2. De-allocate all worker resources immediately upon hitting the interrupt.
3. When an accounting manager clicks "Approve" in the web dashboard, push an event to Kafka; a stateless worker consumes the event, rehydrates graph state from the checkpoint, and completes the payment.

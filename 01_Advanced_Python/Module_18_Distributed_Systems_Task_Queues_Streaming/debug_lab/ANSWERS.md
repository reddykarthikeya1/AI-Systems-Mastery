# Debug Lab Answers: Module 18

<details>
<summary>Bug 1: Non-idempotent task processing</summary>

### Root Cause
In distributed messaging (e.g. Redis Streams, SQS, RabbitMQ), "at-least-once" delivery is the standard delivery guarantee. If a consumer crashes before ACKing, the message is redelivered. Handlers must be idempotent.

### Fix
Implement deduplication checking against an idempotency store (e.g. Redis `SETNX` or DB primary key):
```python
executed_tx_ids = set()

def process_bank_transfer(transfer_id: str, amount: float, balances: dict[str, float]):
    if transfer_id in executed_tx_ids:
        print(f"Skipping duplicate transfer {transfer_id}")
        return
    balances["alice"] -= amount
    balances["bob"] += amount
    executed_tx_ids.add(transfer_id)
```
</details>

# Design Rationale: Enterprise Banking Ledger & Account Hierarchy

## Architectural Overview
A polymorphic banking system implementing strict double-entry ledger tracking, abstract base classes (`abc.ABC`), operator overloading, and encapsulated transactional balance management.

## Key Design Decisions
1. **Abstract Base Class Enforcement:** `Account` inherits from `abc.ABC` with `@abstractmethod` decorators for deposit and withdrawal, guaranteeing no partial or unvalidated account types can be instantiated.
2. **Immutable Audit Ledger Entries:** Transactions are appended as immutable dataclass records. Account balances are calculated from verifiable historical credit/debit events.
3. **Encapsulated Private State (`_balance`):** Direct mutation of balances is blocked; state changes require audited domain method execution.

## Rejected Alternatives
1. **Direct Attribute Mutation (`account.balance += 500`):**
   - *Reason for Rejection:* Bypassing transaction ledger recording prevents reconciliation, breaks audit compliance, and allows overdraft violations.
2. **Single Monolithic Account Class with Conditional Type Strings:**
   - *Reason for Rejection:* Using `if account_type == 'savings':` inside methods violates the Open/Closed Principle and results in branchy, bug-prone business logic.

## Invariants & Guarantees
- Total deposits minus withdrawals strictly equals current ledger balance.
- Overdraft limits are strictly enforced at transaction execution time.

## Verification
```bash
pytest test_banking_system.py -v
```

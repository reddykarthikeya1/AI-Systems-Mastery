# Debug Lab: Module 04 — Deep OOP Traps

## How to Run
```bash
python debug_lab/broken_banking.py
```

## Observed Symptoms
1. **Shared transaction history across all customer accounts**:
   Bob's account instance displays deposits made by Alice.
2. **TypeError when using custom object as dictionary key**:
   ```
   TypeError: unhashable type: 'AccountIdentifier'
   ```
3. **Broken cooperative inheritance (MRO bypass)**:
   `SecurityMixin.log` is skipped because `AuditMixin` hardcodes `BaseService.log(self, ...)`.

# Debug Lab: Module 21 — Metaprogramming & Descriptor Traps

## How to Run
```bash
python debug_lab/broken_mini_orm.py
```

## Observed Symptoms
1. **Cross-instance state bleeding**:
   Setting `u2.name = "Bob"` inadvertently overwrites `u1.name`, because state is stored on the descriptor instance rather than on `instance.__dict__`.

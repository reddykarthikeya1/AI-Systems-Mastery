# Debug Lab: Module 17 — WebSockets Traps

## How to Run
```bash
python debug_lab/broken_chat_api.py
```

## Observed Symptoms
1. **Cascading broadcast failure**:
   A single disconnected client crashes the entire broadcast loop, preventing healthy connected clients from receiving updates.

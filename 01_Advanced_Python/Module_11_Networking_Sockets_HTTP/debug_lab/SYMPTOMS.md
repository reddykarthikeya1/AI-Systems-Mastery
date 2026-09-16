# Debug Lab: Module 11 — Sockets & Networking Traps

## How to Run
```bash
python debug_lab/broken_chat_server.py
```

## Observed Symptoms
1. **OSError on server restart (TIME_WAIT state)**:
   ```
   OSError: [Errno 98/10048] Address already in use
   ```
2. **Message concatenation / fragmentation bug**:
   Sending two rapid messages `"Hello"` and `"World"` results in the receiver getting `"HelloWorld"` in a single read.
3. **No message boundaries**:
   Receiver cannot determine where one message ends and the next begins.

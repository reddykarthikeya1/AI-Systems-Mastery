# Debug Lab: Module 19 — Containerization Traps

## How to Run
```bash
python debug_lab/broken_app.py
```

## Observed Symptoms
1. **Container port unreachable (Connection refused)**:
   Running `docker run -p 8000:8000 ...` fails with `ConnectionRefusedError` from host browser or `curl`, even though the container logs indicate the server is running.

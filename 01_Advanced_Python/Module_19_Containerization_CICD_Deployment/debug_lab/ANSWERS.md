# Debug Lab Answers: Module 19

<details>
<summary>Bug 1: Binding to 127.0.0.1 inside a container</summary>

### Root Cause
Inside a container network namespace, `127.0.0.1` refers strictly to the container's isolated local loopback. Outside requests routed via Docker's bridge interface arrive on `eth0`, which is ignored unless bound to all interfaces (`0.0.0.0`).

### Fix
Bind to `0.0.0.0`:
```python
uvicorn.run("broken_app:app", host="0.0.0.0", port=8000)
```
</details>

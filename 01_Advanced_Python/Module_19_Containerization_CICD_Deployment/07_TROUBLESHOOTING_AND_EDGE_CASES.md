# Module 19: Troubleshooting, Docker Traps & Container Security

This reference guide details common Dockerization and CI/CD deployment bugs in Python.

---

## 1. The Python Output Buffering Trap

### The Bug
Container runs, but `docker logs` remains completely blank for 10 minutes until the container stops.

### Why It Happens
Python buffers standard output (`stdout`) when not connected to an interactive TTY terminal.

### The Fix
Set `PYTHONUNBUFFERED=1` in your `Dockerfile` environment variables:
```dockerfile
ENV PYTHONUNBUFFERED=1
```

---

## 2. Docker Cache Invalidation Trap

### The Mistake
```dockerfile
COPY . /app
RUN pip install -r requirements.txt # ❌ Re-installs all packages on every single code change!
```

### The Fix
Always copy dependency manifests first to leverage Docker layer caching:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt # ✅ Cached unless requirements.txt changes!
COPY . /app
```

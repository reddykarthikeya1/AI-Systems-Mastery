# 🐣 Interactive Foundations Playground: Containerization, CI/CD & Deployment

> *"Twelve-factor applications store configuration in the environment and separate build, release, and run."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import os
```

---

## 1. Twelve-Factor Environment Configuration

Production services parse runtime settings from environment variables with fallback defaults.

```python
os.environ["APP_PORT"] = "8080"
os.environ["APP_ENV"] = "production"

port = int(os.environ.get("APP_PORT", 3000))
env = os.environ.get("APP_ENV", "development")

assert port == 8080
assert env == "production"
assert os.environ.get("UNSET_KEY", "default") == "default"
print(f"Twelve-factor config loaded: ENV={env}, PORT={port}")
```

---

## 2. Health Check Probe Endpoints

Kubernetes readiness and liveness probes inspect service dependencies before sending traffic.

```python
def liveness_probe():
    return {"status": "alive", "uptime": 120}

def readiness_probe(db_connected):
    if not db_connected:
        return {"status": "unhealthy", "code": 503}
    return {"status": "ready", "code": 200}

assert liveness_probe()["status"] == "alive"
assert readiness_probe(True)["code"] == 200
assert readiness_probe(False)["code"] == 503
print("Health check probes validated readiness and liveness.")
```

---

## 3. Pipeline Stage Orchestration

Continuous deployment pipelines sequence build, test, and release stages sequentially.

```python
stages = ["lint", "test", "build", "deploy"]
executed_stages = []
for s in stages:
    executed_stages.append(s)

assert executed_stages == ["lint", "test", "build", "deploy"]
assert len(executed_stages) == 4
print(f"CI/CD pipeline executed all stages: {' -> '.join(executed_stages)}")
```

---

"""Beginner playground for Module 19 - Containerization, CI/CD & Deployment.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import os

# -------------------------------------------- 1. Twelve-Factor Environment Configuration
os.environ["APP_PORT"] = "8080"
os.environ["APP_ENV"] = "production"

port = int(os.environ.get("APP_PORT", 3000))
env = os.environ.get("APP_ENV", "development")

assert port == 8080
assert env == "production"
assert os.environ.get("UNSET_KEY", "default") == "default"
print(f"Twelve-factor config loaded: ENV={env}, PORT={port}")

# -------------------------------------------- 2. Health Check Probe Endpoints
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

# -------------------------------------------- 3. Pipeline Stage Orchestration
stages = ["lint", "test", "build", "deploy"]
executed_stages = []
for s in stages:
    executed_stages.append(s)

assert executed_stages == ["lint", "test", "build", "deploy"]
assert len(executed_stages) == 4
print(f"CI/CD pipeline executed all stages: {' -> '.join(executed_stages)}")

print()
print("All checks passed.")

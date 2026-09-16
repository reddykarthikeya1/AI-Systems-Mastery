# Module 19: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Docker Containers, CI/CD Pipelines, and Production Deployment before moving to **Module 18**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Virtualization vs Containers:** How do Docker containers differ from traditional Virtual Machines (VMs) in terms of kernel sharing and resource overhead?
2. **Multi-Stage Builds:** What is the primary security and performance benefit of using a Multi-Stage Dockerfile?
3. **Container Security:** Why should production containers create and run as a dedicated non-root user (`USER appuser`)?
4. **Log Buffering:** Why is `ENV PYTHONUNBUFFERED=1` essential for Python microservices running in Docker?
5. **Layer Caching:** Why should `COPY requirements.txt .` and `RUN pip install ...` appear before `COPY . .` in a Dockerfile?
6. **Command Execution:** What is the difference between `ENTRYPOINT` and `CMD` instructions in a Dockerfile?
7. **Service Orchestration:** What role does `docker-compose.yml` play when developing multi-service stacks locally?
8. **Telemetry:** What is the standard format of a Prometheus `/metrics` exposition response?
9. **Health Probes:** What is the difference between a **Liveness Probe** and a **Readiness Probe**?
10. **CI/CD Automation:** What are the 4 fundamental stages of a production GitHub Actions CI/CD pipeline?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
VMs virtualize hardware and run an entire guest OS kernel. Containers share the host OS kernel and isolate processes using Linux namespaces and cgroups, booting in milliseconds with negligible RAM overhead.

#### Answer 2:
It allows compiling dependencies (which requires heavy build tools and compilers like `gcc`) in an ephemeral stage and copying only pure wheels to a minimal slim production image, cutting image size from 1 GB to $< 80$ MB.

#### Answer 3:
If a hacker exploits a remote code execution (RCE) vulnerability in a root container, they gain root access to the host kernel. Non-root users constrain attackers inside the unprivileged container sandbox.

#### Answer 4:
It forces Python to flush standard output immediately to the terminal stdout stream, ensuring logs appear in `docker logs` and CloudWatch in real time without lag.

#### Answer 5:
Because source code changes frequently while dependencies change rarely. Placing dependencies first allows Docker to reuse cached layers, cutting build times from minutes to seconds.

#### Answer 6:
- `ENTRYPOINT`: Sets the fixed executable command (e.g. `uvicorn`).
- `CMD`: Provides default arguments that can be easily overridden when running the container.

#### Answer 7:
It defines multi-container applications (API + PostgreSQL + Redis + Prometheus) in a single declarative YAML file, configuring shared internal networks and storage volumes.

#### Answer 8:
Plaintext lines containing metric names, key-value label pairs in curly braces, and floating-point values (e.g. `http_requests_total{method="GET",status="200"} 42`).

#### Answer 9:
- **Liveness:** Checks if the process is alive; if failing, restarts the container.
- **Readiness:** Checks if the app is ready to accept incoming traffic (e.g. database connected); if failing, stops routing traffic.

#### Answer 10:
1. **Linting & Type Checking** (`ruff`, `mypy`)
2. **Automated Testing** (`pytest`)
3. **Docker Image Build & Push** (Docker Hub / AWS ECR)
4. **Zero-Downtime Deployment** (Kubernetes / ECS / Cloud Run)

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Liveness and Readiness Probe Route

**Goal:** Implement separate `/healthz/live` and `/healthz/ready` endpoints in FastAPI.

<details>
<summary><b>Solution Code</b></summary>

```python
from fastapi import FastAPI, HTTPException, status
from starlette.testclient import TestClient

app = FastAPI()
db_connected = True

@app.get("/healthz/live")
def liveness():
    return {"status": "ALIVE"}

@app.get("/healthz/ready")
def readiness():
    if not db_connected:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DB disconnected")
    return {"status": "READY"}

# Verification:
client = TestClient(app)
print("Liveness Check :", client.get("/healthz/live").json())
print("Readiness Check:", client.get("/healthz/ready").json())
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Dockerfile layer cache always busted

```
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]
```

**Observed symptom:** Every build reinstalls all dependencies, taking 4 minutes even for a one-character code change.

**(a)** Which layer invalidates the cache, and why?

**(b)** Rewrite the relevant lines.

**(c)** What second problem does `COPY . .` create beyond build time?

<details>
<summary><b>Show the diagnosis</b></summary>

`COPY . .` copies the whole source tree, so **any** file change alters that layer's hash. Every layer after it — including `pip install` — is rebuilt.

**Rewrite:**

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Dependencies now reinstall only when `requirements.txt` changes.

**Second problem:** `COPY . .` also ships your `.git` directory, `.env` files, test fixtures, and any local secrets into the image — where `docker history` can retrieve them even if a later layer deletes them. Always pair it with a `.dockerignore`. Image size and secret leakage are both fixed by the same file.

</details>

---

### D2. App unreachable from outside the container

```
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
```

**Observed symptom:** `docker run -p 8000:8000 img` starts cleanly, but `curl localhost:8000` from the host gets connection refused.

**(a)** Why can the host not reach the app?

**(b)** What is the fix?

**(c)** Why is that fix safe here but dangerous on a bare-metal host?

<details>
<summary><b>Show the diagnosis</b></summary>

`127.0.0.1` inside the container is the **container's own** loopback interface. Docker's port forwarding delivers traffic to the container's external interface, where nothing is listening.

**Fix:** `--host 0.0.0.0` — listen on all interfaces within the container.

**Safe in a container** because the network namespace is the boundary: only the ports you explicitly publish with `-p` are reachable, so `0.0.0.0` means 'all of my private interfaces', not 'the public internet'. On bare metal, `0.0.0.0` genuinely exposes the service on every NIC, and you would rely on a host firewall instead. Same flag, entirely different risk — which is why copying container advice onto a VM is a common mistake.

</details>

---

### D3. Container runs as root

```
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]
```

**Observed symptom:** A container escape or a path-traversal bug gives the attacker root on the host namespace.

**(a)** What is the default user, and why does it matter?

**(b)** Add the lines that fix it.

**(c)** What breaks if you add `USER` too early in the file?

<details>
<summary><b>Show the diagnosis</b></summary>

The default is **root** (uid 0). Combined with a kernel vulnerability or a misconfigured bind mount, root in the container is effectively root on the host — and even without an escape it lets an attacker write to any mounted volume.

**Fix:**

```dockerfile
RUN useradd --create-home --uid 1000 appuser
USER appuser
```

placed **after** the `pip install`.

**Too early breaks the build:** `pip install` into system site-packages needs write access to `/usr/local/lib`, and `COPY` would create files the new user cannot read. The correct order is: install as root, `chown` what the app needs, then drop privileges with `USER` as the last step before `CMD`. Also prefer a numeric uid — some orchestrators enforce `runAsNonRoot` and cannot verify a username.

</details>

---

### D4. Healthcheck that always passes

```
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 0
```

**Observed symptom:** The orchestrator never restarts the container, even when the app is hard-down.

**(a)** Spot the bug in one character.

**(b)** What is the correct exit code convention?

**(c)** What makes a good health endpoint, as opposed to a useless one?

<details>
<summary><b>Show the diagnosis</b></summary>

`|| exit 0` — the fallback exits **successfully**, so the healthcheck reports healthy no matter what. It should be `|| exit 1`.

**Convention:** exit 0 = healthy, exit 1 = unhealthy. Docker also treats exit 2 as reserved. Add `--interval`, `--timeout`, `--retries` and especially `--start-period` so a slow boot is not counted as a failure.

**A good health endpoint** checks that this instance can do its job — can it reach its database, is its worker pool responsive — and returns quickly without doing expensive work. A useless one returns `{"status": "ok"}` unconditionally, which only proves the process is running, something the orchestrator already knows. Distinguish **liveness** (restart me) from **readiness** (send me traffic); conflating them causes restart loops during a dependency outage.

</details>

---

### D5. Prometheus counter as a gauge

```python
from prometheus_client import Gauge

requests_total = Gauge("requests_total", "Total requests")

@app.middleware("http")
async def count(request, call_next):
    requests_total.inc()
    return await call_next(request)
```

**Observed symptom:** The `rate()` query in Grafana produces nonsense after every deployment.

**(a)** Why is `Gauge` the wrong metric type here?

**(b)** What should it be, and what does that change?

**(c)** Why does a deployment specifically break the graph?

<details>
<summary><b>Show the diagnosis</b></summary>

A **Gauge** is for values that go up *and down* — temperature, queue depth, memory in use. A monotonically increasing total is a **Counter**, and Prometheus's `rate()`/`increase()` functions are built specifically around counter semantics.

**Fix:** `Counter('requests_total', ...)`. The `_total` suffix is also the naming convention for counters, so the current code contradicts itself.

**Deployments break it** because a restart resets the value to zero. `rate()` detects and corrects for counter resets — that logic is why the type exists. Applied to a gauge, Prometheus interprets the drop to zero as a real, enormous negative change, and the graph spikes or goes blank. Also add labels (`method`, `status`, `path` — bounded values only) so the counter is actually queryable; unbounded label values such as a raw URL with ids cause cardinality explosion.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.

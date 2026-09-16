# W3Schools-Style Playground: Containerization & CI/CD Pipelines

> *"A Docker container is a standardized shipping container for code: pack it once, run it anywhere."*

Welcome to the **Module 19 Containerization CICD Deployment** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Containerization packages your code, Python runtime, and dependencies into a lightweight image. CI/CD (Continuous Integration/Continuous Deployment) automatically tests and builds this container on every Git push.

---

## 2. Micro-Code Example (3-5 Lines)

```dockerfile
# Anatomy of a clean Python Dockerfile:
# 1. Base image with Python runtime
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy source code and run
COPY . .
CMD ["python", "main.py"]
```

### Line-by-Line Breakdown:
- `FROM`: Specifies the operating system base image containing Python.
- `WORKDIR`: Sets the working directory inside the container filesystem.
- `COPY`: Transfers files from your computer into the container.
- `RUN`: Executes build-time commands (like `pip install`).
- `CMD`: The default command executed when the container starts up.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What is the difference between `RUN` and `CMD` in a Dockerfile?

<details><summary><b>Show Answer</b></summary>

`RUN` executes during the image build process (e.g. installing packages); `CMD` specifies what runs when the container starts.
</details>

---

### Drill 2: Quick Check
Why should you copy `requirements.txt` before copying the rest of your source code?

<details><summary><b>Show Answer</b></summary>

To leverage Docker's layer cache: package installation won't re-run every time you modify application code!
</details>

---

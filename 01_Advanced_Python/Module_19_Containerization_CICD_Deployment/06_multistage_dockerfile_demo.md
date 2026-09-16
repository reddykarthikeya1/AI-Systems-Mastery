# Production Multi-Stage Dockerfile & GitHub Actions Reference

## 1. Multi-Stage Dockerfile (`Dockerfile`)

```dockerfile
# ----------------------------------------------------
# Stage 1: Build & Dependencies Compiler
# ----------------------------------------------------
FROM python:3.11-slim as builder

WORKDIR /build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ----------------------------------------------------
# Stage 2: Final Production Minimal Image
# ----------------------------------------------------
FROM python:3.11-slim

WORKDIR /app
ENV PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Security: Create non-root system user
RUN useradd -m -u 1000 appuser
USER appuser

# Copy installed packages from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . /app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

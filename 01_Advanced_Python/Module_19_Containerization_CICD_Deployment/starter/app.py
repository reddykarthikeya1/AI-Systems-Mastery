"""STARTER - Module 19: Containerization CICD Deployment

Production Containerized Microservice.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_app.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/app.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import PlainTextResponse
app = FastAPI(
    title="Cloud-Native Production Microservice",
    version=os.getenv("APP_VERSION", "1.0.0"),
)
request_counts: dict[str, int] = defaultdict(int)
request_durations: dict[str, list[float]] = defaultdict(list)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next) -> Response:
    # [Tier 2] Algorithm: Implement metrics_middleware adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_prometheus_metrics_endpoint
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 19: implement metrics_middleware()")


@app.get("/healthz/live", status_code=status.HTTP_200_OK)
def liveness_probe() -> dict[str, object]:
    # [Tier 2] Algorithm: Implement liveness_probe adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_liveness_probe_timestamp_is_recent
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 19: implement liveness_probe()")


@app.get("/healthz/ready", status_code=status.HTTP_200_OK)
def readiness_probe() -> dict[str, object]:
    # [Tier 2] Algorithm: Implement readiness_probe adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_liveness_and_readiness_probes
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 19: implement readiness_probe()")


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    # [Tier 2] Algorithm: Implement prometheus_metrics adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_prometheus_metrics_endpoint
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 19: implement prometheus_metrics()")

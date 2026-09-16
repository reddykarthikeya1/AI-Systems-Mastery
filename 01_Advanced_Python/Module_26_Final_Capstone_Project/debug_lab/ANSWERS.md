# Debug Lab Answers: Module 26

<details>
<summary>Bug 1: Cross-subsystem payload contract drift</summary>

### Root Cause
Without shared Pydantic validation schemas across producer (FastAPI route) and consumer (Background worker), field renames cause silent task failures in distributed systems.

### Fix
Define a shared Pydantic payload schema used by both gateway and worker:
```python
from pydantic import BaseModel

class ExportTaskPayload(BaseModel):
    target_format: str = "parquet"
```
</details>

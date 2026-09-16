# Debug Lab Answers: Module 14

<details>
<summary>Bug 1: Post-initialization mutation bypassing validation</summary>

### Root Cause
By default in Pydantic V2, validation is only executed when the model is initialized (`__init__`). Attribute assignments on already-instantiated models (`p.age = -50`) are plain Python attribute sets that do not trigger validators unless explicitly configured.

### Fix
Add `ConfigDict(validate_assignment=True)`:
```python
from pydantic import BaseModel, ConfigDict, Field

class PatientRecord(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    mrn: str
    age: int = Field(..., ge=0, le=120)
```
</details>

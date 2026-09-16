# Debug Lab Solution: Leaky Guardrail Bug

### The Defect
`BrokenGuardrail` passes text directly to the model without scanning for PII entities or checking prompt injection rules.

### The Fix
Implement comprehensive regex pattern matching and policy checking as shown in `project_solution/production_guardrails_pipeline.py`.

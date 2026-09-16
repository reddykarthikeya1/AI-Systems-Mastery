# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. How does constrained decoding (e.g. Outlines) guarantee valid JSON at zero rejection rate?
   - *Answer*: By modifying the logit bias vector at each generation step, masking out tokens that would violate the CFG or JSON Schema state machine.
2. Why is type coercion necessary even when the LLM outputs valid JSON?
   - *Answer*: LLMs frequently output numeric values or booleans as strings (e.g., `"100"` instead of `100`), requiring safe host-side coercion.
3. What is the security hazard of executing tools with raw SQL or shell commands?
   - *Answer*: Indirect Prompt Injection: untrusted content retrieved from web pages can instruct the agent to drop tables or execute malicious commands.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Secure Tool Execution for Multi-Tenant SaaS
**Context**: An enterprise agent runs custom customer-provided Python tools in a multi-tenant cloud environment. A malicious prompt tries to read `/etc/passwd` or query the cloud metadata service `http://169.254.169.254`.
**Question**: Architect an execution pipeline that isolates tool calls and prevents data exfiltration.
**Solution**:
1. Execute tool invocations inside ephemeral microVMs (e.g., AWS Firecracker or gVisor sandbox).
2. Configure iptables / network namespaces to block access to internal private IP blocks and metadata endpoints.
3. Enforce strict CPU/memory cgroups and execution timeouts (e.g., max 2 seconds, 128 MB RAM).

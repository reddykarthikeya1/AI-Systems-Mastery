# Agentic AI Chapter 8: Capstone Project: Autonomous Research & Code Assistant

> **Core Learning Objective:** Bring everything together in an intuitive, non-overwhelming end-to-end capstone project. Build an autonomous multi-agent pipeline from scratch in pure Python with zero external paid APIs or framework churn.

---

## 1. Project Overview & Architectural Flow

We will build an **Autonomous Technical Research & Code Generation Agent**. Given a user's high-level request (e.g., *"Build an in-memory sliding window rate limiter in Python"*), the system autonomously:
1. **Plans:** Decomposes the user prompt into structured research and coding milestones.
2. **Researches:** Queries a knowledge base of algorithm trade-offs.
3. **Codes:** Writes clean, typed Python implementation code.
4. **Audits:** Validates the generated code against security vulnerabilities and correctness checks.
5. **Streams Output:** Delivers a complete, audited engineering deliverable.

```mermaid
flowchart TD
    User["User Goal"] --> Guardrail["1. Input Security Guardrail (PII / Injection Check)"]
    Guardrail --> Planner["2. Planner Agent (Decomposes into Milestones)"]
    
    subgraph Multi_Agent_Core ["Multi-Agent Execution Pipeline"]
        Planner --> Researcher["3. Researcher Agent (Gathers Algorithmic Trade-Offs)"]
        Researcher --> Coder["4. Software Engineer Agent (Generates Typed Python Code)"]
        Coder --> Auditor["5. QA / Security Auditor Agent (Verifies Correctness)"]
    end

    Auditor --> FinalReport["6. Final Production Markdown Deliverable"]
```

---

## 2. Runnable Capstone Skeleton (Pure Python, Simulated LLM Calls)

```python
import json
import re
import time
from typing import TypedDict, List, Dict, Any

# ==============================================================================
# STAGE 1: GUARDRAIL & SECURITY ENGINE
# ==============================================================================
class SecurityGuardrail:
    """Detects prompt injection attempts and sanitizes sensitive data."""
    INJECTIONS = ["ignore previous", "system prompt", "override rules", "you are now dan"]

    @classmethod
    def sanitize(cls, text: str) -> str:
        for inj in cls.INJECTIONS:
            if inj in text.lower():
                raise ValueError(f"Security Alert: Malicious prompt injection detected ('{inj}')!")
        # Redact any accidental credit card numbers
        return re.sub(r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[REDACTED_CARD]", text)

# ==============================================================================
# STAGE 2: IN-MEMORY TOOL REGISTRY
# ==============================================================================
class KnowledgeBaseTools:
    """Domain tools providing verified architectural knowledge."""
    _ARCH_KNOWLEDGE = {
        "rate_limiter": (
            "Sliding Window Log: Maintains timestamps in deque; exact 100% precision. "
            "Token Bucket: Memory O(1), allows bursts. "
            "Recommendation: Use Token Bucket for general APIs, Sliding Window for strict financial limits."
        ),
        "lru_cache": (
            "LRU Cache requires a Doubly-Linked List for O(1) removals and a Hash Map for O(1) lookups. "
            "Sentinel head/tail nodes eliminate null pointer checks."
        )
    }

    @classmethod
    def query_architecture(cls, topic: str) -> str:
        key = "rate_limiter" if "rate" in topic.lower() else "lru_cache"
        return cls._ARCH_KNOWLEDGE.get(key, "General best practice: Keep algorithms modular and thread-safe.")

# ==============================================================================
# STAGE 3: AGENT STATE SCHEMA & SPECIALIZED SUBAGENTS
# ==============================================================================
class ProjectState(TypedDict):
    user_goal: str
    plan: List[str]
    research_summary: str
    code_artifact: str
    audit_report: str
    is_complete: bool

class AutonomousAgentPipeline:
    def __init__(self):
        self.guardrail = SecurityGuardrail()
        self.tools = KnowledgeBaseTools()

    def run_planner(self, state: ProjectState) -> None:
        print("\n[Step 1: Planner Agent] Formulating task decomposition...")
        state["plan"] = [
            "Research architectural trade-offs for target algorithm",
            "Implement production Python code with type hints and docstrings",
            "Run security audit and verification assertions"
        ]
        print(f"  -> Generated {len(state['plan'])} execution milestones.")

    def run_researcher(self, state: ProjectState) -> None:
        print("\n[Step 2: Researcher Agent] Querying internal architectural knowledge base...")
        research = self.tools.query_architecture(state["user_goal"])
        state["research_summary"] = research
        print(f"  -> Research Findings: {research[:80]}...")

    def run_coder(self, state: ProjectState) -> None:
        print("\n[Step 3: Engineer Agent] Synthesizing typed production Python implementation...")
        # Synthesizes clean implementation adhering to research findings
        code = '''
import time
from collections import deque

class SlidingWindowRateLimiter:
    """Thread-safe Sliding Window Log Rate Limiter."""
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque()

    def allow_request(self) -> bool:
        now = time.monotonic()
        # Evict expired timestamps
        while self.timestamps and self.timestamps[0] <= now - self.window_seconds:
            self.timestamps.popleft()

        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
            return True
        return False
'''
        state["code_artifact"] = code.strip()
        print("  -> Python implementation synthesized successfully.")

    def run_auditor(self, state: ProjectState) -> None:
        print("\n[Step 4: Auditor Agent] Performing static code audit & security check...")
        code = state["code_artifact"]
        issues = []
        if "eval(" in code or "exec(" in code:
            issues.append("Critical: Dangerous dynamic code execution detected.")
        if "except Exception:" in code:
            issues.append("Warning: Broad exception catching without logging.")

        if not issues:
            state["audit_report"] = "Audit Passed: Clean code, zero security vulnerabilities, full type annotations."
        else:
            state["audit_report"] = f"Audit Issues: {', '.join(issues)}"
        
        state["is_complete"] = True
        print(f"  -> {state['audit_report']}")

    def execute(self, user_goal: str) -> ProjectState:
        # Step 0: Input sanitization
        clean_goal = self.guardrail.sanitize(user_goal)
        print(f"=== Starting Autonomous Agent Project: '{clean_goal}' ===")

        state: ProjectState = {
            "user_goal": clean_goal,
            "plan": [],
            "research_summary": "",
            "code_artifact": "",
            "audit_report": "",
            "is_complete": False
        }

        # Sequential multi-agent pipeline
        self.run_planner(state)
        self.run_researcher(state)
        self.run_coder(state)
        self.run_auditor(state)

        return state

# ==============================================================================
# STAGE 4: VERIFICATION DRIVER & DELIVERABLE RENDERING
# ==============================================================================
if __name__ == "__main__":
    pipeline = AutonomousAgentPipeline()
    result = pipeline.execute("Build a clean, high-precision sliding window rate limiter")

    print("\n" + "=" * 60)
    print("           FINAL PRODUCTION AGENT DELIVERABLE")
    print("=" * 60)
    print(f"\n### Project Goal: {result['user_goal']}")
    print(f"\n### Architectural Research:\n{result['research_summary']}")
    print(f"\n### Audited Implementation:\n```python\n{result['code_artifact']}\n```")
    print(f"\n### Quality Verification:\n{result['audit_report']}")
```

---

## How to Turn the Skeleton into a Real Agent

The capstone is a skeleton with simulated model calls. To make it real: (1) implement `get_llm()` for your provider (see `examples/llm.py`, which has Anthropic and OpenAI adapters behind `LLM_PROVIDER=anthropic|openai` (set `LLM_MODEL` to a current model id; both are unit-tested with stub clients)), (2) keep a `FakeLLM` script for each scenario so tests stay offline and deterministic, (3) add the evaluation loop from `examples/ex05_eval_harness.py` (repeat each task 5 to 10 times and report `pass^k` with a confidence interval), and (4) gate side effects behind the approval pattern from `examples/ex02_langgraph_hitl.py`.


## 4. Runnable Model: Acceptance Tests for the Capstone

A capstone is only finished when it can be graded without opinion. These checks are deterministic, run offline, and are the kind of automated gate a review would apply to your agent's output.

```python
import re

def check_report(report: str, sources: dict) -> list:
    """Return a list of problems. Rules: every cited id must exist, every sentence with a number must cite a source,
    and a source must not be listed that was never cited."""
    problems, cited = [], set()
    for sentence in re.split(r"(?<=[.!?])\s+", report.strip()):
        ids = re.findall(r"\[(S\d+)\]", sentence)
        cited.update(ids)
        for i in ids:
            if i not in sources:
                problems.append(f"unknown source {i}")
        if re.search(r"\d", re.sub(r"\[S\d+\]", "", sentence)) and not ids:
            problems.append(f"uncited figure: {sentence[:40]}")
    for unused in sorted(set(sources) - cited):
        problems.append(f"unused source {unused}")
    return problems

sources = {"S1": "Annual report 2024", "S2": "Industry survey"}
good = "Revenue grew 12% in 2024 [S1]. Analysts expect continued demand [S2]."
assert check_report(good, sources) == []
assert check_report("Revenue grew 12% in 2024. Demand is strong [S2].", sources) == [
    "uncited figure: Revenue grew 12% in 2024.", "unused source S1"]
assert check_report("Revenue grew 12% [S9]. Demand [S1] [S2].", sources) == ["unknown source S9"]
```

### Rubric the grader (human or script) applies

| Area | Passing evidence | Automated check |
| :--- | :--- | :--- |
| Grounding | Every factual claim carries a citation that exists | `check_report` above |
| Tool discipline | No calls outside the allowlist; arguments validated; step and cost budgets enforced | Replay the trace and assert limits |
| Recovery | A failed tool call leads to a retry, an alternative or a clear partial answer, never a crash | Inject a failing tool in a test and assert the final status |
| Safety | Untrusted web content cannot trigger a write or send action | Feed a hostile page and assert no privileged tool was called |
| Reproducibility | The same inputs and recorded model outputs give the same report | Run the pipeline twice against a recording |
| Cost | Cost per task is reported and under the stated cap | Sum token usage from the trace |

### Suggested milestones

1. **Day 1, the loop:** a ReAct loop with two tools (search stub, calculator), a step budget and a trace log, tested with a scripted model.
2. **Day 2, grounding:** retrieval over a small fixed corpus, citations in the output, `check_report` as a test.
3. **Day 3, safety and recovery:** tool allowlist and argument validation, a failing-tool test, a hostile-page test.
4. **Day 4, evaluation:** 20 golden tasks, a pass-rate gate with a confidence bound, and a cost report.
5. **Day 5, polish:** README with architecture, limits, a demo transcript and the evaluation results.

The deliverable that distinguishes strong submissions is not a clever prompt; it is the **evidence**: tests, a trace, an evaluation table and an honest list of known failures.

---

## Further Reading

- [Anthropic: building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [SWE-bench](https://arxiv.org/abs/2310.06770)


---

## Check Yourself

Answer in your head or on paper first, then open each answer.

<details>
<summary><strong>1.</strong> What makes a capstone agent testable offline?</summary>

A scripted fake model, deterministic tools and assertions on the final state.

</details>

<details>
<summary><strong>2.</strong> Which three checks gate a side-effecting action?</summary>

Argument validation, authorisation and (for risky actions) human approval.

</details>

<details>
<summary><strong>3.</strong> What should the capstone log?</summary>

Each step: prompt, tool call, result, latency, tokens and cost.

</details>

<details>
<summary><strong>4.</strong> How do you turn a simulation into a real agent?</summary>

Swap the fake model for a provider adapter and keep the scripted tests as regression cases.

</details>

# Agentic AI Chapter 2: Prompt Engineering, Tool Calling & Structured Outputs

> **Core Learning Objective:** Move beyond simple text generation. Learn how LLMs interface with the external world through the Function Calling protocol, JSONSchema validation, and Pydantic v2 structured outputs.

---

## 1. The Prompt Engineering Hierarchy

```mermaid
flowchart TD
    Prompts["Prompting Paradigms"]
    Prompts --> Zero["1. Zero-Shot<br/>(Direct prompt without examples)"]
    Prompts --> Few["2. Few-Shot<br/>(In-context input/output demonstrations)"]
    Prompts --> CoT["3. Chain-of-Thought (CoT)<br/>('Let's think step by step' forces intermediate reasoning tokens)"]
    Prompts --> Structured["4. Structured Schema Prompting<br/>(Guaranteed JSON generation validated against Pydantic)"]
```

---

## 2. The Tool Calling (Function Calling) Protocol Under the Hood

Tool calling transforms an LLM from a passive text generator into an **autonomous computational agent**. The LLM itself does **not** execute the code; it acts as a **smart orchestrator that decides which function to call and formats valid JSON arguments**.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Runtime as Agent Execution Runtime (Python)
    participant LLM as LLM API (GPT-4 / Claude / Gemini)
    participant Tool as Real World Tool (Weather API / DB)

    User->>Runtime: "What's the weather in Tokyo?"
    Note over Runtime: Injects tool schema (JSONSchema) into LLM system prompt
    Runtime->>LLM: Prompt + Available Tools: [get_weather(city: str)]
    Note over LLM: LLM decides: Tool needed! Emits tool_call object (not text)
    LLM-->>Runtime: tool_call: get_weather({"city": "Tokyo"})
    Runtime->>Tool: Execute Python function: get_weather("Tokyo")
    Tool-->>Runtime: Return: {"temp_c": 19.5, "condition": "Sunny"}
    Runtime->>LLM: Append Tool Result message to conversation history
    Note over LLM: Synthesizes final answer using tool result
    LLM-->>Runtime: "The current weather in Tokyo is 19.5°C and sunny."
    Runtime-->>User: Delivers final response
```

---

## 3. Tool-Calling Implementation in Python (Teaching Version)

Here is a complete, runnable in-memory tool loop implementing function calling without third-party dependencies:

```python
import json
import inspect
from typing import Callable, Any, Dict, List

# --- Tool Registry ---
class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register(self, func: Callable):
        """Inspects Python function signature and auto-generates JSONSchema."""
        name = func.__name__
        doc = func.__doc__ or "No description provided."
        sig = inspect.signature(func)
        
        properties = {}
        required = []
        for param_name, param in sig.parameters.items():
            param_type = "string" if param.annotation == str else "number"
            properties[param_name] = {"type": param_type, "description": f"Parameter {param_name}"}
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": doc.strip(),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
        self._tools[name] = func
        self._schemas.append(schema)

    def execute(self, tool_name: str, arguments_json: str) -> str:
        if tool_name not in self._tools:
            return json.dumps({"error": f"Tool '{tool_name}' not found."})
        
        try:
            kwargs = json.loads(arguments_json)
            result = self._tools[tool_name](**kwargs)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @property
    def schemas(self) -> List[Dict[str, Any]]:
        return self._schemas

# --- Define Native Tools ---
tools = ToolRegistry()

def get_stock_price(symbol: str) -> dict:
    """Fetches real-time stock price for a given ticker symbol."""
    prices = {"AAPL": 225.50, "GOOGL": 178.20, "NVDA": 130.40}
    return {"symbol": symbol.upper(), "price": prices.get(symbol.upper(), "Ticker not found")}

tools.register(get_stock_price)

print("Generated Tool Schema:")
print(json.dumps(tools.schemas, indent=2))

# Simulate LLM tool execution:
simulated_llm_call = {
    "name": "get_stock_price",
    "arguments": '{"symbol": "NVDA"}'
}

tool_output = tools.execute(simulated_llm_call["name"], simulated_llm_call["arguments"])
print("\nTool Execution Output:", tool_output)
```

---

## 4. Structured Output Enforcement with Pydantic v2

Modern enterprise systems forbid free-form text when extracting entities or generating database records. Pydantic v2 guarantees schema adherence:

```python
from pydantic import BaseModel, Field
from typing import List

class ExtractedEntities(BaseModel):
    company_name: str = Field(description="Name of the enterprise")
    quarter: str = Field(description="Fiscal quarter e.g. Q3 2026")
    revenue_billions: float = Field(description="Reported revenue in billions USD")
    risks_identified: List[str] = Field(description="Bullet list of identified risks")

# Models configured with response_format={"type": "json_object"} enforce 
# that output conforms 100% to ExtractedEntities.model_json_schema()!
print("\nPydantic Validation JSON Schema:")
print(json.dumps(ExtractedEntities.model_json_schema(), indent=2))
```

---

## Verified Worked Example: Tool Errors the Model Can Fix

In [`examples/ex01_tool_loop.py`](examples/ex01_tool_loop.py) the `get_history` tool raises `ValueError("days must be between 1 and 7")`. The harness converts it into the observation `ERROR: days must be between 1 and 7`, which is what lets the model retry with a valid argument. **Design rule:** an error message is part of the tool's interface; say what was wrong and what valid input looks like.

**Real-SDK caveat.** In `mcp==2.3.0`, an exception raised inside an MCP tool reaches the model only as "Error executing tool <name>" (the detail is not forwarded). For fixable mistakes, return the explanation in the result text instead (see [`examples/ex04_mcp_server.py`](examples/ex04_mcp_server.py)). Verify how *your* SDK version reports tool errors before relying on them.

Pinned for the verified examples: `langgraph==1.2.13`, `mcp==2.3.0`, `pytest==9.1.1` (see `examples/requirements.txt`). All examples run offline with a scripted fake model: `cd examples && pip install -r requirements.txt && pytest -q`.


## Further Reading

- [Anthropic: tool use overview](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
- [OpenAI: function calling](https://platform.openai.com/docs/guides/function-calling)
- [Lilian Weng: prompt engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)


---

## Check Yourself

Answer in your head or on paper first, then open each answer.

<details>
<summary><strong>1.</strong> What is the difference between a system prompt and a user prompt?</summary>

The system prompt sets role and rules for the conversation; the user prompt carries the request. Neither is a security boundary.

</details>

<details>
<summary><strong>2.</strong> In function calling, who executes the function?</summary>

Your application. The model only emits a structured call (name and arguments); you validate, run and return the result.

</details>

<details>
<summary><strong>3.</strong> Why give tool parameters enums and descriptions?</summary>

They constrain and document the call, reducing wrong or invented arguments.

</details>

<details>
<summary><strong>4.</strong> What is few-shot prompting?</summary>

Including worked examples in the prompt so the model imitates the format and reasoning.

</details>

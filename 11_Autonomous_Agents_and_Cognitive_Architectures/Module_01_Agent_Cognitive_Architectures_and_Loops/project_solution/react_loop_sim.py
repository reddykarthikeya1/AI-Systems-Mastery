"""Production ReAct and Reflexion Loop Engine."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class AgentStep:
    step_number: int
    thought: str
    action_name: Optional[str] = None
    action_args: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    is_terminal: bool = False
    final_answer: Optional[str] = None


@dataclass
class AgentTrajectory:
    goal: str
    steps: List[AgentStep] = field(default_factory=list)
    success: bool = False
    error: Optional[str] = None
    reflections: List[str] = field(default_factory=list)


class ReActLoopEngine:
    """Production ReAct Engine with loop detection and reflexion correction."""

    def __init__(
        self,
        tools: Dict[str, Callable[..., str]],
        max_steps: int = 10,
        cycle_threshold: int = 2,
    ) -> None:
        self.tools = tools
        self.max_steps = max_steps
        self.cycle_threshold = cycle_threshold
        self._action_fingerprints: Dict[str, int] = {}

    def _fingerprint(self, action_name: str, action_args: Dict[str, Any]) -> str:
        canonical = json.dumps(action_args, sort_keys=True)
        return hashlib.sha256(f"{action_name}::{canonical}".encode("utf-8")).hexdigest()

    def parse_llm_response(self, raw_text: str) -> Dict[str, Any]:
        """Parses raw LLM generation into Thought, Action, Action Args, or Final Answer."""
        thought_match = re.search(r"Thought:\s*(.*?)(?=(?:Action:|Final Answer:|$))", raw_text, re.DOTALL | re.IGNORECASE)
        thought = thought_match.group(1).strip() if thought_match else ""

        final_match = re.search(r"Final Answer:\s*(.*)", raw_text, re.DOTALL | re.IGNORECASE)
        if final_match:
            return {
                "thought": thought,
                "is_terminal": True,
                "final_answer": final_match.group(1).strip(),
                "action_name": None,
                "action_args": None,
            }

        action_match = re.search(r"Action:\s*([A-Za-z0-9_]+)", raw_text, re.IGNORECASE)
        args_match = re.search(r"Action Input:\s*(\{.*?\}|\[.*?\]|.+)", raw_text, re.DOTALL | re.IGNORECASE)

        if not action_match:
            raise ValueError(f"Unable to parse Action or Final Answer from LLM response: {raw_text}")

        action_name = action_match.group(1).strip()
        raw_args = args_match.group(1).strip() if args_match else "{}"

        # Try parsing JSON args, fallback to string wrapper
        try:
            action_args = json.loads(raw_args)
            if not isinstance(action_args, dict):
                action_args = {"input": action_args}
        except json.JSONDecodeError:
            action_args = {"input": raw_args}

        return {
            "thought": thought,
            "is_terminal": False,
            "final_answer": None,
            "action_name": action_name,
            "action_args": action_args,
        }

    def execute_tool(self, action_name: str, action_args: Dict[str, Any]) -> str:
        """Executes tool safely with argument forwarding and error wrapping."""
        if action_name not in self.tools:
            return f"Error: Tool '{action_name}' is not registered. Available tools: {list(self.tools.keys())}"

        tool_fn = self.tools[action_name]
        try:
            # Check if tool expects dict unpacking or direct positional input
            if "input" in action_args and len(action_args) == 1:
                return str(tool_fn(action_args["input"]))
            return str(tool_fn(**action_args))
        except Exception as exc:
            return f"Tool Execution Error ({action_name}): {str(exc)}"

    def run(
        self,
        goal: str,
        llm_generate_fn: Callable[[str, List[str]], str],
    ) -> AgentTrajectory:
        """Runs the complete ReAct control loop."""
        trajectory = AgentTrajectory(goal=goal)
        reflections: List[str] = []
        self._action_fingerprints.clear()

        for step_idx in range(1, self.max_steps + 1):
            # Formulate context prompt
            prompt = f"Goal: {goal}\n"
            for past in trajectory.steps:
                prompt += f"Thought: {past.thought}\n"
                if past.action_name:
                    prompt += f"Action: {past.action_name}\nAction Input: {json.dumps(past.action_args)}\n"
                    prompt += f"Observation: {past.observation}\n"

            raw_response = llm_generate_fn(prompt, reflections)
            parsed = self.parse_llm_response(raw_response)

            if parsed["is_terminal"]:
                step = AgentStep(
                    step_number=step_idx,
                    thought=parsed["thought"],
                    is_terminal=True,
                    final_answer=parsed["final_answer"],
                )
                trajectory.steps.append(step)
                trajectory.success = True
                return trajectory

            action_name = parsed["action_name"]
            action_args = parsed["action_args"]
            fp = self._fingerprint(action_name, action_args)
            self._action_fingerprints[fp] = self._action_fingerprints.get(fp, 0) + 1

            # Cycle Detection
            if self._action_fingerprints[fp] >= self.cycle_threshold:
                reflection = (
                    f"Cycle Detected: You have called {action_name} with arguments {action_args} "
                    f"{self._action_fingerprints[fp]} times. You must change your strategy."
                )
                reflections.append(reflection)
                trajectory.reflections.append(reflection)
                observation = f"System Interruption: {reflection}"
            else:
                observation = self.execute_tool(action_name, action_args)

            step = AgentStep(
                step_number=step_idx,
                thought=parsed["thought"],
                action_name=action_name,
                action_args=action_args,
                observation=observation,
            )
            trajectory.steps.append(step)

        trajectory.success = False
        trajectory.error = f"Exceeded maximum steps ({self.max_steps}) without reaching Final Answer."
        return trajectory

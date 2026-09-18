# Debug Lab Incident Report: Code Execution Tool Gives LLM-Generated Code Full Access to the Host Process

- **Severity:** P0 Security - Remote Code Execution
- **Affected Subsystem:** Module_06_Sandboxed_Code_Execution_and_Security
- **Reported Impact:** A penetration test of the agent's "run Python" tool found that any code the model (or a prompt-injected document) asked to execute ran with the same privileges as the host application itself, including reading and overwriting live objects and secrets held by the calling process -- not inside any kind of restricted sandbox.

---

## 🚨 Observable Symptoms & Logs
```text
untrusted code can reach the live runner instance via self: <broken_runner.BrokenCodeRunner object at 0x000001AFD39F87D0>
untrusted code can read secrets off it: sk-prod-do-not-leak-4471
untrusted code also has full os module access, e.g. os.getenv exists: True
owner_api_key on the runner AFTER execute() returns: PWNED-BY-UNTRUSTED-CODE
```
`BrokenCodeRunner.execute(code)` looks like a minimal, single-purpose helper -- it just runs the code string it's given, which is exactly what a "code execution tool" is supposed to do. Nothing about calling it raises an exception or looks obviously wrong. The problem shows up once the executed code itself tries to reach outside the string it was given: it can read `self` -- the live runner instance that called it -- straight out of thin air, pull a secret value off of it, import arbitrary standard-library modules, and overwrite that secret's value permanently, all without being passed any of those things as arguments.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_Sandboxed_Code_Execution_and_Security/debug_lab
   ```
2. `broken_runner.py` only defines `BrokenCodeRunner`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_runner import BrokenCodeRunner

   runner = BrokenCodeRunner()
   runner.owner_api_key = "sk-prod-do-not-leak-4471"  # a secret living on the host runner instance

   # Attacker-controlled "tool code" that a sandboxed runner should have isolated
   # from the runner's own internals and from the host interpreter:
   payload = """
   import sys
   print('untrusted code can reach the live runner instance via self:', self)
   print('untrusted code can read secrets off it:', self.owner_api_key)
   import os
   print('untrusted code also has full os module access, e.g. os.getenv exists:', callable(os.getenv))
   self.owner_api_key = 'PWNED-BY-UNTRUSTED-CODE'
   """

   runner.execute(payload)
   print("owner_api_key on the runner AFTER execute() returns:", runner.owner_api_key)
   ```
3. Observe that the executed string -- which was never passed `self`, `os`, or the secret as an argument -- can read and overwrite all three anyway.

---

## 🎯 Your Objective
1. Inspect `execute()` -- what exactly does it pass to `exec()`, and what globals/locals does that call end up running with?
2. Consider what `self` refers to inside the executed code, and why it is reachable at all.
3. Formulate a hypothesis for what a real sandboxed execution environment would need to restrict that this implementation does not, then check `ANSWERS.md`.

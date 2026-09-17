# Module 06: Sandboxed Code Execution and Security

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **5** | **[03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **6** | **[02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **7** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **8** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

## 1. Threat Modeling: The Autonomous Agent Attack Surface

When an agent executes code or interprets tools, it is exposed to distinct attack vectors:
1. **Direct Prompt Injection**: A user tricks the agent into executing arbitrary host commands.
2. **Indirect Prompt Injection**: Malicious instructions embedded in external webpages, emails, or PDF documents read by the agent.
3. **Sandbox Escape**: Exploiting Python runtime internals (`object.__subclasses__()`) to circumvent simple namespace restrictions.

---

## 2. Sandboxing Architectures Compared

| Isolation Tier | Technology | Startup Latency | Overhead | Security Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Language AST Filter** | Python `ast.NodeVisitor` | $< 1$ ms | None | Weak (circumventable via reflection) |
| **User-Space Kernel** | Google gVisor / nsjail | 50 - 150 ms | Low | Strong (intercepts all syscalls) |
| **MicroVM Isolation** | AWS Firecracker | 5 - 15 ms | Minimal | Hardware-grade (KVM virtualization) |
| **Full VM** | QEMU / Cloud Instance | $5 - 30$ s | High | Complete hardware hypervisor |

---

## 3. AST Static Validation + Subprocess Boundary

In production, defense-in-depth pairs AST analysis with OS-level subprocess isolation:
1. **Pre-execution AST Check**: Disallows dynamic `eval`, `exec`, `__import__`, banned packages (`os`, `subprocess`, `sys`), and private attribute traversal (`_` prefixes).
2. **Ephemeral Subprocess**: Executes valid code in an isolated sub-process with bounded CPU time and memory cgroups.
3. **Telemetry & Output Redaction**: Sanitizes stdout/stderr with regular expressions to strip API keys, Bearer tokens, and sensitive paths.

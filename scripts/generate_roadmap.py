"""Generate ROADMAP.md: one path that mixes roadmap.sh and this repo's own courses.

roadmap.sh is the tracker for topics it covers; everything it does not cover
(maths depth, GPU programming, distributed training, database/system internals,
LLM evaluation depth, CPython internals) is followed in this repo's modules.
Every one of the 175 modules is assigned to exactly one phase (checked below).

    python scripts/generate_roadmap.py
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = "https://roadmap.sh/"

HEAD = re.compile(r"^### Module (\d+): (.+)$")
PRIM = re.compile(r"^- \*\*Recommended Lecture\*\*: \[(.+)\]\((https://www\.youtube\.com/watch\?v=[\w-]{11})\)$")
SUPP = re.compile(r"^\s*- \[.+\]\(https://www\.youtube\.com/watch\?v=[\w-]{11}\) \| \*\*.+\*\* \| Covers: .+$")

C01, C02, C03, C04 = "01_Advanced_Python", "02_Data_Structures_and_Algorithms", "03_Databases_and_Storage_Engines", "04_System_Design_and_Distributed_Systems"
C05, C06, C07, C08 = "05_Mathematics_for_ML_and_AI", "06_Deep_Learning_and_AI_Foundations", "07_GPU_Programming_and_AI_Kernels", "08_Distributed_Training_and_GPU_Infrastructure"
C09, C10, C11, C12 = "09_Inference_Systems_and_Serving_Engines", "10_Advanced_Retrieval_and_Context_Engineering", "11_Autonomous_Agents_and_Cognitive_Architectures", "12_LLM_Evaluation_Science_and_Guardrails"


# roadmap.sh topics (node names) that none of our course text names. Produced by
# comparing every node of the roadmaps on this path with the text of all 12
# courses; a topic can be missing under a different spelling, so treat it as
# "check this on roadmap.sh", not as a proven hole.
GAPS = json.loads((ROOT / "scripts" / "roadmap_sh_gaps.json").read_text(encoding="utf-8"))


def rng(a, b):
    return list(range(a, b + 1))


# (title, goal, roadmap.sh slugs [(slug, optional?)], {course: [module numbers]}, "only our material" note)
PHASES = [
    ("Phase 0 - Tools", "Use git, a Linux shell and a modern Python toolchain without friction.",
     [("git-github", 0), ("linux", 0), ("shell-bash", 1)], {C01: [0]},
     "uv, ruff and the project workflow are in our Module 0."),
    ("Phase 1 - Python", "Write correct, tested, typed Python.",
     [("python", 0), ("python-data-analysis", 1)], {C01: rng(1, 8) + [23]},
     "Testing with pytest/Hypothesis, logging, serialization and strict typing go deeper in our modules."),
    ("Phase 2 - Computer science core", "Reason about complexity and pick the right data structure and algorithm.",
     [("computer-science", 0), ("datastructures-and-algorithms", 0), ("leetcode", 1)], {C02: rng(1, 17)},
     "Network flow, string matching, skip lists, Bloom filters and segment trees are only in our material."),
    ("Phase 3 - Data", "Store, query and index data correctly, in relational, document, key-value and analytical systems.",
     [("sql", 0), ("postgresql-dba", 0), ("redis", 0), ("mongodb", 0), ("data-engineer", 0), ("elasticsearch", 1)],
     {C01: [24], C03: [1, 2, 3, 4, 5, 10, 11, 12, 13, 17, 18, 19, 20]},
     "Columnar/OLAP, BM25 relevance and vector databases (pgvector, HNSW) are mostly in our modules."),
    ("Phase 4 - Backend and system design", "Build real services, then design systems that scale and survive failure.",
     [("backend-beginner", 0), ("backend", 0), ("api-design", 0), ("software-design-architecture", 0), ("system-design", 0), ("software-architect", 1)],
     {C01: [9, 10, 11] + rng(13, 18), C04: rng(0, 20) + [23, 24]},
     "Concurrency/asyncio, FastAPI internals, consistent hashing, Raft, vector clocks, sagas and every case study (TinyURL to payment gateway) are only in our material."),
    ("Phase 5 - Shipping", "Containerise, deploy, cache and observe what you built.",
     [("docker", 0), ("kubernetes", 0), ("devops-beginner", 0), ("devops", 0), ("terraform", 1), ("aws", 1), ("devsecops", 1)],
     {C01: [19, 20], C04: [25]},
     "Redis multi-tier caching, SRE and distributed tracing are in our modules."),
    ("Phase 6 - Maths and machine-learning core", "Get the maths, then build and train neural networks yourself.",
     [("machine-learning", 0), ("ai-data-scientist", 0)],
     {C05: rng(1, 12), C06: [1, 3, 4, 5, 6, 7]},
     "roadmap.sh names the maths topics only at basics level. SVD, Gram-Schmidt, MLE, PCA and Karpathy-style from-scratch builds are in our course 05 and 06."),
    ("Phase 7 - Applied LLM systems", "Prompt, retrieve, call tools and build agents, then measure them.",
     [("prompt-engineering", 0), ("ai-engineer", 0), ("ai-agents", 0)],
     {C01: [25], C04: [21], C06: [2, 8, 9, 10, 12], C10: rng(1, 9), C11: rng(1, 8), C12: rng(1, 5)},
     "ColBERT, GraphRAG, hybrid search/RRF, LangGraph internals, sandboxing and the evaluation science (judges, benchmark harnesses, guardrails) go deeper in our courses 10 to 12."),
    ("Phase 8 - Production AI", "Serve models fast and cheaply, operate them, and attack them before others do.",
     [("mlops", 0), ("inference-engineering", 0), ("ai-red-teaming", 0)],
     {C04: [22], C06: [11], C09: rng(1, 9), C12: [6, 7, 8]},
     "roadmap.sh's Inference Engineering is the tracker; our course 09 adds the paper-level internals (PagedAttention, RadixAttention, Medusa, Marlin)."),
    ("Phase 9 - Hardware, training scale and Python depth (our material only)", "Understand GPUs and kernels, how large models train across clusters, and what CPython does underneath.",
     [], {C01: [12, 21, 22], C07: rng(1, 11), C08: rng(1, 10)},
     "roadmap.sh has no roadmap for CUDA/Triton, ZeRO/FSDP/Megatron, ring attention or 3D parallelism. Follow these modules in full."),
    ("Phase 10 - Database and distributed-data internals (our material only)", "Know how the engines you used in Phase 3 actually work.",
     [], {C03: [6, 7, 8, 9, 14, 15, 16, 21, 22, 23, 24]},
     "MySQL/InnoDB, Oracle (SGA, PL/SQL, RAC), Cassandra/Scylla, LSM-trees, Neo4j, buffer pools, query optimisation, 2PC/consensus and DBRE. Oracle modules are optional unless you work with Oracle."),
    ("Phase 11 - Capstones", "Prove it end to end.",
     [], {C01: [26], C03: [25], C04: [26]},
     "Build one project that uses each phase: a served, retrieval-grounded agent with evaluation and guardrails behind a load-tested API."),
]


def parse(path: pathlib.Path) -> dict[int, dict]:
    mods, cur = {}, None
    for line in path.read_text(encoding="utf-8", errors="replace").split("\n"):
        h = HEAD.match(line)
        if h:
            cur = mods.setdefault(int(h.group(1)), {"topic": h.group(2).strip(), "main": None, "supp": 0})
            continue
        if cur is None:
            continue
        m = PRIM.match(line)
        if m:
            cur["main"] = (m.group(1), m.group(2))
        elif SUPP.match(line):
            cur["supp"] += 1
    return mods


def short(course: str) -> str:
    return course[:2]


def main() -> None:
    data = {c: parse(ROOT / c / "CURATED_VIDEO_LECTURES.md")
            for c in (C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12)}

    # every module in exactly one phase
    seen: dict[tuple[str, int], str] = {}
    for title, _, _, mods, _ in PHASES:
        for c, nums in mods.items():
            for n in nums:
                assert n in data[c], f"{c} has no module {n}"
                assert (c, n) not in seen, f"{c} M{n} is in two phases: {seen[(c, n)]} and {title}"
                seen[(c, n)] = title
    missing = [(c, n) for c, d in data.items() for n in d if (c, n) not in seen]
    assert not missing, f"modules not in any phase: {missing}"

    total_mods = sum(len(d) for d in data.values())
    out = [
        "# Final Learning Roadmap: roadmap.sh + our courses", "",
        "One ordered path. **roadmap.sh is the tracker** for every topic it covers (tick nodes off there and use its AI tutor",
        "for deep dives). **Our modules cover everything roadmap.sh does not**: maths depth, GPU programming, distributed",
        "training, database and system internals, LLM-evaluation depth and CPython internals. Nothing is left out:",
        f"all {total_mods} modules sit in exactly one phase below.", "",
        "## How to work each phase", "",
        "1. Open the phase's roadmap.sh roadmaps and work the **must-know** nodes (skip the optional ones until later).",
        "2. Do the phase's **our-material modules** in the listed order: watch the main lecture (in-app *Watch Video*),",
        "   read the lesson and the *Read More* pages, run the playground/problem bank, then pass the quiz.",
        "3. For anything still fuzzy, ask your AI to explain it with a small runnable example, give you three exercises,",
        "   then quiz you. Do not move on until you can solve them without help.",
        "4. Pass the course gate (`make check-gates`) for each course before leaving its last phase.", "",
        "Pace: one module every 1 to 2 days plus the roadmap.sh nodes. The whole path is long (many months part-time);",
        "Phase 9 and 10 can be deferred until you need them.", "",
        "**Honest note:** videos and reading pages were chosen for relevance and checked to name each concept; nobody has",
        "watched every minute. Swap any weak resource in the course's `CURATED_VIDEO_LECTURES.md` or `RECOMMENDED_READING.md`.", "",
    ]
    out += ["## Biggest holes in our courses that roadmap.sh fills", "",
            "- **Classical machine learning:** decision trees, random forests, gradient boosting, unsupervised and semi-supervised learning, ROC/AUC, CNN/RNN/GAN applications (Phase 6).",
            "- **LLM ecosystem and tooling:** MCP servers/clients/hosts, Hugging Face Hub and inference SDKs, Ollama/LM Studio local models, OpenRouter, agent SDKs, DeepEval, Helicone (Phase 7).",
            "- **Prompting techniques:** chain-of-thought, tree-of-thoughts, prompt ensembling, calibration (Phase 7).",
            "- **MLOps tooling:** Airflow, MLflow, DVC, Kubeflow, Jenkins, Ansible, data lakes/warehouses (Phase 8).",
            "- **Cloud design patterns:** strangler fig, publisher/subscriber, competing consumers, valet key and the other Azure patterns (Phase 4).",
            "- **Auth and protocols:** OpenID, SAML, SOAP, TLS, twelve-factor apps (Phase 4).",
            "- **Ops breadth:** most of Git, Linux, shell, Kubernetes, Terraform, AWS and DevSecOps (Phases 0 and 5).",
            "- **Vision, speech and diffusion inference** (Inference Engineering roadmap, Phase 8).", ""]
    for title, goal, slugs, mods, note in PHASES:
        n = sum(len(v) for v in mods.values())
        out += [f"## {title}", "", f"**Goal:** {goal}", ""]
        if slugs:
            req = [f"[{s}]({RS}{s})" for s, opt in slugs if not opt]
            opt = [f"[{s}]({RS}{s})" for s, o in slugs if o]
            out.append("**roadmap.sh (in order):** " + " → ".join(req) + (f"  \n*Optional:* {', '.join(opt)}" if opt else ""))
        else:
            out.append("**roadmap.sh:** none covers this. Follow our modules.")
        out += ["", f"**Our modules ({n}):** {note}", "",
                "| Course | # | Module | Main lecture | More videos |", "|---|---|--------|--------------|-------------|"]
        for c, nums in mods.items():
            for num in nums:
                m = data[c][num]
                main_cell = f"[{m['main'][0][:60]}]({m['main'][1]})" if m["main"] else "-"
                out.append(f"| {short(c)} | {num} | {m['topic']} | {main_cell} | {m['supp'] or '-'} |")
        extras = [(s, GAPS.get(s, [])) for s, _ in slugs if GAPS.get(s)]
        if extras:
            out += ["", "**On roadmap.sh but not in our courses (learn these on roadmap.sh):**", ""]
            for s, names in extras:
                out.append(f"- [{s}]({RS}{s}) ({len(names)}): " + ", ".join(names))
        out.append("")
    out += ["---", f"_{total_mods} modules, {sum(1 for d in data.values() for m in d.values() if m['main']) + sum(m['supp'] for d in data.values() for m in d.values())} videos. "
            "Regenerate with `python scripts/generate_roadmap.py`._", ""]
    (ROOT / "ROADMAP.md").write_text("\n".join(out), encoding="utf-8")
    print(f"ROADMAP.md written: {total_mods} modules in {len(PHASES)} phases")


if __name__ == "__main__":
    main()

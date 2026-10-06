"""Mutation test of the DSA fuzz oracles: mutate a reference solution and expect a cross-check to fail.

    python tools/mutation_dsa.py

A surviving mutant means either an equivalent mutation (for example `<` versus `<=` in a loop whose boundary case is
unreachable) or a weak oracle. Last measured result is recorded in QUALITY_REPORT.md.
"""
import glob, json, os, shutil, subprocess, sys, tempfile

PRACTICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "05-DSA-Interview-Playbook", "practice")
WORK = os.path.join(tempfile.gettempdir(), "dsa_mut")
NEW = [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 17, 18, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 43, 45, 49, 51, 52, 61, 68, 71]
OPS = [(" <= ", " < "), (" < ", " <= "), (" + 1", " + 2"), (" - 1", " - 2"), (" > ", " >= "), (" max(", " min("),
       (" == ", " != "), ("not ", ""), ("True", "False"), ("False", "True")]


def run_fuzz(n, work):
    code = "import fuzz_checks, json; r = fuzz_checks.run(); print(json.dumps({str(k): [v[0], v[1]] for k, v in r.items()}))"
    env = {**os.environ, "DSA_SRC_DIR": work, "DSA_ONLY": str(n), "PYTHONIOENCODING": "utf-8"}
    try:
        p = subprocess.run([sys.executable, "-c", code], cwd=PRACTICE, capture_output=True, text=True, timeout=25, env=env)
    except subprocess.TimeoutExpired:
        return "timeout"
    lines = p.stdout.strip().splitlines()
    if p.returncode != 0 or not lines:
        return "crash"
    data = json.loads(lines[-1])
    return "mismatch" if data.get(str(n), ["", 0])[1] > 0 else "survived"


def main():
    results = {"killed": [], "survived": [], "skipped": []}
    for n in NEW:
        src = glob.glob(os.path.join(PRACTICE, "solutions", f"p{n:02d}_*.py"))[0]
        original = open(src, encoding="utf-8").read()
        cut = original.find("def run_tests")
        head = original if cut < 0 else original[:cut]
        marker = max(head.rfind("class GraphNode"), head.rfind("class TreeNode"), head.rfind("def from_list"))
        start = head.find("\n\n", marker) if marker >= 0 else 0
        outcomes = []
        for old, new in OPS:
            idx = head.find(old, start)
            if idx < 0:
                continue
            work = f"{WORK}_{n}_{len(outcomes)}"
            shutil.rmtree(work, ignore_errors=True)
            shutil.copytree(os.path.join(PRACTICE, "solutions"), work, ignore=shutil.ignore_patterns("__pycache__"))
            mutated = head[:idx] + new + head[idx + len(old):] + original[len(head):]
            open(os.path.join(work, os.path.basename(src)), "w", encoding="utf-8").write(mutated)
            outcomes.append((old.strip(), run_fuzz(n, work)))
            shutil.rmtree(work, ignore_errors=True)
            if len(outcomes) == 3:
                break
        if not outcomes:
            results["skipped"].append(n)
        for op, res in outcomes:
            results["survived" if res == "survived" else "killed"].append((n, op, res))
    print("killed:", len(results["killed"]), "survived:", len(results["survived"]), "problems skipped:", results["skipped"])
    print("survivors:", results["survived"])


main()

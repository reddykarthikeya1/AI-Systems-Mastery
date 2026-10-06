"""Generate a dry-run trace of a Core 75 solution on an input of your choice.

    python trace.py 1 "[2,7,11,15]" 9          # problem 1 (Two Sum) on nums=[2,7,11,15], target=9
    python trace.py 20 "[1,3,5,7,9]" 7         # Binary Search
    python trace.py 1 "[2,7,11,15]" 9 --stub   # trace YOUR stub in stubs/ instead of the reference solution

Arguments after the problem number are Python literals. For every executed line of the solution function the
tracer prints the line number, the source, and the local variables that changed since the previous line (so the
values next to a line are the effect of the line above it), which is exactly what a dry-run on a whiteboard records. Because the trace is generated from the code, it cannot drift away from what the code does.
"""
import ast
import glob
import importlib.util
import inspect
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    spec = importlib.util.spec_from_file_location("traced", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pick_function(mod, path):
    """The solution function is the first top-level function defined in the problem's own code (not helpers)."""
    skip = {"to_list", "from_list", "run_tests"}
    src = open(path, encoding="utf-8").read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and node.name not in skip:
            return getattr(mod, node.name)
    raise SystemExit("no solution function found in " + path)


def short(v, width=60):
    text = repr(v)
    return text if len(text) <= width else text[: width - 3] + "..."


def trace_call(fn, args, max_lines=200):
    lines, _ = inspect.getsourcelines(fn)
    first = fn.__code__.co_firstlineno
    prev, rows = {}, []

    def tracer(frame, event, arg):
        if frame.f_code is not fn.__code__:
            return tracer if event == "call" and frame.f_code.co_filename != fn.__code__.co_filename else None
        if event == "line":
            changed = {k: v for k, v in frame.f_locals.items() if k not in prev or prev[k] != v}
            src = lines[frame.f_lineno - first].strip() if 0 <= frame.f_lineno - first < len(lines) else ""
            rows.append((frame.f_lineno, src, changed))
            prev.clear()
            prev.update({k: (list(v) if isinstance(v, (list, dict, set)) else v) for k, v in frame.f_locals.items()})
            if len(rows) >= max_lines:
                return None
        elif event == "return":
            rows.append((frame.f_lineno, f"return {short(arg)}", {}))
        return tracer

    sys.settrace(tracer)
    try:
        result = fn(*args)
    finally:
        sys.settrace(None)
    return result, rows


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    stub = "--stub" in sys.argv
    if not argv:
        print(__doc__)
        return 0
    n = int(argv[0])
    folder = "stubs" if stub else "solutions"
    matches = glob.glob(os.path.join(HERE, folder, f"p{n:02d}_*.py"))
    if not matches:
        print(f"no file for problem {n} in {folder}/")
        return 1
    mod = load(matches[0])
    fn = pick_function(mod, matches[0])
    args = [ast.literal_eval(a) for a in argv[1:]]
    result, rows = trace_call(fn, args)
    print(f"{fn.__name__}({', '.join(short(a, 30) for a in args)})")
    for lineno, src, changed in rows:
        delta = "  ".join(f"{k}={short(v)}" for k, v in changed.items() if not k.startswith("__"))
        print(f"  line {lineno:>3}  {src:<48} {delta}")
    print(f"=> {short(result, 80)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

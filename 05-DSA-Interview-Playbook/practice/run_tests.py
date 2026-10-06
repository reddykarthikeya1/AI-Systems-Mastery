"""
Core 75 Automated Test Runner Harness
Usage:
  python run_tests.py            # Runs all 75 problems
  python run_tests.py <problem>  # Runs specific problem (e.g. '1', 'p01_two_sum', 'two_sum')
"""
import sys
import os
import glob
import importlib.util

def run_problem(sol_file):
    spec = importlib.util.spec_from_file_location("sol", sol_file)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        if hasattr(mod, "run_tests"):
            mod.run_tests()
        return True, "PASSED"
    except Exception as e:
        return False, str(e)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sol_dir = os.path.join(script_dir, "solutions")
    files = sorted(glob.glob(os.path.join(sol_dir, "p*.py")))

    if len(sys.argv) > 1:
        query = sys.argv[1].lower().strip()
        filtered = []
        for f in files:
            basename = os.path.basename(f).lower()
            # Match number like '1' or '01'
            if query.isdigit():
                prefix = f"p{int(query):02d}_"
                if basename.startswith(prefix):
                    filtered.append(f)
            elif query in basename:
                filtered.append(f)
        if not filtered:
            print(f"No problem matching '{query}' found.")
            sys.exit(1)
        files = filtered

    passed = 0
    failed = 0
    print(f"Running Core 75 Test Suite ({len(files)} problem(s))...\n" + "=" * 60)
    for f in files:
        prob_name = os.path.splitext(os.path.basename(f))[0]
        ok, msg = run_problem(f)
        if ok:
            passed += 1
            print(f" [PASS] {prob_name}")
        else:
            failed += 1
            print(f" [FAIL] {prob_name} -> {msg}")
    print("=" * 60)
    print(f"Results: {passed} PASSED, {failed} FAILED out of {len(files)} tests.")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

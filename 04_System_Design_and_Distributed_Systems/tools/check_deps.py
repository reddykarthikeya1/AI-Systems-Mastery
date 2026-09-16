#!/usr/bin/env python3
"""System Design Dependency and Environment Verifier.

Checks that the local Python environment satisfies all prerequisites for running
the architectural simulation prototypes, async servers, and pytest test suites.
"""

import importlib
import sys

REQUIRED_PYTHON_VERSION = (3, 10)

REQUIRED_PACKAGES = [
    ("pytest", "pytest", "Test execution framework"),
    ("pytest_asyncio", "pytest-asyncio", "Async test runner for asyncio L7 gateways & event streams"),
    ("ruff", "ruff", "Fast linter and code formatter"),
]

OPTIONAL_PACKAGES = [
    ("matplotlib", "matplotlib", "Visualization for latency charts and simulation plots"),
]

def check_python_version() -> bool:
    current = sys.version_info[:2]
    req_str = f"{REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}"
    cur_str = f"{current[0]}.{current[1]}"
    if current < REQUIRED_PYTHON_VERSION:
        print(f"[-] Python version {cur_str} is below required {req_str}")
        return False
    print(f"[+] Python runtime: {cur_str} (>= {req_str}) OK")
    return True

def check_packages(packages: list[tuple[str, str, str]], required: bool = True) -> int:
    missing = 0
    prefix = "[+]" if required else "[*]"
    category = "Required" if required else "Optional"
    print(f"\n--- Checking {category} Dependencies ---")
    for module_name, pip_name, desc in packages:
        try:
            mod = importlib.import_module(module_name)
            ver = getattr(mod, "__version__", "unknown")
            print(f"  {prefix} {pip_name:<18} (version {ver}) - {desc}")
        except ImportError:
            if required:
                print(f"  [-] MISSING REQUIRED: {pip_name:<18} - {desc}")
                print(f"      Install via: pip install {pip_name}")
                missing += 1
            else:
                print(f"  [ ] Optional omitted: {pip_name:<18} - {desc}")
    return missing

def main() -> int:
    print("=" * 65)
    print("  System Design Course: Environment & Dependency Verification")
    print("=" * 65)

    py_ok = check_python_version()
    missing_req = check_packages(REQUIRED_PACKAGES, required=True)
    check_packages(OPTIONAL_PACKAGES, required=False)

    print("\n" + "=" * 65)
    if not py_ok or missing_req > 0:
        print(f"[-] FAILED: {missing_req} required package(s) missing or Python too old.")
        print("    Run: pip install pytest pytest-asyncio ruff")
        return 1

    print("[+] SUCCESS: All System Design prerequisites are satisfied!")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    sys.exit(main())

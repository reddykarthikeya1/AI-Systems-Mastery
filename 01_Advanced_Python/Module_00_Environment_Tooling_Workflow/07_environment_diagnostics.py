#!/usr/bin/env python3
"""Module 00: Environment Diagnostics & Introspection Script.

This script inspects the running Python interpreter, active virtual environment,
search paths (sys.path), platform details, and modern runtime flags (GIL, free-threading).
"""

from __future__ import annotations

import os
import platform
import sys
import sysconfig


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def check_runtime_version() -> None:
    print_section("1. Python Runtime & Interpreter")
    print(f"Python Version      : {sys.version.split()[0]}")
    print(f"Full Version Info   : {sys.version}")
    print(f"Compiler            : {platform.python_compiler()}")
    print(f"Implementation      : {platform.python_implementation()}")
    print(f"Interpreter Path    : {sys.executable}")


def check_virtual_environment() -> None:
    print_section("2. Virtual Environment Detection")
    is_venv = sys.prefix != sys.base_prefix
    venv_env_var = os.environ.get("VIRTUAL_ENV")

    print(f"Inside Virtualenv?  : {'YES (Isolated)' if is_venv else 'NO (System / Global Python)'}")
    print(f"sys.prefix          : {sys.prefix}")
    print(f"sys.base_prefix     : {sys.base_prefix}")
    print(f"VIRTUAL_ENV env var : {venv_env_var if venv_env_var else 'Not set'}")

    if not is_venv:
        print("\n  [WARNING] You are currently running in the global/base Python environment.")
        print("            Best practice is to use a virtual environment via `uv venv` or `python -m venv .venv`.")


def check_site_packages_and_syspath() -> None:
    print_section("3. Module Resolution & sys.path")
    site_packages = sysconfig.get_paths().get("purelib", "Unknown")
    print(f"Primary site-packages directory:\n  {site_packages}\n")

    print("sys.path entries (in search order):")
    for idx, path in enumerate(sys.path, start=1):
        print(f"  [{idx:02d}] {path}")


def check_modern_features_and_gil() -> None:
    print_section("4. Concurrency & Runtime Capabilities")

    # Check for free-threading / GIL status if running Python 3.13+
    has_gil_api = hasattr(sys, "_is_gil_enabled")
    if has_gil_api:
        gil_enabled = sys._is_gil_enabled()
        print("Free-Threading API  : Supported")
        print(f"GIL Enabled?        : {'YES' if gil_enabled else 'NO (Free-threaded build)'}")
    else:
        print("Free-Threading API  : Not available in this Python build (Standard GIL active)")

    print(f"Bytecode Cache Dir  : {sys.pycache_prefix or 'Default (__pycache__ alongside .py)'}")
    print(f"Recursion Limit     : {sys.getrecursionlimit()}")
    print(f"Float Info (Epsilon): {sys.float_info.epsilon}")


def check_system_platform() -> None:
    print_section("5. Host Machine & Platform")
    print(f"OS Platform         : {platform.platform()}")
    print(f"System Architecture : {platform.machine()} ({platform.architecture()[0]})")
    print(f"CPU Core Count      : {os.cpu_count()} logical cores")
    print(f"Current Working Dir : {os.getcwd()}")


def main() -> None:
    print("\n" + "#" * 60)
    print("      PYTHON ENVIRONMENT INTROSPECTION & DIAGNOSTICS")
    print("#" * 60)

    check_runtime_version()
    check_virtual_environment()
    check_site_packages_and_syspath()
    check_modern_features_and_gil()
    check_system_platform()

    print("\n" + "#" * 60)
    print("  Diagnostics complete. Review the settings above.")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()

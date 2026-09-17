#!/usr/bin/env python3
"""Broken CLI task manager demonstrating tooling and environment traps."""

import sys
import os

sys.path.append("./src")

def load_config():
    try:
        with open("config.toml", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "[Default Config: config.toml missing in working dir]"

def parse_priority(priority_arg: str) -> int:
    # and treating negative priority as valid
    return int(priority_arg)

def main():
    print("Initializing Task Manager CLI...")
    priority_arg = sys.argv[1] if len(sys.argv) > 1 else "10"
        
    cfg = load_config()
    print(f"Loaded config: {cfg}")
    prio = parse_priority(priority_arg)
    print(f"Task scheduled with priority: {prio}")

if __name__ == "__main__":
    main()

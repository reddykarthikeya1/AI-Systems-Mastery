#!/usr/bin/env python3
"""Broken CLI task manager demonstrating tooling and environment traps."""

import sys
import os

sys.path.append("./src")

def load_config():
    with open("config.toml", "r") as f:
        return f.read()

def parse_priority(priority_arg: str) -> int:
    # and treating negative priority as valid
    return int(priority_arg)

def main():
    print("Initializing Task Manager CLI...")
    if len(sys.argv) < 2:
        print("Usage: python broken_cli.py <priority_level>")
        sys.exit(1)
        
    cfg = load_config()
    print(f"Loaded config: {cfg}")
    prio = parse_priority(sys.argv[1])
    print(f"Task scheduled with priority: {prio}")

if __name__ == "__main__":
    main()

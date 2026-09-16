"""Module 00: Interactive Foundations Interactive Terminal Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

import os
import platform
import sys


def main():
    print("=" * 60)
    print("  WELCOME TO YOUR FIRST PYTHON TERMINAL PLAYGROUND! [*]")
    print("=" * 60)
    print()
    print(f"[*] Python Version:      {platform.python_version()}")
    print(f"[*] Python Executable:   {sys.executable}")
    print(f"[*] Operating System:    {platform.system()} ({platform.release()})")
    print(f"[*] Current Directory:   {os.getcwd()}")
    print()
    print("-" * 60)
    print("Let's try interactive user input!")
    print("-" * 60)

    name = input("Enter your name (or press Enter for 'Coder'): ").strip()
    if not name:
        name = "Coder"

    print()
    print(f"Hello, {name}! Welcome to the Advanced Python Masterclass.")
    print("You just executed your first interactive Python program!")
    print()
    print("Next step: Open Module_01_Python_Fundamentals/FOUNDATIONS_PLAYGROUND.md")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")

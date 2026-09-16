#!/usr/bin/env bash
# AI & Systems Academy - Linux Launcher
# Copyright (c) Karthikeya Reddy. All rights reserved.

# Ensure working directory is the repository root
cd "$(dirname "$0")"

echo "================================================================================"
echo "   AI & SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY"
echo "   Ultra Gold Standard 12-Course Interactive Learning Platform"
echo "================================================================================"
echo ""
echo "[*] Locating Python 3 runtime..."

PY_CMD=""
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null && python -c 'import sys; exit(0 if sys.version_info[0] >= 3 else 1)' &>/dev/null; then
    PY_CMD="python"
elif [ -x "/usr/bin/python3" ]; then
    PY_CMD="/usr/bin/python3"
elif [ -x "/usr/local/bin/python3" ]; then
    PY_CMD="/usr/local/bin/python3"
fi

if [ -z "$PY_CMD" ]; then
    echo ""
    echo "[!] Python 3.10+ was not automatically detected on this system."
    echo "[!] Please install python3 from your package manager (e.g., sudo apt install python3)"
    echo ""
    read -p "Press [Enter] to exit..."
    exit 1
fi

echo "[OK] Python runtime detected: $($PY_CMD --version)"
echo "[*] Launching Academy Platform in Standalone Application Mode..."
echo "[*] Close the application window or press Ctrl+C to exit."
echo ""

$PY_CMD start_platform.py "$@"

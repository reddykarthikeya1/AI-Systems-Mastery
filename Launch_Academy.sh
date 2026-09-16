#!/usr/bin/env bash
# AI & Systems Academy - Linux / macOS Launcher
# Copyright (c) Karthikeya Reddy. All rights reserved.

set -e

echo "================================================================================"
echo "   AI & SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY"
echo "   Ultra Gold Standard 12-Course Interactive Learning Platform"
echo "================================================================================"
echo ""
echo "[*] Locating Python runtime..."

PY_CMD=""
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "[!] Python 3 is required. Please install Python from https://python.org or your package manager."
    exit 1
fi

echo "[OK] Python detected: $($PY_CMD --version)"
echo "[*] Launching Academy Platform..."
$PY_CMD start_platform.py

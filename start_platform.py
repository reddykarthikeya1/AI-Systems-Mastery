"""Root Standalone Platform Launcher.

Launches the Coursera-grade AI & Systems Academy web application locally.
Serves the production React client and FastAPI dynamic auto-discovery backend.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SERVER_DIR = ROOT_DIR / "learning_platform" / "server"
CLIENT_DIR = ROOT_DIR / "learning_platform" / "client"
DIST_DIR = CLIENT_DIR / "dist"

BANNER = r"""
================================================================================
   AI & SYSTEMS ENGINEERING ACADEMY — BY KARTHIKEYA REDDY
   Ultra Gold Standard 12-Course Interactive Learning Platform
================================================================================
  * Dynamic Auto-Discovery Engine: Active
  * Interactive Pytest & Demo Runner: Enabled
  * Dual Local Progress Persistence: Active (.study_progress.json)
  * Platform URL: http://localhost:8000
================================================================================
"""


def ensure_client_built() -> None:
    """Ensures the React client is built into dist/ before starting server."""
    if not (DIST_DIR / "index.html").is_file():
        print("[*] Client production build not detected. Building frontend...")
        try:
            subprocess.run(["npm", "run", "build"], cwd=str(CLIENT_DIR), check=True)
            print("[✓] Frontend successfully built.")
        except Exception as exc:
            print(f"[!] Warning: Frontend build encountered an error ({exc}).")
            print("[!] Running in API mode; please ensure client dependencies are installed.")


def main() -> None:
    print(BANNER)
    ensure_client_built()

    sys.path.insert(0, str(SERVER_DIR))
    import uvicorn

    def open_browser() -> None:
        time.sleep(1.2)
        print("\n[+] Opening Academy Learning Portal in your default browser...")
        webbrowser.open("http://localhost:8000")

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    print("[*] Starting High-Performance Local Server at http://127.0.0.1:8000 ...")
    print("[*] Press Ctrl+C at any time to stop.\n")

    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            log_level="info",
            app_dir=str(SERVER_DIR),
        )
    except KeyboardInterrupt:
        print("\n[*] Academy Platform safely stopped. Happy studying!")


if __name__ == "__main__":
    main()

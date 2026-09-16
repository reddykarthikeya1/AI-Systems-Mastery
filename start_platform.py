"""Root Standalone Platform Launcher.

Launches the Coursera-grade AI and Systems Academy web application locally with ZERO manual setup.
Serves the production React client and FastAPI dynamic auto-discovery backend.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent
SERVER_DIR = ROOT_DIR / "learning_platform" / "server"
CLIENT_DIR = ROOT_DIR / "learning_platform" / "client"
DIST_DIR = CLIENT_DIR / "dist"
PROGRESS_FILE = ROOT_DIR / ".study_progress.json"

BANNER = r"""
================================================================================
   AI AND SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY
   Ultra Gold Standard 12-Course Interactive Learning Platform
================================================================================
  * Dynamic Auto-Discovery Engine: Ready
  * Interactive Pytest and Demo Runner: Ready
  * Dual Local Progress Persistence: Ready (.study_progress.json)
  * Platform URL: http://localhost:8000
================================================================================
"""


def ensure_client_built() -> None:
    """Ensures the React client is built into dist/ before starting server."""
    if not (DIST_DIR / "index.html").is_file():
        print("[*] Client production build not detected. Attempting to build frontend...")
        try:
            subprocess.run(["npm", "run", "build"], cwd=str(CLIENT_DIR), check=True)
            print("[OK] Frontend successfully built.")
        except Exception as exc:
            print(f"[!] Warning: Frontend build skipped or encountered an error ({exc}).")


def ensure_dependencies() -> bool:
    """Verifies backend dependencies (fastapi, uvicorn).
    If missing, automatically installs them via pip.
    Returns True if fastapi/uvicorn are ready, False otherwise.
    """
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        print("[*] First-time setup: Installing required dependencies (fastapi, uvicorn)...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "--quiet"],
                check=True,
            )
            import fastapi  # type: ignore # noqa: F401
            import uvicorn  # type: ignore # noqa: F401
            print("[OK] Dependencies installed successfully.")
            return True
        except Exception as exc:
            print(f"[!] Pip install unavailable or offline: {exc}")
            print("[*] Switching to Native Zero-Dependency Fallback Server...")
            return False


def run_fallback_server(port: int = 8000) -> None:
    """Zero-dependency fallback HTTP server using Python standard library.
    Ensures the platform operates even on completely offline machines or environments without pip.
    """
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import urllib.parse

    COURSE_CATEGORIES = {
        "01": ("Language and Systems Mastery", "Advanced", 30),
        "02": ("Core Computer Science", "Advanced", 25),
        "03": ("Storage Engines and Distributed DBs", "Staff", 35),
        "04": ("Distributed Systems and Reliability", "Staff", 30),
        "05": ("Foundations for Machine Learning", "Advanced", 40),
        "06": ("Deep Learning and Transformer Foundations", "Advanced", 35),
        "07": ("GPU Systems and High-Performance Kernels", "Staff", 40),
        "08": ("GPU Clusters and Large-Scale Training", "Principal", 45),
        "09": ("LLM Serving and Low-Latency Engines", "Principal", 40),
        "10": ("Context Engineering and Vector Retrieval", "Staff", 30),
        "11": ("Autonomous Systems and Cognitive Topologies", "Staff", 35),
        "12": ("GenAI Security, Red Teaming and Guardrails", "Staff", 30),
    }

    def get_courses():
        courses = []
        for item in sorted(ROOT_DIR.iterdir()):
            if not item.is_dir():
                continue
            match = re.match(r"^(\d{2})_(.+)$", item.name)
            if not match:
                continue
            num_str = match.group(1)
            course_num = int(num_str)
            clean_title = match.group(2).replace("_", " ")
            category, difficulty, est_hours = COURSE_CATEGORIES.get(
                num_str, ("Advanced AI Systems", "Advanced", 30)
            )
            desc = f"Mastery of {clean_title} through production-grade systems implementations."
            readme_path = item / "README.md"
            if readme_path.is_file():
                try:
                    for line in readme_path.read_text(encoding="utf-8", errors="ignore").splitlines()[:10]:
                        if line.startswith("> **") or (line.strip() and not line.startswith("#")):
                            desc = line.strip().lstrip(">").strip()
                            break
                except Exception:
                    pass
            modules = [m for m in item.iterdir() if m.is_dir() and m.name.startswith("Module_")]
            quickstart = item / "00_quickstart_interactive_demo.py"
            quickstart_rel = quickstart.relative_to(ROOT_DIR).as_posix() if quickstart.exists() else None
            courses.append({
                "id": item.name,
                "course_num": course_num,
                "title": clean_title,
                "folder_name": item.name,
                "category": category,
                "difficulty": difficulty,
                "estimated_hours": est_hours,
                "module_count": len(modules),
                "description": desc,
                "quickstart_script": quickstart_rel,
            })
        return sorted(courses, key=lambda c: c["course_num"])

    def get_modules(course_folder_name: str):
        course_path = ROOT_DIR / course_folder_name
        if not course_path.is_dir():
            return None
        raw_dirs = [d for d in course_path.iterdir() if d.is_dir() and d.name.startswith("Module_")]
        def get_mod_num(d: Path) -> int:
            m = re.search(r"Module_(\d+)", d.name)
            return int(m.group(1)) if m else 999
        module_dirs = sorted(raw_dirs, key=get_mod_num)
        result = []
        for mod_dir in module_dirs:
            mod_num = get_mod_num(mod_dir)
            clean_mod_name = re.sub(r"^Module_\d+_", "", mod_dir.name).replace("_", " ")
            lessons = []
            for f in sorted(mod_dir.iterdir()):
                if not f.is_file() or f.name.startswith("."):
                    continue
                if f.name.endswith(".md"):
                    title = f.stem.replace("_", " ")
                    ltype = "theory"
                    if "FOUNDATIONS_PLAYGROUND" in f.name:
                        ltype = "playground"
                        title = "Interactive Foundations Playground"
                    elif "PROJECT" in f.name:
                        ltype = "project"
                    elif "QUIZ" in f.name:
                        ltype = "quiz"
                    elif "TROUBLESHOOTING" in f.name:
                        ltype = "troubleshooting"
                    lessons.append({
                        "id": f.name,
                        "title": title,
                        "file_path": f.relative_to(ROOT_DIR).as_posix(),
                        "type": ltype,
                    })
                elif f.name.endswith(".py") and not f.name.startswith("__"):
                    lessons.append({
                        "id": f.name,
                        "title": f"Interactive Code: {f.name}",
                        "file_path": f.relative_to(ROOT_DIR).as_posix(),
                        "type": "code",
                    })
            has_sol = (mod_dir / "project_solution").is_dir() or any("solution" in f.name.lower() for f in mod_dir.iterdir() if f.is_file())
            has_star = (mod_dir / "starter").is_dir() or any("starter" in f.name.lower() for f in mod_dir.iterdir() if f.is_file())
            has_debug = (mod_dir / "debug_lab").is_dir()
            result.append({
                "id": mod_dir.name,
                "module_num": mod_num,
                "title": clean_mod_name,
                "folder_path": mod_dir.relative_to(ROOT_DIR).as_posix(),
                "lessons": lessons,
                "has_solution": has_sol,
                "has_starter": has_star,
                "has_debug_lab": has_debug,
            })
        return result

    def get_progress():
        if PROGRESS_FILE.is_file():
            try:
                return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"completed_lessons": [], "completed_modules": [], "current_course": None, "current_lesson": None, "last_updated": time.time(), "theme": "dark"}

    def save_progress(data):
        data["last_updated"] = time.time()
        PROGRESS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data

    class FallbackHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIST_DIR), **kwargs)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)

            if parsed.path == "/api/courses":
                self.send_json(get_courses())
                return
            elif parsed.path.startswith("/api/courses/") and parsed.path.endswith("/modules"):
                course_id = parsed.path.split("/")[3]
                mods = get_modules(course_id)
                if mods is not None:
                    self.send_json(mods)
                else:
                    self.send_error(404, "Course not found")
                return
            elif parsed.path == "/api/content":
                file_path = query.get("path", [None])[0]
                if not file_path:
                    self.send_error(400, "Missing path parameter")
                    return
                target = ROOT_DIR / file_path
                if not target.is_file():
                    self.send_error(404, "File not found")
                    return
                try:
                    content = target.read_text(encoding="utf-8", errors="replace")
                    self.send_json({"content": content, "path": file_path})
                except Exception as exc:
                    self.send_error(500, str(exc))
                return
            elif parsed.path == "/api/progress":
                self.send_json(get_progress())
                return
            elif parsed.path == "/api/project-files":
                mod_path = query.get("module_path", [None])[0]
                if not mod_path:
                    self.send_error(400, "Missing module_path")
                    return
                safe_mod = (ROOT_DIR / mod_path).resolve()
                if not str(safe_mod).startswith(str(ROOT_DIR)) or not safe_mod.is_dir():
                    self.send_error(404, "Module not found")
                    return

                starter_dir = safe_mod / "starter"
                solution_dir = safe_mod / "project_solution"
                user_ws = ROOT_DIR / ".user_workspaces" / mod_path

                file_dict = {}
                if starter_dir.is_dir():
                    for f in starter_dir.rglob("*.py"):
                        if f.is_file() and not f.name.startswith("."):
                            rel = f.relative_to(starter_dir).as_posix()
                            file_dict[rel] = {"filename": rel, "starter": f.read_text(encoding="utf-8", errors="replace"), "solution": None, "user": None}

                if solution_dir.is_dir():
                    for f in solution_dir.rglob("*.py"):
                        if f.is_file() and not f.name.startswith("."):
                            rel = f.relative_to(solution_dir).as_posix()
                            if rel in file_dict:
                                file_dict[rel]["solution"] = f.read_text(encoding="utf-8", errors="replace")
                            else:
                                file_dict[rel] = {"filename": rel, "starter": "", "solution": f.read_text(encoding="utf-8", errors="replace"), "user": None}

                if user_ws.is_dir():
                    for f in user_ws.rglob("*.py"):
                        if f.is_file() and not f.name.startswith("."):
                            rel = f.relative_to(user_ws).as_posix()
                            if rel in file_dict:
                                file_dict[rel]["user"] = f.read_text(encoding="utf-8", errors="replace")

                files = []
                for fname, d in file_dict.items():
                    content = d["user"] if d["user"] is not None else d["starter"]
                    files.append({
                        "filename": fname,
                        "content": content,
                        "starter_content": d["starter"],
                        "solution_content": d["solution"],
                        "is_modified": d["user"] is not None,
                    })

                self.send_json({
                    "has_project": bool(file_dict),
                    "module_path": mod_path,
                    "files": files,
                })
                return
            elif parsed.path == "/api/debug-files":
                mod_path = query.get("module_path", [None])[0]
                if not mod_path:
                    self.send_error(400, "Missing module_path")
                    return
                safe_mod = (ROOT_DIR / mod_path).resolve()
                if not str(safe_mod).startswith(str(ROOT_DIR)) or not safe_mod.is_dir():
                    self.send_error(404, "Module not found")
                    return

                debug_dir = safe_mod / "debug_lab"
                if not debug_dir.is_dir():
                    self.send_json({"has_debug_lab": False, "files": []})
                    return

                files = []
                symptoms = ""
                for f in sorted(debug_dir.iterdir()):
                    if not f.is_file() or f.name.startswith(".") or f.name == "__pycache__":
                        continue
                    txt = f.read_text(encoding="utf-8", errors="replace")
                    if f.name.upper() == "SYMPTOMS.MD":
                        symptoms = txt
                    files.append({"filename": f.name, "content": txt})

                self.send_json({
                    "has_debug_lab": True,
                    "module_path": mod_path,
                    "symptoms": symptoms,
                    "files": files,
                })
                return
            elif parsed.path == "/api/search":
                q = query.get("q", [""])[0].lower().strip()
                if len(q) < 2:
                    self.send_json([])
                    return
                results = []
                courses = get_courses()
                for c in courses:
                    if q in c["title"].lower() or q in c["category"].lower():
                        results.append({
                            "type": "course",
                            "id": c["id"],
                            "course_id": c["id"],
                            "title": c["title"],
                            "subtitle": f"{c['category']} • {c['module_count']} Modules",
                            "path": c["folder_name"],
                        })
                    mods = get_modules(c["folder_name"])
                    if mods:
                        for m in mods:
                            if q in m["title"].lower():
                                results.append({
                                    "type": "module",
                                    "id": m["id"],
                                    "course_id": c["id"],
                                    "course_title": c["title"],
                                    "title": f"Module {m['module_num']:02d}: {m['title']}",
                                    "subtitle": f"Course: {c['title']}",
                                    "path": m["folder_path"],
                                })
                            for l in m["lessons"]:
                                if q in l["title"].lower() or q in l["file_path"].lower():
                                    results.append({
                                        "type": "lesson",
                                        "id": l["id"],
                                        "course_id": c["id"],
                                        "course_title": c["title"],
                                        "module_id": m["id"],
                                        "module_title": m["title"],
                                        "title": l["title"],
                                        "subtitle": f"{c['title']} • Module {m['module_num']:02d}",
                                        "path": l["file_path"],
                                        "lesson_type": l.get("type", "theory"),
                                    })
                self.send_json(results[:35])
                return

            req_path = parsed.path.lstrip("/")
            local_target = DIST_DIR / req_path
            if not local_target.is_file():
                self.path = "/index.html"
            return super().do_GET()

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            if parsed.path == "/api/progress":
                res = save_progress(payload)
                self.send_json(res)
                return
            elif parsed.path == "/api/save-project-file":
                mod_path = payload.get("module_path", "")
                fname = payload.get("filename", "")
                content_str = payload.get("content", "")
                safe_mod = (ROOT_DIR / mod_path).resolve()
                if not str(safe_mod).startswith(str(ROOT_DIR)):
                    self.send_error(403, "Access denied")
                    return
                target_dir = ROOT_DIR / ".user_workspaces" / mod_path
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_dir / Path(fname).name
                target_file.write_text(content_str, encoding="utf-8")
                self.send_json({"status": "saved", "path": str(target_file.relative_to(ROOT_DIR))})
                return
            elif parsed.path == "/api/run-code":
                code = payload.get("code", "")
                mode = payload.get("mode", "python")
                wdir = payload.get("working_dir")
                timeout_sec = payload.get("timeout_sec", 25)

                target_cwd = ROOT_DIR
                if wdir:
                    cand = (ROOT_DIR / wdir).resolve()
                    if cand.is_dir() and str(cand).startswith(str(ROOT_DIR)):
                        target_cwd = cand

                import tempfile
                temp_file = None
                start_time = time.perf_counter()
                try:
                    if mode == "powershell":
                        with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False, encoding="utf-8") as tf:
                            tf.write(code)
                            temp_file = tf.name
                        ps_exe = "powershell.exe" if sys.platform == "win32" else "pwsh"
                        cmd = [ps_exe, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", temp_file]
                    elif mode == "shell":
                        if sys.platform == "win32":
                            with tempfile.NamedTemporaryFile(mode="w", suffix=".bat", delete=False, encoding="utf-8") as tf:
                                tf.write("@echo off\n" + code)
                                temp_file = tf.name
                            cmd = ["cmd.exe", "/c", temp_file]
                        else:
                            with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False, encoding="utf-8") as tf:
                                tf.write("#!/usr/bin/env bash\n" + code)
                                temp_file = tf.name
                            cmd = ["/bin/bash", temp_file]
                    else:
                        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
                            tf.write(code)
                            temp_file = tf.name
                        cmd = [sys.executable, temp_file]

                    proc = subprocess.run(
                        cmd,
                        cwd=str(target_cwd),
                        capture_output=True,
                        text=True,
                        timeout=timeout_sec,
                        input="",
                    )
                    duration = time.perf_counter() - start_time
                    rel_cwd = target_cwd.relative_to(ROOT_DIR).as_posix() if target_cwd != ROOT_DIR else "."
                    self.send_json({
                        "exit_code": proc.returncode,
                        "stdout": proc.stdout,
                        "stderr": proc.stderr,
                        "duration_sec": round(duration, 3),
                        "status": "passed" if proc.returncode == 0 else "failed",
                        "cwd": rel_cwd,
                        "mode": mode,
                    })
                except Exception as exc:
                    rel_cwd = target_cwd.relative_to(ROOT_DIR).as_posix() if target_cwd != ROOT_DIR else "."
                    self.send_json({
                        "exit_code": -1,
                        "stdout": "",
                        "stderr": str(exc),
                        "duration_sec": 0.0,
                        "status": "error",
                        "cwd": rel_cwd,
                        "mode": mode,
                    })
                finally:
                    if temp_file and os.path.exists(temp_file):
                        try:
                            os.remove(temp_file)
                        except Exception:
                            pass
                return

            self.send_error(404, "Not found")

        def send_json(self, data: Any):
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    httpd = HTTPServer(("127.0.0.1", port), FallbackHandler)
    print(f"[*] Native Fallback Server active at http://127.0.0.1:{port} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Academy Platform safely stopped. Happy studying!")


def main() -> None:
    print(BANNER)
    ensure_client_built()

    has_uvicorn = ensure_dependencies()

    def open_browser() -> None:
        time.sleep(1.2)
        print("\n[+] Opening Academy Learning Portal in your default browser...")
        webbrowser.open("http://localhost:8000")

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    if has_uvicorn:
        sys.path.insert(0, str(SERVER_DIR))
        import uvicorn

        print("[*] Starting High-Performance FastAPI Server at http://127.0.0.1:8000 ...")
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
    else:
        run_fallback_server(port=8000)


if __name__ == "__main__":
    main()

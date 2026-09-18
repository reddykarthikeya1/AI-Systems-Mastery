"""Root Standalone Platform Launcher.

Launches the AI and Systems Academy interactive learning platform locally with ZERO manual setup.
Can run as a dedicated desktop application window or standard web browser interface.
Serves the pre-compiled React client and FastAPI / fallback dynamic auto-discovery backend.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent
SERVER_DIR = ROOT_DIR / "learning_platform" / "server"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))
CLIENT_DIR = ROOT_DIR / "learning_platform" / "client"
DIST_DIR = CLIENT_DIR / "dist"
PROGRESS_FILE = ROOT_DIR / ".study_progress.json"

BANNER = r"""
================================================================================
   AI AND SYSTEMS ENGINEERING ACADEMY - BY KARTHIKEYA REDDY
   Ultra Gold Standard 12-Course Interactive Learning Platform
================================================================================
  * Desktop Application Mode: Ready (Standalone native window)
  * Dynamic Auto-Discovery Engine: Ready
  * Interactive Pytest & LeetCode Arena: Ready
  * Dual Local Progress Persistence: Ready (.study_progress.json)
  * Platform URL: http://127.0.0.1:{port}
================================================================================
"""


def ensure_client_built(force_rebuild: bool = False) -> None:
    """Ensures the React client is built into dist/ before starting server.
    Rebuilds if dist/index.html is missing or if force_rebuild is requested.
    """
    dist_index = DIST_DIR / "index.html"
    needs_build = not dist_index.is_file() or force_rebuild

    if needs_build:
        print("[*] Client production build is missing or rebuild requested. Building frontend...")
        try:
            subprocess.run(["npm", "run", "build"], cwd=str(CLIENT_DIR), check=True, shell=(sys.platform == "win32"))
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


def run_fallback_server(port: int = 8000, server_holder: Optional[Dict[str, Any]] = None) -> None:
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
            def get_f_num(f: Path) -> int:
                m = re.match(r"^(\d+)", f.name)
                return int(m.group(1)) if m else 999

            cand_files = []
            for f in mod_dir.iterdir():
                if not f.is_file() or f.name.startswith("."):
                    continue
                if f.name.startswith("__") or f.name in [
                    "conftest.py", "pyproject.toml", "uv.lock", "requirements.txt",
                    "student.json", "groceries.txt", "notes.txt"
                ]:
                    continue
                if f.suffix.lower() in [".md", ".py", ".ps1", ".sh", ".ipynb"]:
                    cand_files.append(f)

            cand_files.sort(key=lambda f: (get_f_num(f), f.name))

            lessons = []
            for target in cand_files:
                fname_upper = target.name.upper()
                ext = target.suffix.lower()

                if ext == ".md":
                    if "README" in fname_upper:
                        label = "Theoretical Foundations & Architecture"
                        ltype = "theory"
                    elif "PLAYGROUND" in fname_upper:
                        label = "Interactive Foundations Playground"
                        ltype = "playground"
                    elif "ZERO_TO_ONE" in fname_upper or "BEGINNER" in fname_upper:
                        label = "Beginner Zero-to-One On-Ramp"
                        ltype = "playground"
                    elif "PROJECT" in fname_upper or "GUIDE" in fname_upper:
                        label = "Guided Hands-on Project"
                        ltype = "project"
                    elif "LEETCODE" in fname_upper:
                        label = "🧠 LeetCode Problem Studio"
                        ltype = "challenge"
                    elif "SELF_ASSESSMENT" in fname_upper or "CHALLENGE" in fname_upper or "QUIZ" in fname_upper:
                        label = "Staff Interview Challenges & Quizzes"
                        ltype = "quiz"
                    elif "TROUBLESHOOTING" in fname_upper or "EDGE_CASES" in fname_upper:
                        label = "Troubleshooting & Forensic Edge Cases"
                        ltype = "troubleshooting"
                    else:
                        clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                        label = f"Guide: {clean_name}"
                        ltype = "theory"
                elif ext == ".py":
                    clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                    if "try_it_yourself" in target.name.lower():
                        label = "Interactive Sandbox: Try It Yourself"
                    elif "demo" in target.name.lower():
                        label = f"Code Demo: {clean_name}"
                    else:
                        label = f"Code Lab: {clean_name}"
                    ltype = "code"
                elif ext == ".ps1":
                    clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                    label = f"PowerShell Automation: {clean_name}"
                    ltype = "powershell"
                elif ext == ".ipynb":
                    clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                    label = f"Jupyter Visual Lab: {clean_name}"
                    ltype = "notebook"
                elif ext == ".sh":
                    clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                    label = f"Shell Script: {clean_name}"
                    ltype = "shell"
                else:
                    clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ").title()
                    label = f"File: {clean_name}"
                    ltype = "theory"

                lessons.append({
                    "id": f"{mod_dir.name}_{target.name}",
                    "title": label,
                    "file_path": target.relative_to(ROOT_DIR).as_posix(),
                    "type": ltype,
                })

            lessons_dir = mod_dir / "lessons"
            if lessons_dir.is_dir():
                sub_files = [
                    lf for lf in lessons_dir.iterdir()
                    if lf.is_file() and not lf.name.startswith(".") and lf.suffix.lower() in [".md", ".py", ".ps1", ".sh", ".ipynb"]
                ]
                sub_files.sort(key=lambda f: (get_f_num(f), f.name))
                for lf in sub_files:
                    clean_l_title = re.sub(r"^\d+_", "", lf.stem).replace("_", " ").title()
                    ext = lf.suffix.lower()
                    if ext == ".py":
                        ltype = "code"
                        clean_l_title = f"Code: {clean_l_title}"
                    elif ext == ".ipynb":
                        ltype = "notebook"
                        clean_l_title = f"Notebook: {clean_l_title}"
                    else:
                        ltype = "theory"
                        clean_l_title = f"Lesson: {clean_l_title}"

                    lessons.append({
                        "id": f"{mod_dir.name}_{lf.name}",
                        "title": clean_l_title,
                        "file_path": lf.relative_to(ROOT_DIR).as_posix(),
                        "type": ltype,
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
            elif parsed.path == "/api/dsa-problems" or parsed.path.startswith("/api/dsa-problems"):
                mod_param = query.get("module", [None])[0]
                try:
                    from dsa_problems import get_dsa_problems
                    self.send_json(get_dsa_problems(mod_param))
                except Exception as exc:
                    self.send_json({"error": str(exc), "problems": []})
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

            if parsed.path == "/api/client-disconnect":
                self.send_json({"status": "shutdown_scheduled"})
                def _fallback_exit():
                    time.sleep(3.5)
                    print("\n[*] Application window/tab closed. Cleaning up and stopping backend...")
                    os._exit(0)
                threading.Thread(target=_fallback_exit, daemon=True).start()
                return
            elif parsed.path == "/api/progress":
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
            elif parsed.path == "/api/run-dsa-test":
                prob_id = payload.get("problem_id", "")
                user_code = payload.get("code", "")
                submit = payload.get("submit", False)
                try:
                    from dsa_problems import run_dsa_solution
                    res = run_dsa_solution(prob_id, user_code, submit=submit)
                    self.send_json(res)
                except Exception as exc:
                    self.send_json({
                        "status": "error",
                        "error": str(exc),
                        "all_passed": False,
                        "passed_cases": 0,
                        "total_cases": 0,
                        "duration_ms": 0.0,
                        "results": []
                    })
                return
            elif parsed.path == "/api/format-code":
                code = payload.get("code", "")
                lang = payload.get("language", "python").lower()
                if not code.strip():
                    self.send_json({"formatted": code, "status": "unchanged"})
                    return
                if lang == "python":
                    try:
                        res = subprocess.run(
                            [sys.executable, "-m", "ruff", "format", "-"],
                            input=code,
                            capture_output=True,
                            text=True,
                            timeout=5,
                        )
                        if res.returncode == 0 and res.stdout:
                            self.send_json({"formatted": res.stdout, "status": "formatted"})
                            return
                    except Exception:
                        pass
                    try:
                        res = subprocess.run(
                            [sys.executable, "-m", "black", "-", "--quiet"],
                            input=code,
                            capture_output=True,
                            text=True,
                            timeout=5,
                        )
                        if res.returncode == 0 and res.stdout:
                            self.send_json({"formatted": res.stdout, "status": "formatted"})
                            return
                    except Exception:
                        pass
                    lines = code.splitlines()
                    normalized = "\n".join(line.rstrip() for line in lines) + "\n"
                    self.send_json({"formatted": normalized, "status": "normalized"})
                    return
                self.send_json({"formatted": code, "status": "unchanged"})
                return
            elif parsed.path == "/api/execute-sql":
                query_str = payload.get("query", "").strip()
                if not query_str:
                    self.send_error(400, "SQL query is empty")
                    return
                preset = payload.get("schema_preset") or "storage_engine"
                t0 = time.perf_counter()
                try:
                    import sqlite3
                    conn = sqlite3.connect(":memory:")
                    cur = conn.cursor()
                    if preset == "storage_engine":
                        cur.executescript("""
                        CREATE TABLE btree_pages (
                            page_id INTEGER PRIMARY KEY,
                            page_type TEXT CHECK(page_type IN ('leaf', 'interior', 'overflow')),
                            item_count INTEGER,
                            free_bytes INTEGER,
                            lsn INTEGER
                        );
                        INSERT INTO btree_pages VALUES
                            (1, 'interior', 3, 1024, 1001),
                            (2, 'leaf', 45, 128, 1002),
                            (3, 'leaf', 52, 64, 1003),
                            (4, 'overflow', 1, 0, 1004);

                        CREATE TABLE wal_frames (
                            frame_no INTEGER PRIMARY KEY,
                            page_id INTEGER,
                            commit_flag INTEGER,
                            salt1 INTEGER,
                            salt2 INTEGER
                        );
                        INSERT INTO wal_frames VALUES
                            (1, 2, 0, 4211, 8812),
                            (2, 3, 1, 4211, 8812),
                            (3, 1, 1, 4211, 8813);

                        CREATE TABLE key_value_store (
                            key TEXT PRIMARY KEY,
                            value TEXT,
                            version INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                        INSERT INTO key_value_store VALUES
                            ('cluster:node1:heartbeat', '171800291', 1, '2026-09-16 10:00:00'),
                            ('cluster:node2:heartbeat', '171800292', 1, '2026-09-16 10:00:01'),
                            ('txn:global:lock', 'granted:tx_99', 4, '2026-09-16 10:00:02');
                        """)
                    elif preset == "ecommerce":
                        cur.executescript("""
                        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, tier TEXT, spend REAL);
                        INSERT INTO customers VALUES 
                            (1, 'Alice Chen', 'Platinum', 12450.00), 
                            (2, 'Bob Smith', 'Gold', 4500.50), 
                            (3, 'Carol Danvers', 'Platinum', 28900.00);
                        CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, status TEXT);
                        INSERT INTO orders VALUES 
                            (101, 1, 350.0, 'SHIPPED'), 
                            (102, 1, 1200.0, 'DELIVERED'), 
                            (103, 2, 85.0, 'PENDING'), 
                            (104, 3, 4500.0, 'DELIVERED');
                        """)
                    conn.commit()

                    plan = []
                    if query_str.upper().startswith("SELECT") or query_str.upper().startswith("WITH"):
                        try:
                            p_cur = conn.cursor()
                            p_cur.execute(f"EXPLAIN QUERY PLAN {query_str}")
                            plan = [f"[{r[0]}|{r[1]}|{r[2]}] {r[3]}" for r in p_cur.fetchall()]
                        except Exception:
                            pass

                    cur.execute(query_str)
                    columns = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchmany(100) if columns else []
                    conn.commit()
                    duration_ms = round((time.perf_counter() - t0) * 1000, 2)
                    self.send_json({
                        "status": "success",
                        "columns": columns,
                        "rows": rows,
                        "row_count": len(rows),
                        "duration_ms": duration_ms,
                        "query_plan": plan,
                    })
                except Exception as exc:
                    duration_ms = round((time.perf_counter() - t0) * 1000, 2)
                    self.send_json({
                        "status": "error",
                        "error": str(exc),
                        "columns": [],
                        "rows": [],
                        "row_count": 0,
                        "duration_ms": duration_ms,
                        "query_plan": [],
                    })
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
    if server_holder is not None:
        server_holder["httpd"] = httpd
    print(f"[*] Native Fallback Server active at http://127.0.0.1:{port} ...")
    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("\n[*] Academy Platform safely stopped. Happy studying!")


def wait_for_http_ready(port: int, host: str = "127.0.0.1", timeout: float = 15.0) -> bool:
    """Verifies that the server is not just accepting TCP connections, but returning HTTP 200 responses."""
    import urllib.request
    start = time.time()
    url = f"http://{host}:{port}/api/courses"
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=0.5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


def find_app_browser() -> Optional[str]:
    """Scans the host OS for a Chromium-based browser capable of running in standalone --app mode."""
    candidates: List[str] = []
    if sys.platform == "win32":
        for base in [
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("LocalAppData", ""),
        ]:
            if not base:
                continue
            candidates.append(os.path.join(base, r"Microsoft\Edge\Application\msedge.exe"))
            candidates.append(os.path.join(base, r"Google\Chrome\Application\chrome.exe"))
            candidates.append(os.path.join(base, r"BraveSoftware\Brave-Browser\Application\brave.exe"))
        for name in ["msedge", "chrome", "brave"]:
            w = shutil.which(name)
            if w:
                candidates.append(w)
    elif sys.platform == "darwin":
        candidates.extend([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            os.path.expanduser("~/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            os.path.expanduser("~/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
        ])
        for name in ["google-chrome", "microsoft-edge", "brave-browser"]:
            w = shutil.which(name)
            if w:
                candidates.append(w)
    else:  # Linux
        for name in [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "microsoft-edge",
            "microsoft-edge-stable",
            "brave-browser",
            "brave",
        ]:
            w = shutil.which(name)
            if w:
                candidates.append(w)
        candidates.extend([
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
            "/usr/bin/microsoft-edge",
            "/usr/bin/brave-browser",
        ])

    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Checks if a TCP port is currently occupied."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False


def is_academy_server_running(port: int, host: str = "127.0.0.1") -> bool:
    """Checks if our own Academy FastAPI or fallback backend is already answering on this port."""
    import urllib.request
    try:
        url = f"http://{host}:{port}/api/courses"
        with urllib.request.urlopen(url, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False


def find_available_port(start_port: int = 8000, max_tries: int = 25) -> int:
    """Finds the first available TCP port starting from start_port."""
    for p in range(start_port, start_port + max_tries):
        if not is_port_in_use(p):
            return p
    return start_port


def clean_stale_browser_locks(profile_dir: Path) -> None:
    """Cleans up stale Chromium singleton lock files that prevent Edge/Chrome from opening."""
    if not profile_dir.is_dir():
        return
    for name in ["SingletonLock", "SingletonCookie", "SingletonSocket", "lockfile"]:
        lock_path = profile_dir / name
        try:
            if lock_path.is_file() or lock_path.is_symlink():
                lock_path.unlink(missing_ok=True)
        except Exception:
            pass


def focus_existing_academy_window() -> bool:
    """Attempts to find and focus an already-open Academy window on Windows desktop."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        user32 = ctypes.windll.user32
        candidates = [
            "AI & Systems Engineering Academy — Karthikeya Reddy",
            "AI & Systems Academy — Karthikeya Reddy",
            "AI & Systems Academy - Karthikeya Reddy",
            "AI & Systems Academy",
            "AI AND SYSTEMS ENGINEERING ACADEMY",
        ]
        for title in candidates:
            hwnd = user32.FindWindowW(None, title)
            if hwnd:
                SW_RESTORE = 9
                user32.ShowWindow(hwnd, SW_RESTORE)
                user32.SetForegroundWindow(hwnd)
                return True
    except Exception:
        pass
    return False


def request_server_shutdown(port: int, host: str = "127.0.0.1") -> None:
    """Requests graceful shutdown of the backend server."""
    import urllib.request
    try:
        req = urllib.request.Request(f"http://{host}:{port}/api/shutdown", data=b"", method="POST")
        urllib.request.urlopen(req, timeout=1.0)
    except Exception:
        try:
            req = urllib.request.Request(f"http://{host}:{port}/api/client-disconnect", data=b"", method="POST")
            urllib.request.urlopen(req, timeout=1.0)
        except Exception:
            pass


def log_launcher_event(msg: str) -> None:
    """Appends diagnostic events to .academy_launcher.log for zero-friction debugging."""
    try:
        log_file = ROOT_DIR / ".academy_launcher.log"
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def launch_interface(
    url: str,
    port: int,
    force_browser: bool = False,
    headless: bool = False,
) -> Optional[subprocess.Popen]:
    """Launches the dedicated standalone desktop app window or falls back to the default web browser."""
    if headless:
        print("[*] Headless mode enabled: skipping GUI window launch.")
        log_launcher_event("Headless mode enabled")
        return None

    ready = wait_for_http_ready(port)
    if not ready:
        print(f"[!] Notice: Waiting for server to initialize on port {port}...")
        time.sleep(1.5)
    else:
        time.sleep(0.3)

    if force_browser:
        print(f"\n[+] Opening Academy Learning Portal in your default web browser ({url})...")
        log_launcher_event(f"Opening browser at {url}")
        webbrowser.open(url)
        return None

    app_browser = find_app_browser()
    if app_browser:
        profile_dir = ROOT_DIR / ".academy_app_profile"
        profile_dir.mkdir(exist_ok=True)
        clean_stale_browser_locks(profile_dir)

        # Check if lockfile is actively locked by another process
        lock_file = profile_dir / "lockfile"
        if lock_file.is_file():
            try:
                with open(lock_file, "r+b"):
                    pass
            except OSError:
                # Profile is locked; use clean alternate directory
                profile_dir = ROOT_DIR / ".academy_app_profile_alt"
                profile_dir.mkdir(exist_ok=True)
                clean_stale_browser_locks(profile_dir)

        cmd = [
            app_browser,
            f"--app={url}",
            f"--user-data-dir={str(profile_dir)}",
            "--window-size=1440,920",
            "--window-position=center",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-mode",
            "--disable-background-networking",
            "--disable-features=TranslateUI,msEdgeStartupBoost",
            "--no-service-autorun",
        ]
        try:
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP

            proc = subprocess.Popen(cmd, creationflags=creationflags)
            browser_name = Path(app_browser).stem.replace(".exe", "")
            print(f"\n[+] Dedicated Desktop Application Window launched via {browser_name} (PID: {proc.pid}).")
            print("[*] Running as standalone desktop application. Close window or press Ctrl+C to exit.")
            log_launcher_event(f"Dedicated desktop window launched via {browser_name} (PID: {proc.pid}) at {url}")

            # Verify the process doesn't immediately crash / exit
            time.sleep(1.2)
            if proc.poll() is not None and proc.returncode != 0:
                exit_code = proc.returncode
                log_launcher_event(f"Dedicated desktop window exited prematurely with code {exit_code}.")
                print(f"[!] Dedicated window exited prematurely (code {exit_code}). Opening in default browser...")
                webbrowser.open(url)
                log_launcher_event(f"Opened default browser fallback at {url}")
                return None

            return proc
        except Exception as exc:
            print(f"[!] Failed to launch dedicated app window ({exc}). Falling back to browser...")
            log_launcher_event(f"Failed to launch dedicated window: {exc}")

    print(f"\n[+] Opening Academy Learning Portal in your default browser ({url})...")
    log_launcher_event(f"Opening default browser at {url}")
    webbrowser.open(url)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="AI & Systems Engineering Academy Platform Launcher")
    parser.add_argument("--browser", action="store_true", help="Launch in default browser tab instead of standalone app window")
    parser.add_argument("--headless", action="store_true", help="Run server without launching any GUI window or browser")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild client production bundle before launch")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind server (default: 8000)")
    args = parser.parse_args()

    req_port = args.port
    log_launcher_event(f"Launcher invoked with port={req_port}, browser={args.browser}, headless={args.headless}")

    # 1. Check if an Academy instance is already running on requested port
    # Or if the port is in use and an Academy instance is warming up
    is_running = is_academy_server_running(req_port)
    if not is_running and is_port_in_use(req_port):
        is_running = wait_for_http_ready(req_port, timeout=2.0)

    if is_running:
        print(f"\n[*] AI & Systems Academy is already running on http://127.0.0.1:{req_port}!")
        log_launcher_event(f"Re-attaching to existing Academy server on port {req_port}")

        if args.headless:
            print("[*] Server is already active in headless mode.")
            return

        # Check if an existing Academy window can be brought to foreground
        if not args.browser and focus_existing_academy_window():
            print("[+] Brought active Academy window to the foreground.")
            log_launcher_event("Focused existing Academy window.")
            return

        print("[+] Opening Academy window now...")
        re_proc = launch_interface(f"http://127.0.0.1:{req_port}", port=req_port, force_browser=args.browser, headless=args.headless)
        if re_proc is not None:
            try:
                log_launcher_event("Supervising re-attached Academy window...")
                re_proc.wait()
                print("\n[*] Academy window closed. Terminating background server...")
                log_launcher_event("Re-attached window closed by user. Terminating server.")
                request_server_shutdown(req_port)
            except Exception as e:
                log_launcher_event(f"Re-attach supervisor notice: {e}")
        return

    # 2. Check if the port is busy with another service; if so, allocate an open port
    port = req_port
    if is_port_in_use(port):
        alt_port = find_available_port(start_port=port + 1)
        print(f"[!] Port {port} is occupied by another process. Automatically switching to port {alt_port}...")
        log_launcher_event(f"Port {port} in use; switched to port {alt_port}")
        port = alt_port

    print(BANNER.format(port=port))
    ensure_client_built(force_rebuild=args.rebuild)

    has_uvicorn = ensure_dependencies()
    url = f"http://127.0.0.1:{port}"
    server_holder: Dict[str, Any] = {}
    window_proc: Optional[subprocess.Popen] = None

    def start_ui_supervisor() -> None:
        nonlocal window_proc
        launch_start = time.time()
        window_proc = launch_interface(url=url, port=port, force_browser=args.browser, headless=args.headless)
        if window_proc is not None:
            try:
                window_proc.wait()
                elapsed = time.time() - launch_start
                # If window was open for more than 2 seconds, user used and closed the application
                if elapsed >= 2.0:
                    print("\n[*] Application window closed by user. Terminating Academy server...")
                    log_launcher_event("Application window closed by user. Terminating server.")
                    if "uvicorn" in server_holder:
                        server_holder["uvicorn"].should_exit = True
                    if "httpd" in server_holder:
                        try:
                            server_holder["httpd"].shutdown()
                        except Exception:
                            pass
                    time.sleep(0.5)
                    os._exit(0)
                else:
                    log_launcher_event("Browser window launcher finished handoff. Server remains active and responsive.")
            except Exception as e:
                log_launcher_event(f"UI supervisor notice: {e}")
                pass

    ui_thread = threading.Thread(target=start_ui_supervisor, daemon=True)
    ui_thread.start()

    try:
        if has_uvicorn:
            sys.path.insert(0, str(SERVER_DIR))
            import uvicorn

            print(f"[*] Starting High-Performance FastAPI Server at {url} ...")
            print("[*] Press Ctrl+C or close the application window at any time to stop.\n")
            log_launcher_event(f"Starting FastAPI uvicorn server on port {port}")

            from main import app as fastapi_app

            config = uvicorn.Config(
                fastapi_app,
                host="127.0.0.1",
                port=port,
                log_level="info",
            )
            server = uvicorn.Server(config)
            server_holder["uvicorn"] = server
            server.run()
        else:
            log_launcher_event(f"Starting native fallback server on port {port}")
            run_fallback_server(port=port, server_holder=server_holder)
    except KeyboardInterrupt:
        print("\n[*] Shutdown requested via Ctrl+C.")
        log_launcher_event("Shutdown requested via Ctrl+C.")
    finally:
        if window_proc is not None and window_proc.poll() is None:
            try:
                window_proc.terminate()
            except Exception:
                pass
        print("[*] Academy Platform safely stopped. Happy studying!")
        log_launcher_event("Academy platform stopped cleanly.")


if __name__ == "__main__":
    main()

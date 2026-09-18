"""AI & Systems Academy Interactive Learning Platform Backend API.

Provides dynamic course auto-discovery, content streaming, live pytest/demo execution,
LeetCode Arena testing sandbox, and dual local progress persistence.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROGRESS_FILE = BASE_DIR / ".study_progress.json"
CLIENT_DIST = Path(__file__).resolve().parent.parent / "client" / "dist"

app = FastAPI(
    title="Karthikeya Reddy's AI & Systems Academy",
    description="Production-grade interactive learning platform for 12 courses.",
    version="2.0.0",
)

custom_origins = os.environ.get("ACADEMY_ALLOWED_ORIGINS", "")
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8999",
    "http://127.0.0.1:8999",
]
if custom_origins:
    allowed_origins.extend([orig.strip() for orig in custom_origins.split(",") if orig.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_last_activity_time: float = time.time()
_request_counter: int = 0
_shutdown_thread: Optional[Any] = None

@app.middleware("http")
async def track_activity_middleware(request, call_next):
    global _last_activity_time, _request_counter
    _last_activity_time = time.time()
    _request_counter += 1
    response = await call_next(request)
    return response

@app.post("/api/client-disconnect")
def client_disconnect():
    """Safely shuts down the server when the user closes the app window or browser tab."""
    global _shutdown_thread
    if _shutdown_thread and _shutdown_thread.is_alive():
        return {"status": "shutdown_scheduled"}

    def _graceful_shutdown():
        count_before = _request_counter
        time.sleep(3.5)
        if _request_counter == count_before:
            print("\n[*] Application window/tab closed. Cleaning up and stopping backend...")
            os._exit(0)

    import threading
    _shutdown_thread = threading.Thread(target=_graceful_shutdown, daemon=True)
    _shutdown_thread.start()
    return {"status": "shutdown_scheduled"}


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
class LessonItem(BaseModel):
    id: str
    title: str
    file_path: str
    type: str  # 'theory', 'playground', 'project', 'quiz', 'troubleshooting', 'code'


class ModuleItem(BaseModel):
    id: str
    module_num: int
    title: str
    folder_path: str
    lessons: List[LessonItem]
    has_solution: bool
    has_starter: bool
    has_debug_lab: bool = False
    has_problems: bool = False
    quickstart_script: Optional[str] = None
    word_count: int = 0
    reading_minutes: int = 0
    quiz_question_count: int = 0


class CourseSummary(BaseModel):
    id: str
    course_num: int
    title: str
    folder_name: str
    category: str
    difficulty: str
    estimated_hours: int
    reading_hours: float = 0.0
    lab_hours: float = 0.0
    total_words: int = 0
    debug_lab_count: int = 0
    module_count: int
    description: str
    depth_badge: str = ""
    quickstart_script: Optional[str] = None


class RunTestRequest(BaseModel):
    target_path: str
    command_type: str = "pytest"  # 'pytest' or 'python'


class RunCodeRequest(BaseModel):
    code: str
    mode: str = "python"  # 'python', 'powershell', 'shell'
    working_dir: Optional[str] = None
    timeout_sec: int = 25


class DsaRunRequest(BaseModel):
    problem_id: str
    code: str
    submit: bool = False


class ProblemRunRequest(BaseModel):
    module_path: str
    problem_filename: str
    code: str


class SaveFilePayload(BaseModel):
    module_path: str
    filename: str
    content: str


class ProgressPayload(BaseModel):
    completed_lessons: List[str] = []
    completed_modules: List[str] = []
    current_course: Optional[str] = None
    current_lesson: Optional[str] = None
    last_updated: float = 0.0
    theme: str = "dark"
    quiz_scores: dict = {}
    bookmarks: List[str] = []
    notes: dict = {}
    last_study_date: Optional[str] = None
    study_streak_days: int = 1


# -----------------------------------------------------------------------------
# Course Discovery Engine
# -----------------------------------------------------------------------------
COURSE_CATEGORIES = {
    "01": ("Language & Systems Mastery", "Advanced", 30),
    "02": ("Core Computer Science", "Advanced", 25),
    "03": ("Storage Engines & Distributed DBs", "Staff", 35),
    "04": ("Distributed Systems & Reliability", "Staff", 30),
    "05": ("Foundations for Machine Learning", "Advanced", 40),
    "06": ("Deep Learning & Transformer Foundations", "Advanced", 35),
    "07": ("GPU Systems & High-Performance Kernels", "Staff", 40),
    "08": ("GPU Clusters & Large-Scale Training", "Principal", 45),
    "09": ("LLM Serving & Low-Latency Engines", "Principal", 40),
    "10": ("Context Engineering & Vector Retrieval", "Staff", 30),
    "11": ("Autonomous Systems & Cognitive Topologies", "Staff", 35),
    "12": ("GenAI Security, Red Teaming & Guardrails", "Staff", 30),
}


_COURSE_METRICS_CACHE: dict = {}

def compute_course_metrics(course_dir: Path) -> dict:
    if course_dir.name in _COURSE_METRICS_CACHE:
        return _COURSE_METRICS_CACHE[course_dir.name]

    total_words = 0
    py_files = 0
    debug_labs = 0

    for r, dirs, files in os.walk(course_dir):
        if any(ign in r for ign in ["node_modules", ".git", "__pycache__"]):
            continue
        if Path(r).name == "debug_lab":
            debug_labs += 1
        for f in files:
            if f.endswith(".md"):
                p = Path(r) / f
                try:
                    total_words += len(p.read_text(encoding="utf-8", errors="ignore").split())
                except Exception:
                    pass
            elif f.endswith(".py"):
                py_files += 1

    reading_hours = round(total_words / (180 * 60), 1)
    lab_hours = round(debug_labs * 0.75 + (py_files * 0.2), 1)
    total_est_hours = max(10, round(reading_hours + lab_hours))

    if total_words > 100000:
        depth_badge = f"Comprehensive Treatise (~{total_words // 1000}k words)"
    elif total_words > 40000:
        depth_badge = f"Deep Architectural Track (~{total_words // 1000}k words)"
    else:
        depth_badge = f"Intensive Systems Sprint (~{total_words // 1000}k words)"

    metrics = {
        "total_words": total_words,
        "reading_hours": reading_hours,
        "lab_hours": lab_hours,
        "estimated_hours": total_est_hours,
        "debug_lab_count": debug_labs,
        "depth_badge": depth_badge,
    }
    _COURSE_METRICS_CACHE[course_dir.name] = metrics
    return metrics


def discover_courses() -> List[CourseSummary]:
    courses = []
    for item in sorted(BASE_DIR.iterdir()):
        if not item.is_dir():
            continue
        match = re.match(r"^(\d{2})_(.+)$", item.name)
        if not match:
            continue

        num_str = match.group(1)
        course_num = int(num_str)
        clean_title = match.group(2).replace("_", " ")

        cat_info = COURSE_CATEGORIES.get(num_str, ("Advanced AI Systems", "Advanced", 30))
        category, difficulty, _ = cat_info

        # Compute real measured metrics
        metrics = compute_course_metrics(item)

        # Extract description from README.md if available
        desc = f"Mastery of {clean_title} through production-grade systems implementations and rigorous testing."
        readme_path = item / "README.md"
        if readme_path.is_file():
            try:
                lines = readme_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                for line in lines[:10]:
                    if line.startswith("> **") or (line.strip() and not line.startswith("#")):
                        desc = line.strip().lstrip(">").strip()
                        break
            except Exception:
                pass

        # Count modules
        modules = [m for m in item.iterdir() if m.is_dir() and m.name.startswith("Module_")]
        module_count = len(modules)

        quickstart = item / "00_quickstart_interactive_demo.py"
        quickstart_rel = quickstart.relative_to(BASE_DIR).as_posix() if quickstart.exists() else None

        courses.append(CourseSummary(
            id=item.name,
            course_num=course_num,
            title=clean_title,
            folder_name=item.name,
            category=category,
            difficulty=difficulty,
            estimated_hours=metrics["estimated_hours"],
            reading_hours=metrics["reading_hours"],
            lab_hours=metrics["lab_hours"],
            total_words=metrics["total_words"],
            debug_lab_count=metrics["debug_lab_count"],
            module_count=module_count,
            description=desc,
            depth_badge=metrics["depth_badge"],
            quickstart_script=quickstart_rel,
        ))

    return sorted(courses, key=lambda c: c.course_num)


def discover_course_modules(course_folder_name: str) -> List[ModuleItem]:
    course_path = BASE_DIR / course_folder_name
    if not course_path.is_dir():
        raise HTTPException(status_code=404, detail="Course not found")

    raw_dirs = [d for d in course_path.iterdir() if d.is_dir() and d.name.startswith("Module_")]

    def get_mod_num(d: Path) -> int:
        m = re.search(r"Module_(\d+)", d.name)
        return int(m.group(1)) if m else 999

    module_dirs = sorted(raw_dirs, key=get_mod_num)
    result = []

    for mod_dir in module_dirs:
        mod_num = get_mod_num(mod_dir)
        clean_mod_name = re.sub(r"^Module_\d+_", "", mod_dir.name).replace("_", " ")

        lessons: List[LessonItem] = []
        seen_rel_paths = set()

        def get_file_num(f: Path) -> int:
            m = re.match(r"^(\d+)", f.name)
            return int(m.group(1)) if m else 999

        # 1. Collect all root lesson files in the module (md, py, ps1, sh, ipynb)
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

        cand_files.sort(key=lambda f: (get_file_num(f), f.name))

        for target in cand_files:
            rel = target.relative_to(BASE_DIR).as_posix()
            if rel in seen_rel_paths:
                continue
            seen_rel_paths.add(rel)

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

            lessons.append(LessonItem(
                id=f"{mod_dir.name}_{target.name}",
                title=label,
                file_path=rel,
                type=ltype,
            ))

        # 2. Collect any lessons under lessons/ subdirectory
        lessons_dir = mod_dir / "lessons"
        if lessons_dir.is_dir():
            sub_files = [
                lf for lf in lessons_dir.iterdir()
                if lf.is_file() and not lf.name.startswith(".") and lf.suffix.lower() in [".md", ".py", ".ps1", ".sh", ".ipynb"]
            ]
            sub_files.sort(key=lambda f: (get_file_num(f), f.name))
            for lf in sub_files:
                rel = lf.relative_to(BASE_DIR).as_posix()
                if rel not in seen_rel_paths:
                    seen_rel_paths.add(rel)
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

                    lessons.append(LessonItem(
                        id=f"{mod_dir.name}_{lf.name}",
                        title=clean_l_title,
                        file_path=rel,
                        type=ltype,
                    ))

        # Quickstart or demo script
        demo_files = list(mod_dir.glob("00_quickstart*.py")) or list(mod_dir.glob("*demo*.py"))
        quickstart_rel = demo_files[0].relative_to(BASE_DIR).as_posix() if demo_files else None

        # Compute real module metrics
        mod_words = 0
        for md_f in mod_dir.glob("*.md"):
            try:
                mod_words += len(md_f.read_text(encoding="utf-8", errors="ignore").split())
            except Exception:
                pass
        reading_mins = max(1, round(mod_words / 180))

        # Check quiz question count
        quiz_q_count = 0
        quiz_file = mod_dir / "quiz.json"
        if quiz_file.is_file():
            try:
                quiz_q_count = len(json.loads(quiz_file.read_text(encoding="utf-8")))
            except Exception:
                pass

        result.append(ModuleItem(
            id=mod_dir.name,
            module_num=mod_num,
            title=clean_mod_name,
            folder_path=mod_dir.relative_to(BASE_DIR).as_posix(),
            lessons=lessons,
            has_solution=(mod_dir / "project_solution").is_dir(),
            has_starter=(mod_dir / "starter").is_dir(),
            has_debug_lab=any((mod_dir / "debug_lab").glob("broken_*.py")),
            has_problems=any((mod_dir / "problems").glob("p*.py")),
            quickstart_script=quickstart_rel,
            word_count=mod_words,
            reading_minutes=reading_mins,
            quiz_question_count=quiz_q_count,
        ))

    return result


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/courses", response_model=List[CourseSummary])
def get_courses():
    """Dynamically returns all discovered courses."""
    return discover_courses()


@app.get("/api/courses/{course_id}/modules", response_model=List[ModuleItem])
def get_course_modules(course_id: str):
    """Returns modules and lesson files for a specific course."""
    return discover_course_modules(course_id)


@app.get("/api/content")
def get_file_content(path: str = Query(..., description="Relative path from repository root")):
    """Safely loads file content from disk."""
    safe_path = (BASE_DIR / path).resolve()
    if not safe_path.is_relative_to(BASE_DIR):
        raise HTTPException(status_code=403, detail="Access denied: Path traversal detected")
    if not safe_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        content = safe_path.read_text(encoding="utf-8", errors="replace")
        ext = safe_path.suffix.lstrip(".").lower()
        return {
            "path": path,
            "filename": safe_path.name,
            "extension": ext,
            "content": content,
            "size_bytes": safe_path.stat().st_size,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/run-test")
def run_test_command(req: RunTestRequest):
    """Executes pytest or python demo and returns execution output."""
    safe_target = (BASE_DIR / req.target_path).resolve()
    if not safe_target.is_relative_to(BASE_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    if req.command_type == "pytest":
        cmd = [sys.executable, "-m", "pytest", str(safe_target), "-v", "--tb=short"]
    else:
        cmd = [sys.executable, str(safe_target)]

    start_time = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=60,
        )
        duration = time.perf_counter() - start_time
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration_sec": round(duration, 3),
            "status": "passed" if proc.returncode == 0 else "failed",
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Execution timed out after 60 seconds.",
            "duration_sec": 60.0,
            "status": "timeout",
        }
    except Exception as exc:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_sec": 0.0,
            "status": "error",
        }


@app.post("/api/run-code")
def run_interactive_code(req: RunCodeRequest):
    """Executes arbitrary Python, PowerShell, or Shell commands in a page-aware isolated subprocess."""
    target_cwd = BASE_DIR
    if req.working_dir:
        candidate = (BASE_DIR / req.working_dir).resolve()
        if candidate.is_dir() and candidate.is_relative_to(BASE_DIR):
            target_cwd = candidate

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = f"{target_cwd}{os.pathsep}{BASE_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}"

    start_time = time.perf_counter()
    temp_file = None
    try:
        if req.mode == "powershell":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False, encoding="utf-8") as tf:
                tf.write(req.code)
                temp_file = tf.name
            ps_exe = "powershell.exe" if sys.platform == "win32" else "pwsh"
            cmd = [ps_exe, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", temp_file]
        elif req.mode == "shell":
            if sys.platform == "win32":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".bat", delete=False, encoding="utf-8") as tf:
                    tf.write("@echo off\n" + req.code)
                    temp_file = tf.name
                cmd = ["cmd.exe", "/c", temp_file]
            else:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False, encoding="utf-8") as tf:
                    tf.write("#!/usr/bin/env bash\n" + req.code)
                    temp_file = tf.name
                cmd = ["/bin/bash", temp_file]
        else:
            # Python mode
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
                tf.write(req.code)
                temp_file = tf.name
            cmd = [sys.executable, temp_file]

        effective_timeout = max(1, min(req.timeout_sec, 120))
        proc = subprocess.run(
            cmd,
            cwd=str(target_cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=effective_timeout,
            input="",
        )
        duration = time.perf_counter() - start_time

        MAX_OUT = 80000
        stdout = proc.stdout
        if len(stdout) > MAX_OUT:
            stdout = stdout[:MAX_OUT] + f"\n... [Output truncated to {MAX_OUT // 1000}KB] ..."
        stderr = proc.stderr
        if len(stderr) > MAX_OUT:
            stderr = stderr[:MAX_OUT] + f"\n... [Error output truncated to {MAX_OUT // 1000}KB] ..."

        rel_cwd = target_cwd.relative_to(BASE_DIR).as_posix() if target_cwd != BASE_DIR else "."

        return {
            "exit_code": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "duration_sec": round(duration, 3),
            "status": "passed" if proc.returncode == 0 else "failed",
            "cwd": rel_cwd,
            "mode": req.mode,
        }
    except subprocess.TimeoutExpired:
        rel_cwd = target_cwd.relative_to(BASE_DIR).as_posix() if target_cwd != BASE_DIR else "."
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {req.timeout_sec} seconds.",
            "duration_sec": float(req.timeout_sec),
            "status": "timeout",
            "cwd": rel_cwd,
            "mode": req.mode,
        }
    except Exception as exc:
        rel_cwd = target_cwd.relative_to(BASE_DIR).as_posix() if target_cwd != BASE_DIR else "."
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_sec": 0.0,
            "status": "error",
            "cwd": rel_cwd,
            "mode": req.mode,
        }
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass



# -----------------------------------------------------------------------------
# DSA LeetCode Problem Solving Studio Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/dsa-problems")
def get_dsa_problems_endpoint(module: Optional[str] = None):
    """Returns curated LeetCode problems for DSA course modules, or on-disk problems for other modules."""
    try:
        from dsa_problems import get_dsa_problems
        res = get_dsa_problems(module)
        if res.get("problems"):
            return res
    except Exception:
        pass

    if module:
        safe_mod = (BASE_DIR / module).resolve()
        if safe_mod.is_relative_to(BASE_DIR) and (safe_mod / "problems").is_dir():
            prob_data = get_module_problems_endpoint(module)
            if prob_data.get("problems"):
                mapped = []
                for p in prob_data["problems"]:
                    mapped.append({
                        "id": f"{module}:{p['filename']}",
                        "title": p["title"],
                        "difficulty": "Medium",
                        "category": safe_mod.name.replace("_", " "),
                        "description": p["description"] or f"Implement {p['title']} according to module invariants.",
                        "starter_code": p["starter_code"],
                        "solution_code": p["code"],
                        "tags": ["Practice Bank", safe_mod.name],
                        "test_cases": [],
                    })
                return {"problems": mapped, "module": module}

    return {"problems": []}


@app.get("/api/problems")
def get_module_problems_endpoint(module_path: str = Query(..., description="Module relative folder path")):
    """Serves on-disk problem bank files (problems/p*.py) and problems/README.md."""
    safe_mod = (BASE_DIR / module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    problems_dir = safe_mod / "problems"
    if not problems_dir.is_dir():
        return {"has_problems": False, "problems": [], "readme": None}

    readme_file = problems_dir / "README.md"
    readme_content = readme_file.read_text(encoding="utf-8", errors="replace") if readme_file.is_file() else None

    user_ws = BASE_DIR / ".user_workspaces" / module_path / "problems"

    problems = []
    for f in sorted(problems_dir.glob("p*.py")):
        if not f.is_file():
            continue
        user_file = user_ws / f.name
        code = user_file.read_text(encoding="utf-8", errors="replace") if user_file.is_file() else f.read_text(encoding="utf-8", errors="replace")
        starter_code = f.read_text(encoding="utf-8", errors="replace")

        docstring = ""
        try:
            tree = ast.parse(starter_code)
            docstring = ast.get_docstring(tree) or ""
        except Exception:
            pass

        title = f.stem.replace("_", " ").title()
        problems.append({
            "id": f.stem,
            "filename": f.name,
            "title": title,
            "description": docstring,
            "code": code,
            "starter_code": starter_code,
            "has_tests": (problems_dir / "tests").is_dir(),
        })

    return {
        "has_problems": len(problems) > 0,
        "module_path": module_path,
        "readme": readme_content,
        "problems": problems,
    }


@app.post("/api/run-problem-test")
def run_problem_test_endpoint(req: ProblemRunRequest):
    """Executes pytest tests on the learner's problem solution."""
    safe_mod = (BASE_DIR / req.module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    problems_dir = safe_mod / "problems"
    if not problems_dir.is_dir():
        raise HTTPException(status_code=404, detail="Problems directory not found")

    user_ws = BASE_DIR / ".user_workspaces" / req.module_path / "problems"
    user_ws.mkdir(parents=True, exist_ok=True)
    (user_ws / req.problem_filename).write_text(req.code, encoding="utf-8")

    target_problem = problems_dir / req.problem_filename
    backup = target_problem.read_text(encoding="utf-8") if target_problem.exists() else None
    try:
        target_problem.write_text(req.code, encoding="utf-8")
        cmd = [sys.executable, "-m", "pytest", "tests", "-v", "--tb=short"]
        t0 = time.perf_counter()
        proc = subprocess.run(
            cmd,
            cwd=str(problems_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        duration = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "status": "passed" if proc.returncode == 0 else "failed",
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration_ms": duration,
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "exit_code": -1,
            "stdout": "",
            "stderr": "Execution timed out after 30 seconds.",
            "duration_ms": 30000.0,
        }
    except Exception as exc:
        return {
            "status": "error",
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_ms": 0.0,
        }
    finally:
        if backup is not None:
            target_problem.write_text(backup, encoding="utf-8")


@app.post("/api/run-dsa-test")
def run_dsa_test_endpoint(req: DsaRunRequest):
    """Executes code against LeetCode testcases (visible or hidden)."""
    try:
        from dsa_problems import run_dsa_solution
        return run_dsa_solution(req.problem_id, req.code, submit=req.submit)
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": 0,
            "duration_ms": 0.0,
            "results": []
        }

@app.get("/api/trace")
def get_trace_endpoint(module_path: str = Query(..., description="Module folder path")):
    """Returns trace.json for algorithm visualization scrubber if available."""
    safe_mod = (BASE_DIR / module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    trace_file = safe_mod / "trace.json"
    if not trace_file.is_file():
        raise HTTPException(status_code=404, detail="Trace file not found")

    try:
        with open(trace_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# -----------------------------------------------------------------------------
# In-Browser Project Studio & Debug Lab Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/project-files")
def get_project_files(module_path: str = Query(..., description="Module folder path")):
    """Safely retrieves starter and reference solution files for the in-browser IDE."""
    safe_mod = (BASE_DIR / module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    starter_dir = safe_mod / "starter"
    solution_dir = safe_mod / "project_solution"
    workspace_dir = BASE_DIR / ".user_workspaces" / module_path

    files = []
    if starter_dir.is_dir():
        for f in sorted(starter_dir.iterdir()):
            if not f.is_file() or f.name.startswith(".") or f.name == "__pycache__":
                continue
            user_version = workspace_dir / f.name
            current_content = (
                user_version.read_text(encoding="utf-8", errors="replace")
                if user_version.is_file()
                else f.read_text(encoding="utf-8", errors="replace")
            )
            starter_content = f.read_text(encoding="utf-8", errors="replace")
            sol_file = solution_dir / f.name if solution_dir.is_dir() else None
            sol_content = (
                sol_file.read_text(encoding="utf-8", errors="replace")
                if sol_file and sol_file.is_file()
                else None
            )
            files.append({
                "filename": f.name,
                "content": current_content,
                "starter_content": starter_content,
                "solution_content": sol_content,
                "is_modified": current_content != starter_content,
                "read_only": False,
            })

    if solution_dir.is_dir():
        for f in sorted(solution_dir.iterdir()):
            if not f.is_file() or f.name.startswith(".") or f.name == "__pycache__":
                continue
            if any(existing["filename"] == f.name for existing in files):
                continue
            sol_content = f.read_text(encoding="utf-8", errors="replace")
            files.append({
                "filename": f.name,
                "content": sol_content,
                "starter_content": sol_content,
                "solution_content": sol_content,
                "is_modified": False,
                "read_only": True,
            })

    return {"module_path": module_path, "files": files}


@app.post("/api/save-project-file")
def save_project_file(payload: SaveFilePayload):
    """Saves student edits to the local project workspace."""
    safe_mod = (BASE_DIR / payload.module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    target_dir = BASE_DIR / ".user_workspaces" / payload.module_path
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / Path(payload.filename).name
    target_file.write_text(payload.content, encoding="utf-8")
    return {"status": "saved", "path": str(target_file.relative_to(BASE_DIR))}


@app.get("/api/debug-files")
def get_debug_files(module_path: str = Query(..., description="Module folder path")):
    """Safely retrieves debug lab broken code and symptoms."""
    safe_mod = (BASE_DIR / module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    debug_dir = safe_mod / "debug_lab"
    if not debug_dir.is_dir():
        return {"has_debug_lab": False, "files": []}

    files = []
    symptoms = ""
    for f in sorted(debug_dir.iterdir()):
        if not f.is_file() or f.name.startswith(".") or f.name == "__pycache__":
            continue
        content_txt = f.read_text(encoding="utf-8", errors="replace")
        if f.name.upper() == "SYMPTOMS.MD":
            symptoms = content_txt
        files.append({"filename": f.name, "content": content_txt})

    return {"has_debug_lab": True, "module_path": module_path, "symptoms": symptoms, "files": files}


@app.get("/api/quiz")
def get_module_quiz(module_path: str = Query(..., description="Module relative folder path")):
    """Returns structured quiz questions with authentic options and explanations."""
    safe_mod = (BASE_DIR / module_path).resolve()
    if not safe_mod.is_relative_to(BASE_DIR) or not safe_mod.is_dir():
        raise HTTPException(status_code=404, detail="Module not found")

    quiz_file = safe_mod / "quiz.json"
    if quiz_file.is_file():
        try:
            return json.loads(quiz_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    master_db = Path(__file__).resolve().parent / "data" / "quizzes.json"
    if master_db.is_file():
        try:
            data = json.loads(master_db.read_text(encoding="utf-8"))
            clean_path = module_path.replace("\\", "/").strip("/")
            for k, v in data.items():
                if k.replace("\\", "/").strip("/").endswith(clean_path) or clean_path.endswith(k.replace("\\", "/").strip("/")):
                    return v
        except Exception:
            pass

    return []


@app.get("/api/search")
def search_curriculum(q: str = Query(..., min_length=2)):
    """Fast search index across all 12 courses, modules, and lessons for Ctrl+K palette."""
    query = q.lower().strip()
    results = []
    courses = discover_courses()
    for c in courses:
        if query in c.title.lower() or query in c.category.lower():
            results.append({
                "type": "course",
                "id": c.id,
                "course_id": c.id,
                "title": c.title,
                "subtitle": f"{c.category} • {c.module_count} Modules",
                "path": c.folder_name,
            })
        try:
            mods = discover_course_modules(c.folder_name)
            for m in mods:
                if query in m.title.lower():
                    results.append({
                        "type": "module",
                        "id": m.id,
                        "course_id": c.id,
                        "course_title": c.title,
                        "title": f"Module {m.module_num:02d}: {m.title}",
                        "subtitle": f"Course: {c.title}",
                        "path": m.folder_path,
                    })
                for l in m.lessons:
                    if query in l.title.lower() or query in l.file_path.lower():
                        results.append({
                            "type": "lesson",
                            "id": l.id,
                            "course_id": c.id,
                            "course_title": c.title,
                            "module_id": m.id,
                            "module_title": m.title,
                            "title": l.title,
                            "subtitle": f"{c.title} • Module {m.module_num:02d}",
                            "path": l.file_path,
                            "lesson_type": l.type,
                        })
        except Exception:
            continue

    return results[:35]


@app.get("/api/progress", response_model=ProgressPayload)
def get_study_progress():
    """Loads persisted study progress from .study_progress.json."""
    if PROGRESS_FILE.is_file():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            return ProgressPayload(**data)
        except Exception:
            pass
    return ProgressPayload()


@app.post("/api/progress")
def save_study_progress(payload: ProgressPayload):
    """Saves study progress to .study_progress.json with study streak tracking."""
    try:
        from datetime import date, timedelta
        today_str = time.strftime("%Y-%m-%d")
        if payload.last_study_date:
            if payload.last_study_date != today_str:
                try:
                    last_d = date.fromisoformat(payload.last_study_date)
                    today_d = date.fromisoformat(today_str)
                    diff = (today_d - last_d).days
                    if diff == 1:
                        payload.study_streak_days += 1
                    elif diff > 1:
                        payload.study_streak_days = 1
                except Exception:
                    payload.study_streak_days = 1
        else:
            payload.study_streak_days = payload.study_streak_days or 1

        payload.last_study_date = today_str
        payload.last_updated = time.time()
        PROGRESS_FILE.write_text(json.dumps(payload.model_dump(), indent=2), encoding="utf-8")
        return {"status": "ok", "saved": True, "streak": payload.study_streak_days}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


class FormatCodeRequest(BaseModel):
    code: str
    language: str = "python"


@app.post("/api/format-code")
def format_code(payload: FormatCodeRequest):
    code = payload.code
    lang = payload.language.lower()
    if not code.strip():
        return {"formatted": code, "status": "unchanged"}

    if lang == "python":
        # 1. Try ruff format
        try:
            res = subprocess.run(
                [sys.executable, "-m", "ruff", "format", "-"],
                input=code,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout:
                return {"formatted": res.stdout, "status": "formatted"}
        except Exception:
            pass

        # 2. Try black format
        try:
            res = subprocess.run(
                [sys.executable, "-m", "black", "-", "--quiet"],
                input=code,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout:
                return {"formatted": res.stdout, "status": "formatted"}
        except Exception:
            pass

        # 3. Fallback: normalize indentation
        lines = code.splitlines()
        normalized = "\n".join(line.rstrip() for line in lines) + "\n"
        return {"formatted": normalized, "status": "normalized"}

    return {"formatted": code, "status": "unchanged"}


class SqlRequest(BaseModel):
    query: str
    schema_preset: Optional[str] = "storage_engine"


def get_demo_sqlite_db(preset: str):
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
    return conn


@app.post("/api/execute-sql")
def execute_sql(payload: SqlRequest):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="SQL query is empty")

    preset = payload.schema_preset or "storage_engine"
    t0 = time.perf_counter()
    try:
        conn = get_demo_sqlite_db(preset)
        cur = conn.cursor()

        plan = []
        if query.upper().startswith("SELECT") or query.upper().startswith("WITH"):
            try:
                p_cur = conn.cursor()
                p_cur.execute(f"EXPLAIN QUERY PLAN {query}")
                plan = [f"[{r[0]}|{r[1]}|{r[2]}] {r[3]}" for r in p_cur.fetchall()]
            except Exception:
                pass

        cur.execute(query)
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchmany(100) if columns else []
        conn.commit()
        duration_ms = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "status": "success",
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "duration_ms": duration_ms,
            "query_plan": plan,
        }
    except Exception as exc:
        duration_ms = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "status": "error",
            "error": str(exc),
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": duration_ms,
            "query_plan": [],
        }


# Serve static React frontend in production if dist/ exists
if CLIENT_DIST.is_dir():
    app.mount("/static", StaticFiles(directory=str(CLIENT_DIST)), name="static")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_target = CLIENT_DIST / full_path
        if file_target.is_file():
            return FileResponse(file_target)
        index_file = CLIENT_DIST / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)
        return JSONResponse({"message": "Frontend is building or dist not found"})

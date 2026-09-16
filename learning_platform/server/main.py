"""Coursera-Style Learning Platform Backend API.

Provides dynamic course auto-discovery, content streaming, live pytest/demo execution,
and dual local progress persistence.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import List, Optional

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    quickstart_script: Optional[str] = None


class CourseSummary(BaseModel):
    id: str
    course_num: int
    title: str
    folder_name: str
    category: str
    difficulty: str
    estimated_hours: int
    module_count: int
    description: str
    quickstart_script: Optional[str] = None


class RunTestRequest(BaseModel):
    target_path: str
    command_type: str = "pytest"  # 'pytest' or 'python'


class RunCodeRequest(BaseModel):
    code: str
    mode: str = "python"  # 'python', 'powershell', 'shell'
    working_dir: Optional[str] = None
    timeout_sec: int = 25


class ProgressPayload(BaseModel):
    completed_lessons: List[str] = []
    completed_modules: List[str] = []
    current_course: Optional[str] = None
    current_lesson: Optional[str] = None
    last_updated: float = 0.0
    theme: str = "dark"


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
        category, difficulty, est_hours = cat_info

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
            estimated_hours=est_hours,
            module_count=module_count,
            description=desc,
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

        # 1. Collect all root markdown files in the module
        root_md_files = sorted(mod_dir.glob("*.md"))
        for target in root_md_files:
            rel = target.relative_to(BASE_DIR).as_posix()
            if rel in seen_rel_paths:
                continue
            seen_rel_paths.add(rel)

            fname_upper = target.name.upper()
            if "README" in fname_upper:
                label = "Theoretical Foundations & Architecture"
                ltype = "theory"
            elif "PLAYGROUND" in fname_upper or "BEGINNER" in fname_upper or "ZERO_TO_ONE" in fname_upper:
                label = "Interactive Foundations Playground"
                ltype = "playground"
            elif "PROJECT" in fname_upper or "GUIDE" in fname_upper:
                label = "Guided Hands-on Project"
                ltype = "project"
            elif "SELF_ASSESSMENT" in fname_upper or "CHALLENGE" in fname_upper or "QUIZ" in fname_upper:
                label = "Staff Interview Challenges & Quizzes"
                ltype = "quiz"
            elif "TROUBLESHOOTING" in fname_upper or "EDGE_CASES" in fname_upper:
                label = "Troubleshooting & Forensic Edge Cases"
                ltype = "troubleshooting"
            else:
                clean_name = re.sub(r"^\d+_", "", target.stem).replace("_", " ")
                label = f"Guide: {clean_name}"
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
            for lf in sorted(lessons_dir.glob("*.md")):
                rel = lf.relative_to(BASE_DIR).as_posix()
                if rel not in seen_rel_paths:
                    seen_rel_paths.add(rel)
                    clean_l_title = re.sub(r"^\d+_", "", lf.stem).replace("_", " ")
                    lessons.append(LessonItem(
                        id=f"{mod_dir.name}_{lf.name}",
                        title=f"Lesson: {clean_l_title}",
                        file_path=rel,
                        type="theory",
                    ))

        # Quickstart or demo script
        demo_files = list(mod_dir.glob("00_quickstart*.py")) or list(mod_dir.glob("*demo*.py"))
        quickstart_rel = demo_files[0].relative_to(BASE_DIR).as_posix() if demo_files else None

        result.append(ModuleItem(
            id=mod_dir.name,
            module_num=mod_num,
            title=clean_mod_name,
            folder_path=mod_dir.relative_to(BASE_DIR).as_posix(),
            lessons=lessons,
            has_solution=(mod_dir / "project_solution").is_dir(),
            has_starter=(mod_dir / "starter").is_dir(),
            quickstart_script=quickstart_rel,
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
    if not str(safe_path).startswith(str(BASE_DIR)):
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
    if not str(safe_target).startswith(str(BASE_DIR)):
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
        if candidate.is_dir() and str(candidate).startswith(str(BASE_DIR)):
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

        proc = subprocess.run(
            cmd,
            cwd=str(target_cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=req.timeout_sec,
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
    """Saves study progress to .study_progress.json for permanent local persistence."""
    try:
        payload.last_updated = time.time()
        PROGRESS_FILE.write_text(json.dumps(payload.model_dump(), indent=2), encoding="utf-8")
        return {"status": "ok", "saved": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


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

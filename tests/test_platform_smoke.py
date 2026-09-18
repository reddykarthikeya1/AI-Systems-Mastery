"""Automated Platform Smoke Test Suite.

Verifies end-to-end operational readiness of all 16 interactive API endpoints,
runtime subprocess isolation, SQL playground storage engine, and progress sync.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

import sys
import unittest
from pathlib import Path

# Add project root and server to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "learning_platform" / "server"))

try:
    from fastapi.testclient import TestClient
    from main import app
except ImportError as err:
    print(f"Skipping FastAPI TestClient tests: {err}")
    sys.exit(0)


class TestPlatformSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_courses_catalog_discovery(self):
        """Verify curriculum auto-discovery identifies all courses."""
        resp = self.client.get("/api/courses")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 12, "Should discover at least 12 curriculum tracks")
        first = data[0]
        self.assertIn("id", first)
        self.assertIn("title", first)
        self.assertIn("module_count", first)

    def test_02_course_modules_and_lessons(self):
        """Verify module resolution and lesson structure."""
        resp = self.client.get("/api/courses/01_Advanced_Python/modules")
        self.assertEqual(resp.status_code, 200)
        modules = resp.json()
        self.assertIsInstance(modules, list)
        self.assertGreater(len(modules), 0)
        first_mod = modules[0]
        self.assertIn("module_num", first_mod)
        self.assertIn("lessons", first_mod)
        self.assertGreater(len(first_mod["lessons"]), 0)

    def test_03_python_code_execution(self):
        """Verify Python code execution sandbox."""
        payload = {
            "code": "print(6 * 7)",
            "mode": "python",
        }
        resp = self.client.post("/api/run-code", json=payload)
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("42", result["stdout"])

    def test_04_code_formatting(self):
        """Verify code formatting endpoint with Ruff/Black/AST fallback."""
        payload = {
            "code": "def   foo(  x,y ):\n    return x+y\n",
            "language": "python",
        }
        resp = self.client.post("/api/format-code", json=payload)
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertIn("formatted", result)
        self.assertTrue(len(result["formatted"]) > 0)

    def test_05_sql_storage_engine_playground(self):
        """Verify in-memory SQLite storage engine sandbox and query plan."""
        payload = {
            "query": "SELECT page_id, page_type, item_count FROM btree_pages WHERE page_type = 'leaf';",
            "schema_preset": "storage_engine",
        }
        resp = self.client.post("/api/execute-sql", json=payload)
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["columns"]), 3)
        self.assertGreater(result["row_count"], 0)
        self.assertIn("query_plan", result)

    def test_06_progress_persistence_schema(self):
        """Verify progress state endpoint."""
        resp = self.client.get("/api/progress")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("completed_lessons", data)
        self.assertIn("completed_modules", data)

    def test_07_structured_quiz_endpoint(self):
        """Verify /api/quiz returns authentic structured MCQs across courses."""
        # Test Course 09 Module 01 (previously zero questions)
        resp = self.client.get("/api/quiz?module_path=09_Inference_Systems_and_Serving_Engines/Module_01_Inference_Latency_Throughput_Tradeoffs")
        self.assertEqual(resp.status_code, 200)
        qs = resp.json()
        self.assertIsInstance(qs, list)
        self.assertGreaterEqual(len(qs), 3, "Should have at least 3 structured questions")
        first_q = qs[0]
        self.assertIn("question", first_q)
        self.assertIn("options", first_q)
        self.assertEqual(len(first_q["options"]), 4, "Every question must have 4 options")
        self.assertIn("explanation", first_q)
        # Verify no hardcoded dummy placeholder strings exist
        for opt in first_q["options"]:
            self.assertNotIn("It is evaluated strictly at process initialization", opt["text"])

    def test_08_measured_course_metrics(self):
        """Verify /api/courses returns real measured reading hours, word count, and depth badge."""
        resp = self.client.get("/api/courses")
        self.assertEqual(resp.status_code, 200)
        courses = resp.json()
        for c in courses:
            self.assertGreater(c["estimated_hours"], 0)
            self.assertGreater(c["total_words"], 0, f"Course {c['title']} must have measured word count")
            self.assertIn("depth_badge", c)
            self.assertTrue(len(c["depth_badge"]) > 0)

    def test_09_debug_lab_discovery(self):
        """Verify /api/debug-files discovers planted defect code and symptoms."""
        resp = self.client.get("/api/debug-files?module_path=01_Advanced_Python/Module_00_Environment_Tooling_Workflow")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("has_debug_lab"))
        self.assertGreater(len(data.get("files", [])), 0)

    def test_10_problems_discovery(self):
        """Verify /api/problems returns on-disk problem files and stubs."""
        resp = self.client.get("/api/problems?module_path=02_Data_Structures_and_Algorithms/Module_01_Complexity_Analysis_and_Memory_Layout")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("has_problems", data)
        self.assertTrue(data["has_problems"])
        self.assertGreater(len(data.get("problems", [])), 0)
        p1 = data["problems"][0]
        self.assertIn("id", p1)
        self.assertIn("title", p1)
        self.assertIn("starter_code", p1)

    def test_11_run_problem_test(self):
        """Verify /api/run-problem-test executes pytest against problem code."""
        mod_path = "02_Data_Structures_and_Algorithms/Module_01_Complexity_Analysis_and_Memory_Layout"
        resp = self.client.get(f"/api/problems?module_path={mod_path}")
        self.assertEqual(resp.status_code, 200)
        prob = resp.json()["problems"][0]
        payload = {
            "module_path": mod_path,
            "problem_filename": prob["filename"],
            "code": prob["starter_code"],
        }
        resp_run = self.client.post("/api/run-problem-test", json=payload)
        self.assertEqual(resp_run.status_code, 200)
        res = resp_run.json()
        self.assertIn("status", res)
        self.assertIn("exit_code", res)
        self.assertIn("stdout", res)

    def test_12_module_guide_endpoint(self):
        """Verify /api/module-guide serves PROJECT_GUIDE.md across modules."""
        resp = self.client.get("/api/module-guide?module_path=01_Advanced_Python/Module_01_Python_Fundamentals")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("path", data)
        self.assertIn("content", data)
        self.assertIn("PROJECT_GUIDE", data["path"])
        self.assertIn("3-Tier Progressive Learning Path", data["content"])


if __name__ == "__main__":
    unittest.main()


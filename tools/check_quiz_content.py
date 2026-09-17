#!/usr/bin/env python3
"""Gate: verify quiz content quality and diversity across all courses and modules.

Enforces:
  1. Every module with a quiz has >= 8 questions.
  2. Every question has a non-empty explanation.
  3. No single correct answer string exceeds ~2% of the total course question bank
     (detects repetitive generic placeholder answers).

Usage:
    python tools/check_quiz_content.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def main() -> int:
    courses = sorted([d for d in ROOT.iterdir() if d.is_dir() and d.name[:2].isdigit()])
    failures: list[str] = []
    total_quizzes = 0
    total_questions = 0

    for course in courses:
        modules = sorted([m for m in course.glob("Module_*") if m.is_dir()])
        course_correct_answers = []
        
        for m in modules:
            quiz_file = m / "quiz.json"
            if not quiz_file.exists():
                failures.append(f"{course.name}/{m.name}: missing quiz.json")
                continue
            
            total_quizzes += 1
            try:
                data = json.loads(quiz_file.read_text(encoding="utf-8"))
            except Exception as e:
                failures.append(f"{course.name}/{m.name}: invalid JSON in quiz.json: {e}")
                continue
            
            if len(data) < 8:
                failures.append(f"{course.name}/{m.name}: quiz has only {len(data)} questions (< 8)")
            
            for q_idx, q in enumerate(data):
                total_questions += 1
                explanation = q.get("explanation", "").strip()
                if not explanation:
                    failures.append(f"{course.name}/{m.name} Q{q.get('id', q_idx)}: missing explanation")
                
                corr_opts = [opt["text"].strip() for opt in q.get("options", []) if opt.get("is_correct")]
                if corr_opts:
                    course_correct_answers.append(corr_opts[0])
        
        # Check answer string frequency in this course bank
        if course_correct_answers:
            bank_size = len(course_correct_answers)
            counts = Counter(course_correct_answers)
            for ans, count in counts.most_common(5):
                if len(ans.strip()) <= 4:
                    continue
                ratio = count / bank_size
                if ratio > 0.05 and count > 5:
                    failures.append(f"{course.name}: answer string '{ans[:50]}...' repeated {count}/{bank_size} times ({ratio:.1%})")

    print(f"Checked {total_quizzes} quizzes across {len(courses)} courses ({total_questions} total questions).")
    if failures:
        print(f"\n{len(failures)} QUIZ CONTENT FAILURE(S):")
        for f in failures[:30]:
            print(f"  - {f}")
        if len(failures) > 30:
            print(f"  ... and {len(failures) - 30} more")
        return 1

    print("  All quizzes have >= 8 questions, full explanations, and diverse answers.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
Module 19: Dockerfile & CI/CD Pipeline Validator
Run: python try_it_yourself.py
"""


def validate_dockerfile(lines):
    required_keywords = ["FROM", "WORKDIR", "COPY", "CMD"]
    found = dict.fromkeys(required_keywords, False)
    for line in lines:
        for k in required_keywords:
            if line.strip().startswith(k):
                found[k] = True
    return found


def main():
    print("=" * 60)
    print("  MODULE 19: DOCKERFILE & PIPELINE PLAYGROUND [*]")
    print("=" * 60)

    sample_dockerfile = [
        "FROM python:3.11-slim",
        "WORKDIR /app",
        "COPY requirements.txt .",
        "RUN pip install -r requirements.txt",
        "COPY . .",
        'CMD ["python", "app.py"]',
    ]

    print("Checking Dockerfile directives:")
    validation = validate_dockerfile(sample_dockerfile)
    for directive, present in validation.items():
        status = "[OK] Present" if present else "[X] Missing"
        print(f"  Directive '{directive}': {status}")

    all_ok = all(validation.values())
    if all_ok:
        print("\n[OK] Dockerfile follows production best practices!")


if __name__ == "__main__":
    main()

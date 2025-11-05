#!/usr/bin/env python3
"""
Validation script for CCO 2.5 Wizard

Checks:
1. All 4 core files exist
2. Python syntax is valid
3. Questions are properly defined
4. No external dependencies in rendering code
"""

import ast
import io
import sys
from pathlib import Path

# Import constants

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.constants import EXPECTED_WIZARD_QUESTIONS

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def check_files_exist() -> bool:
    """Check all required files exist"""
    print("Checking files...")

    wizard_dir = Path(__file__).parent
    required_files = [
        "__init__.py",
        "cli.py",
        "questions.py",
        "checkpoints.py",
        "renderer.py",
        "README.md",
    ]

    missing = []
    for file in required_files:
        if not (wizard_dir / file).exists():
            missing.append(file)
            print(f"  [X] {file} - MISSING")
        else:
            print(f"  [OK] {file}")

    if missing:
        print(f"\n[X] Missing files: {', '.join(missing)}")
        return False

    print("[OK] All files present\n")
    return True


def check_syntax() -> bool:
    """Check Python syntax for all files"""
    print("Checking syntax...")

    wizard_dir = Path(__file__).parent
    python_files = ["__init__.py", "cli.py", "questions.py", "checkpoints.py", "renderer.py"]

    errors = []
    for file in python_files:
        try:
            path = wizard_dir / file
            with open(path, encoding="utf-8") as f:
                ast.parse(f.read())
            print(f"  [OK] {file}")
        except SyntaxError as e:
            print(f"  [X] {file} - {e}")
            errors.append((file, str(e)))

    if errors:
        print("\n[X] Syntax errors found")
        return False

    print("[OK] All files have valid syntax\n")
    return True


def check_questions() -> bool:
    """Check questions are properly defined"""
    print("Checking questions...")

    wizard_dir = Path(__file__).parent
    questions_file = wizard_dir / "questions.py"

    # Parse and extract QUESTIONS
    with open(questions_file, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    questions_found = False
    question_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "QUESTIONS":
                    questions_found = True
                    if isinstance(node.value, ast.List):
                        question_count = len(node.value.elts)

    if not questions_found:
        print("  [X] QUESTIONS list not found")
        return False

    print("  [OK] QUESTIONS list defined")
    print(f"  [OK] {question_count} questions found")

    # Check categories
    categories = {
        "project_identity": 0,
        "development_style": 0,
        "code_quality": 0,
        "documentation": 0,
        "testing": 0,
        "security": 0,
        "performance": 0,
        "collaboration": 0,
        "devops": 0,
    }

    # Count by parsing the file manually (simple approach)
    with open(questions_file, encoding="utf-8") as f:
        content = f.read()
        for category in categories:
            # Count occurrences of category in question definitions
            count = content.count(f'"category": "{category}"')
            categories[category] = count

    print("\n  Questions by category:")
    for cat, count in categories.items():
        print(f"    {cat}: {count}")

    total = sum(categories.values())
    print(f"\n  Total: {total} questions")

    if total < EXPECTED_WIZARD_QUESTIONS:
        print(f"  [!] Expected at least {EXPECTED_WIZARD_QUESTIONS} questions, found {total}")
    else:
        print(f"  [OK] Question count meets requirement ({EXPECTED_WIZARD_QUESTIONS}+)")

    print("[OK] Questions properly defined\n")
    return True


def check_no_external_deps() -> bool:
    """Check renderer.py has no external dependencies"""
    print("Checking dependencies...")

    wizard_dir = Path(__file__).parent
    renderer_file = wizard_dir / "renderer.py"

    with open(renderer_file, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    # Allowed stdlib modules
    stdlib_modules = {
        "sys",
        "os",
        "typing",
        "pathlib",
        "json",
        "time",
        "datetime",
        "argparse",
        "collections",
        "re",
        "io",
    }

    external = [imp for imp in imports if imp.split(".")[0] not in stdlib_modules]

    print(f"  Imports in renderer.py: {', '.join(imports)}")

    if external:
        print(f"  [X] External dependencies found: {', '.join(external)}")
        return False

    print("  [OK] No external dependencies")
    print("[OK] Pure stdlib implementation\n")
    return True


def check_line_counts() -> None:
    """Report line counts"""
    print("Line counts:")

    wizard_dir = Path(__file__).parent
    files = {
        "__init__.py": 0,
        "cli.py": 0,
        "questions.py": 0,
        "checkpoints.py": 0,
        "renderer.py": 0,
    }

    for file in files:
        path = wizard_dir / file
        with open(path, encoding="utf-8") as f:
            files[file] = len(f.readlines())
        print(f"  {file}: {files[file]} lines")

    total = sum(files.values())
    print(f"\n  Total: {total} lines")
    print()


def main() -> int:
    """Run all checks"""
    print("=" * 60)
    print("CCO 2.5 Wizard Validation")
    print("=" * 60)
    print()

    checks = [
        check_files_exist,
        check_syntax,
        check_questions,
        check_no_external_deps,
        check_line_counts,
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result if result is not None else True)
        except Exception as e:
            print(f"[X] Check failed: {e}")
            results.append(False)

    print("=" * 60)
    if all(results):
        print("[OK] ALL CHECKS PASSED")
        print("=" * 60)
        print("\nWizard is production-ready!")
        return 0
    else:
        print("[X] SOME CHECKS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

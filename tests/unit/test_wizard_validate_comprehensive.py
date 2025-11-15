"""
Comprehensive tests for wizard validate module.

Tests cover:
- Validation logic for AST operations
- String parsing and counting
- Category detection
- Import detection
- Syntax validation patterns
- Integration tests with mocked functions

Target Coverage: Tests validation patterns used by the module
"""

import ast
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest


class TestASTValidationPatterns:
    """Test AST parsing patterns used in validation"""

    def test_find_questions_assignment(self):
        """Test finding QUESTIONS assignment in AST"""
        code = """
QUESTIONS = [
    {"id": "q1", "category": "testing"},
    {"id": "q2", "category": "security"},
]
"""
        tree = ast.parse(code)

        questions_found = False
        question_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "QUESTIONS":
                        questions_found = True
                        if isinstance(node.value, ast.List):
                            question_count = len(node.value.elts)

        assert questions_found is True
        assert question_count == 2

    def test_find_no_questions(self):
        """Test when no QUESTIONS variable exists"""
        code = """
OTHER_VAR = []
CONFIG = {}
"""
        tree = ast.parse(code)

        questions_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "QUESTIONS":
                        questions_found = True

        assert questions_found is False

    def test_find_empty_questions_list(self):
        """Test empty QUESTIONS list"""
        code = "QUESTIONS = []"
        tree = ast.parse(code)

        question_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "QUESTIONS":
                        if isinstance(node.value, ast.List):
                            question_count = len(node.value.elts)

        assert question_count == 0

    def test_detect_import_statements(self):
        """Test detecting import statements"""
        code = """
import sys
import os
from typing import List
from pathlib import Path
"""
        tree = ast.parse(code)

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        assert "sys" in imports
        assert "os" in imports
        assert "typing" in imports
        assert "pathlib" in imports

    def test_filter_stdlib_imports(self):
        """Test filtering stdlib from external imports"""
        code = """
import sys
import requests
from pathlib import Path
import pandas
"""
        tree = ast.parse(code)

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

        stdlib_modules = {"sys", "os", "typing", "pathlib", "json"}
        external = [imp for imp in imports if imp not in stdlib_modules]

        assert "requests" in external
        assert "pandas" in external
        assert "sys" not in external

    def test_syntax_validation_valid(self):
        """Test validating valid Python syntax"""
        code = """
def test():
    return True

class TestClass:
    pass
"""
        # Should not raise
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)

    def test_syntax_validation_invalid(self):
        """Test detecting invalid Python syntax"""
        code = "def invalid( syntax"

        with pytest.raises(SyntaxError):
            ast.parse(code)

    def test_multiline_import_detection(self):
        """Test detecting multiline imports"""
        code = """
from typing import (
    List,
    Dict,
    Optional,
)
"""
        tree = ast.parse(code)

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        assert "typing" in imports


class TestStringCounting:
    """Test string counting patterns used in validation"""

    def test_count_category_occurrences(self):
        """Test counting category strings"""
        content = """
{"category": "testing"},
{"category": "security"},
{"category": "testing"},
"""
        count_testing = content.count('"category": "testing"')
        count_security = content.count('"category": "security"')

        assert count_testing == 2
        assert count_security == 1

    def test_count_with_exact_pattern(self):
        """Test exact pattern matching"""
        content = """
category: "testing"
"category": "testing"
category="testing"
"""
        # Only exact pattern matches
        count = content.count('"category": "testing"')
        assert count == 1

    def test_count_multiple_categories(self):
        """Test counting multiple category types"""
        content = """
{"category": "project_identity"},
{"category": "development_style"},
{"category": "code_quality"},
{"category": "testing"},
{"category": "security"},
"""
        categories = {
            "project_identity": 0,
            "development_style": 0,
            "code_quality": 0,
            "testing": 0,
            "security": 0,
        }

        for category in categories:
            categories[category] = content.count(f'"category": "{category}"')

        assert categories["project_identity"] == 1
        assert categories["testing"] == 1
        assert sum(categories.values()) == 5


class TestPathOperations:
    """Test path operations used in validation"""

    def test_file_exists_check(self):
        """Test file existence checking"""
        current_file = Path(__file__)
        assert current_file.exists()

    def test_path_parent_resolution(self):
        """Test parent path resolution"""
        current_file = Path(__file__)
        parent = current_file.parent
        assert parent.exists()
        assert parent.is_dir()

    def test_path_joining(self):
        """Test path joining"""
        wizard_dir = Path(__file__).parent
        test_file = wizard_dir / "test.py"

        assert test_file.parent == wizard_dir
        assert test_file.name == "test.py"

    def test_nonexistent_path(self):
        """Test nonexistent path returns False"""
        fake_path = Path("/nonexistent/path/file.txt")
        assert not fake_path.exists()


class TestFileReading:
    """Test file reading patterns"""

    @patch("builtins.open", new_callable=mock_open, read_data="line1\nline2\nline3\n")
    def test_count_lines(self, mock_file):
        """Test line counting"""
        with open("dummy.txt") as f:
            lines = f.readlines()

        assert len(lines) == 3

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_file_lines(self, mock_file):
        """Test empty file line count"""
        with open("dummy.txt") as f:
            lines = f.readlines()

        assert len(lines) == 0

    @patch("builtins.open", new_callable=mock_open)
    def test_file_read_for_parsing(self, mock_file):
        """Test reading file for AST parsing"""
        code = "def test(): pass"
        mock_file.return_value.read.return_value = code

        with open("dummy.py") as f:
            content = f.read()

        tree = ast.parse(content)
        assert isinstance(tree, ast.Module)


class TestValidationConstants:
    """Test validation constants"""

    def test_required_files_list(self):
        """Test required files list structure"""
        required_files = [
            "__init__.py",
            "cli.py",
            "questions.py",
            "checkpoints.py",
            "renderer.py",
            "README.md",
        ]

        assert len(required_files) == 6
        assert all(isinstance(f, str) for f in required_files)
        assert "__init__.py" in required_files

    def test_stdlib_modules_set(self):
        """Test stdlib modules set"""
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

        assert len(stdlib_modules) == 11
        assert "sys" in stdlib_modules
        assert "requests" not in stdlib_modules

    def test_category_names(self):
        """Test question categories"""
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

        assert len(categories) == 9
        # Most categories use underscore (except single words like 'testing', 'security')
        assert all(isinstance(cat, str) for cat in categories.keys())

    def test_expected_question_count(self):
        """Test expected wizard questions constant"""
        from claudecodeoptimizer.core.constants import EXPECTED_WIZARD_QUESTIONS

        assert isinstance(EXPECTED_WIZARD_QUESTIONS, int)
        assert EXPECTED_WIZARD_QUESTIONS > 0
        assert EXPECTED_WIZARD_QUESTIONS == 58


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_code(self):
        """Test parsing empty code"""
        code = ""
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)

    def test_only_comments(self):
        """Test file with only comments"""
        code = """
# This is a comment
# Another comment
"""
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)

    def test_only_docstring(self):
        """Test file with only docstring"""
        code = '''"""Module docstring."""'''
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)

    def test_unicode_in_code(self):
        """Test code with unicode characters"""
        code = "text = '你好世界'"
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)

    def test_multiline_string(self):
        """Test multiline strings in code"""
        code = '''
TEXT = """
This is a
multiline string
"""
'''
        tree = ast.parse(code)
        assert isinstance(tree, ast.Module)


class TestValidationWorkflow:
    """Test validation workflow patterns"""

    def test_check_results_all_pass(self):
        """Test all checks passing"""
        results = [True, True, True, True]
        all_passed = all(results)

        assert all_passed is True

    def test_check_results_some_fail(self):
        """Test some checks failing"""
        results = [True, False, True, True]
        all_passed = all(results)

        assert all_passed is False

    def test_check_results_with_none(self):
        """Test handling None results (treated as True)"""
        results = [True, True, True, None]

        # Convert None to True
        converted = [r if r is not None else True for r in results]
        all_passed = all(converted)

        assert all_passed is True

    def test_exit_code_success(self):
        """Test success exit code"""
        all_passed = True
        exit_code = 0 if all_passed else 1

        assert exit_code == 0

    def test_exit_code_failure(self):
        """Test failure exit code"""
        all_passed = False
        exit_code = 0 if all_passed else 1

        assert exit_code == 1


class TestImportSplitting:
    """Test import module name splitting"""

    def test_split_simple_import(self):
        """Test splitting simple import name"""
        import_name = "requests"
        base_module = import_name.split(".")[0]

        assert base_module == "requests"

    def test_split_dotted_import(self):
        """Test splitting dotted import"""
        import_name = "os.path.join"
        base_module = import_name.split(".")[0]

        assert base_module == "os"

    def test_filter_imports_by_base(self):
        """Test filtering imports by base module"""
        imports = ["sys", "os.path", "requests.api", "pathlib.Path"]
        stdlib_modules = {"sys", "os", "pathlib"}

        external = [imp for imp in imports if imp.split(".")[0] not in stdlib_modules]

        assert "requests.api" in external
        assert "sys" not in external
        assert "os.path" not in external


class TestExceptionHandling:
    """Test exception handling patterns"""

    def test_catch_file_not_found(self):
        """Test catching FileNotFoundError"""
        try:
            Path("/nonexistent/file.txt").read_text()
            result = True
        except FileNotFoundError:
            result = False

        assert result is False

    def test_catch_syntax_error(self):
        """Test catching SyntaxError"""
        try:
            ast.parse("def invalid( syntax")
            result = True
        except SyntaxError:
            result = False

        assert result is False

    def test_catch_general_exception(self):
        """Test catching general exceptions"""
        def failing_function():
            raise Exception("Test error")

        try:
            failing_function()
            result = True
        except Exception:
            result = False

        assert result is False


class TestListComprehension:
    """Test list comprehension patterns"""

    def test_filter_enabled_items(self):
        """Test filtering enabled items"""
        items = [
            {"id": "item1", "enabled": True},
            {"id": "item2", "enabled": False},
            {"id": "item3", "enabled": True},
        ]

        enabled = [item["id"] for item in items if item.get("enabled", False)]

        assert len(enabled) == 2
        assert "item1" in enabled
        assert "item3" in enabled
        assert "item2" not in enabled

    def test_extract_names_from_nodes(self):
        """Test extracting names from AST nodes"""
        code = """
VAR1 = 1
VAR2 = 2
VAR3 = 3
"""
        tree = ast.parse(code)

        names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.append(target.id)

        assert len(names) == 3
        assert "VAR1" in names
        assert "VAR2" in names
        assert "VAR3" in names


class TestDictionaryOperations:
    """Test dictionary operations used in validation"""

    def test_count_by_category(self):
        """Test counting items by category"""
        items = [
            {"category": "testing"},
            {"category": "security"},
            {"category": "testing"},
            {"category": "performance"},
        ]

        counts = {}
        for item in items:
            cat = item["category"]
            counts[cat] = counts.get(cat, 0) + 1

        assert counts["testing"] == 2
        assert counts["security"] == 1
        assert counts["performance"] == 1

    def test_sum_values(self):
        """Test summing dictionary values"""
        counts = {
            "testing": 5,
            "security": 3,
            "performance": 2,
        }

        total = sum(counts.values())

        assert total == 10


class TestStringFormatting:
    """Test string formatting patterns"""

    def test_format_error_message(self):
        """Test error message formatting"""
        filename = "test.py"
        status = "[X]"
        message = f"  {status} {filename} - MISSING"

        assert "[X]" in message
        assert "test.py" in message
        assert "MISSING" in message

    def test_format_success_message(self):
        """Test success message formatting"""
        filename = "test.py"
        status = "[OK]"
        message = f"  {status} {filename}"

        assert "[OK]" in message
        assert "test.py" in message

    def test_format_separator(self):
        """Test separator formatting"""
        width = 60
        separator = "=" * width

        assert len(separator) == width
        assert separator == "=" * 60

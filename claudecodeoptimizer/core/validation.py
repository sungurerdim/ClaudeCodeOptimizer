"""
Validation engine for ClaudeCodeOptimizer.

Validates code against active principles using pattern matching.
Supports multiple languages: Python, JavaScript, TypeScript, Go, Rust, Java.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .principles import Principle, PrinciplesManager


@dataclass
class Violation:
    """Represents a principle violation found in code."""

    principle_id: str
    principle_title: str
    rule_id: str
    file_path: Path
    line_number: int
    line_content: str
    severity: str
    description: str
    pattern: str
    category: str


@dataclass
class ValidationResult:
    """Results of validation run."""

    violations: List[Violation]
    files_scanned: int
    principles_checked: int
    total_issues: int
    by_severity: Dict[str, int]
    by_category: Dict[str, int]
    by_principle: Dict[str, int]


class ValidationEngine:
    """Validates code against principles using pattern matching."""

    def __init__(self, principles_manager: PrinciplesManager) -> None:
        """
        Initialize validation engine.

        Args:
            principles_manager: PrinciplesManager instance
        """
        self.principles_manager = principles_manager

        # Language file extensions
        self.language_extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "go": [".go"],
            "rust": [".rs"],
            "java": [".java"],
            "c": [".c", ".h"],
            "cpp": [".cpp", ".hpp", ".cc", ".hh"],
            "csharp": [".cs"],
            "ruby": [".rb"],
            "php": [".php"],
            "swift": [".swift"],
            "kotlin": [".kt"],
        }

    def validate_project(
        self,
        project_root: Path,
        principle_ids: List[str],
        exclude_patterns: Optional[List[str]] = None,
    ) -> ValidationResult:
        """
        Validate entire project against given principles.

        Args:
            project_root: Project root directory
            principle_ids: List of principle IDs to check
            exclude_patterns: Optional list of glob patterns to exclude

        Returns:
            ValidationResult object
        """
        violations = []
        files_scanned = 0

        # Default exclusions
        if exclude_patterns is None:
            exclude_patterns = [
                "**/node_modules/**",
                "**/__pycache__/**",
                "**/venv/**",
                "**/env/**",
                "**/.git/**",
                "**/dist/**",
                "**/build/**",
                "**/*.min.js",
                "**/*.min.css",
            ]

        # Get all code files
        code_files = self._find_code_files(project_root, exclude_patterns)

        # Validate each file
        for file_path in code_files:
            file_violations = self.validate_file(file_path, principle_ids)
            violations.extend(file_violations)
            files_scanned += 1

        # Calculate statistics
        return self._create_validation_result(violations, files_scanned, principle_ids)

    def validate_file(
        self,
        file_path: Path,
        principle_ids: List[str],
    ) -> List[Violation]:
        """
        Validate a single file against principles.

        Args:
            file_path: Path to file
            principle_ids: List of principle IDs to check

        Returns:
            List of violations found
        """
        violations = []

        try:
            # Read file content
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            # Detect language from extension
            language = self._detect_language(file_path)

            # Check each principle
            for principle_id in principle_ids:
                principle = self.principles_manager.get_principle(principle_id)
                if not principle:
                    continue

                # Check each rule in the principle
                for rule in principle.rules:
                    rule_violations = self._check_rule(
                        file_path,
                        lines,
                        language,
                        principle,
                        rule,
                    )
                    violations.extend(rule_violations)

        except Exception:
            # Skip files that can't be read
            pass

        return violations

    def _check_rule(
        self,
        file_path: Path,
        lines: List[str],
        language: str,
        principle: Principle,
        rule: Dict[str, Any],
    ) -> List[Violation]:
        """
        Check a single rule against file content.

        Args:
            file_path: Path to file
            lines: File lines
            language: Detected language
            principle: Principle being checked
            rule: Rule to check

        Returns:
            List of violations found
        """
        violations = []

        # Check if rule applies to this language
        rule_languages = rule.get("languages", ["all"])
        if "all" not in rule_languages and language not in rule_languages:
            return violations

        # Get pattern
        pattern = rule.get("check_pattern", "")
        if not pattern:
            return violations

        # Compile regex pattern
        try:
            regex = re.compile(pattern, re.MULTILINE)
        except re.error:
            # Invalid pattern, skip
            return violations

        # Check each line
        full_content = "\n".join(lines)

        # Try multiline match first
        for match in regex.finditer(full_content):
            # Find line number
            line_num = full_content[: match.start()].count("\n") + 1
            line_content = lines[line_num - 1] if line_num <= len(lines) else ""

            violation = Violation(
                principle_id=principle.id,
                principle_title=principle.title,
                rule_id=rule.get("id", "unknown"),
                file_path=file_path,
                line_number=line_num,
                line_content=line_content.strip(),
                severity=rule.get("severity", principle.severity),
                description=rule.get("description", ""),
                pattern=pattern,
                category=principle.category,
            )
            violations.append(violation)

        return violations

    def _find_code_files(
        self,
        project_root: Path,
        exclude_patterns: List[str],
    ) -> List[Path]:
        """
        Find all code files in project.

        Args:
            project_root: Project root directory
            exclude_patterns: Glob patterns to exclude

        Returns:
            List of code file paths
        """
        code_files = []

        # Get all extensions we support
        all_extensions = set()
        for exts in self.language_extensions.values():
            all_extensions.update(exts)

        # Walk the project directory
        for file_path in project_root.rglob("*"):
            if not file_path.is_file():
                continue

            # Check extension
            if file_path.suffix not in all_extensions:
                continue

            # Check exclusions
            relative_path = file_path.relative_to(project_root)
            excluded = False
            for pattern in exclude_patterns:
                if relative_path.match(pattern):
                    excluded = True
                    break

            if not excluded:
                code_files.append(file_path)

        return code_files

    def _detect_language(self, file_path: Path) -> str:
        """
        Detect programming language from file extension.

        Args:
            file_path: Path to file

        Returns:
            Language name or "unknown"
        """
        suffix = file_path.suffix

        for language, extensions in self.language_extensions.items():
            if suffix in extensions:
                return language

        return "unknown"

    def _create_validation_result(
        self,
        violations: List[Violation],
        files_scanned: int,
        principle_ids: List[str],
    ) -> ValidationResult:
        """
        Create ValidationResult from violations.

        Args:
            violations: List of violations found
            files_scanned: Number of files scanned
            principle_ids: List of principle IDs checked

        Returns:
            ValidationResult object
        """
        # Count by severity
        by_severity = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for violation in violations:
            severity = violation.severity
            by_severity[severity] = by_severity.get(severity, 0) + 1

        # Count by category
        by_category: Dict[str, int] = {}
        for violation in violations:
            category = violation.category
            by_category[category] = by_category.get(category, 0) + 1

        # Count by principle
        by_principle: Dict[str, int] = {}
        for violation in violations:
            principle_id = violation.principle_id
            by_principle[principle_id] = by_principle.get(principle_id, 0) + 1

        return ValidationResult(
            violations=violations,
            files_scanned=files_scanned,
            principles_checked=len(principle_ids),
            total_issues=len(violations),
            by_severity=by_severity,
            by_category=by_category,
            by_principle=by_principle,
        )

    def get_violations_by_severity(
        self,
        result: ValidationResult,
        severity: str,
    ) -> List[Violation]:
        """Get violations filtered by severity."""
        return [v for v in result.violations if v.severity == severity]

    def get_violations_by_principle(
        self,
        result: ValidationResult,
        principle_id: str,
    ) -> List[Violation]:
        """Get violations filtered by principle."""
        return [v for v in result.violations if v.principle_id == principle_id]

    def get_violations_by_file(
        self,
        result: ValidationResult,
        file_path: Path,
    ) -> List[Violation]:
        """Get violations filtered by file."""
        return [v for v in result.violations if v.file_path == file_path]

    def format_violation(self, violation: Violation) -> str:
        """
        Format a violation for display.

        Args:
            violation: Violation to format

        Returns:
            Formatted string
        """
        severity_prefix = {
            "critical": "[CRITICAL]",
            "high": "[HIGH]",
            "medium": "[MEDIUM]",
            "low": "[LOW]",
        }

        prefix = severity_prefix.get(violation.severity, "[INFO]")

        return (
            f"{prefix} {violation.principle_title}\n"
            f"  File: {violation.file_path}:{violation.line_number}\n"
            f"  Rule: {violation.rule_id} - {violation.description}\n"
            f"  Code: {violation.line_content}\n"
        )

    def format_summary(self, result: ValidationResult) -> str:
        """
        Format validation result summary.

        Args:
            result: ValidationResult to format

        Returns:
            Formatted summary string
        """
        lines = [
            "=== Validation Summary ===",
            f"Files scanned: {result.files_scanned}",
            f"Principles checked: {result.principles_checked}",
            f"Total issues: {result.total_issues}",
            "",
            "By Severity:",
        ]

        for severity in ["critical", "high", "medium", "low"]:
            count = result.by_severity.get(severity, 0)
            if count > 0:
                lines.append(f"  {severity.upper()}: {count}")

        if result.by_category:
            lines.append("")
            lines.append("By Category:")
            for category, count in sorted(result.by_category.items()):
                lines.append(f"  {category}: {count}")

        return "\n".join(lines)


__all__ = [
    "Violation",
    "ValidationResult",
    "ValidationEngine",
]

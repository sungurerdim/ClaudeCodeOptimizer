"""
Comprehensive Code Analyzer for CCO Benchmarks.

Multi-dimensional analysis covering:
- Functional Completeness
- Code Quality
- Security
- Test Quality
- Documentation
- Best Practices

Language-agnostic core with language-specific analyzers.
"""

import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DimensionScore:
    """Score for a single dimension with details."""

    name: str
    score: float  # 0-100
    weight: float  # Weight in overall score
    details: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    positives: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "weight": self.weight,
            "weighted_score": round(self.score * self.weight, 1),
            "details": self.details,
            "issues": self.issues,
            "positives": self.positives,
        }


@dataclass
class ComprehensiveMetrics:
    """Multi-dimensional metrics for comprehensive analysis."""

    # Identity
    name: str = ""
    variant: str = ""
    language: str = ""  # primary language detected

    # Dimension scores (0-100 each)
    functional_completeness: DimensionScore | None = None
    code_quality: DimensionScore | None = None
    security: DimensionScore | None = None
    test_quality: DimensionScore | None = None
    documentation: DimensionScore | None = None
    best_practices: DimensionScore | None = None

    # Overall
    overall_score: float = 0.0
    grade: str = ""  # A, B, C, D, F

    # Raw data
    file_count: int = 0
    total_loc: int = 0
    source_loc: int = 0
    test_loc: int = 0

    # Requirement tracking
    requirements_found: list[str] = field(default_factory=list)
    requirements_missing: list[str] = field(default_factory=list)

    # Generation info
    generation_time_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "variant": self.variant,
            "language": self.language,
            "overall_score": round(self.overall_score, 1),
            "grade": self.grade,
            "dimensions": {
                "functional_completeness": self.functional_completeness.to_dict()
                if self.functional_completeness
                else None,
                "code_quality": self.code_quality.to_dict() if self.code_quality else None,
                "security": self.security.to_dict() if self.security else None,
                "test_quality": self.test_quality.to_dict() if self.test_quality else None,
                "documentation": self.documentation.to_dict() if self.documentation else None,
                "best_practices": self.best_practices.to_dict() if self.best_practices else None,
            },
            "file_count": self.file_count,
            "total_loc": self.total_loc,
            "source_loc": self.source_loc,
            "test_loc": self.test_loc,
            "requirements_found": self.requirements_found,
            "requirements_missing": self.requirements_missing,
            "generation_time_seconds": self.generation_time_seconds,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComprehensiveMetrics":
        dims = data.pop("dimensions", {})
        m = cls(**{k: v for k, v in data.items() if k != "dimensions"})

        for dim_name, dim_data in (dims or {}).items():
            if dim_data:
                score = DimensionScore(
                    name=dim_data["name"],
                    score=dim_data["score"],
                    weight=dim_data["weight"],
                    details=dim_data.get("details", []),
                    issues=dim_data.get("issues", []),
                    positives=dim_data.get("positives", []),
                )
                setattr(m, dim_name, score)

        return m


class ComprehensiveAnalyzer:
    """Analyzes code comprehensively across multiple dimensions."""

    # Dimension weights (must sum to 1.0)
    WEIGHTS = {
        "functional_completeness": 0.25,  # Does it work?
        "code_quality": 0.20,  # Is it well-written?
        "security": 0.15,  # Is it secure?
        "test_quality": 0.20,  # Is it tested?
        "documentation": 0.10,  # Is it documented?
        "best_practices": 0.10,  # Does it follow standards?
    }

    # Skip patterns
    SKIP_DIRS = {
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".git",
        "dist",
        "build",
        ".egg-info",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "coverage",
        ".next",
        ".nuxt",
    }

    def __init__(self, project_dir: Path, requirements: list[str] | None = None):
        self.project_dir = project_dir
        self.requirements = requirements or []
        self.metrics = ComprehensiveMetrics()
        self._files: dict[str, list[Path]] = {}
        self._file_contents: dict[Path, str] = {}

    def analyze(self) -> ComprehensiveMetrics:
        """Perform comprehensive analysis."""
        self._discover_files()
        self._detect_language()
        self._count_loc()

        # Analyze each dimension
        self.metrics.functional_completeness = self._analyze_functional_completeness()
        self.metrics.code_quality = self._analyze_code_quality()
        self.metrics.security = self._analyze_security()
        self.metrics.test_quality = self._analyze_test_quality()
        self.metrics.documentation = self._analyze_documentation()
        self.metrics.best_practices = self._analyze_best_practices()

        # Calculate overall score
        self._calculate_overall()

        return self.metrics

    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped."""
        skip_prefixes = ("_benchmark_", "_ccbox_", "_cco_")
        skip_suffixes = (".log",)

        if path.name.startswith(skip_prefixes):
            return True
        if path.name.endswith(skip_suffixes):
            return True
        return any(d in path.parts for d in self.SKIP_DIRS)

    def _discover_files(self) -> None:
        """Discover and categorize all source files.

        Uses optimized directory walking that skips entire directories
        like node_modules early for performance.
        """
        import os

        extensions = {
            "python": {".py"},
            "typescript": {".ts", ".tsx"},
            "javascript": {".js", ".jsx", ".mjs"},
            "go": {".go"},
            "json": {".json"},
            "markdown": {".md"},
            "yaml": {".yml", ".yaml"},
        }

        # Initialize file lists
        for lang in extensions:
            self._files[lang] = []

        # Walk directory tree, skipping entire directories early
        for root, dirs, files in os.walk(self.project_dir):
            # Prune directories we want to skip (modifies dirs in place)
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            root_path = Path(root)

            for filename in files:
                filepath = root_path / filename

                # Skip by filename patterns
                if filename.startswith(("_benchmark_", "_ccbox_", "_cco_")):
                    continue
                if filename.endswith(".log"):
                    continue

                # Get extension and categorize
                suffix = filepath.suffix.lower()

                for lang, exts in extensions.items():
                    if suffix in exts:
                        # Skip .d.ts files
                        if suffix == ".ts" and filename.endswith(".d.ts"):
                            continue
                        self._files[lang].append(filepath)
                        self.metrics.file_count += 1
                        break

    def _detect_language(self) -> None:
        """Detect primary language."""
        counts = {
            "python": len(self._files.get("python", [])),
            "typescript": len(self._files.get("typescript", [])),
            "javascript": len(self._files.get("javascript", [])),
            "go": len(self._files.get("go", [])),
        }

        if counts:
            self.metrics.language = max(counts, key=counts.get)  # type: ignore

    def _read_file(self, path: Path) -> str:
        """Read file content with caching."""
        if path not in self._file_contents:
            try:
                self._file_contents[path] = path.read_text(encoding="utf-8")
            except Exception:
                self._file_contents[path] = ""
        return self._file_contents[path]

    def _count_loc(self) -> None:
        """Count lines of code."""
        for lang, files in self._files.items():
            if lang in ("json", "markdown", "yaml"):
                continue

            for f in files:
                content = self._read_file(f)
                lines = content.splitlines()
                loc = len(lines)
                self.metrics.total_loc += loc

                is_test = self._is_test_file(f)
                if is_test:
                    self.metrics.test_loc += loc
                else:
                    self.metrics.source_loc += loc

    def _is_test_file(self, path: Path) -> bool:
        """Check if file is a test file."""
        name = path.name.lower()
        parent = path.parent.name.lower()

        # Common test patterns
        test_patterns = [
            "test" in name,
            "spec" in name,
            parent in ("tests", "test", "__tests__", "specs"),
            name.startswith("test_"),
            name.endswith("_test.py"),
            name.endswith("_test.go"),
            ".test." in name,
            ".spec." in name,
        ]
        return any(test_patterns)

    # =========================================================================
    # DIMENSION ANALYZERS
    # =========================================================================

    def _analyze_functional_completeness(self) -> DimensionScore:
        """Analyze if code meets functional requirements."""
        score = 50.0  # Start neutral
        details = []
        issues = []
        positives = []

        # Check if there's any code at all
        source_files = sum(
            len(self._files.get(lang, [])) for lang in ["python", "typescript", "javascript", "go"]
        )

        if source_files == 0:
            return DimensionScore(
                name="Functional Completeness",
                score=0,
                weight=self.WEIGHTS["functional_completeness"],
                details=["No source code found"],
                issues=["Project appears to be empty"],
            )

        details.append(f"{source_files} source files found")

        # Check for entry points
        has_entry = self._check_entry_points()
        if has_entry:
            score += 15
            positives.append("Entry point found")
        else:
            score -= 10
            issues.append("No clear entry point")

        # Check for exports (modules, APIs)
        exports = self._count_exports()
        if exports > 0:
            score += min(15, exports * 2)
            positives.append(f"{exports} exports/public APIs found")
        else:
            score -= 5
            issues.append("No exports found")

        # Check for error handling
        error_handling = self._check_error_handling()
        if error_handling["has_handling"]:
            score += 10
            positives.append(f"{error_handling['count']} error handling patterns")
        else:
            score -= 10
            issues.append("No error handling found")

        # Check for input validation
        validation = self._check_input_validation()
        if validation["has_validation"]:
            score += 10
            positives.append(f"{validation['count']} validation patterns")

        # Check requirements if provided
        if self.requirements:
            found, missing = self._check_requirements()
            self.metrics.requirements_found = found
            self.metrics.requirements_missing = missing

            if found:
                coverage = len(found) / len(self.requirements) * 100
                score_bonus = min(20, coverage * 0.2)
                score += score_bonus
                positives.append(f"{len(found)}/{len(self.requirements)} requirements met")

            if missing:
                score -= len(missing) * 5
                for m in missing[:5]:
                    issues.append(f"Missing: {m}")

        return DimensionScore(
            name="Functional Completeness",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["functional_completeness"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_code_quality(self) -> DimensionScore:
        """Analyze code quality (complexity, patterns, style)."""
        score = 60.0  # Start slightly positive
        details = []
        issues = []
        positives = []

        # Analyze by language
        lang = self.metrics.language

        if lang == "python":
            result = self._analyze_python_quality()
        elif lang in ("typescript", "javascript"):
            result = self._analyze_ts_quality()
        elif lang == "go":
            result = self._analyze_go_quality()
        else:
            result = {"score_adj": 0, "issues": [], "positives": []}

        score += result.get("score_adj", 0)
        issues.extend(result.get("issues", []))
        positives.extend(result.get("positives", []))

        # Common quality checks
        # Check function sizes
        large_functions = self._count_large_functions()
        if large_functions > 0:
            score -= large_functions * 3
            issues.append(f"{large_functions} functions over 50 lines")
        else:
            score += 5
            positives.append("No oversized functions")

        # Check for magic numbers
        magic_numbers = self._count_magic_numbers()
        if magic_numbers > 10:
            score -= min(15, magic_numbers)
            issues.append(f"{magic_numbers} magic numbers")
        elif magic_numbers < 3:
            score += 5
            positives.append("Minimal magic numbers")

        # Check for duplicate code patterns
        duplication = self._estimate_duplication()
        if duplication > 20:
            score -= min(20, duplication // 2)
            issues.append(f"~{duplication}% code duplication estimated")
        elif duplication < 5:
            score += 5
            positives.append("Low code duplication")

        details.append(f"Primary language: {lang}")
        details.append(f"Source LOC: {self.metrics.source_loc}")

        return DimensionScore(
            name="Code Quality",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["code_quality"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_security(self) -> DimensionScore:
        """Analyze security vulnerabilities and practices."""
        score = 70.0  # Start optimistic
        details = []
        issues = []
        positives = []

        vulnerabilities = []

        # Check for common security issues across all files
        for lang in ["python", "typescript", "javascript", "go"]:
            for f in self._files.get(lang, []):
                content = self._read_file(f)
                file_vulns = self._check_security_patterns(content, f, lang)
                vulnerabilities.extend(file_vulns)

        # Categorize and score
        critical = [v for v in vulnerabilities if v["severity"] == "critical"]
        high = [v for v in vulnerabilities if v["severity"] == "high"]
        medium = [v for v in vulnerabilities if v["severity"] == "medium"]
        low = [v for v in vulnerabilities if v["severity"] == "low"]

        score -= len(critical) * 25
        score -= len(high) * 15
        score -= len(medium) * 5
        score -= len(low) * 2

        for v in critical[:3]:
            issues.append(f"CRITICAL: {v['issue']} ({v['file']})")
        for v in high[:3]:
            issues.append(f"HIGH: {v['issue']} ({v['file']})")
        for v in medium[:5]:
            issues.append(f"MEDIUM: {v['issue']}")

        # Check for security positives
        has_auth = self._check_auth_patterns()
        if has_auth:
            score += 5
            positives.append("Authentication patterns found")

        has_sanitization = self._check_sanitization()
        if has_sanitization:
            score += 5
            positives.append("Input sanitization found")

        has_rate_limiting = self._check_rate_limiting()
        if has_rate_limiting:
            score += 5
            positives.append("Rate limiting found")

        if not vulnerabilities:
            score += 10
            positives.append("No obvious security issues detected")

        details.append(
            f"Vulnerabilities: {len(critical)} critical, {len(high)} high, {len(medium)} medium"
        )

        return DimensionScore(
            name="Security",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["security"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_test_quality(self) -> DimensionScore:
        """Analyze test coverage and quality."""
        score = 30.0  # Start low, tests must prove themselves
        details = []
        issues = []
        positives = []

        # Count test files
        test_files = []
        for lang in ["python", "typescript", "javascript", "go"]:
            for f in self._files.get(lang, []):
                if self._is_test_file(f):
                    test_files.append(f)

        if not test_files:
            return DimensionScore(
                name="Test Quality",
                score=0,
                weight=self.WEIGHTS["test_quality"],
                details=["No test files found"],
                issues=["No tests written"],
            )

        details.append(f"{len(test_files)} test files found")
        score += min(20, len(test_files) * 3)
        positives.append(f"{len(test_files)} test files")

        # Count test cases
        test_count = 0
        assertion_count = 0
        edge_case_tests = 0

        for tf in test_files:
            content = self._read_file(tf)
            tc, ac, ec = self._analyze_test_file(content, self.metrics.language)
            test_count += tc
            assertion_count += ac
            edge_case_tests += ec

        if test_count > 0:
            score += min(20, test_count)
            positives.append(f"{test_count} test cases")

        if assertion_count > 0:
            avg_assertions = assertion_count / max(1, test_count)
            if avg_assertions >= 2:
                score += 10
                positives.append(f"Good assertion density ({avg_assertions:.1f}/test)")
            elif avg_assertions < 1:
                score -= 5
                issues.append("Low assertion count per test")

        if edge_case_tests > 0:
            score += min(15, edge_case_tests * 2)
            positives.append(f"{edge_case_tests} edge case tests")
        else:
            issues.append("No obvious edge case testing")

        # Check test/source ratio
        if self.metrics.source_loc > 0:
            test_ratio = self.metrics.test_loc / self.metrics.source_loc
            if test_ratio >= 0.5:
                score += 10
                positives.append(f"Good test/source ratio ({test_ratio:.1%})")
            elif test_ratio < 0.1:
                score -= 10
                issues.append(f"Low test coverage ({test_ratio:.1%} test/source ratio)")

        # Try to run tests and get coverage
        coverage = self._run_tests_with_coverage()
        if coverage is not None:
            details.append(f"Coverage: {coverage}%")
            if coverage >= 80:
                score += 15
                positives.append(f"Excellent coverage: {coverage}%")
            elif coverage >= 60:
                score += 10
                positives.append(f"Good coverage: {coverage}%")
            elif coverage < 40:
                score -= 10
                issues.append(f"Low coverage: {coverage}%")

        return DimensionScore(
            name="Test Quality",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["test_quality"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_documentation(self) -> DimensionScore:
        """Analyze documentation quality."""
        score = 40.0  # Start neutral
        details = []
        issues = []
        positives = []

        # Check for README
        readme_files = list(self.project_dir.rglob("README*"))
        readme_files = [r for r in readme_files if not self._should_skip(r)]

        if readme_files:
            readme_content = self._read_file(readme_files[0])
            readme_len = len(readme_content)

            if readme_len > 500:
                score += 15
                positives.append("Comprehensive README")
            elif readme_len > 100:
                score += 5
                positives.append("Basic README present")
            else:
                issues.append("README is too brief")
        else:
            score -= 15
            issues.append("No README file")

        # Check for inline documentation (docstrings, JSDoc, etc.)
        doc_coverage = self._calculate_doc_coverage()
        if doc_coverage >= 50:
            score += 20
            positives.append(f"{doc_coverage}% functions documented")
        elif doc_coverage >= 20:
            score += 10
            positives.append(f"{doc_coverage}% functions documented")
        elif doc_coverage < 10:
            score -= 10
            issues.append("Very few documented functions")

        # Check for type annotations/hints
        type_coverage = self._calculate_type_coverage()
        if type_coverage >= 80:
            score += 15
            positives.append(f"Excellent type coverage: {type_coverage}%")
        elif type_coverage >= 50:
            score += 10
            positives.append(f"Good type coverage: {type_coverage}%")
        elif type_coverage < 20:
            issues.append(f"Low type coverage: {type_coverage}%")

        # Check for changelog
        changelog = list(self.project_dir.rglob("CHANGELOG*"))
        if changelog:
            score += 5
            positives.append("CHANGELOG present")

        details.append(f"Documentation coverage: {doc_coverage}%")
        details.append(f"Type coverage: {type_coverage}%")

        return DimensionScore(
            name="Documentation",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["documentation"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_best_practices(self) -> DimensionScore:
        """Analyze adherence to best practices."""
        score = 50.0
        details: list[str] = []
        issues: list[str] = []
        positives: list[str] = []

        lang = self.metrics.language

        # Check for configuration files
        config_checks = [
            ("pyproject.toml", "Modern Python packaging"),
            ("package.json", "Node.js project config"),
            ("tsconfig.json", "TypeScript configuration"),
            ("go.mod", "Go modules"),
            (".gitignore", "Git ignore file"),
            (".editorconfig", "Editor configuration"),
        ]

        for filename, desc in config_checks:
            if (self.project_dir / filename).exists():
                score += 3
                positives.append(desc)

        # Check for linting configuration
        lint_configs = [".eslintrc", ".eslintrc.js", ".eslintrc.json", "ruff.toml", ".golangci.yml"]
        has_linting = any((self.project_dir / lc).exists() for lc in lint_configs)
        if has_linting:
            score += 10
            positives.append("Linting configured")
        else:
            issues.append("No linting configuration")

        # Check for CI/CD
        ci_dirs = [".github/workflows", ".gitlab-ci.yml", ".circleci", "Jenkinsfile"]
        has_ci = any((self.project_dir / ci).exists() for ci in ci_dirs)
        if has_ci:
            score += 10
            positives.append("CI/CD configured")

        # Language-specific best practices
        if lang == "python":
            bp_result = self._check_python_best_practices()
        elif lang in ("typescript", "javascript"):
            bp_result = self._check_ts_best_practices()
        elif lang == "go":
            bp_result = self._check_go_best_practices()
        else:
            bp_result = {"score_adj": 0, "issues": [], "positives": []}

        score += bp_result.get("score_adj", 0)
        issues.extend(bp_result.get("issues", []))
        positives.extend(bp_result.get("positives", []))

        # Check for consistent code style
        style_consistency = self._check_style_consistency()
        if style_consistency >= 80:
            score += 10
            positives.append("Consistent code style")
        elif style_consistency < 50:
            score -= 10
            issues.append("Inconsistent code style")

        return DimensionScore(
            name="Best Practices",
            score=max(0, min(100, score)),
            weight=self.WEIGHTS["best_practices"],
            details=details,
            issues=issues,
            positives=positives,
        )

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _check_entry_points(self) -> bool:
        """Check if project has clear entry points."""
        entry_patterns = [
            "main.py",
            "__main__.py",
            "index.ts",
            "index.js",
            "main.ts",
            "main.js",
            "main.go",
            "app.py",
            "app.ts",
            "server.py",
            "server.ts",
        ]

        for lang_files in self._files.values():
            for f in lang_files:
                if f.name.lower() in entry_patterns:
                    return True

        # Check for main function in Go
        for f in self._files.get("go", []):
            content = self._read_file(f)
            if "func main()" in content:
                return True

        return False

    def _count_exports(self) -> int:
        """Count exports/public APIs."""
        count = 0
        lang = self.metrics.language

        if lang == "python":
            for f in self._files.get("python", []):
                content = self._read_file(f)
                # Count __all__ entries and public classes/functions
                if "__all__" in content:
                    match = re.search(r"__all__\s*=\s*\[(.*?)\]", content, re.DOTALL)
                    if match:
                        count += len(re.findall(r'["\'](\w+)["\']', match.group(1)))
                # Count public functions/classes
                count += len(re.findall(r"^(?:def|class)\s+(?!_)\w+", content, re.MULTILINE))

        elif lang in ("typescript", "javascript"):
            for f in self._files.get(lang, []):
                content = self._read_file(f)
                count += len(
                    re.findall(
                        r"\bexport\s+(?:default\s+)?(?:function|class|const|let|interface|type)",
                        content,
                    )
                )

        elif lang == "go":
            for f in self._files.get("go", []):
                content = self._read_file(f)
                # Exported = starts with uppercase
                count += len(re.findall(r"^func\s+[A-Z]\w*", content, re.MULTILINE))
                count += len(re.findall(r"^type\s+[A-Z]\w*", content, re.MULTILINE))

        return count

    def _check_error_handling(self) -> dict[str, Any]:
        """Check for error handling patterns."""
        count = 0
        has_handling = False

        for lang, files in self._files.items():
            if lang in ("json", "markdown", "yaml"):
                continue

            for f in files:
                content = self._read_file(f)

                if lang == "python":
                    count += len(re.findall(r"\btry\s*:", content))
                    count += len(re.findall(r"\bexcept\s+\w+", content))
                elif lang in ("typescript", "javascript"):
                    count += len(re.findall(r"\btry\s*\{", content))
                    count += len(re.findall(r"\.catch\s*\(", content))
                    count += len(re.findall(r"\bthrow\s+new\s+\w*Error", content))
                elif lang == "go":
                    count += len(re.findall(r"if\s+err\s*!=\s*nil", content))

        has_handling = count > 0
        return {"has_handling": has_handling, "count": count}

    def _check_input_validation(self) -> dict[str, Any]:
        """Check for input validation patterns."""
        count = 0
        has_validation = False

        validation_patterns = [
            r"\bvalidate\w*\s*\(",
            r"\bschema\.\w+",
            r"\bzod\.\w+",
            r"\byup\.\w+",
            r"\bpydantic\b",
            r"\b@validator\b",
            r"\bclass\s+\w+\(BaseModel\)",
            r"\bclass\s+\w+\(Schema\)",
            r"\bif\s+not\s+isinstance\(",
            r"\bif\s+typeof\s+\w+\s*[!=]==",
            r"\brequired:\s*true",
            r"\.required\(\)",
            r"\.min\(\d+\)",
            r"\.max\(\d+\)",
        ]

        for files in self._files.values():
            for f in files:
                content = self._read_file(f)
                for pattern in validation_patterns:
                    count += len(re.findall(pattern, content, re.IGNORECASE))

        has_validation = count > 0
        return {"has_validation": has_validation, "count": count}

    def _check_requirements(self) -> tuple[list[str], list[str]]:
        """Check which requirements are met."""
        found = []
        missing = []

        all_content = ""
        for files in self._files.values():
            for f in files:
                all_content += self._read_file(f).lower() + "\n"

        for req in self.requirements:
            req_lower = req.lower()
            # Simple keyword matching - could be enhanced
            keywords = req_lower.split()
            matches = sum(1 for kw in keywords if kw in all_content)
            if matches >= len(keywords) * 0.5:  # At least 50% keyword match
                found.append(req)
            else:
                missing.append(req)

        return found, missing

    def _count_large_functions(self) -> int:
        """Count functions over 50 lines."""
        count = 0
        lang = self.metrics.language

        for f in self._files.get(lang, []) + self._files.get("python", []):
            content = self._read_file(f)
            lines = content.splitlines()

            if lang == "python" or f.suffix == ".py":
                # Use AST for Python
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            func_lines = (node.end_lineno or 0) - node.lineno
                            if func_lines > 50:
                                count += 1
                except SyntaxError:
                    pass
            else:
                # Simple brace counting for other languages
                in_function = False
                brace_depth = 0
                func_start = 0

                for i, line in enumerate(lines):
                    if re.match(
                        r"^\s*(async\s+)?function\s+|^\s*\w+\s*[=:]\s*(async\s+)?\(|^\s*func\s+",
                        line,
                    ):
                        in_function = True
                        func_start = i
                        brace_depth = 0

                    if in_function:
                        brace_depth += line.count("{") - line.count("}")
                        if brace_depth <= 0 and "{" in content[content.find(lines[func_start]) :]:
                            func_lines = i - func_start
                            if func_lines > 50:
                                count += 1
                            in_function = False

        return count

    def _count_magic_numbers(self) -> int:
        """Count magic numbers in code."""
        count = 0
        allowed = {0, 1, -1, 2, 10, 100, 1000, 60, 24, 365, 404, 200, 500}

        for lang, files in self._files.items():
            if lang in ("json", "markdown", "yaml"):
                continue

            for f in files:
                if self._is_test_file(f):
                    continue
                content = self._read_file(f)
                # Find standalone numbers
                matches = re.findall(r"(?<![a-zA-Z_])\d+(?![a-zA-Z_])", content)
                for m in matches:
                    try:
                        num = int(m)
                        if num not in allowed and num > 2:
                            count += 1
                    except ValueError:
                        pass

        return count

    def _estimate_duplication(self) -> int:
        """Estimate code duplication percentage."""
        # Simple approach: count repeated line sequences
        all_lines = []
        for lang, files in self._files.items():
            if lang in ("json", "markdown", "yaml"):
                continue
            for f in files:
                content = self._read_file(f)
                lines = [
                    line.strip()
                    for line in content.splitlines()
                    if line.strip() and not line.strip().startswith(("#", "//", "/*", "*"))
                ]
                all_lines.extend(lines)

        if len(all_lines) < 10:
            return 0

        # Count duplicates
        from collections import Counter

        line_counts = Counter(all_lines)
        duplicated_lines = sum(count - 1 for count in line_counts.values() if count > 1)

        return int(duplicated_lines / len(all_lines) * 100)

    def _check_security_patterns(self, content: str, path: Path, lang: str) -> list[dict[str, Any]]:
        """Check for security vulnerabilities."""
        vulnerabilities = []
        filename = path.name

        patterns = [
            # Critical
            (r"eval\s*\(", "critical", "Use of eval()"),
            (r"exec\s*\(", "critical", "Use of exec()"),
            (r"subprocess\.call\([^)]*shell\s*=\s*True", "critical", "Shell injection risk"),
            (r"os\.system\s*\(", "critical", "OS command execution"),
            (r"innerHTML\s*=", "high", "Potential XSS via innerHTML"),
            (r"dangerouslySetInnerHTML", "high", "React XSS risk"),
            # High
            (r"password\s*=\s*['\"][^'\"]+['\"]", "high", "Hardcoded password"),
            (r"api_key\s*=\s*['\"][^'\"]+['\"]", "high", "Hardcoded API key"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "high", "Hardcoded secret"),
            (r"SELECT\s+.*\s+FROM\s+.*\s+WHERE.*\+", "high", "SQL injection risk"),
            (r"f['\"].*\{.*\}.*SELECT", "high", "SQL injection in f-string"),
            # Medium
            (r"pickle\.load", "medium", "Insecure deserialization"),
            (r"yaml\.load\s*\([^)]*\)", "medium", "Unsafe YAML loading"),
            (r"verify\s*=\s*False", "medium", "SSL verification disabled"),
            (r"disable_ssl", "medium", "SSL disabled"),
            (r"md5\s*\(", "medium", "Weak hash algorithm (MD5)"),
            (r"sha1\s*\(", "medium", "Weak hash algorithm (SHA1)"),
            # Low
            (r"console\.log\(", "low", "Console logging in production"),
            (r"debugger;", "low", "Debugger statement"),
            (r"TODO.*password", "low", "TODO mentioning password"),
            (r"FIXME.*security", "low", "FIXME mentioning security"),
        ]

        for pattern, severity, issue in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                vulnerabilities.append(
                    {
                        "file": filename,
                        "severity": severity,
                        "issue": issue,
                    }
                )

        return vulnerabilities

    def _check_auth_patterns(self) -> bool:
        """Check for authentication patterns."""
        patterns = [
            r"\bauthenticat\w*",
            r"\bauthoriz\w*",
            r"\bjwt\b",
            r"\btoken\b.*\bvalid",
            r"\bsession\b",
            r"\blogin\b",
            r"\blogout\b",
            r"\bpassword\b.*\bhash",
        ]

        for files in self._files.values():
            for f in files:
                content = self._read_file(f).lower()
                for pattern in patterns:
                    if re.search(pattern, content):
                        return True
        return False

    def _check_sanitization(self) -> bool:
        """Check for input sanitization."""
        patterns = [
            r"\bsanitize\w*",
            r"\bescape\w*",
            r"\bclean\w*input",
            r"\bstrip_tags",
            r"\bhtmlspecialchars",
            r"DOMPurify",
            r"bleach\.",
        ]

        for files in self._files.values():
            for f in files:
                content = self._read_file(f)
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return True
        return False

    def _check_rate_limiting(self) -> bool:
        """Check for rate limiting."""
        patterns = [
            r"\brate.?limit",
            r"\bthrottle",
            r"express-rate-limit",
            r"slowapi",
            r"ratelimit",
        ]

        for files in self._files.values():
            for f in files:
                content = self._read_file(f).lower()
                for pattern in patterns:
                    if re.search(pattern, content):
                        return True
        return False

    def _analyze_test_file(self, content: str, lang: str) -> tuple[int, int, int]:
        """Analyze a test file for test count, assertions, edge cases."""
        test_count = 0
        assertion_count = 0
        edge_case_count = 0

        # Test patterns by language
        if lang == "python":
            test_count = len(re.findall(r"def\s+test_\w+", content))
            assertion_count = len(re.findall(r"\bassert\w*\s*\(", content))
            assertion_count += len(re.findall(r"\bassert\s+", content))
        elif lang in ("typescript", "javascript"):
            test_count = len(re.findall(r"\b(?:it|test)\s*\(", content))
            assertion_count = len(re.findall(r"\bexpect\s*\(", content))
            assertion_count += len(re.findall(r"\bassert\s*\.", content))
        elif lang == "go":
            test_count = len(re.findall(r"func\s+Test\w+", content))
            assertion_count = len(re.findall(r"t\.(?:Error|Fatal|Assert)", content))

        # Edge case patterns
        edge_patterns = [
            r"edge\s*case",
            r"boundary",
            r"empty\s*(?:string|array|list|input)",
            r"null|nil|None",
            r"zero|negative",
            r"overflow",
            r"invalid\s*input",
            r"error\s*(?:case|handling)",
            r"exception",
            r"should\s*(?:fail|throw|error)",
        ]

        for pattern in edge_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                edge_case_count += 1

        return test_count, assertion_count, edge_case_count

    def _run_tests_with_coverage(self) -> float | None:
        """Try to run tests and get coverage.

        Note: This is disabled by default for performance. Set RUN_COVERAGE=1 to enable.
        """
        import os

        # Skip coverage by default (too slow for interactive use)
        if not os.environ.get("RUN_COVERAGE"):
            return None

        lang = self.metrics.language

        try:
            if lang == "python":
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "--cov", "--cov-report=term", "-q", "--tb=no"],
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding="utf-8",
                    errors="replace",
                )
                for line in result.stdout.splitlines():
                    if "TOTAL" in line and "%" in line:
                        match = re.search(r"(\d+)%", line)
                        if match:
                            return float(match.group(1))

            elif lang in ("typescript", "javascript"):
                # Try vitest first, then jest
                for cmd in [
                    ["npx", "vitest", "run", "--coverage"],
                    ["npm", "test", "--", "--coverage"],
                ]:
                    try:
                        result = subprocess.run(
                            cmd,
                            cwd=self.project_dir,
                            capture_output=True,
                            text=True,
                            timeout=60,
                            encoding="utf-8",
                            errors="replace",
                        )
                        for line in result.stdout.splitlines():
                            match = re.search(
                                r"All files\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*([\d.]+)",
                                line,
                            )
                            if match:
                                return float(match.group(1))
                    except Exception:  # noqa: S112
                        continue  # Try next command

            elif lang == "go":
                result = subprocess.run(
                    ["go", "test", "-cover", "./..."],
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding="utf-8",
                    errors="replace",
                )
                for line in result.stdout.splitlines():
                    match = re.search(r"coverage:\s*([\d.]+)%", line)
                    if match:
                        return float(match.group(1))

        except Exception:
            pass

        return None

    def _calculate_doc_coverage(self) -> int:
        """Calculate documentation coverage percentage."""
        total_funcs = 0
        documented = 0
        lang = self.metrics.language

        if lang == "python":
            for f in self._files.get("python", []):
                content = self._read_file(f)
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                            total_funcs += 1
                            if ast.get_docstring(node):
                                documented += 1
                except SyntaxError:
                    pass

        elif lang in ("typescript", "javascript"):
            for f in self._files.get(lang, []):
                content = self._read_file(f)
                # Count functions
                funcs = re.findall(
                    r"(?:function\s+\w+|(?:const|let)\s+\w+\s*=\s*(?:async\s*)?\()", content
                )
                total_funcs += len(funcs)
                # Count JSDoc comments before functions
                documented += len(
                    re.findall(
                        r"/\*\*[\s\S]*?\*/\s*(?:export\s+)?(?:async\s+)?(?:function|const|let)",
                        content,
                    )
                )

        elif lang == "go":
            for f in self._files.get("go", []):
                content = self._read_file(f)
                # Exported functions
                funcs = re.findall(r"^func\s+[A-Z]\w*", content, re.MULTILINE)
                total_funcs += len(funcs)
                # Check for comments before functions
                documented += len(re.findall(r"//\s*[A-Z]\w+.*\n\s*func\s+[A-Z]", content))

        if total_funcs == 0:
            return 0
        return int(documented / total_funcs * 100)

    def _calculate_type_coverage(self) -> int:
        """Calculate type annotation coverage."""
        total = 0
        typed = 0
        lang = self.metrics.language

        if lang == "python":
            for f in self._files.get("python", []):
                content = self._read_file(f)
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            total += 1
                            if node.returns is not None:
                                typed += 1
                            # Also count parameters
                            for arg in node.args.args:
                                total += 1
                                if arg.annotation:
                                    typed += 1
                except SyntaxError:
                    pass

        elif lang == "typescript":
            # TypeScript is inherently typed
            return 90  # Assume good coverage for TS

        elif lang == "javascript":
            # Check for JSDoc type annotations
            for f in self._files.get("javascript", []):
                content = self._read_file(f)
                total += len(re.findall(r"\bfunction\s+\w+", content))
                typed += len(re.findall(r"@param\s*\{", content))
                typed += len(re.findall(r"@returns?\s*\{", content))

        if total == 0:
            return 0
        return int(typed / total * 100)

    def _analyze_python_quality(self) -> dict[str, Any]:
        """Analyze Python-specific quality."""
        score_adj = 0
        issues = []
        positives = []

        for f in self._files.get("python", []):
            content = self._read_file(f)

            # Check for bare excepts
            bare_excepts = len(re.findall(r"\bexcept\s*:", content))
            if bare_excepts:
                score_adj -= bare_excepts * 5
                issues.append(f"{bare_excepts} bare except clauses")

            # Check for pass in except
            silent_passes = len(re.findall(r"except[^:]*:\s*\n\s*pass", content))
            if silent_passes:
                score_adj -= silent_passes * 10
                issues.append(f"{silent_passes} silent exception passes")

            # Check for exception chaining
            chains = len(re.findall(r"raise\s+\w+.*\bfrom\b", content))
            if chains:
                score_adj += min(10, chains * 2)
                positives.append("Exception chaining used")

            # Check for context managers
            context_mgrs = len(re.findall(r"\bwith\s+", content))
            if context_mgrs >= 3:
                score_adj += 5
                positives.append("Context managers used")

            # Check for dataclasses
            if "@dataclass" in content:
                score_adj += 5
                positives.append("Dataclasses used")

            # Check for type hints
            if "->" in content and ":" in content:
                score_adj += 5
                positives.append("Type hints used")

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _analyze_ts_quality(self) -> dict[str, Any]:
        """Analyze TypeScript/JavaScript quality."""
        score_adj = 0
        issues = []
        positives = []

        for f in self._files.get("typescript", []) + self._files.get("javascript", []):
            content = self._read_file(f)

            # Check for any type (TypeScript anti-pattern)
            any_count = len(re.findall(r":\s*any\b", content))
            if any_count > 5:
                score_adj -= min(15, any_count * 2)
                issues.append(f"{any_count} uses of 'any' type")
            elif any_count == 0 and f.suffix == ".ts":
                score_adj += 5
                positives.append("No 'any' types")

            # Check for console.log in non-test files
            if not self._is_test_file(f):
                console_logs = len(re.findall(r"console\.log\(", content))
                if console_logs > 3:
                    score_adj -= 5
                    issues.append(f"{console_logs} console.log statements")

            # Check for async/await usage
            if "async " in content and "await " in content:
                score_adj += 3
                positives.append("Async/await used")

            # Check for proper error handling
            try_catch = len(re.findall(r"\btry\s*\{", content))
            if try_catch >= 2:
                score_adj += 5
                positives.append("Try/catch error handling")

            # Check for interfaces/types
            if re.search(r"\b(interface|type)\s+\w+", content):
                score_adj += 5
                positives.append("Interfaces/types defined")

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _analyze_go_quality(self) -> dict[str, Any]:
        """Analyze Go-specific quality."""
        score_adj = 0
        issues = []
        positives = []

        for f in self._files.get("go", []):
            content = self._read_file(f)

            # Check for error handling
            err_checks = len(re.findall(r"if\s+err\s*!=\s*nil", content))
            err_ignores = len(re.findall(r"_\s*=\s*\w+\(", content))

            if err_checks > 0:
                score_adj += min(10, err_checks)
                positives.append("Proper error checking")

            if err_ignores > 3:
                score_adj -= err_ignores * 2
                issues.append(f"{err_ignores} ignored errors")

            # Check for defer usage
            defers = len(re.findall(r"\bdefer\s+", content))
            if defers > 0:
                score_adj += 5
                positives.append("Defer for cleanup")

            # Check for context usage
            if "context.Context" in content:
                score_adj += 5
                positives.append("Context-aware functions")

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _check_python_best_practices(self) -> dict[str, Any]:
        """Check Python best practices."""
        score_adj = 0
        issues: list[str] = []
        positives: list[str] = []

        # Check for modern Python features
        for f in self._files.get("python", []):
            content = self._read_file(f)

            if "from __future__ import annotations" in content:
                score_adj += 3
                positives.append("Modern annotations")

            if re.search(r"\|\s*None\b", content):  # Union type syntax
                score_adj += 3
                positives.append("Modern union types")

            if "pathlib" in content:
                score_adj += 3
                positives.append("Pathlib usage")

            if re.search(r"if\s+__name__\s*==\s*['\"]__main__['\"]", content):
                score_adj += 2
                positives.append("Proper main guard")

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _check_ts_best_practices(self) -> dict[str, Any]:
        """Check TypeScript/JavaScript best practices."""
        score_adj = 0
        issues = []
        positives = []

        # Check tsconfig
        tsconfig = self.project_dir / "tsconfig.json"
        if tsconfig.exists():
            try:
                config = json.loads(self._read_file(tsconfig))
                compiler = config.get("compilerOptions", {})

                if compiler.get("strict"):
                    score_adj += 10
                    positives.append("Strict mode enabled")
                else:
                    issues.append("Strict mode not enabled")

                if compiler.get("noImplicitAny"):
                    score_adj += 5
                    positives.append("No implicit any")

            except json.JSONDecodeError:
                pass

        # Check package.json
        pkg_json = self.project_dir / "package.json"
        if pkg_json.exists():
            try:
                pkg = json.loads(self._read_file(pkg_json))

                if "eslint" in str(pkg.get("devDependencies", {})):
                    score_adj += 5
                    positives.append("ESLint configured")

                if "prettier" in str(pkg.get("devDependencies", {})):
                    score_adj += 3
                    positives.append("Prettier configured")

                if pkg.get("scripts", {}).get("test"):
                    score_adj += 5
                    positives.append("Test script defined")

            except json.JSONDecodeError:
                pass

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _check_go_best_practices(self) -> dict[str, Any]:
        """Check Go best practices."""
        score_adj = 0
        issues = []
        positives = []

        # Check for go.mod
        if (self.project_dir / "go.mod").exists():
            score_adj += 5
            positives.append("Go modules used")
        else:
            issues.append("No go.mod file")

        # Check for golangci-lint config
        lint_configs = [".golangci.yml", ".golangci.yaml", ".golangci.toml"]
        if any((self.project_dir / lc).exists() for lc in lint_configs):
            score_adj += 5
            positives.append("golangci-lint configured")

        return {"score_adj": score_adj, "issues": issues, "positives": positives}

    def _check_style_consistency(self) -> int:
        """Check code style consistency (returns 0-100)."""
        # Simple heuristic: check indent consistency
        indent_styles = {"tabs": 0, "2space": 0, "4space": 0}

        for files in self._files.values():
            for f in files:
                content = self._read_file(f)
                for line in content.splitlines():
                    if line.startswith("\t"):
                        indent_styles["tabs"] += 1
                    elif line.startswith("    "):
                        indent_styles["4space"] += 1
                    elif line.startswith("  ") and not line.startswith("    "):
                        indent_styles["2space"] += 1

        total = sum(indent_styles.values())
        if total == 0:
            return 100

        dominant = max(indent_styles.values())
        return int(dominant / total * 100)

    def _calculate_overall(self) -> None:
        """Calculate overall score and grade."""
        dimensions = [
            self.metrics.functional_completeness,
            self.metrics.code_quality,
            self.metrics.security,
            self.metrics.test_quality,
            self.metrics.documentation,
            self.metrics.best_practices,
        ]

        total_weighted = 0.0
        total_weight = 0.0

        for dim in dimensions:
            if dim:
                total_weighted += dim.score * dim.weight
                total_weight += dim.weight

        if total_weight > 0:
            self.metrics.overall_score = total_weighted / total_weight
        else:
            self.metrics.overall_score = 0

        # Assign grade
        score = self.metrics.overall_score
        if score >= 90:
            self.metrics.grade = "A"
        elif score >= 80:
            self.metrics.grade = "B"
        elif score >= 70:
            self.metrics.grade = "C"
        elif score >= 60:
            self.metrics.grade = "D"
        else:
            self.metrics.grade = "F"


def compare_comprehensive(
    cco: ComprehensiveMetrics, vanilla: ComprehensiveMetrics
) -> dict[str, Any]:
    """Compare two comprehensive analyses."""
    dimensions = [
        "functional_completeness",
        "code_quality",
        "security",
        "test_quality",
        "documentation",
        "best_practices",
    ]

    comparisons = []
    cco_wins = 0
    vanilla_wins = 0
    ties = 0

    for dim_name in dimensions:
        cco_dim = getattr(cco, dim_name)
        vanilla_dim = getattr(vanilla, dim_name)

        if not cco_dim or not vanilla_dim:
            continue

        cco_score = cco_dim.score
        vanilla_score = vanilla_dim.score
        diff = cco_score - vanilla_score

        if diff > 5:
            winner = "cco"
            cco_wins += 1
        elif diff < -5:
            winner = "vanilla"
            vanilla_wins += 1
        else:
            winner = "tie"
            ties += 1

        comparisons.append(
            {
                "dimension": dim_name.replace("_", " ").title(),
                "cco_score": round(cco_score, 1),
                "vanilla_score": round(vanilla_score, 1),
                "difference": round(diff, 1),
                "winner": winner,
                "cco_issues": cco_dim.issues[:3],
                "vanilla_issues": vanilla_dim.issues[:3],
                "cco_positives": cco_dim.positives[:3],
                "vanilla_positives": vanilla_dim.positives[:3],
            }
        )

    overall_diff = cco.overall_score - vanilla.overall_score

    if overall_diff >= 15:
        verdict = "Strong CCO Advantage"
    elif overall_diff >= 5:
        verdict = "Moderate CCO Advantage"
    elif overall_diff >= -5:
        verdict = "Mixed Results"
    elif overall_diff >= -15:
        verdict = "Moderate Vanilla Advantage"
    else:
        verdict = "Strong Vanilla Advantage"

    return {
        "comparisons": comparisons,
        "cco_wins": cco_wins,
        "vanilla_wins": vanilla_wins,
        "ties": ties,
        "cco_overall": round(cco.overall_score, 1),
        "vanilla_overall": round(vanilla.overall_score, 1),
        "cco_grade": cco.grade,
        "vanilla_grade": vanilla.grade,
        "overall_diff": round(overall_diff, 1),
        "verdict": verdict,
    }

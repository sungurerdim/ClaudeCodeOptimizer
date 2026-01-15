"""
Unified Code Analyzer for CCO Benchmarks.

Multi-dimensional analysis supporting 40+ languages:
- Functional Completeness
- Code Quality
- Security
- Test Quality
- Documentation
- Best Practices

Combines detailed metrics collection with 6-dimension scoring.
"""

import ast
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# =============================================================================
# DIMENSION SCORING SYSTEM
# =============================================================================


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


# Dimension weights (must sum to 1.0)
# Production-grade priorities: functionality > security > testing > quality > practices > docs
DIMENSION_WEIGHTS = {
    "functional_completeness": 0.25,  # Does it work? (Most critical)
    "security": 0.20,  # Is it secure? (Critical for production)
    "test_quality": 0.20,  # Is it tested? (Reliability)
    "code_quality": 0.15,  # Is it well-written? (Maintainability)
    "best_practices": 0.15,  # Standards + UX/DX scores (Design quality)
    "documentation": 0.05,  # Is it documented? (Nice to have)
}


def calculate_grade(score: float) -> str:
    """Convert score to letter grade."""
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 80:
        return "B+"
    elif score >= 75:
        return "B"
    elif score >= 70:
        return "B-"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "C-"
    elif score >= 50:
        return "D"
    else:
        return "F"


@dataclass
class FunctionInfo:
    """Information about a single function."""

    name: str
    loc: int
    complexity: int
    has_return_type: bool
    has_docstring: bool
    param_count: int
    typed_params: int


@dataclass
class Metrics:
    """Comprehensive metrics for a codebase with 6-dimension scoring."""

    # Identity
    name: str = ""
    variant: str = ""  # "cco" or "vanilla"
    language: str = ""  # primary language detected

    # Overall score and grade
    overall_score: float = 0.0
    grade: str = ""  # A+, A, A-, B+, B, B-, C+, C, C-, D, F

    # 6-Dimension Scores
    functional_completeness: DimensionScore | None = None
    code_quality: DimensionScore | None = None
    security: DimensionScore | None = None
    test_quality: DimensionScore | None = None
    documentation: DimensionScore | None = None
    best_practices: DimensionScore | None = None

    # Timing
    generation_time_seconds: float = 0.0

    # File metrics
    total_files: int = 0
    python_files: int = 0
    typescript_files: int = 0
    go_files: int = 0
    test_files: int = 0

    # Size metrics
    total_loc: int = 0
    code_loc: int = 0  # Excluding comments/blanks
    test_loc: int = 0

    # Structure
    functions: int = 0
    methods: int = 0
    classes: int = 0

    # Function size distribution
    small_funcs: int = 0  # < 10 LOC
    medium_funcs: int = 0  # 10-30 LOC
    large_funcs: int = 0  # 30-50 LOC
    giant_funcs: int = 0  # > 50 LOC (problem!)

    # Type coverage
    typed_functions: int = 0
    typed_params: int = 0
    total_params: int = 0
    type_coverage_pct: float = 0.0

    # Documentation
    documented_funcs: int = 0
    documented_classes: int = 0
    docstring_coverage_pct: float = 0.0

    # Quality (anti-patterns - lower is better)
    bare_excepts: int = 0
    silent_passes: int = 0
    broad_excepts: int = 0
    magic_numbers: int = 0
    global_vars: int = 0
    mutable_defaults: int = 0
    star_imports: int = 0

    # Best practices (higher is better)
    exception_chains: int = 0
    context_managers: int = 0
    dataclasses_used: int = 0
    enums_used: int = 0
    pathlib_used: bool = False

    # Complexity
    max_complexity: int = 0
    avg_complexity: float = 0.0
    high_complexity_funcs: int = 0  # > 10

    # Testing
    test_count: int = 0
    tests_passed: bool | None = None
    coverage_pct: float | None = None

    # UX/DX scores (0-100)
    modularity_score: float = 0.0  # Based on function sizes
    srp_score: float = 0.0  # Single responsibility
    naming_score: float = 0.0  # Variable/function naming
    error_handling_score: float = 0.0  # Error message quality

    # Function details for analysis
    function_details: list[FunctionInfo] = field(default_factory=list)

    # Raw data for inspection
    anti_patterns_detail: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        d: dict[str, Any] = {}
        # Dimension names for special handling
        dimension_names = {
            "functional_completeness",
            "code_quality",
            "security",
            "test_quality",
            "documentation",
            "best_practices",
        }

        for k, v in self.__dict__.items():
            if k == "function_details":
                d[k] = [f.__dict__ for f in v]
            elif k in dimension_names and v is not None:
                d[k] = v.to_dict()
            elif isinstance(v, Path):
                d[k] = str(v)
            else:
                d[k] = v

        # Add dimensions summary for easy access
        d["dimensions"] = {
            name: getattr(self, name).to_dict() if getattr(self, name) else None
            for name in dimension_names
        }
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Metrics":
        """Create from dictionary."""
        func_details = data.pop("function_details", [])
        dimensions = data.pop("dimensions", {})

        # Remove dimension fields as they'll be set separately
        dimension_names = {
            "functional_completeness",
            "code_quality",
            "security",
            "test_quality",
            "documentation",
            "best_practices",
        }
        for dim in dimension_names:
            data.pop(dim, None)

        m = cls(**data)
        m.function_details = [FunctionInfo(**f) for f in func_details]

        # Restore dimension scores
        for dim_name, dim_data in (dimensions or {}).items():
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


class CodeAnalyzer:
    """Analyzes code and collects metrics."""

    # Magic number patterns (excluding common ones like 0, 1, -1)
    MAGIC_PATTERN = re.compile(r"\b(?<!\.)\d+(?!\.\d)(?![a-zA-Z_])\b")
    # Common acceptable numbers: 0-10, powers of 2/10, time constants, HTTP codes, common ports
    ALLOWED_NUMBERS = {
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        -1,  # Small numbers
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
        8192,  # Powers of 2
        100,
        1000,
        10000,
        100000,
        1000000,  # Powers of 10
        60,
        24,
        365,
        12,
        30,
        31,
        52,  # Time constants
        80,
        443,
        8080,
        3000,
        5000,
        8000,
        8888,  # Common ports
        200,
        201,
        204,
        301,
        302,
        400,
        401,
        403,
        404,
        500,
        502,
        503,  # HTTP codes
        255,  # Byte values
    }

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.metrics = Metrics()

    # All languages supported by cco-adaptive
    LANGUAGE_EXTENSIONS: dict[str, str] = {
        # Tier 1: Full analysis support
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".go": "go",
        # Tier 2: Extended analysis
        ".rs": "rust",
        ".java": "java",
        ".kt": "kotlin",
        ".kts": "kotlin",
        ".cs": "csharp",
        ".swift": "swift",
        ".rb": "ruby",
        ".php": "php",
        # Tier 3: Basic analysis (C-family)
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".hxx": "hpp",
        # Tier 4: Functional languages
        ".hs": "haskell",
        ".fs": "fsharp",
        ".fsx": "fsharp",
        ".ml": "ocaml",
        ".mli": "ocaml",
        ".ex": "elixir",
        ".exs": "elixir",
        ".erl": "erlang",
        ".hrl": "erlang",
        ".clj": "clojure",
        ".cljs": "clojure",
        ".cljc": "clojure",
        ".scala": "scala",
        ".sc": "scala",
        ".gleam": "gleam",
        # Tier 5: Other languages
        ".js": "javascript",
        ".jsx": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",
        ".lua": "lua",
        ".r": "r",
        ".R": "r",
        ".jl": "julia",
        ".pl": "perl",
        ".pm": "perl",
        ".dart": "dart",
        ".zig": "zig",
        # Tier 6: Shell/Config
        ".sh": "shell",
        ".bash": "shell",
        ".zsh": "shell",
        ".ps1": "powershell",
        ".psm1": "powershell",
    }

    # Test file patterns by language
    TEST_PATTERNS: dict[str, list[str]] = {
        "python": ["test_", "_test.py", "tests/"],
        "typescript": [".test.", ".spec.", "__tests__/"],
        "javascript": [".test.", ".spec.", "__tests__/"],
        "go": ["_test.go"],
        "rust": ["tests/", "#[test]", "#[cfg(test)]"],
        "java": ["Test.java", "Tests.java", "test/"],
        "kotlin": ["Test.kt", "Tests.kt", "test/"],
        "csharp": ["Test.cs", "Tests.cs", ".Tests/"],
        "swift": ["Tests.swift", "Test.swift", "Tests/"],
        "ruby": ["_test.rb", "_spec.rb", "spec/", "test/"],
        "php": ["Test.php", "test/", "tests/"],
        "elixir": ["_test.exs", "test/"],
        "haskell": ["Spec.hs", "Test.hs", "test/"],
        "scala": ["Spec.scala", "Test.scala", "test/"],
    }

    def analyze(self, comprehensive: bool = True) -> Metrics:
        """Perform full analysis with optional 6-dimension scoring.

        Args:
            comprehensive: If True, calculate 6-dimension scores and grade.
                          If False, only collect raw metrics (faster).
        """
        self._count_files()
        self._detect_language()

        # Tier 1: Full analysis
        self._analyze_python()
        self._analyze_typescript()
        self._analyze_go()
        # Tier 2: Extended analysis
        self._analyze_rust()
        self._analyze_java()
        self._analyze_csharp()
        self._analyze_ruby()
        self._analyze_php()
        self._analyze_swift()
        self._analyze_kotlin()
        # Tier 3+: Generic analysis for all other languages
        self._analyze_other_languages()
        self._calculate_scores()

        if comprehensive:
            # 6-Dimension Analysis
            self.metrics.functional_completeness = self._analyze_functional_completeness()
            self.metrics.code_quality = self._analyze_code_quality()
            self.metrics.security = self._analyze_security()
            self.metrics.test_quality = self._analyze_test_quality()
            self.metrics.documentation = self._analyze_documentation()
            self.metrics.best_practices = self._analyze_best_practices()

            # Calculate overall score and grade
            self._calculate_overall_score()

        self._run_tests()
        return self.metrics

    def _detect_language(self) -> None:
        """Detect primary language from file counts."""
        counts = {
            "python": self.metrics.python_files,
            "typescript": self.metrics.typescript_files,
            "go": self.metrics.go_files,
        }
        # Add other languages from extension counts
        for f in self.project_dir.rglob("*"):
            if self._should_skip(f) or not f.is_file():
                continue
            suffix = f.suffix.lower()
            lang = self.LANGUAGE_EXTENSIONS.get(suffix)
            if lang and lang not in counts:
                counts[lang] = 0
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

        if counts:
            self.metrics.language = max(counts, key=lambda k: counts.get(k, 0))

    def _calculate_overall_score(self) -> None:
        """Calculate overall score from 6 dimensions and assign grade."""
        total = 0.0
        for dim_name, weight in DIMENSION_WEIGHTS.items():
            dim_score = getattr(self.metrics, dim_name)
            if dim_score:
                total += dim_score.score * weight

        self.metrics.overall_score = round(total, 1)
        self.metrics.grade = calculate_grade(total)

    def _count_files(self) -> None:
        """Count files by type."""
        for f in self.project_dir.rglob("*"):
            if self._should_skip(f):
                continue
            if not f.is_file():
                continue

            self.metrics.total_files += 1
            suffix = f.suffix.lower()
            lang = self.LANGUAGE_EXTENSIONS.get(suffix)

            if suffix == ".py":
                self.metrics.python_files += 1
                if self._is_test_file(f, "python"):
                    self.metrics.test_files += 1
            elif suffix in (".ts", ".tsx"):
                self.metrics.typescript_files += 1
                if self._is_test_file(f, "typescript"):
                    self.metrics.test_files += 1
            elif suffix == ".go":
                self.metrics.go_files += 1
                if self._is_test_file(f, "go"):
                    self.metrics.test_files += 1
            elif lang:
                # Count other known languages
                if self._is_test_file(f, lang):
                    self.metrics.test_files += 1

    def _is_test_file(self, path: Path, lang: str) -> bool:
        """Check if file is a test file based on language patterns."""
        patterns = self.TEST_PATTERNS.get(lang, [])
        name = path.name
        path_str = str(path)
        for pattern in patterns:
            if pattern.endswith("/"):
                if pattern.rstrip("/") in path.parts:
                    return True
            elif pattern in name or pattern in path_str:
                return True
        return False

    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped (deps/cache/build dirs)."""
        skip_dirs = {
            "__pycache__",
            ".venv",
            "venv",
            "node_modules",
            ".git",
            "dist",
            "build",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "coverage",
            ".deps",  # ccbox dependency cache
            "site-packages",
        }
        # Skip benchmark metadata files
        skip_prefixes = ("_benchmark_", "_ccbox_", "_context_")
        # Skip suffixes (e.g., mlserve.egg-info)
        skip_suffixes = (".log", ".egg-info")

        if path.name.startswith(skip_prefixes):
            return True
        for part in path.parts:
            if part in skip_dirs:
                return True
            if any(part.endswith(suffix) for suffix in skip_suffixes):
                return True
        return False

    def _analyze_python(self) -> None:
        """Analyze Python files."""
        for py_file in self.project_dir.rglob("*.py"):
            if self._should_skip(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                self._analyze_python_file(py_file, content)
            except Exception:
                pass

    def _analyze_python_file(self, path: Path, content: str) -> None:
        """Analyze a single Python file."""
        lines = content.splitlines()
        loc = len(lines)

        # Count LOC
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

        is_test = "test" in path.name.lower()
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc

        # Check for pathlib usage
        if "pathlib" in content or "from pathlib" in content:
            self.metrics.pathlib_used = True

        # Magic numbers (simple check)
        self._check_magic_numbers(content, str(path))

        # Star imports
        if re.search(r"from .+ import \*", content):
            self.metrics.star_imports += 1
            self._add_anti_pattern("star_imports", str(path))

        # Parse AST
        try:
            tree = ast.parse(content)
            self._analyze_python_ast(tree, content, str(path))
        except SyntaxError:
            pass

    def _analyze_python_ast(self, tree: ast.AST, source: str, filepath: str) -> None:
        """Analyze Python AST."""
        lines = source.splitlines()

        for node in ast.walk(tree):
            # Classes
            if isinstance(node, ast.ClassDef):
                self.metrics.classes += 1
                if self._has_docstring(node):
                    self.metrics.documented_classes += 1

                # Check for dataclass
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                        self.metrics.dataclasses_used += 1
                    elif isinstance(decorator, ast.Call):
                        if (
                            isinstance(decorator.func, ast.Name)
                            and decorator.func.id == "dataclass"
                        ):
                            self.metrics.dataclasses_used += 1

                # Check for Enum
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id in ("Enum", "StrEnum", "IntEnum"):
                        self.metrics.enums_used += 1

            # Functions
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                self._analyze_function(node, lines, filepath)

            # Exception handlers
            elif isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    self.metrics.bare_excepts += 1
                    self._add_anti_pattern("bare_excepts", f"{filepath}:{node.lineno}")
                elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
                    self.metrics.broad_excepts += 1

                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    self.metrics.silent_passes += 1
                    self._add_anti_pattern("silent_passes", f"{filepath}:{node.lineno}")

            # Exception chains
            elif isinstance(node, ast.Raise) and node.cause is not None:
                self.metrics.exception_chains += 1

            # Context managers
            elif isinstance(node, ast.With | ast.AsyncWith):
                self.metrics.context_managers += 1

            # Global variables
            elif isinstance(node, ast.Global):
                self.metrics.global_vars += len(node.names)
                self._add_anti_pattern("global_vars", f"{filepath}")

    def _analyze_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, lines: list[str], filepath: str
    ) -> None:
        """Analyze a function node."""
        # Determine if method or function
        is_method = node.args.args and node.args.args[0].arg in ("self", "cls")

        if is_method:
            self.metrics.methods += 1
        else:
            self.metrics.functions += 1

        # Calculate LOC
        start = node.lineno - 1
        end = node.end_lineno or start + 1
        func_lines = end - start

        # Categorize by size
        if func_lines < 10:
            self.metrics.small_funcs += 1
        elif func_lines < 30:
            self.metrics.medium_funcs += 1
        elif func_lines < 50:
            self.metrics.large_funcs += 1
        else:
            self.metrics.giant_funcs += 1
            self._add_anti_pattern(
                "giant_functions", f"{filepath}:{node.lineno} ({node.name}: {func_lines} LOC)"
            )

        # Type hints
        has_return = node.returns is not None
        if has_return:
            self.metrics.typed_functions += 1

        param_count = len(node.args.args)
        typed_count = sum(1 for arg in node.args.args if arg.annotation)

        self.metrics.total_params += param_count
        self.metrics.typed_params += typed_count

        # Docstring
        has_doc = self._has_docstring(node)
        if has_doc:
            self.metrics.documented_funcs += 1

        # Complexity
        complexity = self._calculate_complexity(node)
        self.metrics.max_complexity = max(self.metrics.max_complexity, complexity)
        if complexity > 10:
            self.metrics.high_complexity_funcs += 1
            self._add_anti_pattern(
                "high_complexity", f"{filepath}:{node.lineno} ({node.name}: {complexity})"
            )

        # Check for mutable defaults
        for default in node.args.defaults + node.args.kw_defaults:
            if isinstance(default, ast.List | ast.Dict | ast.Set):
                self.metrics.mutable_defaults += 1
                self._add_anti_pattern("mutable_defaults", f"{filepath}:{node.lineno}")

        # Store function details
        self.metrics.function_details.append(
            FunctionInfo(
                name=node.name,
                loc=func_lines,
                complexity=complexity,
                has_return_type=has_return,
                has_docstring=has_doc,
                param_count=param_count,
                typed_params=typed_count,
            )
        )

    def _has_docstring(self, node: ast.AST) -> bool:
        """Check if node has a docstring."""
        if not hasattr(node, "body") or not node.body:
            return False
        first = node.body[0]
        return (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )

    def _calculate_complexity(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, ast.If | ast.While | ast.For | ast.AsyncFor):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1 + len(child.ifs)
            elif isinstance(child, ast.Match):
                complexity += len(child.cases)
        return complexity

    def _check_magic_numbers(self, content: str, filepath: str) -> None:
        """Check for magic numbers in code."""
        for match in self.MAGIC_PATTERN.finditer(content):
            try:
                num = int(match.group())
                if num not in self.ALLOWED_NUMBERS and num > 2:
                    self.metrics.magic_numbers += 1
            except ValueError:
                pass

    def _add_anti_pattern(self, category: str, location: str) -> None:
        """Record an anti-pattern occurrence."""
        if category not in self.metrics.anti_patterns_detail:
            self.metrics.anti_patterns_detail[category] = []
        self.metrics.anti_patterns_detail[category].append(location)

    def _analyze_typescript(self) -> None:
        """Analyze TypeScript files with comprehensive metrics."""
        for ts_file in self.project_dir.rglob("*.ts"):
            if self._should_skip(ts_file):
                continue
            if ts_file.suffix == ".d.ts":
                continue

            try:
                content = ts_file.read_text(encoding="utf-8")
                self._analyze_typescript_file(ts_file, content)
            except Exception:
                pass

        # Also analyze .tsx files
        for tsx_file in self.project_dir.rglob("*.tsx"):
            if self._should_skip(tsx_file):
                continue
            try:
                content = tsx_file.read_text(encoding="utf-8")
                self._analyze_typescript_file(tsx_file, content)
            except Exception:
                pass

    def _analyze_typescript_file(self, path: Path, content: str) -> None:
        """Analyze a single TypeScript file with detailed metrics."""
        lines = content.splitlines()
        loc = len(lines)
        filepath = str(path)

        # Count LOC
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))

        is_test = ".test." in path.name or ".spec." in path.name
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc
            # Count test cases
            self.metrics.test_count += len(re.findall(r"\b(?:it|test|describe)\s*\(", content))

        # --- Function Analysis ---
        # Match function declarations, arrow functions, and methods
        func_patterns = [
            # Named functions: function name(
            r"function\s+(\w+)\s*\([^)]*\)",
            # Arrow functions with name: const name = (...) =>
            r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*(?::\s*[^=]+)?\s*=>",
            # Methods in class/object: name(
            r"^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{",
            # Arrow function methods: name: (...) =>
            r"(\w+)\s*:\s*(?:async\s*)?\([^)]*\)\s*=>",
        ]

        functions_found: list[tuple[str, int, int]] = []  # (name, start_line, loc)

        for i, line in enumerate(lines, 1):
            for pattern in func_patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(1)
                    # Estimate function size by finding closing brace
                    func_loc = self._estimate_ts_function_loc(lines, i - 1)
                    functions_found.append((func_name, i, func_loc))
                    break

        # Update metrics
        self.metrics.functions += len(functions_found)

        for func_name, start_line, func_loc in functions_found:
            # Categorize by size
            if func_loc < 10:
                self.metrics.small_funcs += 1
            elif func_loc < 30:
                self.metrics.medium_funcs += 1
            elif func_loc < 50:
                self.metrics.large_funcs += 1
            else:
                self.metrics.giant_funcs += 1
                self._add_anti_pattern(
                    "giant_functions", f"{filepath}:{start_line} ({func_name}: {func_loc} LOC)"
                )

            # Store function details for score calculation
            self.metrics.function_details.append(
                FunctionInfo(
                    name=func_name,
                    loc=func_loc,
                    complexity=1,  # Basic estimate
                    has_return_type=True,  # TypeScript usually has return types
                    has_docstring=False,  # Check below
                    param_count=0,
                    typed_params=0,
                )
            )

        # --- Type Safety Analysis ---
        # Count 'any' usage (anti-pattern in strict TS)
        any_count = len(re.findall(r":\s*any\b|<any>|as\s+any", content))
        if any_count > 0:
            self.metrics.magic_numbers += any_count  # Reuse as type safety penalty
            self._add_anti_pattern("any_usage", f"{filepath}: {any_count} 'any' types")

        # Count explicit type annotations (good practice)
        type_annotations = len(re.findall(r":\s*(?!any\b)\w+[\[\]<>|&,\s\w]*(?=[=,\)])", content))
        self.metrics.typed_params += type_annotations
        self.metrics.total_params += type_annotations + any_count

        # Return type annotations
        return_types = len(
            re.findall(r"\)\s*:\s*(?!void\b)\w+[\[\]<>|&,\s\w]*\s*(?=[{=>])", content)
        )
        self.metrics.typed_functions += return_types

        # --- Best Practices ---
        # Check for enums
        enum_count = len(re.findall(r"\benum\s+\w+", content))
        self.metrics.enums_used += enum_count

        # Check for interfaces/types (good for type safety)
        interface_count = len(re.findall(r"\b(?:interface|type)\s+\w+", content))
        self.metrics.classes += interface_count  # Count as "classes" for structure

        # Check for readonly (immutability)
        readonly_count = len(re.findall(r"\breadonly\b", content))
        self.metrics.dataclasses_used += min(readonly_count, 5)  # Bonus for immutability

        # --- Anti-patterns ---
        # eslint-disable comments
        eslint_disable = len(re.findall(r"eslint-disable|@ts-ignore|@ts-nocheck", content))
        if eslint_disable > 0:
            self.metrics.star_imports += eslint_disable
            self._add_anti_pattern("lint_disable", f"{filepath}: {eslint_disable} lint disables")

        # console.log in non-test files
        if not is_test:
            console_logs = len(re.findall(r"\bconsole\.(log|warn|error)\b", content))
            if console_logs > 3:
                self._add_anti_pattern(
                    "console_logs", f"{filepath}: {console_logs} console statements"
                )

        # --- Documentation ---
        # JSDoc/TSDoc comments
        jsdoc_count = len(re.findall(r"/\*\*[\s\S]*?\*/", content))
        self.metrics.documented_funcs += jsdoc_count

        # --- Error Handling ---
        # try-catch blocks
        try_catch = len(re.findall(r"\btry\s*\{", content))
        self.metrics.context_managers += try_catch

        # throw statements with Error
        throws = len(re.findall(r"\bthrow\s+new\s+\w*Error", content))
        self.metrics.exception_chains += throws

        # Bare catch (catch without type)
        bare_catch = len(re.findall(r"\bcatch\s*\(\s*\w+\s*\)\s*\{", content))
        if bare_catch > 0:
            self.metrics.broad_excepts += bare_catch

        # Empty catch blocks
        empty_catch = len(re.findall(r"\bcatch\s*\([^)]*\)\s*\{\s*\}", content))
        if empty_catch > 0:
            self.metrics.silent_passes += empty_catch
            self._add_anti_pattern("empty_catch", f"{filepath}: {empty_catch} empty catch blocks")

    def _estimate_ts_function_loc(self, lines: list[str], start_idx: int) -> int:
        """Estimate function length by counting lines until brace balance returns to 0."""
        brace_count = 0
        started = False
        loc = 0

        for i in range(start_idx, min(start_idx + 200, len(lines))):
            line = lines[i]
            loc += 1

            # Count braces (simplified, doesn't handle strings/comments)
            open_braces = line.count("{")
            close_braces = line.count("}")

            if open_braces > 0:
                started = True

            brace_count += open_braces - close_braces

            if started and brace_count <= 0:
                return loc

        return min(loc, 50)  # Cap at 50 if we can't find the end

    def _analyze_go(self) -> None:
        """Analyze Go files with comprehensive metrics."""
        for go_file in self.project_dir.rglob("*.go"):
            if self._should_skip(go_file):
                continue

            try:
                content = go_file.read_text(encoding="utf-8")
                self._analyze_go_file(go_file, content)
            except Exception:
                pass

    def _analyze_go_file(self, path: Path, content: str) -> None:
        """Analyze a single Go file with detailed metrics."""
        lines = content.splitlines()
        loc = len(lines)
        filepath = str(path)

        # Count LOC
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))

        is_test = "_test.go" in path.name
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc
            # Count test functions
            self.metrics.test_count += len(re.findall(r"func\s+Test\w+", content))

        # --- Function Analysis ---
        # Match func declarations: func Name( or func (r *Type) Name(
        func_pattern = r"func\s+(?:\([^)]+\)\s+)?(\w+)\s*\("
        functions_found: list[tuple[str, int, int]] = []

        for i, line in enumerate(lines, 1):
            match = re.search(func_pattern, line)
            if match:
                func_name = match.group(1)
                func_loc = self._estimate_go_function_loc(lines, i - 1)
                functions_found.append((func_name, i, func_loc))

        self.metrics.functions += len(functions_found)

        for func_name, start_line, func_loc in functions_found:
            # Categorize by size
            if func_loc < 10:
                self.metrics.small_funcs += 1
            elif func_loc < 30:
                self.metrics.medium_funcs += 1
            elif func_loc < 50:
                self.metrics.large_funcs += 1
            else:
                self.metrics.giant_funcs += 1
                self._add_anti_pattern(
                    "giant_functions", f"{filepath}:{start_line} ({func_name}: {func_loc} LOC)"
                )

            # Store function details
            self.metrics.function_details.append(
                FunctionInfo(
                    name=func_name,
                    loc=func_loc,
                    complexity=1,
                    has_return_type=True,  # Go always has explicit returns
                    has_docstring=False,
                    param_count=0,
                    typed_params=0,
                )
            )

        # --- Type Safety Analysis ---
        # Go is statically typed, count interface{} usage (like any)
        interface_any = len(re.findall(r"\binterface\s*\{\s*\}|any\b", content))
        if interface_any > 0:
            self.metrics.magic_numbers += interface_any
            self._add_anti_pattern(
                "interface_any", f"{filepath}: {interface_any} interface{{}}/any"
            )

        # Count struct definitions (good structure)
        struct_count = len(re.findall(r"\btype\s+\w+\s+struct\b", content))
        self.metrics.classes += struct_count

        # Count interface definitions
        iface_count = len(re.findall(r"\btype\s+\w+\s+interface\b", content))
        self.metrics.classes += iface_count

        # All params are typed in Go
        param_annotations = len(
            re.findall(r"\w+\s+\w+(?:\.\w+)?(?:\s*,\s*\w+\s+\w+)*\s*\)", content)
        )
        self.metrics.typed_params += param_annotations
        self.metrics.total_params += param_annotations

        # --- Best Practices ---
        # Check for const blocks
        const_count = len(re.findall(r"\bconst\s*\(", content))
        self.metrics.dataclasses_used += min(const_count, 3)

        # Check for iota (enum-like)
        iota_count = len(re.findall(r"\biota\b", content))
        self.metrics.enums_used += min(iota_count, 3)

        # --- Error Handling ---
        # Go error handling: if err != nil
        error_checks = len(re.findall(r"if\s+err\s*!=\s*nil", content))
        self.metrics.context_managers += error_checks

        # Error wrapping: fmt.Errorf with %w
        error_wraps = len(re.findall(r"fmt\.Errorf\([^)]*%w", content))
        self.metrics.exception_chains += error_wraps

        # errors.New usage
        error_new = len(re.findall(r"errors\.New\(", content))
        self.metrics.exception_chains += error_new

        # Ignoring errors: _ = funcThatReturnsError()
        ignored_errors = len(re.findall(r"_\s*,?\s*=\s*\w+\(", content))
        if ignored_errors > 3:
            self._add_anti_pattern("ignored_errors", f"{filepath}: potential ignored errors")

        # --- Documentation ---
        # Go doc comments (// FuncName ...)
        doc_comments = len(re.findall(r"//\s*\w+\s+", content))
        self.metrics.documented_funcs += min(doc_comments // 2, len(functions_found))

        # --- Anti-patterns ---
        # panic usage (should be avoided in libraries)
        panic_count = len(re.findall(r"\bpanic\s*\(", content))
        if panic_count > 0 and not is_test:
            self.metrics.bare_excepts += panic_count
            self._add_anti_pattern("panic_usage", f"{filepath}: {panic_count} panic calls")

        # defer without error handling
        defer_count = len(re.findall(r"\bdefer\s+", content))
        self.metrics.context_managers += defer_count

    def _estimate_go_function_loc(self, lines: list[str], start_idx: int) -> int:
        """Estimate function length by counting lines until brace balance returns to 0."""
        brace_count = 0
        started = False
        loc = 0

        for i in range(start_idx, min(start_idx + 200, len(lines))):
            line = lines[i]
            loc += 1

            open_braces = line.count("{")
            close_braces = line.count("}")

            if open_braces > 0:
                started = True

            brace_count += open_braces - close_braces

            if started and brace_count <= 0:
                return loc

        return min(loc, 50)

    # ==================== TIER 2: Extended Analysis ====================

    def _analyze_rust(self) -> None:
        """Analyze Rust files."""
        for rs_file in self.project_dir.rglob("*.rs"):
            if self._should_skip(rs_file):
                continue
            try:
                content = rs_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(rs_file, content, "rust")
            except Exception:
                pass

    def _analyze_java(self) -> None:
        """Analyze Java files."""
        for java_file in self.project_dir.rglob("*.java"):
            if self._should_skip(java_file):
                continue
            try:
                content = java_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(java_file, content, "java")
            except Exception:
                pass

    def _analyze_csharp(self) -> None:
        """Analyze C# files."""
        for cs_file in self.project_dir.rglob("*.cs"):
            if self._should_skip(cs_file):
                continue
            try:
                content = cs_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(cs_file, content, "csharp")
            except Exception:
                pass

    def _analyze_ruby(self) -> None:
        """Analyze Ruby files."""
        for rb_file in self.project_dir.rglob("*.rb"):
            if self._should_skip(rb_file):
                continue
            try:
                content = rb_file.read_text(encoding="utf-8")
                self._analyze_ruby_file(rb_file, content)
            except Exception:
                pass

    def _analyze_php(self) -> None:
        """Analyze PHP files."""
        for php_file in self.project_dir.rglob("*.php"):
            if self._should_skip(php_file):
                continue
            try:
                content = php_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(php_file, content, "php")
            except Exception:
                pass

    def _analyze_swift(self) -> None:
        """Analyze Swift files."""
        for swift_file in self.project_dir.rglob("*.swift"):
            if self._should_skip(swift_file):
                continue
            try:
                content = swift_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(swift_file, content, "swift")
            except Exception:
                pass

    def _analyze_kotlin(self) -> None:
        """Analyze Kotlin files."""
        for kt_file in self.project_dir.rglob("*.kt"):
            if self._should_skip(kt_file):
                continue
            try:
                content = kt_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(kt_file, content, "kotlin")
            except Exception:
                pass
        for kts_file in self.project_dir.rglob("*.kts"):
            if self._should_skip(kts_file):
                continue
            try:
                content = kts_file.read_text(encoding="utf-8")
                self._analyze_curly_brace_lang(kts_file, content, "kotlin")
            except Exception:
                pass

    def _analyze_curly_brace_lang(self, path: Path, content: str, lang: str) -> None:
        """Generic analyzer for curly-brace languages (Rust, Java, C#, PHP, Swift, Kotlin)."""
        lines = content.splitlines()
        loc = len(lines)
        filepath = str(path)

        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))

        is_test = self._is_test_file(path, lang)
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc

        # Function detection patterns by language
        func_patterns = {
            "rust": r"(?:pub\s+)?(?:async\s+)?fn\s+(\w+)",
            "java": r"(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*(?:throws\s+\w+)?\s*\{",
            "csharp": r"(?:public|private|protected|internal)?\s*(?:static\s+)?(?:async\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{",
            "php": r"(?:public|private|protected)?\s*(?:static\s+)?function\s+(\w+)",
            "swift": r"(?:public\s+|private\s+|internal\s+)?func\s+(\w+)",
            "kotlin": r"(?:fun|suspend\s+fun)\s+(\w+)",
        }

        pattern = func_patterns.get(lang, r"(?:fn|func|function|def)\s+(\w+)")
        functions_found: list[tuple[str, int, int]] = []

        for i, line in enumerate(lines, 1):
            match = re.search(pattern, line)
            if match:
                func_name = match.group(1)
                func_loc = self._estimate_brace_function_loc(lines, i - 1)
                functions_found.append((func_name, i, func_loc))

        self.metrics.functions += len(functions_found)

        for func_name, start_line, func_loc in functions_found:
            if func_loc < 10:
                self.metrics.small_funcs += 1
            elif func_loc < 30:
                self.metrics.medium_funcs += 1
            elif func_loc < 50:
                self.metrics.large_funcs += 1
            else:
                self.metrics.giant_funcs += 1
                self._add_anti_pattern(
                    "giant_functions", f"{filepath}:{start_line} ({func_name}: {func_loc} LOC)"
                )

            self.metrics.function_details.append(
                FunctionInfo(
                    name=func_name,
                    loc=func_loc,
                    complexity=1,
                    has_return_type=True,
                    has_docstring=False,
                    param_count=0,
                    typed_params=0,
                )
            )

        # Language-specific anti-patterns and best practices
        self._check_lang_specific(content, filepath, lang, is_test)

        # Test counting
        if is_test:
            test_patterns = {
                "rust": r"#\[test\]|#\[tokio::test\]",
                "java": r"@Test|@ParameterizedTest",
                "csharp": r"\[Test\]|\[Fact\]|\[Theory\]",
                "php": r"function\s+test\w+|@test",
                "swift": r"func\s+test\w+",
                "kotlin": r"@Test|fun\s+`[^`]+`",
            }
            test_pattern = test_patterns.get(lang, r"test|spec")
            self.metrics.test_count += len(re.findall(test_pattern, content, re.IGNORECASE))

    def _check_lang_specific(self, content: str, filepath: str, lang: str, is_test: bool) -> None:
        """Check language-specific patterns and anti-patterns."""
        # Unsafe/dangerous patterns
        unsafe_patterns: dict[str, list[tuple[str, str, int]]] = {
            "rust": [(r"\bunsafe\s*\{", "unsafe_block", 0)],
            "java": [(r"\bsuppresswarnings\b", "suppress_warnings", re.IGNORECASE)],
            "csharp": [(r"\bunsafe\s*\{", "unsafe_block", 0)],
            "php": [(r"\beval\s*\(", "eval_usage", 0), (r"\$\$\w+", "variable_variable", 0)],
            "swift": [(r"force\s*!", "force_unwrap", 0)],
            "kotlin": [(r"!!", "force_unwrap", 0)],
        }

        for pattern, name, flags in unsafe_patterns.get(lang, []):
            count = len(re.findall(pattern, content, flags))
            if count > 0 and not is_test:
                self._add_anti_pattern(name, f"{filepath}: {count} occurrences")

        # Type escape patterns (like 'any' in TypeScript)
        type_escape = {
            "rust": r"dyn\s+Any",
            "java": r"\bObject\b(?!\s*\.\s*class)",
            "csharp": r"\bdynamic\b|\bobject\b",
            "php": r"\bmixed\b",
            "swift": r"\bAny\b",
            "kotlin": r"\bAny\??\b",
        }
        if lang in type_escape:
            count = len(re.findall(type_escape[lang], content))
            if count > 3:
                self._add_anti_pattern("type_escape", f"{filepath}: {count} type escapes")
                self.metrics.magic_numbers += count

        # Documentation comments
        doc_patterns = {
            "rust": r"///|//!|/\*\*",
            "java": r"/\*\*[\s\S]*?\*/",
            "csharp": r"///|/\*\*[\s\S]*?\*/",
            "php": r"/\*\*[\s\S]*?\*/",
            "swift": r"///|/\*\*[\s\S]*?\*/",
            "kotlin": r"/\*\*[\s\S]*?\*/|//",
        }
        if lang in doc_patterns:
            doc_count = len(re.findall(doc_patterns[lang], content))
            self.metrics.documented_funcs += min(doc_count, len(content) // 500)

        # Error handling
        error_patterns = {
            "rust": (r"\?|\.unwrap\(\)|\.expect\(", r"\.unwrap\(\)|\.expect\("),
            "java": (r"\btry\s*\{", r"\bcatch\s*\(\s*Exception\s"),
            "csharp": (r"\btry\s*\{", r"\bcatch\s*\(\s*Exception\s"),
            "php": (r"\btry\s*\{", r"\bcatch\s*\(\s*\\?Exception\s"),
            "swift": (r"\bdo\s*\{|\btry\b", r"\bcatch\s*\{"),
            "kotlin": (r"\btry\s*\{", r"\bcatch\s*\(\s*e:\s*Exception"),
        }
        if lang in error_patterns:
            good_pattern, bad_pattern = error_patterns[lang]
            good_count = len(re.findall(good_pattern, content))
            bad_count = len(re.findall(bad_pattern, content))
            self.metrics.context_managers += good_count
            if bad_count > 0:
                self.metrics.broad_excepts += bad_count

    def _analyze_ruby_file(self, path: Path, content: str) -> None:
        """Analyze Ruby file (uses 'end' instead of braces)."""
        lines = content.splitlines()
        loc = len(lines)
        filepath = str(path)

        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

        is_test = self._is_test_file(path, "ruby")
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc

        # Ruby function detection
        func_pattern = r"def\s+(\w+[\?!=]?)"
        functions_found: list[tuple[str, int, int]] = []

        for i, line in enumerate(lines, 1):
            match = re.search(func_pattern, line)
            if match:
                func_name = match.group(1)
                func_loc = self._estimate_ruby_function_loc(lines, i - 1)
                functions_found.append((func_name, i, func_loc))

        self.metrics.functions += len(functions_found)

        for func_name, start_line, func_loc in functions_found:
            if func_loc < 10:
                self.metrics.small_funcs += 1
            elif func_loc < 30:
                self.metrics.medium_funcs += 1
            elif func_loc < 50:
                self.metrics.large_funcs += 1
            else:
                self.metrics.giant_funcs += 1
                self._add_anti_pattern(
                    "giant_functions", f"{filepath}:{start_line} ({func_name}: {func_loc} LOC)"
                )

            self.metrics.function_details.append(
                FunctionInfo(
                    name=func_name,
                    loc=func_loc,
                    complexity=1,
                    has_return_type=False,
                    has_docstring=False,
                    param_count=0,
                    typed_params=0,
                )
            )

        # Class/module detection
        class_count = len(re.findall(r"\bclass\s+\w+|\bmodule\s+\w+", content))
        self.metrics.classes += class_count

        # Ruby anti-patterns
        eval_count = len(re.findall(r"\beval\s*\(|\binstance_eval\b|\bclass_eval\b", content))
        if eval_count > 0 and not is_test:
            self._add_anti_pattern("eval_usage", f"{filepath}: {eval_count} eval calls")

        # Test counting
        if is_test:
            self.metrics.test_count += len(
                re.findall(r"\b(?:it|describe|context|test)\s+['\"]", content)
            )

    def _estimate_ruby_function_loc(self, lines: list[str], start_idx: int) -> int:
        """Estimate Ruby function length by counting to matching 'end'."""
        depth = 0
        started = False
        loc = 0

        for i in range(start_idx, min(start_idx + 200, len(lines))):
            line = lines[i].strip()
            loc += 1

            # Count block starters
            if re.search(r"\b(def|class|module|do|if|unless|case|while|until|for|begin)\b", line):
                depth += 1
                started = True

            # Count block enders
            if re.search(r"\bend\b", line):
                depth -= 1

            if started and depth <= 0:
                return loc

        return min(loc, 50)

    def _estimate_brace_function_loc(self, lines: list[str], start_idx: int) -> int:
        """Estimate function length for curly-brace languages."""
        brace_count = 0
        started = False
        loc = 0

        for i in range(start_idx, min(start_idx + 200, len(lines))):
            line = lines[i]
            loc += 1

            open_braces = line.count("{")
            close_braces = line.count("}")

            if open_braces > 0:
                started = True

            brace_count += open_braces - close_braces

            if started and brace_count <= 0:
                return loc

        return min(loc, 50)

    # ==================== TIER 3+: Generic Analysis ====================

    def _analyze_other_languages(self) -> None:
        """Analyze all other supported languages with generic patterns."""
        analyzed_extensions = {
            ".py",
            ".ts",
            ".tsx",
            ".go",
            ".rs",
            ".java",
            ".cs",
            ".rb",
            ".php",
            ".swift",
            ".kt",
            ".kts",
        }

        for ext, lang in self.LANGUAGE_EXTENSIONS.items():
            if ext in analyzed_extensions:
                continue

            for file_path in self.project_dir.rglob(f"*{ext}"):
                if self._should_skip(file_path):
                    continue
                try:
                    content = file_path.read_text(encoding="utf-8")
                    self._analyze_generic_file(file_path, content, lang)
                except Exception:
                    pass

    def _analyze_generic_file(self, path: Path, content: str, lang: str) -> None:
        """Generic file analysis for any language."""
        lines = content.splitlines()
        loc = len(lines)
        filepath = str(path)

        # Comment patterns by language family
        comment_starts = {
            "c": "//",
            "cpp": "//",
            "javascript": "//",
            "haskell": "--",
            "lua": "--",
            "elm": "--",
            "python": "#",
            "ruby": "#",
            "perl": "#",
            "r": "#",
            "julia": "#",
            "shell": "#",
            "clojure": ";",
            "lisp": ";",
            "scheme": ";",
            "erlang": "%",
            "elixir": "#",
        }
        comment_start = comment_starts.get(lang, "//")

        code_lines = sum(
            1 for line in lines if line.strip() and not line.strip().startswith(comment_start)
        )

        is_test = self._is_test_file(path, lang)
        self.metrics.total_loc += loc
        self.metrics.code_loc += code_lines
        if is_test:
            self.metrics.test_loc += loc

        # Generic function detection
        func_patterns = [
            r"\bfn\s+(\w+)",  # Rust, Zig
            r"\bfunc\s+(\w+)",  # Go, Swift
            r"\bfunction\s+(\w+)",  # JS, PHP, Lua
            r"\bdef\s+(\w+)",  # Python, Ruby, Elixir
            r"\blet\s+(\w+)\s*=",  # Haskell, OCaml, F#
            r"\b(\w+)\s*::\s*",  # Haskell type signatures
            r"defn?\s+(\w+)",  # Clojure
            r"\bsub\s+(\w+)",  # Perl
        ]

        functions_found = 0
        for pattern in func_patterns:
            functions_found += len(re.findall(pattern, content))

        self.metrics.functions += functions_found

        # Universal anti-patterns
        self._check_universal_anti_patterns(content, filepath, is_test)

        # Test detection
        if is_test:
            test_keywords = r"\btest\b|\bspec\b|\bdescribe\b|\bit\s*\(|\bexpect\b|\bassert"
            self.metrics.test_count += len(re.findall(test_keywords, content, re.IGNORECASE))

    def _check_universal_anti_patterns(self, content: str, filepath: str, is_test: bool) -> None:
        """Check for universal anti-patterns across all languages."""
        # TODO/FIXME comments (technical debt)
        todo_count = len(re.findall(r"\b(TODO|FIXME|HACK|XXX)\b", content, re.IGNORECASE))
        if todo_count > 5:
            self._add_anti_pattern("tech_debt", f"{filepath}: {todo_count} TODO/FIXME comments")

        # Hardcoded secrets (critical security)
        secret_patterns = [
            r'(?:password|passwd|pwd|secret|api_key|apikey|token)\s*[=:]\s*["\'][^"\']{8,}["\']',
            r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----",
            r"(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{20,}",
        ]
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self._add_anti_pattern(
                    "hardcoded_secret", f"{filepath}: potential hardcoded secret"
                )
                break

        # Very long lines (readability)
        long_lines = sum(1 for line in content.splitlines() if len(line) > 200)
        if long_lines > 10:
            self._add_anti_pattern("long_lines", f"{filepath}: {long_lines} lines >200 chars")

        # Deeply nested code (complexity indicator)
        max_indent = 0
        for line in content.splitlines():
            if line.strip():
                indent = len(line) - len(line.lstrip())
                spaces_per_level = 2 if "  " in line[:indent] else 4
                level = indent // spaces_per_level if spaces_per_level else 0
                max_indent = max(max_indent, level)

        if max_indent > 6:
            self._add_anti_pattern("deep_nesting", f"{filepath}: nesting depth {max_indent}")

        # Commented-out code (cleanup needed)
        commented_code_patterns = [
            r"//\s*(if|for|while|return|function|def|class)\s",
            r"#\s*(if|for|while|return|def|class)\s",
        ]
        commented_code = 0
        for pattern in commented_code_patterns:
            commented_code += len(re.findall(pattern, content))
        if commented_code > 5:
            self._add_anti_pattern(
                "commented_code", f"{filepath}: {commented_code} commented code blocks"
            )

    def _calculate_scores(self) -> None:
        """Calculate UX/DX scores."""
        total_funcs = self.metrics.functions + self.metrics.methods

        # Type coverage
        if self.metrics.total_params > 0:
            self.metrics.type_coverage_pct = (
                self.metrics.typed_params / self.metrics.total_params * 100
            )

        # Docstring coverage
        if total_funcs > 0:
            self.metrics.docstring_coverage_pct = self.metrics.documented_funcs / total_funcs * 100

        # Average complexity
        if self.metrics.function_details:
            complexities = [f.complexity for f in self.metrics.function_details]
            self.metrics.avg_complexity = sum(complexities) / len(complexities)

        # Modularity score (penalize giant functions with cap)
        if total_funcs > 0:
            small_ratio = self.metrics.small_funcs / total_funcs
            # Cap giant penalty at 40 - even many giants shouldn't zero the score
            giant_penalty = min(self.metrics.giant_funcs * 6, 40)
            self.metrics.modularity_score = max(
                0,
                min(
                    100,
                    small_ratio * 60
                    + (self.metrics.medium_funcs / total_funcs) * 30
                    + (self.metrics.large_funcs / total_funcs) * 10
                    - giant_penalty,
                ),
            )

        # SRP score (based on function sizes and complexity)
        if total_funcs > 0:
            avg_loc = (
                sum(f.loc for f in self.metrics.function_details) / total_funcs
                if self.metrics.function_details
                else 0
            )
            # Cap complexity penalty at 30
            complexity_penalty = min(self.metrics.high_complexity_funcs * 4, 30)
            # Cap avg_loc penalty at 40 (reached at avg 40 LOC)
            avg_loc_penalty = min(max(0, avg_loc - 20) * 2, 40)
            self.metrics.srp_score = max(0, min(100, 100 - avg_loc_penalty - complexity_penalty))

        # Naming score (basic heuristic based on function name length)
        if self.metrics.function_details:
            good_names = sum(
                1
                for f in self.metrics.function_details
                if 3 <= len(f.name) <= 30 and not f.name.startswith("_")
            )
            self.metrics.naming_score = good_names / len(self.metrics.function_details) * 100

        # Error handling score
        total_handlers = (
            self.metrics.bare_excepts + self.metrics.broad_excepts + self.metrics.exception_chains
        )
        if total_handlers > 0:
            good_handling = self.metrics.exception_chains
            bad_handling = self.metrics.bare_excepts + self.metrics.silent_passes
            # Cap bad handling penalty at 40
            bad_penalty = min(bad_handling * 8, 40)
            self.metrics.error_handling_score = max(
                0, min(100, (good_handling / total_handlers) * 100 - bad_penalty)
            )
        else:
            self.metrics.error_handling_score = 50  # Neutral if no exception handling

    def _run_tests(self) -> None:
        """Try to run tests and get coverage."""
        # Look for Python tests
        if self.metrics.python_files > 0:
            self._run_python_tests()
        elif self.metrics.typescript_files > 0:
            self._run_typescript_tests()
        elif self.metrics.go_files > 0:
            self._run_go_tests()

    def _run_python_tests(self) -> None:
        """Run Python tests with coverage."""
        try:
            # Check for pyproject.toml or setup.py
            has_setup = (self.project_dir / "pyproject.toml").exists() or (
                self.project_dir / "setup.py"
            ).exists()

            if has_setup:
                # Install
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", ".[dev]", "-q"],
                    cwd=self.project_dir,
                    capture_output=True,
                    timeout=120,
                )

            # Run tests
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "--tb=no",
                    "-q",
                    f"--cov={self.project_dir}",
                    "--cov-report=term",
                ],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300,
                encoding="utf-8",
                errors="replace",
            )

            self.metrics.tests_passed = result.returncode == 0

            # Extract coverage
            for line in result.stdout.splitlines():
                if "TOTAL" in line and "%" in line:
                    for part in line.split():
                        if "%" in part:
                            try:
                                self.metrics.coverage_pct = float(part.rstrip("%"))
                            except ValueError:
                                pass
                            break

            # Count test functions
            self.metrics.test_count = len(re.findall(r"(?:passed|failed|error)", result.stdout))
        except Exception:
            pass

    def _run_typescript_tests(self) -> None:
        """Run TypeScript tests."""
        try:
            # npm test
            result = subprocess.run(
                ["npm", "test", "--", "--passWithNoTests"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300,
                encoding="utf-8",
                errors="replace",
            )
            self.metrics.tests_passed = result.returncode == 0
        except Exception:
            pass

    def _run_go_tests(self) -> None:
        """Run Go tests."""
        try:
            result = subprocess.run(
                ["go", "test", "-v", "-cover", "./..."],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300,
                encoding="utf-8",
                errors="replace",
            )
            self.metrics.tests_passed = result.returncode == 0

            # Extract coverage
            for line in result.stdout.splitlines():
                if "coverage:" in line:
                    match = re.search(r"(\d+\.?\d*)%", line)
                    if match:
                        self.metrics.coverage_pct = float(match.group(1))
                        break
        except Exception:
            pass

    # =========================================================================
    # 6-DIMENSION ANALYZERS
    # =========================================================================

    def _analyze_functional_completeness(self) -> DimensionScore:
        """Analyze if code meets functional requirements.

        Production-grade scoring philosophy:
        - Measure whether the code appears complete and functional
        - Entry points, error handling, and structure matter
        - Code quantity indicates implementation depth
        - Range: 0 (empty) to 100 (fully featured)
        """
        score = 45.0
        details = []
        issues = []
        positives = []

        # Check if there's any code
        total_code_files = (
            self.metrics.python_files + self.metrics.typescript_files + self.metrics.go_files
        )

        if total_code_files == 0:
            return DimensionScore(
                name="Functional Completeness",
                score=0,
                weight=DIMENSION_WEIGHTS["functional_completeness"],
                details=["No source code found"],
                issues=["Project appears to be empty"],
            )

        details.append(f"{total_code_files} source files")

        # Check for entry points - essential for runnable code
        has_entry = self._check_entry_points()
        if has_entry:
            score += 15
            positives.append("Entry point found")
        else:
            score -= 5
            issues.append("No clear entry point")

        # Function/method count indicates implementation depth
        func_count = self.metrics.functions + self.metrics.methods
        if func_count >= 30:
            score += 18
            positives.append(f"{func_count} functions/methods (comprehensive)")
        elif func_count >= 15:
            score += 12
            positives.append(f"{func_count} functions/methods")
        elif func_count >= 8:
            score += 6
        elif func_count < 5:
            issues.append(f"Only {func_count} functions (minimal)")

        # Error handling shows production readiness
        error_handling_count = self.metrics.context_managers + self.metrics.exception_chains
        if error_handling_count >= 5:
            score += 12
            positives.append(f"Robust error handling ({error_handling_count} patterns)")
        elif error_handling_count > 0:
            score += 6
            positives.append("Error handling present")
        else:
            issues.append("No error handling patterns")

        # Classes indicate structured/OOP design (not always needed)
        if self.metrics.classes >= 5:
            score += 10
            positives.append(f"{self.metrics.classes} classes (well-structured)")
        elif self.metrics.classes >= 2:
            score += 5
            positives.append(f"{self.metrics.classes} classes")

        return DimensionScore(
            name="Functional Completeness",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["functional_completeness"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _check_entry_points(self) -> bool:
        """Check for common entry point patterns."""
        entry_patterns = [
            "main.py",
            "app.py",
            "index.ts",
            "index.js",
            "main.go",
            "server.py",
            "cli.py",
            "__main__.py",
            "main.rs",
            "Main.java",
        ]
        for f in self.project_dir.rglob("*"):
            if f.name in entry_patterns:
                return True
            # Check for if __name__ == "__main__"
            if f.suffix == ".py":
                try:
                    content = f.read_text(encoding="utf-8")
                    if '__name__ == "__main__"' in content or "__name__ == '__main__'" in content:
                        return True
                except Exception:
                    pass
        return False

    def _analyze_code_quality(self) -> DimensionScore:
        """Analyze code quality (complexity, patterns, style).

        Production-grade scoring philosophy:
        - Start neutral (50), let evidence move the score
        - All penalties have reasonable caps (real code has anti-patterns)
        - Penalize things that cause production issues, not style preferences
        - Giant functions are concerning but sometimes necessary (handlers, state machines)
        - Module-level constants (globals) are acceptable in moderation
        - Balance: max penalty ~35, max bonus ~50 → range 15-100
        """
        score = 50.0
        details = []
        issues = []
        positives = []

        # === Anti-pattern penalties (all capped for realism) ===

        # Bare excepts hide bugs and make debugging hard - HIGH severity
        if self.metrics.bare_excepts > 0:
            penalty = min(self.metrics.bare_excepts * 4, 12)
            score -= penalty
            issues.append(f"HIGH: {self.metrics.bare_excepts} bare except clauses")

        # Silent passes can hide errors but sometimes intentional - MEDIUM severity
        if self.metrics.silent_passes > 0:
            penalty = min(self.metrics.silent_passes * 2, 8)
            score -= penalty
            issues.append(f"MEDIUM: {self.metrics.silent_passes} silent passes")

        # Giant functions (>50 LOC) hurt maintainability but sometimes unavoidable
        # Cap at 18 points - even 6+ giant funcs shouldn't tank the score
        if self.metrics.giant_funcs > 0:
            penalty = min(self.metrics.giant_funcs * 3, 18)
            score -= penalty
            severity = "HIGH" if self.metrics.giant_funcs >= 5 else "MEDIUM"
            issues.append(f"{severity}: {self.metrics.giant_funcs} giant functions (>50 LOC)")

        # Magic numbers - only penalize excessive use (>20), cap at 8
        # Config values and test data often have legitimate magic numbers
        if self.metrics.magic_numbers > 20:
            penalty = min((self.metrics.magic_numbers - 20) // 5, 8)
            score -= penalty
            issues.append(f"LOW: {self.metrics.magic_numbers} magic numbers")

        # Mutable defaults are genuine bugs - but cap at 9
        if self.metrics.mutable_defaults > 0:
            penalty = min(self.metrics.mutable_defaults * 3, 9)
            score -= penalty
            issues.append(f"MEDIUM: {self.metrics.mutable_defaults} mutable defaults")

        # Star imports pollute namespace - LOW severity, cap at 6
        if self.metrics.star_imports > 0:
            penalty = min(self.metrics.star_imports * 2, 6)
            score -= penalty
            issues.append(f"LOW: {self.metrics.star_imports} star imports")

        # Global variables - module-level constants are OK, mutable globals are not
        # Only penalize after 5 (allow config constants), cap at 10
        if self.metrics.global_vars > 5:
            penalty = min((self.metrics.global_vars - 5) * 2, 10)
            score -= penalty
            issues.append(f"MEDIUM: {self.metrics.global_vars} global variables")

        # High complexity functions (cyclomatic >10) - cap at 12
        if self.metrics.high_complexity_funcs > 0:
            penalty = min(self.metrics.high_complexity_funcs * 2, 12)
            score -= penalty
            severity = "HIGH" if self.metrics.high_complexity_funcs >= 4 else "MEDIUM"
            issues.append(
                f"{severity}: {self.metrics.high_complexity_funcs} high-complexity functions"
            )

        # === Best practice bonuses (reward good patterns generously) ===

        # Exception chaining shows proper error handling
        if self.metrics.exception_chains > 0:
            bonus = min(self.metrics.exception_chains * 2, 12)
            score += bonus
            positives.append(f"Exception chaining ({self.metrics.exception_chains})")

        # Context managers ensure resource cleanup
        if self.metrics.context_managers > 0:
            bonus = min(self.metrics.context_managers, 12)
            score += bonus
            positives.append(f"Context managers ({self.metrics.context_managers})")

        # Dataclasses reduce boilerplate and add type safety
        if self.metrics.dataclasses_used > 0:
            bonus = min(self.metrics.dataclasses_used * 2, 10)
            score += bonus
            positives.append(f"Dataclasses used ({self.metrics.dataclasses_used})")

        # Enums improve type safety and readability
        if self.metrics.enums_used > 0:
            bonus = min(self.metrics.enums_used * 2, 8)
            score += bonus
            positives.append(f"Enums used ({self.metrics.enums_used})")

        # Pathlib is modern Python best practice
        if self.metrics.pathlib_used:
            score += 4
            positives.append("Pathlib used")

        # Function size distribution - use total callable count for accurate ratio
        total_callables = self.metrics.functions + self.metrics.methods
        if total_callables > 0:
            # small_funcs already counts both functions and methods
            small_ratio = self.metrics.small_funcs / total_callables
            if small_ratio >= 0.6:
                score += 8
                positives.append(f"Good function sizes ({small_ratio:.0%} small)")
            elif small_ratio >= 0.4:
                score += 4
                positives.append(f"Moderate function sizes ({small_ratio:.0%} small)")

        details.append(f"Language: {self.metrics.language}")
        details.append(f"LOC: {self.metrics.code_loc}")

        return DimensionScore(
            name="Code Quality",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["code_quality"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_security(self) -> DimensionScore:
        """Analyze security vulnerabilities."""
        score = 70.0
        details = []
        issues = []
        positives = []

        vulnerabilities = []

        # Scan all source files for security issues
        for f in self.project_dir.rglob("*"):
            if self._should_skip(f) or not f.is_file():
                continue
            suffix = f.suffix.lower()
            if suffix not in self.LANGUAGE_EXTENSIONS:
                continue

            try:
                content = f.read_text(encoding="utf-8")
                filepath = str(f.relative_to(self.project_dir))
                file_vulns = self._check_security_patterns(content, filepath)
                vulnerabilities.extend(file_vulns)
            except Exception:
                pass

        # Categorize and apply penalties
        critical = [v for v in vulnerabilities if v["severity"] == "critical"]
        high = [v for v in vulnerabilities if v["severity"] == "high"]
        medium = [v for v in vulnerabilities if v["severity"] == "medium"]
        low = [v for v in vulnerabilities if v["severity"] == "low"]

        score -= len(critical) * 25
        score -= len(high) * 15
        score -= len(medium) * 5
        score -= len(low) * 2

        for v in critical:
            issues.append(f"CRITICAL: {v['issue']} ({v['file']})")
        for v in high:
            issues.append(f"HIGH: {v['issue']} ({v['file']})")
        for v in medium:
            issues.append(f"MEDIUM: {v['issue']} ({v['file']})")
        for v in low[:5]:  # Limit low severity
            issues.append(f"LOW: {v['issue']} ({v['file']})")

        if not vulnerabilities:
            score += 10
            positives.append("No security vulnerabilities detected")

        details.append(f"Scanned {self.metrics.total_files} files")

        return DimensionScore(
            name="Security",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["security"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _check_security_patterns(self, content: str, filepath: str) -> list[dict[str, Any]]:
        """Check for security vulnerabilities in code."""
        vulns = []

        # Hardcoded secrets
        secret_patterns = [
            (
                r'(?:password|passwd|pwd)\s*[=:]\s*["\'][^"\']{4,}["\']',
                "Hardcoded password",
                "critical",
            ),
            (
                r'(?:api_?key|apikey|secret_?key)\s*[=:]\s*["\'][^"\']{8,}["\']',
                "Hardcoded API key",
                "critical",
            ),
            (
                r"-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
                "Private key in code",
                "critical",
            ),
        ]

        for pattern, issue, severity in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                vulns.append({"issue": issue, "file": filepath, "severity": severity})

        # SQL injection
        if re.search(r'execute\s*\(\s*["\'].*%s', content) or re.search(r'f".*SELECT.*\{', content):
            vulns.append({"issue": "Potential SQL injection", "file": filepath, "severity": "high"})

        # Command injection
        if re.search(r"shell\s*=\s*True", content) and re.search(r"subprocess", content):
            vulns.append(
                {"issue": "shell=True with subprocess", "file": filepath, "severity": "high"}
            )

        # Eval usage
        if re.search(r"\beval\s*\(", content):
            vulns.append({"issue": "eval() usage", "file": filepath, "severity": "high"})

        # Pickle with untrusted data
        if "pickle.load" in content:
            vulns.append(
                {
                    "issue": "pickle.load (unsafe deserialization)",
                    "file": filepath,
                    "severity": "medium",
                }
            )

        return vulns

    def _analyze_test_quality(self) -> DimensionScore:
        """Analyze test coverage and quality."""
        score = 30.0  # Start low
        details = []
        issues = []
        positives = []

        if self.metrics.test_files == 0:
            return DimensionScore(
                name="Test Quality",
                score=0,
                weight=DIMENSION_WEIGHTS["test_quality"],
                details=["No test files found"],
                issues=["No tests written"],
            )

        # Test file ratio
        total_source = (
            self.metrics.python_files
            + self.metrics.typescript_files
            + self.metrics.go_files
            - self.metrics.test_files
        )
        test_ratio = self.metrics.test_files / max(1, total_source)

        if test_ratio >= 0.5:
            score += 25
            positives.append(f"Good test coverage ({test_ratio:.0%} test/source ratio)")
        elif test_ratio >= 0.3:
            score += 15
            positives.append(f"Moderate test coverage ({test_ratio:.0%})")
        else:
            issues.append(f"Low test coverage ({test_ratio:.0%})")

        # Test LOC ratio
        if self.metrics.test_loc > 0 and self.metrics.code_loc > 0:
            loc_ratio = self.metrics.test_loc / self.metrics.code_loc
            if loc_ratio >= 0.5:
                score += 15
                positives.append(f"Strong test code ({loc_ratio:.0%} of source)")
            elif loc_ratio >= 0.2:
                score += 10

        # Tests passed
        if self.metrics.tests_passed is True:
            score += 20
            positives.append("All tests passing")
        elif self.metrics.tests_passed is False:
            score -= 20
            issues.append("Tests failing")

        # Coverage
        if self.metrics.coverage_pct:
            if self.metrics.coverage_pct >= 80:
                score += 15
                positives.append(f"Excellent coverage: {self.metrics.coverage_pct}%")
            elif self.metrics.coverage_pct >= 60:
                score += 10
                positives.append(f"Good coverage: {self.metrics.coverage_pct}%")
            elif self.metrics.coverage_pct < 40:
                issues.append(f"Low coverage: {self.metrics.coverage_pct}%")

        details.append(f"Test files: {self.metrics.test_files}")
        details.append(f"Test LOC: {self.metrics.test_loc}")

        return DimensionScore(
            name="Test Quality",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["test_quality"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_documentation(self) -> DimensionScore:
        """Analyze documentation quality."""
        score = 40.0
        details = []
        issues = []
        positives = []

        # Check for README
        readme_files = list(self.project_dir.glob("README*"))
        if readme_files:
            try:
                readme_content = readme_files[0].read_text(encoding="utf-8")
                if len(readme_content) > 500:
                    score += 15
                    positives.append("Comprehensive README")
                elif len(readme_content) > 100:
                    score += 5
                    positives.append("Basic README")
                else:
                    issues.append("README too brief")
            except Exception:
                pass
        else:
            score -= 15
            issues.append("No README file")

        # Docstring coverage
        if self.metrics.functions > 0:
            doc_coverage = self.metrics.documented_funcs / self.metrics.functions * 100
            if doc_coverage >= 50:
                score += 20
                positives.append(f"{doc_coverage:.0f}% functions documented")
            elif doc_coverage >= 20:
                score += 10
            elif doc_coverage < 10:
                score -= 10
                issues.append("Very few documented functions")
            details.append(f"Doc coverage: {doc_coverage:.0f}%")

        # Type coverage
        if self.metrics.type_coverage_pct >= 80:
            score += 15
            positives.append(f"Excellent type coverage: {self.metrics.type_coverage_pct:.0f}%")
        elif self.metrics.type_coverage_pct >= 50:
            score += 10
            positives.append(f"Good type coverage: {self.metrics.type_coverage_pct:.0f}%")
        elif self.metrics.type_coverage_pct < 20:
            issues.append(f"Low type coverage: {self.metrics.type_coverage_pct:.0f}%")

        # Check for CHANGELOG
        if list(self.project_dir.glob("CHANGELOG*")):
            score += 5
            positives.append("CHANGELOG present")

        return DimensionScore(
            name="Documentation",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["documentation"],
            details=details,
            issues=issues,
            positives=positives,
        )

    def _analyze_best_practices(self) -> DimensionScore:
        """Analyze adherence to best practices and code design quality."""
        score = 30.0  # Start lower to account for UX/DX bonuses
        details = []
        issues = []
        positives = []

        # === UX/DX Quality Scores (from code analysis) ===
        # These measure code design quality beyond just anti-patterns

        # Modularity score (function size distribution) - max +15
        if self.metrics.modularity_score >= 70:
            score += 15
            positives.append(f"Good modularity ({self.metrics.modularity_score:.0f}/100)")
        elif self.metrics.modularity_score >= 50:
            score += 10
            positives.append(f"Moderate modularity ({self.metrics.modularity_score:.0f}/100)")
        elif self.metrics.modularity_score >= 30:
            score += 5
        else:
            issues.append(f"Poor modularity ({self.metrics.modularity_score:.0f}/100)")

        # SRP score (Single Responsibility Principle) - max +15
        if self.metrics.srp_score >= 70:
            score += 15
            positives.append(f"Good SRP adherence ({self.metrics.srp_score:.0f}/100)")
        elif self.metrics.srp_score >= 50:
            score += 10
        elif self.metrics.srp_score >= 30:
            score += 5
        else:
            issues.append(f"SRP violations detected ({self.metrics.srp_score:.0f}/100)")

        # Error handling quality - max +15
        if self.metrics.error_handling_score >= 70:
            score += 15
            positives.append(f"Good error handling ({self.metrics.error_handling_score:.0f}/100)")
        elif self.metrics.error_handling_score >= 50:
            score += 10
        elif self.metrics.error_handling_score >= 30:
            score += 5
        else:
            issues.append(f"Poor error handling ({self.metrics.error_handling_score:.0f}/100)")

        # === Configuration & Tooling === max +25

        # Configuration files - max +8
        config_checks = [
            ("pyproject.toml", "Modern Python packaging"),
            ("package.json", "Node.js config"),
            ("tsconfig.json", "TypeScript config"),
            ("go.mod", "Go modules"),
            (".gitignore", "Git ignore"),
        ]

        config_count = 0
        for filename, desc in config_checks:
            if (self.project_dir / filename).exists():
                config_count += 1
                positives.append(desc)

        if config_count > 0:
            score += min(config_count * 2, 8)

        # Linting configuration - +7
        lint_configs = [
            ".eslintrc",
            ".eslintrc.js",
            ".eslintrc.json",
            ".eslintrc.yaml",
            "ruff.toml",
            ".golangci.yml",
            ".golangci.yaml",
            "biome.json",
            "deno.json",
        ]
        # Also check pyproject.toml for ruff config
        has_lint = any((self.project_dir / lc).exists() for lc in lint_configs)
        if not has_lint:
            pyproject = self.project_dir / "pyproject.toml"
            if pyproject.exists():
                try:
                    content = pyproject.read_text(encoding="utf-8")
                    has_lint = "[tool.ruff]" in content or "[tool.pylint]" in content
                except Exception:
                    pass

        if has_lint:
            score += 7
            positives.append("Linting configured")
        else:
            issues.append("No linting configuration")

        # CI/CD - +5
        ci_paths = [".github/workflows", ".gitlab-ci.yml", ".circleci", "Jenkinsfile"]
        if any((self.project_dir / ci).exists() for ci in ci_paths):
            score += 5
            positives.append("CI/CD configured")

        # Dependencies lockfile - +3
        lockfiles = [
            "poetry.lock",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "go.sum",
            "Cargo.lock",
        ]
        if any((self.project_dir / lf).exists() for lf in lockfiles):
            score += 3
            positives.append("Dependencies locked")

        # Project structure - +2
        if (self.project_dir / "src").exists() or (self.project_dir / "lib").exists():
            score += 2
            positives.append("Organized project structure")

        details.append(f"Language: {self.metrics.language}")
        details.append(f"Modularity: {self.metrics.modularity_score:.0f}")
        details.append(f"SRP: {self.metrics.srp_score:.0f}")
        details.append(f"Error handling: {self.metrics.error_handling_score:.0f}")

        return DimensionScore(
            name="Best Practices",
            score=max(0, min(100, score)),
            weight=DIMENSION_WEIGHTS["best_practices"],
            details=details,
            issues=issues,
            positives=positives,
        )


def compare_metrics(cco: Metrics, vanilla: Metrics) -> dict[str, Any]:
    """Compare two sets of metrics and determine winner per category."""
    comparisons: list[dict[str, Any]] = []
    cco_wins = 0
    vanilla_wins = 0
    ties = 0

    def add(name: str, cco_val: Any, van_val: Any, better: str, category: str) -> None:
        nonlocal cco_wins, vanilla_wins, ties

        if cco_val == van_val:
            winner = "tie"
            ties += 1
        elif better == "lower":
            winner = "cco" if cco_val < van_val else "vanilla"
        else:
            winner = "cco" if cco_val > van_val else "vanilla"

        if winner == "cco":
            cco_wins += 1
        elif winner == "vanilla":
            vanilla_wins += 1

        comparisons.append(
            {
                "name": name,
                "category": category,
                "cco": cco_val,
                "vanilla": van_val,
                "winner": winner,
                "better_is": better,
            }
        )

    # Anti-patterns (lower is better)
    add("Bare Excepts", cco.bare_excepts, vanilla.bare_excepts, "lower", "Anti-patterns")
    add("Silent Passes", cco.silent_passes, vanilla.silent_passes, "lower", "Anti-patterns")
    add("Broad Excepts", cco.broad_excepts, vanilla.broad_excepts, "lower", "Anti-patterns")
    add("Giant Functions (>50 LOC)", cco.giant_funcs, vanilla.giant_funcs, "lower", "Anti-patterns")
    add("Magic Numbers", cco.magic_numbers, vanilla.magic_numbers, "lower", "Anti-patterns")
    add(
        "Mutable Defaults", cco.mutable_defaults, vanilla.mutable_defaults, "lower", "Anti-patterns"
    )
    add("Star Imports", cco.star_imports, vanilla.star_imports, "lower", "Anti-patterns")
    add(
        "High Complexity Funcs",
        cco.high_complexity_funcs,
        vanilla.high_complexity_funcs,
        "lower",
        "Anti-patterns",
    )

    # Best practices (higher is better)
    add(
        "Exception Chains",
        cco.exception_chains,
        vanilla.exception_chains,
        "higher",
        "Best Practices",
    )
    add(
        "Context Managers",
        cco.context_managers,
        vanilla.context_managers,
        "higher",
        "Best Practices",
    )
    add(
        "Dataclasses Used",
        cco.dataclasses_used,
        vanilla.dataclasses_used,
        "higher",
        "Best Practices",
    )
    add("Enums Used", cco.enums_used, vanilla.enums_used, "higher", "Best Practices")

    # Type & Doc coverage (higher is better)
    add(
        "Type Coverage %",
        round(cco.type_coverage_pct, 1),
        round(vanilla.type_coverage_pct, 1),
        "higher",
        "Coverage",
    )
    add(
        "Docstring Coverage %",
        round(cco.docstring_coverage_pct, 1),
        round(vanilla.docstring_coverage_pct, 1),
        "higher",
        "Coverage",
    )

    # Testing (higher is better)
    add("Test Files", cco.test_files, vanilla.test_files, "higher", "Testing")
    add("Test LOC", cco.test_loc, vanilla.test_loc, "higher", "Testing")
    if cco.coverage_pct is not None and vanilla.coverage_pct is not None:
        add(
            "Coverage %",
            round(cco.coverage_pct, 1),
            round(vanilla.coverage_pct, 1),
            "higher",
            "Testing",
        )

    # UX/DX scores (higher is better)
    add(
        "Modularity Score",
        round(cco.modularity_score, 1),
        round(vanilla.modularity_score, 1),
        "higher",
        "UX/DX",
    )
    add("SRP Score", round(cco.srp_score, 1), round(vanilla.srp_score, 1), "higher", "UX/DX")
    add(
        "Error Handling Score",
        round(cco.error_handling_score, 1),
        round(vanilla.error_handling_score, 1),
        "higher",
        "UX/DX",
    )

    # Size metrics (informational)
    add("Total LOC", cco.total_loc, vanilla.total_loc, "info", "Size")
    add(
        "Functions + Methods",
        cco.functions + cco.methods,
        vanilla.functions + vanilla.methods,
        "info",
        "Size",
    )

    # Use dimension-based overall_score (calculated by CodeAnalyzer)
    diff = cco.overall_score - vanilla.overall_score

    return {
        "comparisons": comparisons,
        "cco_wins": cco_wins,
        "vanilla_wins": vanilla_wins,
        "ties": ties,
        "cco_score": round(cco.overall_score, 1),
        "vanilla_score": round(vanilla.overall_score, 1),
        "score_diff": round(diff, 1),
        "verdict": calculate_verdict(diff),
    }


def calculate_verdict(score_diff: float) -> str:
    """Calculate verdict based on score difference (SSOT for verdict logic).

    Args:
        score_diff: CCO score - Vanilla score (positive = CCO better)

    Returns:
        Human-readable verdict string
    """
    if score_diff >= 15:
        return "Strong CCO Advantage"
    elif score_diff >= 5:
        return "Moderate CCO Advantage"
    elif score_diff >= -5:
        return "Mixed Results"
    elif score_diff >= -15:
        return "Moderate Vanilla Advantage"
    else:
        return "Strong Vanilla Advantage"


def compare_comprehensive(cco: Metrics, vanilla: Metrics) -> dict[str, Any]:
    """Compare two comprehensive 6-dimension analyses.

    This is the main comparison function for the benchmark UI's Static button.
    """
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
                "cco_issues": cco_dim.issues,
                "vanilla_issues": vanilla_dim.issues,
                "cco_positives": cco_dim.positives,
                "vanilla_positives": vanilla_dim.positives,
                "cco_details": cco_dim.details,
                "vanilla_details": vanilla_dim.details,
            }
        )

    overall_diff = cco.overall_score - vanilla.overall_score
    verdict = calculate_verdict(overall_diff)

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

"""
Advanced metrics collection for CCO benchmarks.

Collects quantitative, quality, and UX/DX metrics from generated code.
"""

import ast
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


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
    """Comprehensive metrics for a codebase."""

    # Identity
    name: str = ""
    variant: str = ""  # "cco" or "vanilla"

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
        d = {}
        for k, v in self.__dict__.items():
            if k == "function_details":
                d[k] = [f.__dict__ for f in v]
            elif isinstance(v, Path):
                d[k] = str(v)
            else:
                d[k] = v
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Metrics":
        """Create from dictionary."""
        func_details = data.pop("function_details", [])
        m = cls(**data)
        m.function_details = [FunctionInfo(**f) for f in func_details]
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

    def analyze(self) -> Metrics:
        """Perform full analysis."""
        self._count_files()
        self._analyze_python()
        self._analyze_typescript()
        self._analyze_go()
        self._calculate_scores()
        self._run_tests()
        return self.metrics

    def _count_files(self) -> None:
        """Count files by type."""
        for f in self.project_dir.rglob("*"):
            if self._should_skip(f):
                continue
            if not f.is_file():
                continue

            self.metrics.total_files += 1
            suffix = f.suffix.lower()

            if suffix == ".py":
                self.metrics.python_files += 1
                if "test" in f.name.lower() or f.parent.name == "tests":
                    self.metrics.test_files += 1
            elif suffix in (".ts", ".tsx"):
                self.metrics.typescript_files += 1
                if ".test." in f.name or ".spec." in f.name:
                    self.metrics.test_files += 1
            elif suffix == ".go":
                self.metrics.go_files += 1
                if "_test.go" in f.name:
                    self.metrics.test_files += 1

    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped."""
        skip_dirs = {
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
        }
        # Skip benchmark metadata files
        skip_prefixes = ("_benchmark_", "_ccbox_")
        skip_suffixes = (".log",)

        if path.name.startswith(skip_prefixes):
            return True
        if path.name.endswith(skip_suffixes):
            return True
        return any(d in path.parts for d in skip_dirs)

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
        """Analyze TypeScript files (basic)."""
        for ts_file in self.project_dir.rglob("*.ts"):
            if self._should_skip(ts_file):
                continue
            if ts_file.suffix == ".d.ts":
                continue

            try:
                content = ts_file.read_text(encoding="utf-8")
                lines = content.splitlines()
                self.metrics.total_loc += len(lines)

                is_test = ".test." in ts_file.name or ".spec." in ts_file.name
                if is_test:
                    self.metrics.test_loc += len(lines)

                # Count functions (simple regex)
                func_count = len(re.findall(r"\bfunction\s+\w+|=>\s*{|\basync\s+\w+\s*\(", content))
                self.metrics.functions += func_count

                # Count test cases
                if is_test:
                    self.metrics.test_count += len(re.findall(r"\bit\(|test\(|describe\(", content))
            except Exception:
                pass

    def _analyze_go(self) -> None:
        """Analyze Go files (basic)."""
        for go_file in self.project_dir.rglob("*.go"):
            if self._should_skip(go_file):
                continue

            try:
                content = go_file.read_text(encoding="utf-8")
                lines = content.splitlines()
                self.metrics.total_loc += len(lines)

                is_test = "_test.go" in go_file.name
                if is_test:
                    self.metrics.test_loc += len(lines)

                # Count functions
                func_count = len(re.findall(r"\bfunc\s+", content))
                self.metrics.functions += func_count

                # Count test functions
                if is_test:
                    self.metrics.test_count += len(re.findall(r"func\s+Test\w+", content))
            except Exception:
                pass

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

        # Modularity score (penalize giant functions)
        if total_funcs > 0:
            small_ratio = self.metrics.small_funcs / total_funcs
            giant_penalty = self.metrics.giant_funcs * 10
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
            complexity_penalty = self.metrics.high_complexity_funcs * 5
            self.metrics.srp_score = max(
                0, min(100, 100 - (max(0, avg_loc - 20) * 2) - complexity_penalty)
            )

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
            self.metrics.error_handling_score = max(
                0, min(100, (good_handling / total_handlers) * 100 - bad_handling * 10)
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


def calculate_overall_score(m: Metrics) -> float:
    """Calculate overall quality score (0-100)."""
    score = 50.0  # Start neutral

    # Anti-patterns (penalties, capped to prevent single category dominance)
    score -= min(m.bare_excepts * 5, 15)  # Max -15
    score -= min(m.silent_passes * 5, 15)  # Max -15 (reduced from 10 per)
    score -= min(m.broad_excepts * 2, 10)  # Max -10
    score -= min(m.giant_funcs * 5, 15)  # Max -15 (reduced from 8 per)
    score -= min(m.magic_numbers * 0.3, 10)  # Max -10 (reduced penalty)
    score -= min(m.mutable_defaults * 3, 10)  # Max -10
    score -= min(m.star_imports * 2, 10)  # Max -10
    score -= min(m.global_vars * 2, 10)  # Max -10

    # Best practices (bonuses)
    score += min(m.exception_chains, 10) * 2
    score += min(m.context_managers, 20) * 0.5
    score += min(m.dataclasses_used, 5) * 2
    score += min(m.enums_used, 5) * 2
    if m.pathlib_used:
        score += 3

    # Type coverage bonus
    score += m.type_coverage_pct * 0.15

    # Test coverage bonus
    if m.coverage_pct:
        score += m.coverage_pct * 0.1
    if m.tests_passed is True:
        score += 10

    # UX/DX scores
    score += m.modularity_score * 0.05
    score += m.srp_score * 0.05
    score += m.error_handling_score * 0.05

    return max(0, min(100, score))


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

    cco_score = calculate_overall_score(cco)
    vanilla_score = calculate_overall_score(vanilla)
    diff = cco_score - vanilla_score

    return {
        "comparisons": comparisons,
        "cco_wins": cco_wins,
        "vanilla_wins": vanilla_wins,
        "ties": ties,
        "cco_score": round(cco_score, 1),
        "vanilla_score": round(vanilla_score, 1),
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

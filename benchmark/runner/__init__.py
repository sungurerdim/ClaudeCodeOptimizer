"""
Benchmark runner module.

The unified CodeAnalyzer in metrics.py provides:
- 40+ language support
- 6-dimension scoring (functional, quality, security, test, docs, best practices)
- Grade system (A+ to F)
- Universal anti-pattern detection
"""

from .executor import (
    DOCKER_INSTALL_URL,
    ActivityState,
    BenchmarkPhase,
    BenchmarkResult,
    DependencyStatus,
    ExecutionResult,
    NewBenchmarkResult,
    ProjectConfig,
    ResultsManager,
    ResumeState,
    TestExecutor,
    check_dependencies,
    discover_projects,
)
from .metrics import (
    DIMENSION_WEIGHTS,
    CodeAnalyzer,
    DimensionScore,
    FunctionInfo,
    Metrics,
    calculate_grade,
    calculate_verdict,
    compare_comprehensive,
    compare_metrics,
)

# Backwards compatibility aliases (deprecated)
# Use CodeAnalyzer and Metrics instead
try:
    from .analyzer import ComprehensiveAnalyzer, ComprehensiveMetrics
except ImportError:
    ComprehensiveAnalyzer = CodeAnalyzer  # type: ignore
    ComprehensiveMetrics = Metrics  # type: ignore

__all__ = [
    # Executor
    "ActivityState",
    "BenchmarkPhase",
    "BenchmarkResult",
    "DependencyStatus",
    "DOCKER_INSTALL_URL",
    "ExecutionResult",
    "NewBenchmarkResult",
    "ProjectConfig",
    "ResultsManager",
    "ResumeState",
    "TestExecutor",
    "check_dependencies",
    "discover_projects",
    # Metrics (unified analyzer)
    "CodeAnalyzer",
    "DimensionScore",
    "DIMENSION_WEIGHTS",
    "FunctionInfo",
    "Metrics",
    "calculate_grade",
    "calculate_verdict",
    "compare_comprehensive",
    "compare_metrics",
    # Backwards compatibility (deprecated)
    "ComprehensiveAnalyzer",
    "ComprehensiveMetrics",
]

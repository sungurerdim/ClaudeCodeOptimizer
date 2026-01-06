"""
DEPRECATED: Use CodeAnalyzer and Metrics from metrics.py instead.

This module provides backwards compatibility aliases for legacy code.
All functionality has been merged into metrics.py with:
- 40+ language support
- 6-dimension scoring (functional, quality, security, test, docs, best practices)
- Grade system (A+ to F)
- Universal anti-pattern detection

Migration:
    # Old (deprecated)
    from benchmark.runner.analyzer import ComprehensiveAnalyzer, ComprehensiveMetrics

    # New (recommended)
    from benchmark.runner import CodeAnalyzer, Metrics
"""

import warnings

# Re-export from metrics.py for backwards compatibility
from .metrics import (
    CodeAnalyzer,
    DimensionScore,
    Metrics,
    compare_comprehensive,
)

# Emit deprecation warning on import
warnings.warn(
    "analyzer.py is deprecated. Use CodeAnalyzer and Metrics from metrics.py instead. "
    "Import from benchmark.runner directly: from benchmark.runner import CodeAnalyzer, Metrics",
    DeprecationWarning,
    stacklevel=2,
)

# Backwards compatibility aliases
ComprehensiveAnalyzer = CodeAnalyzer
ComprehensiveMetrics = Metrics

__all__ = [
    "ComprehensiveAnalyzer",
    "ComprehensiveMetrics",
    "DimensionScore",
    "compare_comprehensive",
]

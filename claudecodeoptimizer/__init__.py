"""ClaudeCodeOptimizer - System-wide project management for Claude Code."""

import sys

__version__ = "0.1.0"
__author__ = "Sungur Zahid Erdim"
__license__ = "MIT"

# Fix Windows console encoding for emoji/Unicode support
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import CCOConfig

__all__ = ["CCOConfig", "__version__"]

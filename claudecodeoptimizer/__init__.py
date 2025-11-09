"""ClaudeCodeOptimizer - System-wide project management for Claude Code."""

import logging
import sys

__version__ = "0.1.0"
__author__ = "Sungur Zahid Erdim"
__license__ = "MIT"

# Fix Windows console encoding for emoji/Unicode support
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Failed to reconfigure console encoding: {e}. Using default encoding.")

from .config import CCOConfig

__all__ = ["CCOConfig", "__version__"]

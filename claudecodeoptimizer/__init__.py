"""ClaudeCodeOptimizer - System-wide project management for Claude Code."""

import logging
import sys

logger = logging.getLogger(__name__)

__version__ = "0.1.0"
__author__ = "Sungur Zahid Erdim"
__license__ = "MIT"

# Fix Windows console encoding for emoji/Unicode support
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception as e:  # noqa: S110
        logger.debug(f"Windows console encoding reconfigure failed: {e}")
        pass  # Silent fail - continue with default encoding

from .config import CCOConfig  # noqa: E402

__all__ = ["CCOConfig", "__version__"]

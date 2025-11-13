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


# Auto-setup global CCO structure on first import
_setup_checked = False


def _ensure_global_setup():
    """
    Ensure ~/.cco/ exists with all content, setup if needed.

    Runs once on first import. Silent operation - doesn't break import on failure.
    """
    global _setup_checked
    if _setup_checked:
        return
    _setup_checked = True

    try:
        from .config import get_global_dir

        global_dir = get_global_dir()

        # Check if setup needed (dir missing or principles incomplete)
        principles_dir = global_dir / "principles"
        if not principles_dir.exists() or len(list(principles_dir.glob("*.md"))) < 80:
            # Silent setup - will create ~/.cco/ with all content
            from .core.knowledge_setup import setup_global_knowledge

            setup_global_knowledge(force=False)
    except Exception:
        # Silent fail - don't break package import
        # User can manually run: python -m claudecodeoptimizer.install_hook
        pass


# Auto-setup on import (pip install → import → auto-setup)
_ensure_global_setup()

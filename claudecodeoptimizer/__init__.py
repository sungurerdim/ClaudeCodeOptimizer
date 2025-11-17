"""ClaudeCodeOptimizer - System-wide project management for Claude Code."""

import sys

__version__ = "0.1.0"
__author__ = "Sungur Zahid Erdim"
__license__ = "MIT"

# Fix Windows console encoding for emoji/Unicode support
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # noqa: S110
        pass  # Silent fail - continue with default encoding

from .config import CCOConfig

__all__ = ["CCOConfig", "__version__"]


# Auto-setup global CCO structure on first import
_setup_checked = False


def _ensure_global_setup() -> None:
    """
    Ensure ~/.claude/ exists with all CCO content, setup if needed.

    Runs once on first import. Shows helpful message if setup needed.
    """
    global _setup_checked
    if _setup_checked:
        return
    _setup_checked = True

    try:
        from .config import get_claude_dir

        claude_dir = get_claude_dir()

        # Check if setup needed (commands dir missing or empty)
        commands_dir = claude_dir / "commands"
        principles_dir = claude_dir / "principles"

        # Setup if commands missing or principles incomplete
        needs_setup = (
            not commands_dir.exists()
            or len(list(commands_dir.glob("cco-*.md"))) < 10
            or not principles_dir.exists()
            or len(list(principles_dir.glob("U_*.md"))) < 5
        )

        if needs_setup:
            # Auto-setup on first import (silent)
            from .core.knowledge_setup import setup_global_knowledge

            setup_global_knowledge(force=False)
    except Exception:  # noqa: S110
        # Silent fail - don't break package import
        # User can manually run: cco-setup
        pass


# Auto-setup on import (pip install → import → auto-setup)
_ensure_global_setup()

"""ClaudeCodeOptimizer - Enhance Claude Code with commands, agents, and rules."""

import sys

__version__ = "1.0.0"
__author__ = "Sungur Zahid Erdim"

# Windows UTF-8 fix
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:
        pass

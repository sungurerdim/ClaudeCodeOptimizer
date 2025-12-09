"""ClaudeCodeOptimizer - A process and rules layer for Claude Code in the Opus 4.5 era."""

import sys

__version__ = "1.1.0"
__description__ = "A process and rules layer for Claude Code in the Opus 4.5 era"
__author__ = "Sungur Zahid Erdim"

# Windows UTF-8 fix
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
            except Exception:
                pass

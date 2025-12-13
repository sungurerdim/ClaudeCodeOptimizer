"""ClaudeCodeOptimizer - A process and rules layer for Claude Code in the Opus 4.5 era."""

import sys

__all__ = ["__version__", "__description__", "__author__"]

__version__ = "1.1.0"
__description__ = "A process and rules layer for Claude Code in the Opus 4.5 era"
__author__ = "Sungur Zahid Erdim"

# Windows UTF-8 fix
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                # reconfigure exists due to hasattr check, but mypy doesn't track control flow
                stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
            except (OSError, AttributeError):
                pass  # Silently fail if reconfigure not supported

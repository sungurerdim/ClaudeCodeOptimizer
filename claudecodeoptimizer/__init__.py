"""ClaudeCodeOptimizer - A process and rules layer for Claude Code in the Opus 4.5 era."""

import logging
import sys

__all__ = ["__version__", "__description__", "__author__"]

__version__ = "2.0.0"
__description__ = "A process and rules layer for Claude Code in the Opus 4.5 era"
__author__ = "Sungur Zahid Erdim"

# Windows UTF-8 fix
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # hasattr guards reconfigure, mypy can't narrow TextIO union
                logging.debug(f"Successfully reconfigured {stream.name} to UTF-8 encoding")
            except (OSError, AttributeError) as e:
                logging.debug(f"Failed to reconfigure {stream.name} to UTF-8: {e}")

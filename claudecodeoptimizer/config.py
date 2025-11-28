"""CCO Configuration - Single source of truth."""

import re
from pathlib import Path

from . import __version__

__all__ = [
    "VERSION",
    "CLAUDE_DIR",
    "COMMANDS_DIR",
    "AGENTS_DIR",
    "get_cco_commands",
    "get_cco_agents",
    "CCO_MARKER_PATTERNS",
    "SUBPROCESS_TIMEOUT",
]

VERSION = __version__  # Single source: __init__.py
CLAUDE_DIR = Path.home() / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
AGENTS_DIR = CLAUDE_DIR / "agents"

# Marker patterns for content removal
CCO_MARKER_PATTERNS: dict[str, tuple[str, int]] = {
    "standards": (r"<!-- CCO_STANDARDS_START -->.*?<!-- CCO_STANDARDS_END -->\n?", re.DOTALL),
    "rules": (r"<!-- CCO_RULES_START -->.*?<!-- CCO_RULES_END -->\n?", re.DOTALL),
    "principles": (r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?", re.DOTALL),
}

SUBPROCESS_TIMEOUT = 5  # seconds


def get_cco_commands() -> list[Path]:
    """Get all CCO command files."""
    return sorted(COMMANDS_DIR.glob("cco-*.md")) if COMMANDS_DIR.exists() else []


def get_cco_agents() -> list[Path]:
    """Get all CCO agent files."""
    return sorted(AGENTS_DIR.glob("cco-*.md")) if AGENTS_DIR.exists() else []

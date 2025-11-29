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
    "get_standards_count",
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
}

SUBPROCESS_TIMEOUT = 5  # seconds


def get_cco_commands() -> list[Path]:
    """Get all CCO command files."""
    return sorted(COMMANDS_DIR.glob("cco-*.md")) if COMMANDS_DIR.exists() else []


def get_cco_agents() -> list[Path]:
    """Get all CCO agent files."""
    return sorted(AGENTS_DIR.glob("cco-*.md")) if AGENTS_DIR.exists() else []


def get_standards_count() -> tuple[int, int]:
    """Count standards and categories from source file.

    Returns:
        Tuple of (standards_count, categories_count)
    """
    standards_file = Path(__file__).parent / "content" / "standards" / "cco-standards.md"
    if not standards_file.exists():
        return (0, 0)
    content = standards_file.read_text(encoding="utf-8")
    standards = len(re.findall(r"^- ", content, re.MULTILINE))
    categories = len(re.findall(r"^## ", content, re.MULTILINE))
    return (standards, categories)

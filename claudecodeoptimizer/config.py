"""CCO Configuration - Single source of truth."""

import re
from pathlib import Path

from . import __version__

__all__ = [
    "VERSION",
    "CLAUDE_DIR",
    "COMMANDS_DIR",
    "AGENTS_DIR",
    "SEPARATOR",
    "get_cco_commands",
    "get_cco_agents",
    "get_standards_breakdown",
    "get_content_path",
    "CCO_MARKER_PATTERNS",
    "SUBPROCESS_TIMEOUT",
    "STATUSLINE_FILE",
    "SETTINGS_FILE",
]

VERSION = __version__  # Single source: __init__.py
CLAUDE_DIR = Path.home() / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
AGENTS_DIR = CLAUDE_DIR / "agents"
STATUSLINE_FILE = CLAUDE_DIR / "statusline.js"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
SEPARATOR = "=" * 50


def get_content_path(subdir: str) -> Path:
    """Get path to content subdirectory.

    Args:
        subdir: One of 'commands', 'agents', 'standards', 'statusline', 'permissions'

    Returns:
        Path to the content subdirectory
    """
    return Path(__file__).parent / "content" / subdir


# Marker patterns for content removal
CCO_MARKER_PATTERNS: dict[str, tuple[str, int]] = {
    "standards": (r"<!-- CCO_STANDARDS_START -->.*?<!-- CCO_STANDARDS_END -->\n?", re.DOTALL),
}

SUBPROCESS_TIMEOUT = 5  # seconds

# Pre-compiled regex patterns for performance
_STANDARD_PATTERN = re.compile(r"^- ", re.MULTILINE)
_CATEGORY_PATTERN = re.compile(r"^## ", re.MULTILINE)


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
    standards = len(_STANDARD_PATTERN.findall(content))
    categories = len(_CATEGORY_PATTERN.findall(content))
    return (standards, categories)


def get_standards_breakdown() -> dict[str, int]:
    """Get detailed breakdown of standards by category.

    Returns:
        Dictionary with universal, ai_specific, cco_specific, project_specific counts
    """
    content_dir = Path(__file__).parent / "content" / "standards"
    result = {
        "universal": 0,
        "ai_specific": 0,
        "cco_specific": 0,
        "project_specific": 0,
        "total": 0,
    }

    # Count from cco-standards.md (Universal + AI-Specific + CCO-Workflow)
    standards_file = content_dir / "cco-standards.md"
    if standards_file.exists():
        content = standards_file.read_text(encoding="utf-8")
        # Split at category headers
        parts = content.split("# AI-Specific Standards")
        if len(parts) >= 2:
            result["universal"] = len(_STANDARD_PATTERN.findall(parts[0]))
            ai_and_cco = parts[1].split("# CCO-Specific Standards")
            if len(ai_and_cco) >= 2:
                result["ai_specific"] = len(_STANDARD_PATTERN.findall(ai_and_cco[0]))
                result["cco_specific"] = len(_STANDARD_PATTERN.findall(ai_and_cco[1]))
            else:
                result["ai_specific"] = len(_STANDARD_PATTERN.findall(parts[1]))

    # Count from cco-standards-conditional.md (Project-Specific)
    conditional_file = content_dir / "cco-standards-conditional.md"
    if conditional_file.exists():
        content = conditional_file.read_text(encoding="utf-8")
        result["project_specific"] = len(_STANDARD_PATTERN.findall(content))

    result["total"] = (
        result["universal"]
        + result["ai_specific"]
        + result["cco_specific"]
        + result["project_specific"]
    )
    return result

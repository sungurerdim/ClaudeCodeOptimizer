"""CCO Configuration - Single source of truth."""

import json
import re
from pathlib import Path
from typing import Any

from . import __version__

__all__ = [
    "VERSION",
    "CLAUDE_DIR",
    "COMMANDS_DIR",
    "AGENTS_DIR",
    "RULES_DIR",
    "CCO_RULES_SUBDIR",
    "OLD_RULES_ROOT",
    "CCO_RULE_FILES",
    "CCO_RULE_NAMES",
    "ALL_RULE_NAMES",
    "OLD_RULE_FILES",
    "SEPARATOR",
    "get_cco_commands",
    "get_cco_agents",
    "get_rules_breakdown",
    "get_content_path",
    "CCO_UNIVERSAL_PATTERN",
    "SUBPROCESS_TIMEOUT",
    "SUBPROCESS_TIMEOUT_PACKAGE",
    "MAX_CLAUDE_MD_SIZE",
    "STATUSLINE_FILE",
    "SETTINGS_FILE",
    "CCO_PERMISSIONS_MARKER",
]

VERSION = __version__  # Single source: __init__.py
CLAUDE_DIR = Path.home() / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
AGENTS_DIR = CLAUDE_DIR / "agents"

# CCO rules are namespaced in cco/ subdirectory to preserve user's custom rules
CCO_RULES_SUBDIR = "cco"
RULES_DIR = CLAUDE_DIR / "rules" / CCO_RULES_SUBDIR  # ~/.claude/rules/cco/
OLD_RULES_ROOT = CLAUDE_DIR / "rules"  # For backward compat cleanup

# Rule files installed to ~/.claude/rules/cco/ (without cco- prefix)
# Only core.md and ai.md are installed globally (always active)
# tools.md and adaptive.md stay in pip package - loaded on-demand by commands
CCO_RULE_NAMES = ("core.md", "ai.md")  # Installed globally
CCO_RULE_FILES = ("cco-core.md", "cco-ai.md")  # Source filenames

# Consolidated rule name lists (for cleanup across all CCO versions)
ALL_RULE_NAMES: list[str] = list(CCO_RULE_NAMES) + ["tools.md", "adaptive.md"]
OLD_RULE_FILES: list[str] = list(CCO_RULE_FILES) + ["cco-adaptive.md", "cco-tools.md"]

STATUSLINE_FILE = CLAUDE_DIR / "cco-statusline.js"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
SEPARATOR = "=" * 50

# CCO Permissions marker - used to identify CCO-installed permissions
# Permissions JSON has _meta.level field when installed by CCO
CCO_PERMISSIONS_MARKER = "_cco_managed"


def get_content_path(subdir: str = "") -> Path:
    """Get path to content subdirectory.

    Args:
        subdir: One of 'commands', 'agents', 'rules', 'statusline', 'permissions', or '' for root

    Returns:
        Path to the content subdirectory or content root if subdir is empty
    """
    base = Path(__file__).parent / "content"
    return base / subdir if subdir else base


# Universal CCO marker pattern - matches ANY cco_* marker block (case-insensitive)
# Used for backward compatibility: removes all CCO content regardless of marker name
# Matches: <!-- CCO_anything_START -->...<!-- CCO_anything_END -->
# Also: <!-- cco-anything-start -->...<!-- cco-anything-end -->
# ReDoS mitigation: File size limited to MAX_CLAUDE_MD_SIZE (1MB) before pattern application.
# The .*? quantifier is safe given this size constraint.
CCO_UNIVERSAL_PATTERN = (
    r"<!--\s*CCO[_-]\w+[_-]START\s*-->.*?<!--\s*CCO[_-]\w+[_-]END\s*-->\n?",
    re.DOTALL | re.IGNORECASE,
)

# Timeout constants (seconds)
SUBPROCESS_TIMEOUT = 5  # Default for quick operations
SUBPROCESS_TIMEOUT_PACKAGE = 30  # Package install/uninstall operations

# File size limits for safety
MAX_CLAUDE_MD_SIZE = 1_000_000  # 1MB - prevent ReDoS on large files

# Pre-compiled regex patterns for performance
# Rules use list format: - **Name**: Description
# OR table format (adaptive): | * Name | Check | Description |
_RULE_PATTERN = re.compile(r"(?:^- \*\*\w+\*\*:|\| \* )", re.MULTILINE)
_CATEGORY_PATTERN = re.compile(r"^## ", re.MULTILINE)


def get_cco_commands() -> list[Path]:
    """Get all CCO command files."""
    return sorted(COMMANDS_DIR.glob("cco-*.md")) if COMMANDS_DIR.exists() else []


def get_cco_agents() -> list[Path]:
    """Get all CCO agent files."""
    return sorted(AGENTS_DIR.glob("cco-*.md")) if AGENTS_DIR.exists() else []


def load_json_file(path: Path) -> dict[str, Any]:
    """Load JSON from file, returning empty dict on decode error.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON dict, or empty dict if file missing/invalid
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_json_file(path: Path, data: dict[str, Any]) -> None:
    """Save data as JSON with pretty formatting.

    Args:
        path: Path to JSON file
        data: Dictionary to save
    """
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def get_rules_breakdown() -> dict[str, int]:
    """Get detailed breakdown of rules by category.

    Returns:
        Dictionary with core, ai, tools, adaptive, total counts
    """
    rules_dir = Path(__file__).parent / "content" / "rules"
    result = {
        "core": 0,
        "ai": 0,
        "tools": 0,
        "adaptive": 0,
        "total": 0,
    }

    # Count from each rule file
    file_mapping = {
        "core": "cco-core.md",
        "ai": "cco-ai.md",
        "tools": "cco-tools.md",
        "adaptive": "cco-adaptive.md",
    }

    for key, filename in file_mapping.items():
        file_path = rules_dir / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            result[key] = len(_RULE_PATTERN.findall(content))

    result["total"] = result["core"] + result["ai"] + result["tools"] + result["adaptive"]
    return result


# Internal function (test-only, use get_rules_breakdown() instead)
def _get_rules_count() -> tuple[int, int]:
    """Count rules and categories from source files.

    Returns:
        Tuple of (rules_count, categories_count)
    """
    rules_dir = Path(__file__).parent / "content" / "rules"
    if not rules_dir.exists():
        return (0, 0)

    total_rules = 0
    total_categories = 0

    for rule_file in CCO_RULE_FILES:
        file_path = rules_dir / rule_file
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            total_rules += len(_RULE_PATTERN.findall(content))
            total_categories += len(_CATEGORY_PATTERN.findall(content))

    return (total_rules, total_categories)

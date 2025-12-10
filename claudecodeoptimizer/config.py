"""CCO Configuration - Single source of truth."""

import re
from pathlib import Path

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
    "CCO_ADAPTIVE_SOURCE",
    "SEPARATOR",
    "get_cco_commands",
    "get_cco_agents",
    "get_rules_breakdown",
    "get_content_path",
    "CCO_UNIVERSAL_PATTERN",
    "SUBPROCESS_TIMEOUT",
    "STATUSLINE_FILE",
    "SETTINGS_FILE",
    "LOCAL_CLAUDE_DIR",
    "LOCAL_SETTINGS_FILE",
    "LOCAL_STATUSLINE_FILE",
    "LOCAL_RULES_DIR",
    "CCO_PERMISSIONS_MARKER",
    "PATH_PATTERNS",
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
# On-demand rules (NOT installed globally - accessed via get_content_path())
CCO_TOOLS_SOURCE = "cco-tools.md"  # Used by CCO commands
CCO_ADAPTIVE_SOURCE = "cco-adaptive.md"  # Used by cco-tune for rule selection

STATUSLINE_FILE = CLAUDE_DIR / "statusline.js"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
SEPARATOR = "=" * 50

# Local project paths (relative to cwd)
LOCAL_CLAUDE_DIR = Path(".claude")
LOCAL_SETTINGS_FILE = LOCAL_CLAUDE_DIR / "settings.json"
LOCAL_STATUSLINE_FILE = LOCAL_CLAUDE_DIR / "statusline.js"
LOCAL_RULES_DIR = LOCAL_CLAUDE_DIR / "rules"  # .claude/rules/

# Path patterns for conditional rule loading (auto-detection based)
PATH_PATTERNS: dict[str, str] = {
    "python": "**/*.py",
    "typescript": "**/*.{ts,tsx}",
    "javascript": "**/*.{js,jsx}",
    "go": "**/*.go",
    "rust": "**/*.rs",
    "cli": "**/__main__.py, **/cli/**/*",
    "library": "**/src/**/*",
    "api": "**/routes/**/*, **/api/**/*",
    "operations": ".github/**/*, .gitlab-ci.yml",
    "testing": "tests/**/*.*, **/*.test.*, **/*_test.*",
    "frontend": "**/components/**/*, **/pages/**/*",
    "database": "**/models/**/*, **/migrations/**/*",
}

# CCO Permissions marker - used to identify CCO-installed permissions
# Permissions JSON has _meta.level field when installed by CCO
CCO_PERMISSIONS_MARKER = "_cco_managed"


def get_content_path(subdir: str) -> Path:
    """Get path to content subdirectory.

    Args:
        subdir: One of 'commands', 'agents', 'rules', 'statusline', 'permissions'

    Returns:
        Path to the content subdirectory
    """
    return Path(__file__).parent / "content" / subdir


# Universal CCO marker pattern - matches ANY cco_* marker block (case-insensitive)
# Used for backward compatibility: removes all CCO content regardless of marker name
# Matches: <!-- CCO_anything_START -->...<!-- CCO_anything_END -->
# Also: <!-- cco-anything-start -->...<!-- cco-anything-end -->
CCO_UNIVERSAL_PATTERN = (
    r"<!--\s*CCO[_-]\w+[_-]START\s*-->.*?<!--\s*CCO[_-]\w+[_-]END\s*-->\n?",
    re.DOTALL | re.IGNORECASE,
)

SUBPROCESS_TIMEOUT = 5  # seconds

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


def get_rules_count() -> tuple[int, int]:
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

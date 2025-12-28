"""CCO Configuration - Single source of truth.

Module Organization:
    - Path Constants (lines 31-130): Directory paths, file patterns, markers
    - Content Discovery (lines 133-191): Functions for finding CCO content files
    - JSON Utilities (lines 193-224): Load/save JSON with error handling
    - Rules Breakdown (lines 226-281): Rule counting and categorization
    - CLI Decorator (lines 283-309): Entry point exception handling
"""

import json
import os
import re
import sys
from collections.abc import Callable
from enum import Enum
from pathlib import Path

# Python 3.10 compatibility: StrEnum added in 3.11
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        """String enum for Python 3.10 compatibility."""

        def __str__(self) -> str:
            return str(self.value)


from typing import Any

from . import __version__

# Module-level target directory override (set by CLI for custom install location)
# WARNING: This global is for test mocking and CLI --dir option ONLY.
# NOT thread-safe - assumes single-threaded CLI usage. Do not use in concurrent contexts.
_TARGET_DIR_OVERRIDE: Path | None = None


def get_claude_dir() -> Path:
    """Get the Claude configuration directory.

    Resolution order:
    1. Module-level override (set via set_target_dir())
    2. CLAUDE_CONFIG_DIR environment variable
    3. Default: ~/.claude

    Returns:
        Path to Claude configuration directory.
    """
    if _TARGET_DIR_OVERRIDE is not None:
        return _TARGET_DIR_OVERRIDE
    if env_dir := os.environ.get("CLAUDE_CONFIG_DIR"):
        return Path(env_dir)
    return Path.home() / ".claude"


def set_target_dir(path: Path | None) -> None:
    """Set the target directory override for installation.

    WARNING: NOT thread-safe. This function modifies module-level global state
    and is intended for test mocking and CLI --dir option only.
    Do not call from concurrent code paths.

    Args:
        path: Target directory path, or None to clear override.
    """
    global _TARGET_DIR_OVERRIDE
    _TARGET_DIR_OVERRIDE = path


class ContentSubdir(StrEnum):
    """Valid subdirectories under content/."""

    COMMANDS = "command-templates"
    AGENTS = "agent-templates"
    RULES = "rules"
    STATUSLINE = "statusline"
    PERMISSIONS = "permissions"


__all__ = [
    "VERSION",
    "get_claude_dir",
    "set_target_dir",
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
    "ContentSubdir",
    "get_cco_commands",
    "get_cco_agents",
    "get_rules_breakdown",
    "get_content_path",
    "load_json_file",
    "save_json_file",
    "CCO_UNIVERSAL_PATTERN",
    "CCO_UNIVERSAL_PATTERN_COMPILED",
    "SUBPROCESS_TIMEOUT",
    "SUBPROCESS_TIMEOUT_PACKAGE",
    "SUBPROCESS_TIMEOUT_DEFAULT",
    "SUBPROCESS_TIMEOUT_PACKAGE_OPS",
    "MAX_CLAUDE_MD_SIZE",
    "STATUSLINE_FILE",
    "SETTINGS_FILE",
    "CCO_PERMISSIONS_MARKER",
    "cli_entrypoint",
]

VERSION = __version__  # Single source: __init__.py
CLAUDE_DIR = Path.home() / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
AGENTS_DIR = CLAUDE_DIR / "agents"

# CCO rules are namespaced in cco/ subdirectory to preserve user's custom rules
CCO_RULES_SUBDIR = "cco"
RULES_DIR = CLAUDE_DIR / "rules" / CCO_RULES_SUBDIR  # ~/.claude/rules/cco/
OLD_RULES_ROOT = CLAUDE_DIR / "rules"  # For cleanup of old root-level rules

# Rule files installed to ~/.claude/rules/cco/ (without cco- prefix)
# ONLY core.md and ai.md - always active, small enough for context
# tools.md and adaptive.md stay in pip package - read on-demand to avoid context bloat
CCO_RULE_NAMES = ("core.md", "ai.md")  # Installed globally (always active)
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


def get_content_path(subdir: ContentSubdir | str = "") -> Path:
    """Get path to content subdirectory.

    Args:
        subdir: ContentSubdir enum or string path. Use ContentSubdir for type safety:
            - ContentSubdir.COMMANDS -> 'command-templates'
            - ContentSubdir.AGENTS -> 'agent-templates'
            - ContentSubdir.RULES -> 'rules'
            - ContentSubdir.STATUSLINE -> 'statusline'
            - ContentSubdir.PERMISSIONS -> 'permissions'
            - "" for content root

    Returns:
        Path to the content subdirectory or content root if subdir is empty
    """
    base = Path(__file__).parent / "content"
    return base / str(subdir) if subdir else base


# Universal CCO marker pattern - matches ANY cco_* marker block (case-insensitive)
# Universal pattern: removes all CCO content regardless of marker name
# Matches: <!-- CCO_anything_START -->...<!-- CCO_anything_END -->
# Also: <!-- cco-anything-start -->...<!-- cco-anything-end -->
# ReDoS mitigation: File size limited to MAX_CLAUDE_MD_SIZE (1MB) before pattern application.
# The .*? quantifier is safe given this size constraint.
_CCO_PATTERN_STRING = r"<!--\s*CCO[_-]\w+[_-]START\s*-->.*?<!--\s*CCO[_-]\w+[_-]END\s*-->\n?"
CCO_UNIVERSAL_PATTERN = (_CCO_PATTERN_STRING, re.DOTALL | re.IGNORECASE)

# Pre-compiled pattern for performance
CCO_UNIVERSAL_PATTERN_COMPILED = re.compile(_CCO_PATTERN_STRING, re.DOTALL | re.IGNORECASE)

# Timeout constants (seconds) - configurable via environment variables
# SUBPROCESS_TIMEOUT_DEFAULT: For quick operations like git status, file operations (default: 5s)
# SUBPROCESS_TIMEOUT_PACKAGE_OPS: For long-running package operations like pip install/uninstall (default: 30s)
SUBPROCESS_TIMEOUT_DEFAULT = int(os.getenv("CCO_SUBPROCESS_TIMEOUT", "5"))
SUBPROCESS_TIMEOUT_PACKAGE_OPS = int(os.getenv("CCO_SUBPROCESS_TIMEOUT_PACKAGE", "30"))

# Legacy aliases for backward compatibility
SUBPROCESS_TIMEOUT = SUBPROCESS_TIMEOUT_DEFAULT
SUBPROCESS_TIMEOUT_PACKAGE = SUBPROCESS_TIMEOUT_PACKAGE_OPS

# File size limits for safety
# Security: File size limit prevents ReDoS attacks on regex-heavy operations
MAX_CLAUDE_MD_SIZE = 1_000_000  # 1MB

# Pre-compiled regex patterns for performance
# Rules use list format: - **Name**: Description (single format for simplicity)
_RULE_PATTERN = re.compile(r"^- \*\*\w+(?:-\w+)*\*\*:", re.MULTILINE)
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

    Raises:
        RuntimeError: If file write fails
    """
    try:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"Failed to write JSON to {path}: {e}") from e


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


def cli_entrypoint(func: Callable[..., int]) -> Callable[..., int]:
    """Decorator for CLI entry points with standard exception handling.

    Handles:
    - KeyboardInterrupt: Returns exit code 130
    - Exception: Prints error and returns exit code 1

    Args:
        func: CLI function to wrap

    Returns:
        Wrapped function with exception handling
    """

    def wrapper(*args: Any, **kwargs: Any) -> int:
        """Wrapper that handles exceptions and logging for CLI entry points."""
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nCancelled.")
            return 130
        except (OSError, RuntimeError, ValueError, TimeoutError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)
            return 1

    return wrapper

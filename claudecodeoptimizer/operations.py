"""Shared file removal operations for CCO setup and uninstall."""

import re
from pathlib import Path

from .config import (
    AGENTS_DIR,
    CCO_RULE_FILES,
    CCO_RULE_NAMES,
    CCO_UNIVERSAL_PATTERN_COMPILED,
    COMMANDS_DIR,
    OLD_RULES_ROOT,
    RULES_DIR,
)


def remove_command_files(path: Path | None = None, verbose: bool = True) -> int:
    """Remove all cco-*.md files from commands directory.

    Args:
        path: Path to commands directory. If None, uses global COMMANDS_DIR.
        verbose: If True, print progress messages during removal.

    Returns:
        Number of files removed.
    """
    if path is None:
        path = COMMANDS_DIR
    count = 0
    if path.exists():
        for f in path.glob("cco-*.md"):
            f.unlink()
            count += 1
    return count


def remove_agent_files(path: Path | None = None, verbose: bool = True) -> int:
    """Remove all cco-*.md files from agents directory.

    Args:
        path: Path to agents directory. If None, uses global AGENTS_DIR.
        verbose: If True, print progress messages during removal.

    Returns:
        Number of files removed.
    """
    if path is None:
        path = AGENTS_DIR
    count = 0
    if path.exists():
        for f in path.glob("cco-*.md"):
            f.unlink()
            count += 1
    return count


def remove_old_rules(path: Path | None = None, verbose: bool = True) -> int:
    """Remove old CCO rule files from rules root directory.

    Args:
        path: Path to old rules root directory. If None, uses global OLD_RULES_ROOT.
        verbose: If True, print progress messages during removal.

    Returns:
        Number of files removed.
    """
    if path is None:
        path = OLD_RULES_ROOT
    old_rule_files = CCO_RULE_FILES + ("cco-adaptive.md", "cco-tools.md")
    count = 0
    if path.exists():
        for rule_file in old_rule_files:
            rule_path = path / rule_file
            if rule_path.exists():
                rule_path.unlink()
                count += 1
    return count


def remove_new_rules(path: Path | None = None, verbose: bool = True) -> int:
    """Remove CCO rules from cco/ subdirectory.

    Args:
        path: Path to rules cco/ subdirectory. If None, uses global RULES_DIR.
        verbose: If True, print progress messages during removal.

    Returns:
        Number of files removed.
    """
    if path is None:
        path = RULES_DIR
    old_rule_names = CCO_RULE_NAMES + ("tools.md", "adaptive.md")
    count = 0
    if path.exists():
        for rule_name in old_rule_names:
            rule_path = path / rule_name
            if rule_path.exists():
                rule_path.unlink()
                count += 1
        # Remove empty cco/ directory
        if path.exists() and not any(path.iterdir()):
            path.rmdir()
    return count


def remove_all_cco_markers(content: str) -> tuple[str, int]:
    """Remove ALL CCO markers from content.

    Uses universal pattern to match any CCO marker regardless of name.
    Ensures clean upgrade from any previous installation.

    Args:
        content: Text content to clean.

    Returns:
        Tuple of (cleaned_content, removed_count)
    """
    matches = CCO_UNIVERSAL_PATTERN_COMPILED.findall(content)
    cleaned = CCO_UNIVERSAL_PATTERN_COMPILED.sub("", content)
    return cleaned, len(matches)


def clean_claude_md_markers(claude_md: Path) -> int:
    """Remove CCO markers from CLAUDE.md.

    Args:
        claude_md: Path to CLAUDE.md file.

    Returns:
        Number of markers removed.
    """
    if not claude_md.exists():
        return 0

    content = claude_md.read_text(encoding="utf-8")
    content, count = remove_all_cco_markers(content)

    if count > 0:
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md.write_text(content, encoding="utf-8")

    return count

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


def remove_command_files(commands_dir: Path | None = None) -> int:
    """Remove all cco-*.md files from commands directory.

    Args:
        commands_dir: Path to commands directory. If None, uses global COMMANDS_DIR.

    Returns:
        Number of files removed.
    """
    if commands_dir is None:
        commands_dir = COMMANDS_DIR
    count = 0
    if commands_dir.exists():
        for f in commands_dir.glob("cco-*.md"):
            f.unlink()
            count += 1
    return count


def remove_agent_files(agents_dir: Path | None = None) -> int:
    """Remove all cco-*.md files from agents directory.

    Args:
        agents_dir: Path to agents directory. If None, uses global AGENTS_DIR.

    Returns:
        Number of files removed.
    """
    if agents_dir is None:
        agents_dir = AGENTS_DIR
    count = 0
    if agents_dir.exists():
        for f in agents_dir.glob("cco-*.md"):
            f.unlink()
            count += 1
    return count


def remove_old_rules(old_rules_dir: Path | None = None) -> int:
    """Remove old CCO rule files from rules root directory.

    Args:
        old_rules_dir: Path to old rules root directory. If None, uses global OLD_RULES_ROOT.

    Returns:
        Number of files removed.
    """
    if old_rules_dir is None:
        old_rules_dir = OLD_RULES_ROOT
    old_rule_files = CCO_RULE_FILES + ("cco-adaptive.md", "cco-tools.md")
    count = 0
    if old_rules_dir.exists():
        for rule_file in old_rule_files:
            rule_path = old_rules_dir / rule_file
            if rule_path.exists():
                rule_path.unlink()
                count += 1
    return count


def remove_new_rules(new_rules_dir: Path | None = None) -> int:
    """Remove CCO rules from cco/ subdirectory.

    Args:
        new_rules_dir: Path to rules cco/ subdirectory. If None, uses global RULES_DIR.

    Returns:
        Number of files removed.
    """
    if new_rules_dir is None:
        new_rules_dir = RULES_DIR
    old_rule_names = CCO_RULE_NAMES + ("tools.md", "adaptive.md")
    count = 0
    if new_rules_dir.exists():
        for rule_name in old_rule_names:
            rule_path = new_rules_dir / rule_name
            if rule_path.exists():
                rule_path.unlink()
                count += 1
        # Remove empty cco/ directory
        if new_rules_dir.exists() and not any(new_rules_dir.iterdir()):
            new_rules_dir.rmdir()
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

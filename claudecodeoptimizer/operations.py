"""Shared file removal operations for CCO setup and uninstall."""

import re
from pathlib import Path

from .config import (
    AGENTS_DIR,
    CCO_UNIVERSAL_PATTERN_COMPILED,
    COMMANDS_DIR,
    OLD_RULES_ROOT,
    RULES_DIR,
)


def remove_command_files(path: Path | None = None) -> list[str]:
    """Remove all cco-*.md files from commands directory.

    Args:
        path: Path to commands directory. If None, uses global COMMANDS_DIR.

    Returns:
        List of removed filenames.

    Raises:
        RuntimeError: If any file fails to be removed.
    """
    if path is None:
        path = COMMANDS_DIR
    removed: list[str] = []
    if path.exists():
        for f in sorted(path.glob("cco-*.md")):
            f.unlink(missing_ok=True)
            # Verify deletion succeeded
            if f.exists():
                raise RuntimeError(f"Failed to remove {f}: file still exists")
            removed.append(f.name)
    return removed


def remove_agent_files(path: Path | None = None) -> list[str]:
    """Remove all cco-*.md files from agents directory.

    Args:
        path: Path to agents directory. If None, uses global AGENTS_DIR.

    Returns:
        List of removed filenames.

    Raises:
        RuntimeError: If any file fails to be removed.
    """
    if path is None:
        path = AGENTS_DIR
    removed: list[str] = []
    if path.exists():
        for f in sorted(path.glob("cco-*.md")):
            f.unlink(missing_ok=True)
            # Verify deletion succeeded
            if f.exists():
                raise RuntimeError(f"Failed to remove {f}: file still exists")
            removed.append(f.name)
    return removed


def remove_old_rules(path: Path | None = None) -> list[str]:
    """Remove old CCO rule files from rules root directory.

    Removes ALL cco-*.md files from rules/ root (old installation format).

    Args:
        path: Path to old rules root directory. If None, uses global OLD_RULES_ROOT.

    Returns:
        List of removed filenames.

    Raises:
        RuntimeError: If any file fails to be removed.
    """
    if path is None:
        path = OLD_RULES_ROOT
    removed: list[str] = []
    if path.exists():
        # Use glob to catch ALL cco-*.md files, not just known ones
        for f in sorted(path.glob("cco-*.md")):
            f.unlink(missing_ok=True)
            # Verify deletion succeeded
            if f.exists():
                raise RuntimeError(f"Failed to remove {f}: file still exists")
            removed.append(f.name)
    return removed


def remove_new_rules(path: Path | None = None) -> list[str]:
    """Remove CCO rules from cco/ subdirectory.

    Removes ALL .md files from rules/cco/ directory (CCO-owned directory).

    Args:
        path: Path to rules cco/ subdirectory. If None, uses global RULES_DIR.

    Returns:
        List of removed filenames (with cco/ prefix).

    Raises:
        RuntimeError: If any file fails to be removed.
    """
    if path is None:
        path = RULES_DIR
    removed: list[str] = []
    if path.exists():
        # Remove ALL .md files from cco/ subdirectory (CCO owns this directory)
        for f in sorted(path.glob("*.md")):
            f.unlink(missing_ok=True)
            # Verify deletion succeeded
            if f.exists():
                raise RuntimeError(f"Failed to remove {f}: file still exists")
            removed.append(f"cco/{f.name}")
        # Remove empty cco/ directory
        try:
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
        except OSError:
            pass  # Directory not empty or already removed
    return removed


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

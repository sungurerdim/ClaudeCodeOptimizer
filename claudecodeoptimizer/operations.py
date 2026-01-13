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


def _remove_files_by_glob(
    path: Path, pattern: str, prefix: str = "", remove_empty_dir: bool = False
) -> list[str]:
    """Remove files matching a glob pattern from a directory.

    Args:
        path: Directory to remove files from.
        pattern: Glob pattern to match files.
        prefix: Optional prefix for returned filenames.
        remove_empty_dir: If True, remove the directory if empty after removal.

    Returns:
        List of removed filenames.

    Raises:
        RuntimeError: If any file fails to be removed.
    """
    removed: list[str] = []
    if not path.exists():
        return removed

    for f in sorted(path.glob(pattern)):
        f.unlink(missing_ok=True)
        if f.exists():
            raise RuntimeError(f"Failed to remove {f}: file still exists")
        removed.append(f"{prefix}{f.name}" if prefix else f.name)

    if remove_empty_dir:
        try:
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
        except OSError:
            pass  # Directory not empty or already removed

    return removed


def remove_command_files(path: Path | None = None) -> list[str]:
    """Remove all cco-*.md files from commands directory."""
    return _remove_files_by_glob(path or COMMANDS_DIR, "cco-*.md")


def remove_agent_files(path: Path | None = None) -> list[str]:
    """Remove all cco-*.md files from agents directory."""
    return _remove_files_by_glob(path or AGENTS_DIR, "cco-*.md")


def remove_old_rules(path: Path | None = None) -> list[str]:
    """Remove old CCO rule files (cco-*.md) from rules root directory."""
    return _remove_files_by_glob(path or OLD_RULES_ROOT, "cco-*.md")


def remove_new_rules(path: Path | None = None) -> list[str]:
    """Remove CCO rules (*.md) from rules/cco/ subdirectory."""
    return _remove_files_by_glob(
        path or RULES_DIR, "*.md", prefix="cco/", remove_empty_dir=True
    )


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

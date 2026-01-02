"""CCO Install - Setup functions for commands, agents, and rules."""

import re
import shutil
from pathlib import Path

from .config import (
    CCO_RULE_FILES,
    CCO_RULE_NAMES,
    CCO_RULES_SUBDIR,
    ContentSubdir,
    get_claude_dir,
    get_content_path,
)
from .operations import (
    clean_claude_md_markers,
    remove_agent_files,
    remove_all_cco_markers,
    remove_command_files,
    remove_new_rules,
    remove_old_rules,
)


def _check_claude_dir(target_dir: Path | None = None, create: bool = False) -> str | None:
    """Check if target directory exists, optionally creating it.

    Args:
        target_dir: Target directory. If None, uses get_claude_dir().
        create: If True, create directory if it doesn't exist.

    Returns:
        Error message if directory doesn't exist and create=False, None if valid.
    """
    claude_dir = target_dir or get_claude_dir()
    if not claude_dir.exists():
        if create:
            claude_dir.mkdir(parents=True, exist_ok=True)
        else:
            return f"{claude_dir} not found. Run 'claude' first to initialize, or use --dir to specify target."
    return None


def clean_previous_installation(
    verbose: bool = True, target_dir: Path | None = None
) -> dict[str, int]:
    """Remove previous CCO commands, agents, and rules.

    This ensures a clean reinstall by removing:
    - All cco-*.md files in commands/ and agents/
    - CCO markers from CLAUDE.md
    - Rules from rules/ root (old location)
    - Rules from rules/cco/ (current location)

    NOTE: Does NOT touch settings.json or statusline.js.
    These are project-local in ./.claude/ only.

    Args:
        verbose: If True, print progress messages during cleanup.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        Dictionary with counts of removed items
    """
    claude_dir = target_dir or get_claude_dir()
    commands_dir = claude_dir / "commands"
    agents_dir = claude_dir / "agents"
    rules_root = claude_dir / "rules"
    rules_cco_dir = rules_root / CCO_RULES_SUBDIR

    # Collect removed items with details
    removed_commands = remove_command_files(commands_dir)
    removed_agents = remove_agent_files(agents_dir)
    removed_old_rules = remove_old_rules(rules_root)
    removed_new_rules = remove_new_rules(rules_cco_dir)

    # Remove CCO markers from CLAUDE.md
    claude_md = claude_dir / "CLAUDE.md"
    claude_md_count = clean_claude_md_markers(claude_md)

    # Build result dict (counts for backward compatibility)
    removed = {
        "commands": len(removed_commands),
        "agents": len(removed_agents),
        "rules": len(removed_old_rules) + len(removed_new_rules) + claude_md_count,
    }

    total = sum(removed.values())
    if verbose and total > 0:
        print("Cleaning previous installation...")
        if removed_commands:
            print(f"  Commands ({len(removed_commands)}):")
            for name in removed_commands:
                print(f"    - {name}")
        if removed_agents:
            print(f"  Agents ({len(removed_agents)}):")
            for name in removed_agents:
                print(f"    - {name}")
        if removed_old_rules or removed_new_rules:
            rule_count = len(removed_old_rules) + len(removed_new_rules)
            print(f"  Rules ({rule_count}):")
            for name in removed_old_rules:
                print(f"    - rules/{name}")
            for name in removed_new_rules:
                print(f"    - rules/{name}")
        if claude_md_count:
            print(f"  CLAUDE.md: {claude_md_count} marker(s) removed")
        print()

    return removed


def _setup_content(src_subdir: str, dest_dir: Path, verbose: bool = True) -> list[str]:
    """Copy cco-*.md files from source to destination directory.

    Idempotent: removes existing cco-*.md files before copying new ones.
    Safe for reinstall - always results in fresh content from current version.

    Args:
        src_subdir: Subdirectory name under content/ (e.g., 'command-templates', 'agent-templates')
        dest_dir: Target directory path (e.g., ~/.claude/commands/)
        verbose: If True, print progress messages during installation

    Returns:
        List of installed filenames (e.g., ['cco-optimize.md', 'cco-config.md'])
    """
    src = get_content_path(src_subdir)
    if not src.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Remove existing cco-*.md files (idempotent reinstall)
    for old in dest_dir.glob("cco-*.md"):
        old.unlink(missing_ok=True)
    installed = []
    for f in sorted(src.glob("cco-*.md")):
        shutil.copy2(f, dest_dir / f.name)
        installed.append(f.name)
        if verbose:
            print(f"  + {f.name}")
    return installed


def setup_commands(verbose: bool = True, target_dir: Path | None = None) -> list[str]:
    """Copy cco-*.md commands to target/commands/

    Args:
        verbose: If True, print progress messages.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        List of installed filenames.

    Raises:
        RuntimeError: If target directory doesn't exist.
    """
    claude_dir = target_dir or get_claude_dir()
    error = _check_claude_dir(claude_dir)
    if error:
        raise RuntimeError(error)
    return _setup_content(ContentSubdir.COMMANDS, claude_dir / "commands", verbose)


def setup_agents(verbose: bool = True, target_dir: Path | None = None) -> list[str]:
    """Copy cco-*.md agents to target/agents/

    Args:
        verbose: If True, print progress messages.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        List of installed filenames.

    Raises:
        RuntimeError: If target directory doesn't exist.
    """
    claude_dir = target_dir or get_claude_dir()
    error = _check_claude_dir(claude_dir)
    if error:
        raise RuntimeError(error)
    return _setup_content(ContentSubdir.AGENTS, claude_dir / "agents", verbose)


def setup_rules(verbose: bool = True, target_dir: Path | None = None) -> dict[str, int]:
    """Copy rule files to target/rules/cco/

    Installs to cco/ subdirectory (namespaced to preserve user's custom rules):
    - core.md (always active)
    - ai.md (always active)

    Note: tools.md and adaptive.md stay in pip package - embedded in commands/agents.

    Args:
        verbose: If True, print progress messages.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        Dictionary with installed counts per category

    Raises:
        RuntimeError: If target directory doesn't exist.
    """
    claude_dir = target_dir or get_claude_dir()
    error = _check_claude_dir(claude_dir)
    if error:
        raise RuntimeError(error)

    src_dir = get_content_path(ContentSubdir.RULES)
    if not src_dir.exists():
        return {"core": 0, "ai": 0, "tools": 0, "total": 0}

    # Create cco/ subdirectory
    rules_cco_dir = claude_dir / "rules" / CCO_RULES_SUBDIR
    rules_cco_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing CCO rule files from cco/ subdirectory
    for rule_name in CCO_RULE_NAMES:
        rule_path = rules_cco_dir / rule_name
        if rule_path.exists():
            rule_path.unlink(missing_ok=True)

    # Copy CCO rule files with new names (cco-core.md -> core.md)
    installed = {}

    for src_filename, dest_filename in zip(CCO_RULE_FILES, CCO_RULE_NAMES, strict=True):
        src_file = src_dir / src_filename
        if src_file.exists():
            shutil.copy2(src_file, rules_cco_dir / dest_filename)
            # Extract key: core.md -> core
            key = dest_filename.replace(".md", "")
            installed[key] = 1
            if verbose:
                print(f"  + cco/{dest_filename}")

    installed["total"] = sum(installed.values())
    return installed


def clean_claude_md(verbose: bool = True, target_dir: Path | None = None) -> int:
    """Clean CCO markers from target/CLAUDE.md.

    CCO no longer writes rules to CLAUDE.md - they're in rules/cco/.
    This function removes old CCO markers from previous installations.

    Args:
        verbose: If True, print progress messages during cleanup.
        target_dir: Target directory. If None, uses get_claude_dir().

    Returns:
        Number of markers removed
    """
    claude_dir = target_dir or get_claude_dir()
    claude_md = claude_dir / "CLAUDE.md"

    if not claude_md.exists():
        return 0

    content = claude_md.read_text(encoding="utf-8")
    content, removed_count = remove_all_cco_markers(content)

    if removed_count > 0:
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = content.strip()
        if content:
            claude_md.write_text(content + "\n", encoding="utf-8")
        else:
            # File is empty after removing CCO content - delete it
            claude_md.unlink(missing_ok=True)

        if verbose:
            print(f"  CLAUDE.md: cleaned {removed_count} old CCO marker(s)")

    return removed_count

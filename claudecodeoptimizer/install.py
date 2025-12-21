"""CCO Install - Setup functions for commands, agents, and rules."""

import shutil
from pathlib import Path

from .config import (
    AGENTS_DIR,
    CCO_RULE_FILES,
    CCO_RULE_NAMES,
    CLAUDE_DIR,
    COMMANDS_DIR,
    RULES_DIR,
    ContentSubdir,
    get_content_path,
)
from .operations import (
    clean_claude_md_markers,
    remove_agent_files,
    remove_command_files,
    remove_new_rules,
    remove_old_rules,
)


def _check_claude_dir() -> str | None:
    """Check if ~/.claude/ directory exists.

    Returns:
        Error message if directory doesn't exist, None if valid.
    """
    if not CLAUDE_DIR.exists():
        return "~/.claude/ not found. Run 'claude' first to initialize."
    return None


def clean_previous_installation(verbose: bool = True) -> dict[str, int]:
    """Remove previous CCO commands, agents, and rules.

    This ensures a clean reinstall by removing:
    - All cco-*.md files in commands/ and agents/
    - CCO markers from CLAUDE.md
    - Rules from ~/.claude/rules/ root (old location)
    - Rules from ~/.claude/rules/cco/ (current location)

    NOTE: Does NOT touch settings.json or statusline.js.
    These are project-local in ./.claude/ only.

    Args:
        verbose: If True, print progress messages during cleanup.

    Returns:
        Dictionary with counts of removed items
    """
    removed = {"commands": 0, "agents": 0, "rules": 0}

    # 1. Remove all cco-*.md files from commands/
    removed["commands"] = remove_command_files(COMMANDS_DIR)

    # 2. Remove all cco-*.md files from agents/
    removed["agents"] = remove_agent_files(AGENTS_DIR)

    # 3a. Remove old CCO rule files from root
    removed["rules"] += remove_old_rules()

    # 3b. Remove CCO rules from cco/ subdirectory (current)
    removed["rules"] += remove_new_rules(RULES_DIR)

    # 4. Remove CCO markers from CLAUDE.md
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    removed["rules"] += clean_claude_md_markers(claude_md)

    total = sum(removed.values())
    if verbose and total > 0:
        print("Cleaning previous installation...")
        if removed["commands"]:
            print(f"  - Removed {removed['commands']} command(s)")
        if removed["agents"]:
            print(f"  - Removed {removed['agents']} agent(s)")
        if removed["rules"]:
            print(f"  - Removed {removed['rules']} rule file(s)/section(s)")
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


def setup_commands(verbose: bool = True) -> list[str]:
    """Copy cco-*.md commands to ~/.claude/commands/

    Returns:
        List of installed filenames.

    Raises:
        RuntimeError: If ~/.claude/ directory doesn't exist.
    """
    error = _check_claude_dir()
    if error:
        raise RuntimeError(error)
    return _setup_content(ContentSubdir.COMMANDS, COMMANDS_DIR, verbose)


def setup_agents(verbose: bool = True) -> list[str]:
    """Copy cco-*.md agents to ~/.claude/agents/

    Returns:
        List of installed filenames.

    Raises:
        RuntimeError: If ~/.claude/ directory doesn't exist.
    """
    error = _check_claude_dir()
    if error:
        raise RuntimeError(error)
    return _setup_content(ContentSubdir.AGENTS, AGENTS_DIR, verbose)


def setup_rules(verbose: bool = True) -> dict[str, int]:
    """Copy rule files to ~/.claude/rules/cco/

    Installs to cco/ subdirectory (namespaced to preserve user's custom rules):
    - core.md (always active)
    - ai.md (always active)

    Note: tools.md and adaptive.md stay in pip package - embedded in commands/agents.

    Returns:
        Dictionary with installed counts per category

    Raises:
        RuntimeError: If ~/.claude/ directory doesn't exist.
    """
    error = _check_claude_dir()
    if error:
        raise RuntimeError(error)

    src_dir = get_content_path(ContentSubdir.RULES)
    if not src_dir.exists():
        return {"core": 0, "ai": 0, "tools": 0, "total": 0}

    # Create cco/ subdirectory
    RULES_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing CCO rule files from cco/ subdirectory
    for rule_name in CCO_RULE_NAMES:
        rule_path = RULES_DIR / rule_name
        if rule_path.exists():
            rule_path.unlink(missing_ok=True)

    # Copy CCO rule files with new names (cco-core.md -> core.md)
    installed = {}

    for src_filename, dest_filename in zip(CCO_RULE_FILES, CCO_RULE_NAMES, strict=True):
        src_file = src_dir / src_filename
        if src_file.exists():
            shutil.copy2(src_file, RULES_DIR / dest_filename)
            # Extract key: core.md -> core
            key = dest_filename.replace(".md", "")
            installed[key] = 1
            if verbose:
                print(f"  + cco/{dest_filename}")

    installed["total"] = sum(installed.values())
    return installed


def clean_claude_md(verbose: bool = True) -> int:
    """Clean CCO markers from ~/.claude/CLAUDE.md.

    CCO no longer writes rules to CLAUDE.md - they're in ~/.claude/rules/cco/.
    This function removes old CCO markers from previous installations.

    Args:
        verbose: If True, print progress messages during cleanup.

    Returns:
        Number of markers removed
    """
    from .operations import remove_all_cco_markers

    claude_md = CLAUDE_DIR / "CLAUDE.md"

    if not claude_md.exists():
        return 0

    content = claude_md.read_text(encoding="utf-8")
    content, removed_count = remove_all_cco_markers(content)

    if removed_count > 0:
        import re

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

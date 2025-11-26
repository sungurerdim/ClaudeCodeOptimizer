"""
Knowledge Setup - Global ~/.claude/ structure initialization

Creates:
- ~/.claude/commands/ (all cco-*.md from claudecodeoptimizer/content/commands/)
- ~/.claude/agents/ (all cco-*.md from claudecodeoptimizer/content/agents/)
- ~/.claude/CLAUDE.md (with inline CCO Rules)
- ~/.claude/*.cco (template files: settings.json.cco, statusline.js.cco)
"""

import re
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .. import config

# Consistent category ordering for all reports
# Agents → Commands → Templates
CATEGORY_ORDER = ["agents", "commands", "templates"]


def check_existing_installation() -> dict[str, int] | None:
    """
    Check if CCO is already installed.

    Returns:
        Dictionary with counts of existing files by category (in consistent order),
        or None if not installed.
        Example: {'agents': 3, 'commands': 10, 'skills': 26}
    """
    claude_dir = config.get_claude_dir()
    if not claude_dir.exists():
        return None

    # Use consistent ordering
    categories = {
        "agents": config.get_agents_dir(),
        "commands": config.get_global_commands_dir(),
        "templates": config.get_claude_dir(),  # Templates are in ~/.claude/ root
    }

    # Build counts dict in consistent order
    counts = {}
    for category in CATEGORY_ORDER:
        dir_path = categories[category]
        if dir_path.exists():
            # Count CCO files only
            if category == "templates":
                # Count template files (*.cco)
                count = sum(1 for _ in dir_path.glob("*.cco"))
            else:
                count = sum(1 for _ in dir_path.glob("cco-*.md"))

            if count > 0:
                counts[category] = count

    return counts if counts else None


def show_installation_diff() -> None:
    """
    Show what files will be overwritten during installation.
    """
    print("\n" + "=" * 60)
    print("FILES TO BE OVERWRITTEN")
    print("=" * 60)

    # Use consistent ordering: agents → commands → templates
    categories = [
        ("Agents", config.get_agents_dir(), "cco-*.md"),
        ("Commands", config.get_global_commands_dir(), "cco-*.md"),
        ("Templates", config.get_claude_dir(), "*.cco"),
    ]

    total_files = 0
    for category, dir_path, pattern in categories:
        if dir_path.exists():
            files = list(dir_path.glob(pattern))
            if files:
                print(f"\n  {category}: {len(files)} files")
                for file in sorted(files)[:3]:  # Show first 3
                    print(f"    • {file.name}")
                if len(files) > 3:
                    print(f"    • ... and {len(files) - 3} more")
                total_files += len(files)

    print("\n" + "-" * 60)
    print(f"  Total: {total_files} files will be overwritten")
    print("=" * 60)


def get_installation_counts() -> dict[str, int]:
    """
    Get current file counts for all CCO categories (in consistent order).

    Returns:
        Dictionary with counts by category in consistent order
        Example: {'agents': 3, 'commands': 10}
    """
    counts = {}

    # Use consistent ordering: agents → commands → templates
    categories_config = {
        "agents": config.get_agents_dir(),
        "commands": config.get_global_commands_dir(),
        "templates": config.get_claude_dir(),
    }

    for category in CATEGORY_ORDER:
        dir_path = categories_config[category]
        if dir_path.exists():
            if category == "templates":
                # Templates are *.cco files
                count = sum(1 for _ in dir_path.glob("*.cco"))
            else:
                # Agents and commands
                count = sum(1 for _ in dir_path.glob("cco-*.md"))

            if count > 0:
                counts[category] = count

    return counts


def _get_content_dir(subdir: str) -> Path:
    """Get content directory path for a given subdirectory."""
    package_dir = Path(__file__).parent.parent
    return package_dir / "content" / subdir


def _setup_files(
    source_dir: Path,
    dest_dir: Path,
    cleanup_patterns: list[str],
    copy_pattern: str,
    recursive_cleanup: bool = False,
    copy_filter: Callable[[Path], bool] | None = None,
) -> None:
    """
    Generic file setup with cleanup and copy.

    Args:
        source_dir: Source directory containing files to copy
        dest_dir: Destination directory
        cleanup_patterns: List of glob patterns for files to remove
        copy_pattern: Glob pattern for files to copy
        recursive_cleanup: Use rglob instead of glob for cleanup
        copy_filter: Optional filter function for copy (receives Path, returns bool)
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Content not found at {source_dir}")

    # Create directory if needed
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Remove old files (preserve user's other files)
    for pattern in cleanup_patterns:
        glob_func = dest_dir.rglob if recursive_cleanup else dest_dir.glob
        for old_file in glob_func(pattern):
            old_file.unlink()

    # Copy files
    for src_file in source_dir.glob(copy_pattern):
        if copy_filter is None or copy_filter(src_file):
            shutil.copy2(src_file, dest_dir / src_file.name)


def setup_global_knowledge() -> dict[str, Any]:
    """
    Initialize global ~/.claude/ directory structure for CCO.

    Copies all CCO files to ~/.claude/ and updates CLAUDE.md with inline CCO Rules.

    Returns:
        Dictionary with setup status including before/after counts
    """
    claude_dir = config.get_claude_dir()
    commands_dir = config.get_global_commands_dir()
    agents_dir = config.get_agents_dir()

    # Capture counts BEFORE setup
    counts_before = get_installation_counts()

    # Ensure base directory exists
    claude_dir.mkdir(parents=True, exist_ok=True)

    actions: list[str] = []

    # Setup all directories
    _setup_commands(commands_dir)
    actions.append("Copied command files to ~/.claude/commands/")

    _setup_agents(agents_dir)
    actions.append("Copied agent files to ~/.claude/agents/")

    # Setup CLAUDE.md with inline CCO Rules
    _setup_claude_md(claude_dir)
    actions.append("Updated ~/.claude/CLAUDE.md with CCO Rules")

    # Setup global templates as .cco files
    _setup_global_templates(claude_dir)
    actions.append("Copied template files (*.cco files for user customization)")

    # Capture counts AFTER setup
    counts_after = get_installation_counts()

    results: dict[str, Any] = {
        "success": True,
        "claude_dir": str(claude_dir),
        "actions": actions,
        "counts_before": counts_before,
        "counts_after": counts_after,
    }

    return results


def _setup_commands(commands_dir: Path) -> None:
    """
    Copy CCO command files to ~/.claude/commands/.

    Only removes cco-*.md files before copying to avoid touching user's other commands.
    Copies all cco-*.md from claudecodeoptimizer/content/commands/.
    """
    _setup_files(
        source_dir=_get_content_dir("commands"),
        dest_dir=commands_dir,
        cleanup_patterns=["cco-*.md"],
        copy_pattern="cco-*.md",
    )


def _setup_agents(agents_dir: Path) -> None:
    """
    Copy CCO agent files to ~/.claude/agents/.

    Only removes cco-*.md files before copying.
    Copies all cco-*.md from claudecodeoptimizer/content/agents/.
    """
    _setup_files(
        source_dir=_get_content_dir("agents"),
        dest_dir=agents_dir,
        cleanup_patterns=["cco-*.md"],
        copy_pattern="cco-*.md",
    )


def _setup_claude_md(claude_dir: Path) -> None:
    """
    Create or update ~/.claude/CLAUDE.md with inline CCO Rules.

    CCO Rules are minimal, research-based guidelines that complement Claude's
    built-in capabilities (Opus 4.5+). Rules focus on:
    - Cross-platform compatibility
    - Reference integrity for code changes
    - Verification protocols
    - Efficient file discovery patterns

    Format:
    <!-- CCO_RULES_START -->
    # CCO Rules
    ...inline rules...
    <!-- CCO_RULES_END -->
    """
    claude_md_path = claude_dir / "CLAUDE.md"

    # CCO Rules - minimal, research-based, complementing Claude's built-in capabilities
    # Based on: Anthropic best practices, community CLAUDE.md examples, Opus 4.5 capabilities
    cco_rules = """<!-- CCO_RULES_START -->
# CCO Rules

## Cross-Platform
- Forward slashes (/) for all paths
- Relative paths preferred
- Quote paths with spaces
- Git Bash commands over OS-specific

## Reference Integrity
Before delete/rename/move/modify:
1. Find ALL refs: definitions, callers, imports, types, tests, docs, configs
2. Update in order: definitions → types → callers → imports → tests → docs
3. Verify: grep old = 0, grep new = expected count

## Verification
- Accounting: total = completed + skipped + failed + cannot-do
- No "fixed" claims without Read/diff verification
- Verify agent outputs before accepting

## File Discovery

### Exclude from Search
**System & VCS:** .git, .svn, .hg, .DS_Store, Thumbs.db, *.log, *.tmp, *.bak, *.swp
**Build outputs:** dist, build, out, target, bin, obj, *.min.js, *.min.css, *.map
**Dependencies:** node_modules, vendor, packages, .gradle, .maven, .cargo
**Virtual envs:** venv, .venv, .env, env, __pycache__, *.pyc, *.pyo
**Caches:** .cache, .pytest_cache, .mypy_cache, .ruff_cache, .tox, .nox, .next, .nuxt, .turbo, .parcel-cache
**Coverage:** coverage, htmlcov, .coverage, .nyc_output, *.lcov
**IDE:** .idea, .vscode, .vs, *.sublime-*
**Binaries:** *.class, *.jar, *.war, *.dll, *.exe, *.so, *.dylib, *.o, *.whl, *.egg-info
**Lock files:** package-lock.json, yarn.lock, pnpm-lock.yaml, poetry.lock, Cargo.lock, go.sum, Gemfile.lock, composer.lock

### Discovery Stages
1. files_with_matches (discover)
2. content with -C (preview)
3. Read offset+limit (precise)

## Change Safety
- Commit/stash before bulk changes
- Test before → change → test after
- Max 10 files per batch, verify each

## Scope
- Define boundaries before starting
- Out-of-scope items → separate tasks
- One change = one purpose
<!-- CCO_RULES_END -->
"""

    # Read existing file or create new
    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding="utf-8")

        # Check for old principle markers and remove them
        if "<!-- CCO_PRINCIPLES_START -->" in existing_content:
            pattern = r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?"
            existing_content = re.sub(pattern, "", existing_content, flags=re.DOTALL)

        # Check if new rules markers exist
        if "<!-- CCO_RULES_START -->" in existing_content:
            # Replace existing rules section
            pattern = r"<!-- CCO_RULES_START -->.*?<!-- CCO_RULES_END -->\n?"
            new_content = re.sub(pattern, cco_rules, existing_content, flags=re.DOTALL)
        else:
            # Append rules section
            new_content = existing_content.rstrip() + "\n\n" + cco_rules
    else:
        # Create new file with rules
        new_content = cco_rules

    # Clean up excessive blank lines
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    # Write updated content
    claude_md_path.write_text(new_content, encoding="utf-8")


def get_available_commands() -> list[str]:
    """
    Get list of available CCO command files.

    Returns:
        List of command filenames without extension (e.g., ['status', 'help', ...])
    """
    commands_dir = config.get_global_commands_dir()
    if not commands_dir.exists():
        return []

    return [f.stem for f in commands_dir.glob("cco-*.md")]


def get_available_agents() -> list[str]:
    """
    Get list of available CCO agent files.

    Returns:
        List of agent filenames without extension
    """
    agents_dir = config.get_agents_dir()
    if not agents_dir.exists():
        return []

    return [f.stem for f in agents_dir.glob("cco-*.md")]


def _setup_global_templates(claude_dir: Path) -> None:
    """
    Copy global template files to ~/.claude/ as .cco files.

    Dynamically discovers *.template files and copies them as .cco files.
    User can manually copy/customize these templates.
    """
    package_dir = Path(__file__).parent.parent
    templates_dir = package_dir.parent / "templates"

    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found at {templates_dir}")

    # Dynamically discover and copy templates as .cco files
    for src_file in templates_dir.glob("*.template"):
        if src_file.is_file():
            # Convert .template to .cco (e.g., settings.json.template -> settings.json.cco)
            dest_name = src_file.name.replace(".template", ".cco")
            shutil.copy2(src_file, claude_dir / dest_name)

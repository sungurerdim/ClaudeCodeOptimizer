"""
Knowledge Setup - Global ~/.claude/ structure initialization

Creates:
- ~/.claude/commands/ (all cco-*.md from claudecodeoptimizer/content/commands/)
- ~/.claude/principles/ (all U_*, C_*, P_*.md from claudecodeoptimizer/content/principles/)
- ~/.claude/agents/ (all cco-*.md from claudecodeoptimizer/content/agents/)
- ~/.claude/skills/ (all cco-*.md from claudecodeoptimizer/content/skills/)
- ~/.claude/CLAUDE.md (with U_* and C_* principle markers)
- ~/.claude/settings.json.example (Claude Code configuration template)
- ~/.claude/statusline.js.example (Status line script template)
"""

import shutil
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .. import config


def check_existing_installation() -> Optional[Dict[str, int]]:
    """
    Check if CCO is already installed.

    Returns:
        Dictionary with counts of existing files by category, or None if not installed
        Example: {'commands': 10, 'skills': 26, 'agents': 3, 'principles': 15}
    """
    claude_dir = config.get_claude_dir()
    if not claude_dir.exists():
        return None

    counts = {}
    categories = {
        "commands": config.get_global_commands_dir(),
        "skills": config.get_skills_dir(),
        "agents": config.get_agents_dir(),
        "principles": config.get_principles_dir(),
    }

    for category, dir_path in categories.items():
        if dir_path.exists():
            # Count CCO files only
            if category == "principles":
                count = (
                    len(list(dir_path.glob("U_*.md")))
                    + len(list(dir_path.glob("C_*.md")))
                    + len(list(dir_path.glob("P_*.md")))
                )
            else:
                count = len(list(dir_path.glob("cco-*.md")))

            if count > 0:
                counts[category] = count

    return counts if counts else None


def show_installation_diff() -> None:
    """
    Show what files will be overwritten during installation.
    """
    print("\n[DIFF] Files that will be overwritten:")
    print()

    categories = {
        "Commands": (config.get_global_commands_dir(), "cco-*.md"),
        "Skills": (config.get_skills_dir(), "cco-*.md"),
        "Agents": (config.get_agents_dir(), "cco-*.md"),
        "Principles (U_*)": (config.get_principles_dir(), "U_*.md"),
        "Principles (C_*)": (config.get_principles_dir(), "C_*.md"),
        "Principles (P_*)": (config.get_principles_dir(), "P_*.md"),
    }

    total_files = 0
    for category, (dir_path, pattern) in categories.items():
        if dir_path.exists():
            files = list(dir_path.glob(pattern))
            if files:
                print(f"  {category}:")
                for file in sorted(files)[:5]:  # Show first 5
                    print(f"    - {file.name}")
                if len(files) > 5:
                    print(f"    ... and {len(files) - 5} more")
                total_files += len(files)
                print()

    print(f"Total: {total_files} files will be overwritten")


def get_installation_counts() -> Dict[str, int]:
    """
    Get current file counts for all CCO categories.

    Returns:
        Dictionary with counts by category
        Example: {'commands': 10, 'skills': 26, 'agents': 3, 'principles': 15}
    """
    counts = {}

    # Commands
    commands_dir = config.get_global_commands_dir()
    if commands_dir.exists():
        counts["commands"] = len(list(commands_dir.glob("cco-*.md")))

    # Skills (recursive - includes subdirectories)
    skills_dir = config.get_skills_dir()
    if skills_dir.exists():
        counts["skills"] = len(list(skills_dir.rglob("cco-*.md")))

    # Agents
    agents_dir = config.get_agents_dir()
    if agents_dir.exists():
        counts["agents"] = len(list(agents_dir.glob("cco-*.md")))

    # Principles (U_*, C_*, P_*)
    principles_dir = config.get_principles_dir()
    if principles_dir.exists():
        counts["principles"] = (
            len(list(principles_dir.glob("U_*.md")))
            + len(list(principles_dir.glob("C_*.md")))
            + len(list(principles_dir.glob("P_*.md")))
        )

    return counts


def _get_content_dir(subdir: str) -> Path:
    """Get content directory path for a given subdirectory."""
    package_dir = Path(__file__).parent.parent
    return package_dir / "content" / subdir


def _setup_files(
    source_dir: Path,
    dest_dir: Path,
    cleanup_patterns: List[str],
    copy_pattern: str,
    recursive_cleanup: bool = False,
    copy_filter: Optional[Callable[[Path], bool]] = None,
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


def setup_global_knowledge(force: bool = False) -> Dict[str, Any]:
    """
    Initialize global ~/.claude/ directory structure for CCO.

    Copies all CCO files to ~/.claude/ and updates CLAUDE.md with principle markers.

    Args:
        force: If True, regenerate even if already exists

    Returns:
        Dictionary with setup status including before/after counts
    """
    claude_dir = config.get_claude_dir()
    commands_dir = config.get_global_commands_dir()
    principles_dir = config.get_principles_dir()
    agents_dir = config.get_agents_dir()
    skills_dir = config.get_skills_dir()

    # Capture counts BEFORE setup
    counts_before = get_installation_counts()

    # Ensure base directory exists
    claude_dir.mkdir(parents=True, exist_ok=True)

    actions: List[str] = []

    # Setup all directories
    _setup_commands(commands_dir)
    actions.append("Copied command files to ~/.claude/commands/")

    _setup_principles(principles_dir)
    actions.append("Copied principle files to ~/.claude/principles/")

    _setup_agents(agents_dir)
    actions.append("Copied agent files to ~/.claude/agents/")

    _setup_skills(skills_dir)
    actions.append("Copied skill files to ~/.claude/skills/")

    # Setup CLAUDE.md with ONLY U_* and C_* markers
    _setup_claude_md(claude_dir, principles_dir)
    actions.append("Updated ~/.claude/CLAUDE.md with principle markers")

    # Setup global templates as .example files
    _setup_global_templates(claude_dir)
    actions.append("Copied template examples (*.example files for user customization)")

    # Capture counts AFTER setup
    counts_after = get_installation_counts()

    results: Dict[str, Any] = {
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


def _setup_principles(principles_dir: Path) -> None:
    """
    Copy CCO principle files to ~/.claude/principles/.

    Only removes U_*, C_*, P_*.md files before copying.
    Copies all [UCP]_*.md from claudecodeoptimizer/content/principles/.
    """

    def is_cco_principle(path: Path) -> bool:
        return (
            len(path.name) > 1
            and path.name[0] in ("U", "C", "P")
            and path.name[1] == "_"
        )

    _setup_files(
        source_dir=_get_content_dir("principles"),
        dest_dir=principles_dir,
        cleanup_patterns=["U_*.md", "C_*.md", "P_*.md"],
        copy_pattern="*.md",
        copy_filter=is_cco_principle,
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


def _setup_skills(skills_dir: Path) -> None:
    """
    Copy CCO skill files to ~/.claude/skills/.

    Only removes cco-*.md files before copying.
    Copies all cco-*.md from claudecodeoptimizer/content/skills/.
    """
    source_skills = _get_content_dir("skills")

    # Use helper for root-level files with recursive cleanup
    _setup_files(
        source_dir=source_skills,
        dest_dir=skills_dir,
        cleanup_patterns=["cco-*.md"],
        copy_pattern="cco-*.md",
        recursive_cleanup=True,
    )

    # Copy from subdirectories (language-specific skills)
    for subdir in source_skills.iterdir():
        if subdir.is_dir() and not subdir.name.startswith(("_", ".")):
            dest_subdir = skills_dir / subdir.name
            dest_subdir.mkdir(parents=True, exist_ok=True)

            for skill_file in subdir.glob("cco-*.md"):
                shutil.copy2(skill_file, dest_subdir / skill_file.name)


def _setup_claude_md(claude_dir: Path, principles_dir: Path) -> None:
    """
    Create or update ~/.claude/CLAUDE.md with CCO principle markers.

    ONLY adds markers for U_* (Universal) and C_* (Claude-specific) principles.
    P_* (Project-specific) principles are loaded dynamically by skills.

    Format:
    <!-- CCO_PRINCIPLES_START -->
    @principles/U_CHANGE_VERIFICATION.md
    @principles/U_COMPLETE_REPORTING.md
    ...
    @principles/C_AGENT_ORCHESTRATION_PATTERNS.md
    ...
    <!-- CCO_PRINCIPLES_END -->
    """
    claude_md_path = claude_dir / "CLAUDE.md"

    # Get all U_* and C_* principle files (sorted)
    u_principles = sorted(principles_dir.glob("U_*.md"))
    c_principles = sorted(principles_dir.glob("C_*.md"))

    # Build marker section - ONLY markers and principle references, nothing else
    marker_lines = ["<!-- CCO_PRINCIPLES_START -->"]

    # Add U_* principles
    for principle_file in u_principles:
        marker_lines.append(f"@principles/{principle_file.name}")

    # Add C_* principles
    for principle_file in c_principles:
        marker_lines.append(f"@principles/{principle_file.name}")

    marker_lines.append("<!-- CCO_PRINCIPLES_END -->")

    marker_content = "\n".join(marker_lines) + "\n"

    # Read existing file or create new
    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding="utf-8")

        # Check if markers exist
        if "<!-- CCO_PRINCIPLES_START -->" in existing_content:
            # Replace existing marker section
            import re

            pattern = r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?"
            new_content = re.sub(
                pattern, marker_content, existing_content, flags=re.DOTALL
            )
        else:
            # Append marker section
            new_content = existing_content.rstrip() + "\n\n" + marker_content
    else:
        # Create new file with just markers
        new_content = marker_content

    # Write updated content
    claude_md_path.write_text(new_content, encoding="utf-8")


def get_available_commands() -> List[str]:
    """
    Get list of available CCO command files.

    Returns:
        List of command filenames without extension (e.g., ['status', 'help', ...])
    """
    commands_dir = config.get_global_commands_dir()
    if not commands_dir.exists():
        return []

    return [f.stem for f in commands_dir.glob("cco-*.md")]


def get_available_agents() -> List[str]:
    """
    Get list of available CCO agent files.

    Returns:
        List of agent filenames without extension
    """
    agents_dir = config.get_agents_dir()
    if not agents_dir.exists():
        return []

    return [f.stem for f in agents_dir.glob("cco-*.md")]


def get_available_skills() -> List[str]:
    """
    Get list of available CCO skill files including language-specific ones.

    Returns:
        List of skill filenames without extension.
        Language-specific skills are returned as "language/skill-name".
    """
    skills_dir = config.get_skills_dir()
    if not skills_dir.exists():
        return []

    skills = []

    # Root level skills
    for f in skills_dir.glob("cco-*.md"):
        skills.append(f.stem)

    # Language-specific skills
    for subdir in skills_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith(("_", ".")):
            for f in subdir.glob("cco-*.md"):
                skills.append(f"{subdir.name}/{f.stem}")

    return skills


def _setup_global_templates(claude_dir: Path) -> None:
    """
    Copy global template files to ~/.claude/ as .example files.

    User can manually copy/customize these templates:
    - settings.json.example → settings.json (Claude Code configuration)
    - statusline.js.example → statusline.js (Status line script)

    Templates are always updated to ensure users have latest examples.
    """
    package_dir = Path(__file__).parent.parent
    templates_dir = package_dir.parent / "templates"

    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found at {templates_dir}")

    # Copy templates as .example files (always update to provide latest)
    templates_to_copy = [
        ("statusline.js.template", "statusline.js.example"),
        ("settings.json.template", "settings.json.example"),
    ]

    for src_name, dest_name in templates_to_copy:
        src_file = templates_dir / src_name
        dest_file = claude_dir / dest_name
        if src_file.exists():
            shutil.copy2(src_file, dest_file)

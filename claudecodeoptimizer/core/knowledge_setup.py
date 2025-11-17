"""
Knowledge Setup - Global ~/.claude/ structure initialization

Creates:
- ~/.claude/commands/ (all cco-*.md from claudecodeoptimizer/content/commands/)
- ~/.claude/principles/ (all U_*, C_*, P_*.md from claudecodeoptimizer/content/principles/)
- ~/.claude/agents/ (all cco-*.md from claudecodeoptimizer/content/agents/)
- ~/.claude/skills/ (all cco-*.md from claudecodeoptimizer/content/skills/)
- ~/.claude/CLAUDE.md (with U_* and C_* principle markers)
"""

import shutil
from pathlib import Path
from typing import Any, Dict, List

from .. import config


def setup_global_knowledge(force: bool = False) -> Dict[str, Any]:
    """
    Initialize global ~/.claude/ directory structure for CCO.

    Copies all CCO files to ~/.claude/ and updates CLAUDE.md with principle markers.

    Args:
        force: If True, regenerate even if already exists

    Returns:
        Dictionary with setup status
    """
    claude_dir = config.get_claude_dir()
    commands_dir = config.get_global_commands_dir()
    principles_dir = config.get_principles_dir()
    agents_dir = config.get_agents_dir()
    skills_dir = config.get_skills_dir()

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

    results: Dict[str, Any] = {
        "success": True,
        "claude_dir": str(claude_dir),
        "actions": actions,
    }

    return results


def _setup_commands(commands_dir: Path) -> None:
    """
    Copy CCO command files to ~/.claude/commands/.

    Only removes cco-*.md files before copying to avoid touching user's other commands.
    Copies all cco-*.md from claudecodeoptimizer/content/commands/.
    """
    # Get source directory
    package_dir = Path(__file__).parent.parent
    source_commands = package_dir / "content" / "commands"

    if not source_commands.exists():
        raise FileNotFoundError(f"Content commands not found at {source_commands}")

    # Create directory if needed
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Remove ONLY cco-*.md files (preserve user's other commands)
    for old_file in commands_dir.glob("cco-*.md"):
        old_file.unlink()

    # Copy all cco-*.md files
    for command_file in source_commands.glob("cco-*.md"):
        dest_file = commands_dir / command_file.name
        shutil.copy2(command_file, dest_file)


def _setup_principles(principles_dir: Path) -> None:
    """
    Copy CCO principle files to ~/.claude/principles/.

    Only removes U_*, C_*, P_*.md files before copying.
    Copies all [UCP]_*.md from claudecodeoptimizer/content/principles/.
    """
    # Get source directory
    package_dir = Path(__file__).parent.parent
    source_principles = package_dir / "content" / "principles"

    if not source_principles.exists():
        raise FileNotFoundError(f"Content principles not found at {source_principles}")

    # Create directory if needed
    principles_dir.mkdir(parents=True, exist_ok=True)

    # Remove ONLY CCO principle files (preserve user's other principles)
    for pattern in ["U_*.md", "C_*.md", "P_*.md"]:
        for old_file in principles_dir.glob(pattern):
            old_file.unlink()

    # Copy all principle files
    for principle_file in source_principles.glob("*.md"):
        # Only copy U_*, C_*, P_* files
        if principle_file.name[0] in ("U", "C", "P") and principle_file.name[1] == "_":
            dest_file = principles_dir / principle_file.name
            shutil.copy2(principle_file, dest_file)


def _setup_agents(agents_dir: Path) -> None:
    """
    Copy CCO agent files to ~/.claude/agents/.

    Only removes cco-*.md files before copying.
    Copies all cco-*.md from claudecodeoptimizer/content/agents/.
    """
    # Get source directory
    package_dir = Path(__file__).parent.parent
    source_agents = package_dir / "content" / "agents"

    if not source_agents.exists():
        raise FileNotFoundError(f"Content agents not found at {source_agents}")

    # Create directory if needed
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Remove ONLY cco-*.md files (preserve user's other agents)
    for old_file in agents_dir.glob("cco-*.md"):
        old_file.unlink()

    # Copy all cco-*.md files
    for agent_file in source_agents.glob("cco-*.md"):
        dest_file = agents_dir / agent_file.name
        shutil.copy2(agent_file, dest_file)


def _setup_skills(skills_dir: Path) -> None:
    """
    Copy CCO skill files to ~/.claude/skills/.

    Only removes cco-*.md files before copying.
    Copies all cco-*.md from claudecodeoptimizer/content/skills/.
    """
    # Get source directory
    package_dir = Path(__file__).parent.parent
    source_skills = package_dir / "content" / "skills"

    if not source_skills.exists():
        raise FileNotFoundError(f"Content skills not found at {source_skills}")

    # Create directory if needed
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Remove ONLY cco-*.md files recursively (preserve user's other skills)
    for old_file in skills_dir.rglob("cco-*.md"):
        old_file.unlink()

    # Copy all cco-*.md files from root
    for skill_file in source_skills.glob("cco-*.md"):
        dest_file = skills_dir / skill_file.name
        shutil.copy2(skill_file, dest_file)

    # Copy from subdirectories (language-specific skills)
    for subdir in source_skills.iterdir():
        if subdir.is_dir() and not subdir.name.startswith(("_", ".")):
            # Create subdirectory in destination
            dest_subdir = skills_dir / subdir.name
            dest_subdir.mkdir(parents=True, exist_ok=True)

            # Copy all cco-*.md files from this subdirectory
            for skill_file in subdir.glob("cco-*.md"):
                dest_file = dest_subdir / skill_file.name
                shutil.copy2(skill_file, dest_file)


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
            new_content = re.sub(pattern, marker_content, existing_content, flags=re.DOTALL)
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

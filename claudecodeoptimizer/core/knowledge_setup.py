"""
Knowledge Setup - Global CCO structure initialization

Ensures ~/.cco/ structure exists with:
- commands/ (copied from content/)
- guides/ (copied from content/)
- principles/ (copied from content/)
- agents/ (copied from content/)
- skills/ (copied from content/)

All content now lives in single content/ directory (single source of truth).
"""

import shutil
from pathlib import Path
from typing import Any, Dict

from .. import config


def setup_global_knowledge(force: bool = False) -> Dict[str, Any]:
    """
    Initialize global CCO directory structure.

    Creates:
    - ~/.cco/commands/ (slash commands from content/commands/)
    - ~/.cco/guides/ (static guides from content/guides/)
    - ~/.cco/principles/ (category files from content/principles/)
    - ~/.cco/agents/ (agent templates from content/agents/)
    - ~/.cco/skills/ (skills from content/skills/)

    All content copied from single content/ directory (single source of truth).

    Args:
        force: If True, regenerate even if already exists

    Returns:
        Dictionary with setup status
    """
    global_dir = config.get_global_dir()
    commands_dir = config.get_global_commands_dir()
    guides_dir = config.get_guides_dir()
    principles_dir = config.get_principles_dir()
    agents_dir = config.get_agents_dir()
    skills_dir = config.get_skills_dir()
    templates_dir = config.get_templates_dir()

    # Ensure global directory exists
    global_dir.mkdir(parents=True, exist_ok=True)

    # ALWAYS regenerate content on pip install to ensure freshness
    # This prevents stale files from lingering after updates

    actions: list[str] = []

    # Setup templates/ (deploy with .template extensions removed)
    _setup_templates(templates_dir)
    actions.append("Deployed template files")

    # Setup commands/
    _setup_commands(commands_dir)
    actions.append("Copied command files")

    # Setup guides/
    _setup_guides(guides_dir)
    actions.append("Copied guide files")

    # Setup principles/
    _setup_principles(principles_dir)
    actions.append("Generated principles files")

    # Setup agents/ (with templates)
    _setup_agents(agents_dir)
    actions.append("Setup agents directory")

    # Setup skills/ (with templates)
    _setup_skills(skills_dir)
    actions.append("Setup skills directory")

    # Setup ~/.claude/ symlinks for universal agents (Claude Code integration)
    _setup_claude_home_links()
    actions.append("Setup ~/.claude/ symlinks for universal agents")

    results: Dict[str, Any] = {
        "success": True,
        "global_dir": str(global_dir),
        "actions": actions,
    }

    return results


def _setup_templates(templates_dir: Path) -> None:
    """
    Deploy template files from package to global directory.

    Templates are deployed with .template extension REMOVED:
    - CLAUDE.md.template → ~/.cco/templates/CLAUDE.md
    - etc.

    Projects will link directly to these deployed files (without .template extension).

    IMPORTANT: Removes entire directory first to ensure clean slate.
    """
    # Get package templates directory
    package_dir = Path(__file__).parent.parent
    source_templates = package_dir.parent / "templates"

    if not source_templates.exists():
        raise FileNotFoundError(f"Template directory not found at {source_templates}")

    # CLEANUP: Remove entire directory for clean slate
    if templates_dir.exists():
        shutil.rmtree(templates_dir)

    # Create fresh directory
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Deploy all .template files (remove .template extension)
    for template_file in source_templates.glob("*.template"):
        # Remove .template extension for deployment
        dest_name = template_file.name.replace(".template", "")
        dest_file = templates_dir / dest_name
        shutil.copy2(template_file, dest_file)


def _setup_principles(principles_dir: Path) -> None:
    """
    Copy individual principle files from content to global directory.

    Copies all principle files:
    - U*.md (universal principles - always included)
    - P*.md (project-specific principles - AI-selected)
    from content/principles/ to ~/.cco/principles/

    IMPORTANT: Removes entire directory first to ensure clean slate.

    See README.md for current principle counts.
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_principles = package_dir.parent / "content" / "principles"

    if not source_principles.exists():
        raise FileNotFoundError(f"Content principles not found at {source_principles}")

    # CLEANUP: Remove entire directory for clean slate
    if principles_dir.exists():
        shutil.rmtree(principles_dir)

    # Create fresh directory
    principles_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for principle_file in source_principles.glob("*.md"):
        dest_file = principles_dir / principle_file.name
        shutil.copy2(principle_file, dest_file)


def _setup_commands(commands_dir: Path) -> None:
    """
    Copy command files from content to global directory.

    Copies from content/commands/ to ~/.cco/commands/

    IMPORTANT: Removes entire directory first to ensure clean slate.
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_commands = package_dir.parent / "content" / "commands"

    if not source_commands.exists():
        raise FileNotFoundError(f"Content commands not found at {source_commands}")

    # CLEANUP: Remove entire directory for clean slate
    if commands_dir.exists():
        shutil.rmtree(commands_dir)

    # Create fresh directory
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for command_file in source_commands.glob("*.md"):
        dest_file = commands_dir / command_file.name
        shutil.copy2(command_file, dest_file)


def _setup_guides(guides_dir: Path) -> None:
    """
    Copy guide files from content to global directory.

    Copies from content/guides/ to ~/.cco/guides/

    IMPORTANT: Removes entire directory first to ensure clean slate.
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_guides = package_dir.parent / "content" / "guides"

    if not source_guides.exists():
        raise FileNotFoundError(f"Content guides not found at {source_guides}")

    # CLEANUP: Remove entire directory for clean slate
    if guides_dir.exists():
        shutil.rmtree(guides_dir)

    # Create fresh directory
    guides_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for guide_file in source_guides.glob("*.md"):
        dest_file = guides_dir / guide_file.name
        shutil.copy2(guide_file, dest_file)


def _setup_agents(agents_dir: Path) -> None:
    """
    Copy agent templates from content to global directory.

    Copies from content/agents/ to ~/.cco/agents/

    IMPORTANT: Removes entire directory first to ensure clean slate.
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_agents = package_dir.parent / "content" / "agents"

    if not source_agents.exists():
        raise FileNotFoundError(f"Content agents not found at {source_agents}")

    # CLEANUP: Remove entire directory for clean slate
    if agents_dir.exists():
        shutil.rmtree(agents_dir)

    # Create fresh directory
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files (templates and README)
    for agent_file in source_agents.glob("*.md"):
        dest_file = agents_dir / agent_file.name
        shutil.copy2(agent_file, dest_file)


def _setup_skills(skills_dir: Path) -> None:
    """
    Copy skill files from content to global directory.

    Copies from content/skills/ including:
    - General skills (*.md files in root)
    - Language-specific skills (subdirectories: python/, go/, rust/, typescript/)
    - Skill registry and Python integration code

    IMPORTANT: Removes entire directory first to ensure clean slate.
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_skills = package_dir.parent / "content" / "skills"

    if not source_skills.exists():
        raise FileNotFoundError(f"Content skills not found at {source_skills}")

    # CLEANUP: Remove entire directory for clean slate
    if skills_dir.exists():
        shutil.rmtree(skills_dir)

    # Create fresh directory
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files from root (general skills)
    for skill_file in source_skills.glob("*.md"):
        dest_file = skills_dir / skill_file.name
        shutil.copy2(skill_file, dest_file)

    # Copy language-specific skills from subdirectories
    for lang_dir in source_skills.iterdir():
        if lang_dir.is_dir() and not lang_dir.name.startswith(("_", ".")):
            # Skip __pycache__, __init__, etc
            # Create language subdirectory in destination
            dest_lang_dir = skills_dir / lang_dir.name
            dest_lang_dir.mkdir(parents=True, exist_ok=True)

            # Copy all .md files from this language directory
            for skill_file in lang_dir.glob("*.md"):
                dest_file = dest_lang_dir / skill_file.name
                shutil.copy2(skill_file, dest_file)


def _setup_claude_home_links() -> None:
    """
    Setup symlinks in ~/.claude/ for universal/global content.

    Creates links for:
    - ~/.claude/agents/ → symlinks to all agents from ~/.cco/agents/

    This enables Claude Code to automatically discover and use CCO agents
    without per-project configuration.
    """
    import platform

    from .. import config

    claude_dir = config.get_claude_dir()
    cco_agents_dir = config.get_agents_dir()

    # Only proceed if CCO agents exist
    if not cco_agents_dir.exists():
        return

    # Create ~/.claude/agents/ directory
    claude_agents_dir = claude_dir / "agents"
    claude_agents_dir.mkdir(parents=True, exist_ok=True)

    # Link all agent files from ~/.cco/agents/ to ~/.claude/agents/
    for agent_file in cco_agents_dir.glob("*.md"):
        # Skip templates and README
        if agent_file.name.startswith("_template") or agent_file.name == "README.md":
            continue

        source = agent_file.resolve()
        target = (claude_agents_dir / agent_file.name).resolve()

        # Path traversal validation
        if not str(source).startswith(str(cco_agents_dir.resolve())):
            continue  # Skip files outside expected directory
        if not str(target).startswith(str(claude_agents_dir.resolve())):
            continue  # Skip targets outside expected directory

        # Remove existing symlink/file if exists
        if target.exists() or target.is_symlink():
            target.unlink()

        # Create symlink (cross-platform)
        try:
            if platform.system() == "Windows":
                # Windows: use mklink
                import subprocess

                # Safe: cmd is built-in Windows command, paths are validated and sanitized above
                subprocess.run(  # noqa: S603
                    [  # noqa: S607 - cmd is built-in Windows command
                        "cmd",
                        "/c",
                        "mklink",
                        str(target),
                        str(source),
                    ],
                    check=True,
                    capture_output=True,
                )
            else:
                # Unix: use symlink_to
                target.symlink_to(source)
        except Exception:
            # If symlink fails, copy the file instead (fallback)
            shutil.copy2(source, target)


def get_principle_categories() -> list[str]:
    """
    Get list of available principle categories dynamically from principle files.

    Returns:
        List of category IDs found in principle files (e.g., ['code_quality', 'security_privacy', 'testing'])
    """
    import re

    principles_dir = config.get_principles_dir()
    if not principles_dir.exists():
        return []

    categories = set()

    # Scan all P*.md files to extract unique categories
    for p_file in principles_dir.glob("P*.md"):
        try:
            content = p_file.read_text(encoding="utf-8")
            # Look for category: line in frontmatter
            match = re.search(r"category:\s*([^\n]+)", content)
            if match:
                cat = match.group(1).strip()
                categories.add(cat)
        except Exception as e:
            # Skip malformed files - log and continue
            import logging

            logging.debug(f"Failed to parse principle file {p_file}: {e}")
            continue

    return sorted(categories)


def get_available_commands() -> list[str]:
    """
    Get list of available command files.

    Returns:
        List of command filenames without extension (e.g., ['audit', 'fix', ...])
    """
    commands_dir = config.get_global_commands_dir()
    if not commands_dir.exists():
        return []

    return [f.stem for f in commands_dir.glob("*.md")]


def get_available_guides() -> list[str]:
    """
    Get list of available guide files.

    Returns:
        List of guide filenames without extension (e.g., ['verification-protocol', ...])
    """
    guides_dir = config.get_guides_dir()
    if not guides_dir.exists():
        return []

    return [f.stem for f in guides_dir.glob("*.md")]


def get_available_agents() -> list[str]:
    """
    Get list of available agent files.

    Returns:
        List of agent filenames without extension (excludes templates and README)
    """
    agents_dir = config.get_agents_dir()
    if not agents_dir.exists():
        return []

    return [
        f.stem
        for f in agents_dir.glob("*.md")
        if f.name != "README.md" and not f.name.startswith("_template")
    ]


def get_available_skills() -> list[str]:
    """
    Get list of available skill files.

    Returns:
        List of skill filenames without extension (excludes templates and README)
    """
    skills_dir = config.get_skills_dir()
    if not skills_dir.exists():
        return []

    return [
        f.stem
        for f in skills_dir.glob("*.md")
        if f.name != "README.md" and not f.name.startswith("_template")
    ]

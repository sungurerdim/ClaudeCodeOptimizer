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

    results = {
        "success": True,
        "global_dir": str(global_dir),
        "actions": [],
    }

    # Ensure global directory exists
    global_dir.mkdir(parents=True, exist_ok=True)

    # Setup templates/ (deploy with .template extensions removed)
    if force or not templates_dir.exists() or not (templates_dir / "settings.json").exists():
        _setup_templates(templates_dir)
        results["actions"].append("Deployed template files")

    # Setup commands/
    if force or not commands_dir.exists() or not list(commands_dir.glob("*.md")):
        _setup_commands(commands_dir)
        results["actions"].append("Copied command files")

    # Setup guides/
    if force or not guides_dir.exists() or not list(guides_dir.glob("*.md")):
        _setup_guides(guides_dir)
        results["actions"].append("Copied guide files")

    # Setup principles/
    if force or not principles_dir.exists() or not list(principles_dir.glob("*.md")):
        _setup_principles(principles_dir)
        results["actions"].append("Generated principles category files")

    # Setup agents/ (with templates)
    if force or not agents_dir.exists() or not (agents_dir / "README.md").exists():
        _setup_agents(agents_dir)
        results["actions"].append("Setup agents directory with templates")

    # Setup skills/ (with templates)
    if force or not skills_dir.exists() or not (skills_dir / "README.md").exists():
        _setup_skills(skills_dir)
        results["actions"].append("Setup skills directory with templates")

    if not results["actions"]:
        results["actions"].append("Knowledge base already up to date")

    return results


def _setup_templates(templates_dir: Path) -> None:
    """
    Deploy template files from package to global directory.

    Templates are deployed with .template extension REMOVED:
    - statusline.js.template → ~/.cco/templates/statusline.js
    - settings.json.template → ~/.cco/templates/settings.json
    - CLAUDE.md.template → ~/.cco/templates/CLAUDE.md
    - etc.

    Projects will link directly to these deployed files (without .template extension).
    """
    # Get package templates directory
    package_dir = Path(__file__).parent.parent
    source_templates = package_dir.parent / "templates"

    if not source_templates.exists():
        raise FileNotFoundError(f"Template directory not found at {source_templates}")

    # Create destination
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

    Copies 74 individual principle files (P001.md - P074.md) from
    content/principles/ to ~/.cco/principles/
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_principles = package_dir.parent / "content" / "principles"

    if not source_principles.exists():
        raise FileNotFoundError(f"Content principles not found at {source_principles}")

    # Create destination
    principles_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for principle_file in source_principles.glob("*.md"):
        dest_file = principles_dir / principle_file.name
        shutil.copy2(principle_file, dest_file)


def _setup_commands(commands_dir: Path) -> None:
    """
    Copy command files from content to global directory.

    Copies from content/commands/ to ~/.cco/commands/
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_commands = package_dir.parent / "content" / "commands"

    if not source_commands.exists():
        raise FileNotFoundError(f"Content commands not found at {source_commands}")

    # Create destination
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for command_file in source_commands.glob("*.md"):
        dest_file = commands_dir / command_file.name
        shutil.copy2(command_file, dest_file)


def _setup_guides(guides_dir: Path) -> None:
    """
    Copy guide files from content to global directory.

    Copies from content/guides/ to ~/.cco/guides/
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_guides = package_dir.parent / "content" / "guides"

    if not source_guides.exists():
        raise FileNotFoundError(f"Content guides not found at {source_guides}")

    # Create destination
    guides_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for guide_file in source_guides.glob("*.md"):
        dest_file = guides_dir / guide_file.name
        shutil.copy2(guide_file, dest_file)


def _setup_agents(agents_dir: Path) -> None:
    """
    Copy agent templates from content to global directory.

    Copies from content/agents/ to ~/.cco/agents/
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_agents = package_dir.parent / "content" / "agents"

    if not source_agents.exists():
        raise FileNotFoundError(f"Content agents not found at {source_agents}")

    # Create destination
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
    """
    # Get content directory
    package_dir = Path(__file__).parent.parent
    source_skills = package_dir.parent / "content" / "skills"

    if not source_skills.exists():
        raise FileNotFoundError(f"Content skills not found at {source_skills}")

    # Create destination
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


def get_principle_categories() -> list[str]:
    """
    Get list of available principle categories.

    Returns:
        List of category IDs (e.g., ['core', 'security', 'testing'])
    """
    return [
        "core",
        "code_quality",
        "security",
        "testing",
        "architecture",
        "performance",
        "operations",
        "git_workflow",
        "api_design",
    ]


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
        f.stem for f in agents_dir.glob("*.md")
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
        f.stem for f in skills_dir.glob("*.md")
        if f.name != "README.md" and not f.name.startswith("_template")
    ]

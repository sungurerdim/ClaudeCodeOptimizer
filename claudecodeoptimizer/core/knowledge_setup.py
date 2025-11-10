"""
Knowledge Setup - Global knowledge base initialization

Ensures ~/.cco/knowledge/ structure exists with:
- commands/ (copied from package)
- guides/ (copied from package)
- principles/ (generated from principles.json)
- agents/ (created empty, user can add custom)
- skills/ (created empty, user can add custom)
"""

import shutil
from pathlib import Path
from typing import Any, Dict

from .. import config


def setup_global_knowledge(force: bool = False) -> Dict[str, Any]:
    """
    Initialize global knowledge directory structure.

    Creates:
    - ~/.cco/knowledge/commands/ (slash commands from package)
    - ~/.cco/knowledge/guides/ (static guides from package)
    - ~/.cco/knowledge/principles/ (category files from principles.json)
    - ~/.cco/knowledge/agents/ (empty, for custom agents)
    - ~/.cco/knowledge/skills/ (empty, for custom skills)

    Args:
        force: If True, regenerate even if already exists

    Returns:
        Dictionary with setup status
    """
    knowledge_dir = config.get_knowledge_dir()
    commands_dir = config.get_knowledge_commands_dir()
    guides_dir = config.get_guides_dir()
    principles_dir = config.get_principles_dir()
    agents_dir = config.get_agents_dir()
    skills_dir = config.get_skills_dir()

    results = {
        "success": True,
        "knowledge_dir": str(knowledge_dir),
        "actions": [],
    }

    # Create knowledge base directory
    knowledge_dir.mkdir(parents=True, exist_ok=True)

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


def _setup_principles(principles_dir: Path) -> None:
    """
    Generate principle category files in global directory.

    Reads from principles.json and generates category-specific files.
    """
    from .principle_selector import PrincipleSelector

    # Create selector with empty preferences (we want all principles for global storage)
    selector = PrincipleSelector({})

    # Generate category files
    principles_dir.mkdir(parents=True, exist_ok=True)
    selector.generate_category_files(principles_dir)


def _setup_commands(commands_dir: Path) -> None:
    """
    Copy command files from package to global directory.

    Copies from claudecodeoptimizer/commands/ to ~/.cco/knowledge/commands/
    """
    # Get package commands directory
    package_dir = Path(__file__).parent.parent
    source_commands = package_dir / "commands"

    if not source_commands.exists():
        raise FileNotFoundError(f"Package commands not found at {source_commands}")

    # Create destination
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for command_file in source_commands.glob("*.md"):
        dest_file = commands_dir / command_file.name
        shutil.copy2(command_file, dest_file)


def _setup_guides(guides_dir: Path) -> None:
    """
    Copy guide files from package to global directory.

    Copies from claudecodeoptimizer/docs/cco/guides/ to ~/.cco/knowledge/guides/
    """
    # Get package guides directory
    package_dir = Path(__file__).parent.parent
    source_guides = package_dir.parent / "docs" / "cco" / "guides"

    if not source_guides.exists():
        # Fallback: try package internal location
        source_guides = package_dir / "docs" / "cco" / "guides"

    if not source_guides.exists():
        raise FileNotFoundError(f"Package guides not found at {source_guides}")

    # Create destination
    guides_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for guide_file in source_guides.glob("*.md"):
        dest_file = guides_dir / guide_file.name
        shutil.copy2(guide_file, dest_file)


def _setup_agents(agents_dir: Path) -> None:
    """
    Copy agent templates from package to global directory.

    Copies from claudecodeoptimizer/knowledge/agents/ to ~/.cco/knowledge/agents/
    """
    # Get package agents directory
    package_dir = Path(__file__).parent.parent
    source_agents = package_dir / "knowledge" / "agents"

    if not source_agents.exists():
        raise FileNotFoundError(f"Package agents not found at {source_agents}")

    # Create destination
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files (templates and README)
    for agent_file in source_agents.glob("*.md"):
        dest_file = agents_dir / agent_file.name
        shutil.copy2(agent_file, dest_file)


def _setup_skills(skills_dir: Path) -> None:
    """
    Copy skill templates from package to global directory.

    Copies from claudecodeoptimizer/knowledge/skills/ to ~/.cco/knowledge/skills/
    """
    # Get package skills directory
    package_dir = Path(__file__).parent.parent
    source_skills = package_dir / "knowledge" / "skills"

    if not source_skills.exists():
        raise FileNotFoundError(f"Package skills not found at {source_skills}")

    # Create destination
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy all .md files (templates and README)
    for skill_file in source_skills.glob("*.md"):
        dest_file = skills_dir / skill_file.name
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
    commands_dir = config.get_knowledge_commands_dir()
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

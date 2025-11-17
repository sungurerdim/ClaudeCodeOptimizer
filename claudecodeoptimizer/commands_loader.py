"""Dynamic command loader from .md templates."""

from pathlib import Path
from typing import Any, Dict

from .core.constants import MARKDOWN_SECTION_COUNT


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith("---"):
        return {}

    try:
        parts = content.split("---", 2)
        if len(parts) < MARKDOWN_SECTION_COUNT:
            return {}

        frontmatter = parts[1].strip()
        result = {}

        # Simple YAML parser for our needs
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()

        return result
    except Exception:
        return {}


def load_global_commands() -> Dict[str, Dict[str, Any]]:
    """
    Load all CLI commands from commands directory.

    Single source of truth: claudecodeoptimizer/content/commands/*.md
    Returns dict: {command_name: {description, file}}
    """
    commands_dir = Path(__file__).parent.parent / "content" / "commands"
    commands: Dict[str, Dict[str, Any]] = {}

    if not commands_dir.exists():
        return commands

    # Only load init and remove (global slash commands)
    for command_name in ["cco-init", "cco-remove"]:
        md_file = commands_dir / f"{command_name}.md"
        if not md_file.exists():
            continue

        # Parse metadata from frontmatter
        content = md_file.read_text(encoding="utf-8")
        metadata = parse_frontmatter(content)

        commands[command_name] = {
            "description": metadata.get("description", f"{command_name.title()} command"),
            "file": md_file,
        }

    return commands


def get_command_list() -> str:
    """Get formatted list of available global commands for display."""
    commands = load_global_commands()
    if not commands:
        return "cco-init.md, cco-remove.md"

    return ", ".join(f"{name}.md" for name in sorted(commands.keys()))


def get_slash_commands() -> str:
    """Get formatted list of slash commands for display."""
    commands = load_global_commands()
    if not commands:
        return "/cco-init, /cco-remove"

    return ", ".join(f"/{name}" for name in sorted(commands.keys()))

"""CCO Configuration - Single source of truth."""

from pathlib import Path

from . import __version__

__all__ = ["VERSION", "CLAUDE_DIR", "COMMANDS_DIR", "AGENTS_DIR"]

VERSION = __version__  # Single source: __init__.py
CLAUDE_DIR = Path.home() / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
AGENTS_DIR = CLAUDE_DIR / "agents"


def get_claude_dir() -> Path:
    """Get ~/.claude/ directory."""
    return CLAUDE_DIR


def get_global_commands_dir() -> Path:
    """Get ~/.claude/commands/ directory."""
    return COMMANDS_DIR


def get_agents_dir() -> Path:
    """Get ~/.claude/agents/ directory."""
    return AGENTS_DIR

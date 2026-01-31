"""Shared path constants for CCO test suite."""

from pathlib import Path

ROOT: Path = Path(__file__).parent.parent
COMMANDS_DIR = ROOT / "commands"
AGENTS_DIR = ROOT / "agents"
HOOKS_DIR = ROOT / "hooks"

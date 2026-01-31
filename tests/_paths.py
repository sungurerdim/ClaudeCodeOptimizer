"""Shared path constants for CCO test suite."""

from pathlib import Path

ROOT: Path = Path(__file__).parent.parent
COMMANDS_DIR = ROOT / "commands"
AGENTS_DIR = ROOT / "agents"
HOOKS_DIR = ROOT / "hooks"
PROFILE_PATH = ROOT / ".claude" / "rules" / "cco-profile.md"
RULES_DIR = ROOT / ".claude" / "rules"
SCHEMAS_DIR = ROOT / "commands" / "schemas"

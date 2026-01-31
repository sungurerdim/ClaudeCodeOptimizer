"""Shared test fixtures for CCO test suite."""

import json
from pathlib import Path
from typing import Any

import pytest

ROOT: Path = Path(__file__).parent.parent
COMMANDS_DIR = ROOT / "commands"
AGENTS_DIR = ROOT / "agents"
HOOKS_DIR = ROOT / "hooks"


@pytest.fixture
def command_files() -> list[Path]:
    """Get all command markdown files."""
    return list(COMMANDS_DIR.glob("*.md"))


@pytest.fixture
def optimize_content() -> str:
    """Load optimize command content."""
    path = COMMANDS_DIR / "optimize.md"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def hooks_json() -> dict[str, Any]:
    """Load hooks.json configuration."""
    path = HOOKS_DIR / "hooks.json"
    return json.loads(path.read_text(encoding="utf-8"))

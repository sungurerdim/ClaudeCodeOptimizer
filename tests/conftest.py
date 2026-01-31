"""Shared test fixtures for CCO test suite."""

import json
from pathlib import Path
from typing import Any

import pytest

from _paths import COMMANDS_DIR, HOOKS_DIR


@pytest.fixture
def command_files() -> list[Path]:
    """Get all command markdown files."""
    return list(COMMANDS_DIR.glob("*.md"))


@pytest.fixture
def optimize_content() -> str:
    """Load optimize command content."""
    return (COMMANDS_DIR / "optimize.md").read_text(encoding="utf-8")


@pytest.fixture
def hooks_json() -> dict[str, Any]:
    """Load hooks.json configuration."""
    return json.loads((HOOKS_DIR / "hooks.json").read_text(encoding="utf-8"))

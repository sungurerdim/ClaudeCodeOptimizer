"""Unit tests for config module."""

from pathlib import Path

from claudecodeoptimizer.config import (
    AGENTS_DIR,
    CLAUDE_DIR,
    COMMANDS_DIR,
    VERSION,
    get_agents_dir,
    get_claude_dir,
    get_global_commands_dir,
)


class TestConstants:
    """Test module constants."""

    def test_version(self):
        """Test VERSION is set."""
        assert VERSION == "1.0.0"

    def test_claude_dir(self):
        """Test CLAUDE_DIR is ~/.claude/"""
        assert CLAUDE_DIR == Path.home() / ".claude"

    def test_commands_dir(self):
        """Test COMMANDS_DIR is ~/.claude/commands/"""
        assert COMMANDS_DIR == CLAUDE_DIR / "commands"

    def test_agents_dir(self):
        """Test AGENTS_DIR is ~/.claude/agents/"""
        assert AGENTS_DIR == CLAUDE_DIR / "agents"


class TestFunctions:
    """Test helper functions."""

    def test_get_claude_dir(self):
        """Test get_claude_dir returns CLAUDE_DIR."""
        assert get_claude_dir() == CLAUDE_DIR

    def test_get_global_commands_dir(self):
        """Test get_global_commands_dir returns COMMANDS_DIR."""
        assert get_global_commands_dir() == COMMANDS_DIR

    def test_get_agents_dir(self):
        """Test get_agents_dir returns AGENTS_DIR."""
        assert get_agents_dir() == AGENTS_DIR

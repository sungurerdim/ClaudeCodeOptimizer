"""Unit tests for config module."""

from pathlib import Path

from claudecodeoptimizer.config import (
    AGENTS_DIR,
    CCO_MARKER_PATTERNS,
    CLAUDE_DIR,
    COMMANDS_DIR,
    SUBPROCESS_TIMEOUT,
    VERSION,
    get_cco_agents,
    get_cco_commands,
    get_standards_count,
)


class TestConstants:
    """Test module constants."""

    def test_version(self):
        """Test VERSION matches __version__."""
        from claudecodeoptimizer import __version__

        assert VERSION == __version__

    def test_claude_dir(self):
        """Test CLAUDE_DIR is ~/.claude/"""
        assert CLAUDE_DIR == Path.home() / ".claude"

    def test_commands_dir(self):
        """Test COMMANDS_DIR is ~/.claude/commands/"""
        assert COMMANDS_DIR == CLAUDE_DIR / "commands"

    def test_agents_dir(self):
        """Test AGENTS_DIR is ~/.claude/agents/"""
        assert AGENTS_DIR == CLAUDE_DIR / "agents"

    def test_subprocess_timeout(self):
        """Test SUBPROCESS_TIMEOUT is defined."""
        assert isinstance(SUBPROCESS_TIMEOUT, int)
        assert SUBPROCESS_TIMEOUT > 0

    def test_cco_marker_patterns(self):
        """Test CCO_MARKER_PATTERNS is defined correctly."""
        assert isinstance(CCO_MARKER_PATTERNS, dict)
        assert "standards" in CCO_MARKER_PATTERNS
        # Each pattern should be a tuple of (regex_string, flags)
        for key, value in CCO_MARKER_PATTERNS.items():
            assert isinstance(value, tuple)
            assert len(value) == 2
            assert isinstance(value[0], str)
            assert isinstance(value[1], int)


class TestFunctions:
    """Test helper functions."""

    def test_get_cco_commands(self):
        """Test get_cco_commands returns list of Path objects."""
        result = get_cco_commands()
        assert isinstance(result, list)
        # All items should be Path objects
        for item in result:
            assert isinstance(item, Path)
            # Should match cco-*.md pattern
            assert item.name.startswith("cco-")
            assert item.suffix == ".md"

    def test_get_cco_agents(self):
        """Test get_cco_agents returns list of Path objects."""
        result = get_cco_agents()
        assert isinstance(result, list)
        # All items should be Path objects
        for item in result:
            assert isinstance(item, Path)
            # Should match cco-*.md pattern
            assert item.name.startswith("cco-")
            assert item.suffix == ".md"

    def test_get_standards_count(self):
        """Test get_standards_count returns tuple of counts."""
        standards, categories = get_standards_count()
        assert isinstance(standards, int)
        assert isinstance(categories, int)
        assert standards > 0
        assert categories > 0

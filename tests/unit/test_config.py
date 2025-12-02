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

    def test_get_standards_count_missing_file(self, tmp_path):
        """Test get_standards_count returns (0, 0) when standards file doesn't exist."""
        from unittest.mock import MagicMock, patch

        # Create a mock path that doesn't exist
        mock_path = MagicMock()
        mock_path.exists.return_value = False

        # Patch Path(__file__) chain to return our mock
        with patch("claudecodeoptimizer.config.Path") as mock_path_cls:
            mock_path_cls.return_value.parent.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_path

            # Need to re-execute the function logic since Path is module-level
            # Instead, directly test the branch by calling the function
            import importlib

            from claudecodeoptimizer import config

            # Reload with patched Path
            importlib.reload(config)

        # Simpler: mock at the point of use
        with patch("claudecodeoptimizer.config.Path") as mock_path_cls:
            mock_file = MagicMock()
            mock_file.exists.return_value = False
            mock_path_cls.return_value.parent.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_file

            # Call the function - it will use our mocked Path
            from claudecodeoptimizer.config import get_standards_count

            result = get_standards_count()
            assert result == (0, 0)

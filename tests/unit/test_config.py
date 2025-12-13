"""Unit tests for config module."""

from pathlib import Path
from unittest.mock import patch

from claudecodeoptimizer.config import (
    AGENTS_DIR,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    COMMANDS_DIR,
    RULES_DIR,
    SUBPROCESS_TIMEOUT,
    VERSION,
    _get_rules_count,
    get_cco_agents,
    get_cco_commands,
    get_content_path,
    get_rules_breakdown,
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

    def test_cco_universal_pattern(self):
        """Test CCO_UNIVERSAL_PATTERN is defined correctly."""
        import re

        assert isinstance(CCO_UNIVERSAL_PATTERN, tuple)
        assert len(CCO_UNIVERSAL_PATTERN) == 2
        pattern, flags = CCO_UNIVERSAL_PATTERN
        assert isinstance(pattern, str)
        assert isinstance(flags, int)

        # Test that pattern matches various CCO marker formats
        test_cases = [
            "<!-- CCO_STANDARDS_START -->content<!-- CCO_STANDARDS_END -->",
            "<!-- CCO_ADAPTIVE_START -->content<!-- CCO_ADAPTIVE_END -->",
            "<!-- cco-standards-start -->content<!-- cco-standards-end -->",
            "<!-- CCO_ANY_NAME_START -->content<!-- CCO_ANY_NAME_END -->",
        ]
        for test in test_cases:
            assert re.search(pattern, test, flags=flags), f"Pattern should match: {test}"


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

    def test_get_rules_count(self):
        """Test _get_rules_count returns tuple of counts."""
        rules, categories = _get_rules_count()
        assert isinstance(rules, int)
        assert isinstance(categories, int)
        assert rules > 0
        assert categories > 0

    def test_get_rules_count_missing_file(self, tmp_path):
        """Test _get_rules_count returns (0, 0) when rules file doesn't exist."""
        from unittest.mock import MagicMock

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
            from claudecodeoptimizer.config import _get_rules_count

            result = _get_rules_count()
            assert result == (0, 0)

    def test_get_content_path(self):
        """Test get_content_path returns correct path for subdirectory."""
        result = get_content_path("command-templates")
        assert isinstance(result, Path)
        assert result.name == "command-templates"
        assert "content" in str(result)

    def test_get_content_path_various_subdirs(self):
        """Test get_content_path works for all expected subdirectories."""
        for subdir in [
            "command-templates",
            "agent-templates",
            "rules",
            "statusline",
            "permissions",
        ]:
            result = get_content_path(subdir)
            assert result.name == subdir

    def test_get_rules_breakdown(self):
        """Test get_rules_breakdown returns correct structure."""
        result = get_rules_breakdown()
        assert isinstance(result, dict)
        assert "core" in result
        assert "ai" in result
        assert "tools" in result
        assert "adaptive" in result
        assert "total" in result
        # Total should be sum of all categories
        assert result["total"] == (
            result["core"] + result["ai"] + result["tools"] + result["adaptive"]
        )

    def test_rules_dir_constant(self):
        """Test RULES_DIR constant is defined correctly (cco/ subdirectory)."""
        assert RULES_DIR == CLAUDE_DIR / "rules" / "cco"

    def test_get_rules_count_no_dir(self, tmp_path):
        """Test _get_rules_count returns (0, 0) when rules dir doesn't exist."""
        # Patch the path to a nonexistent directory
        with patch("claudecodeoptimizer.config.Path") as mock_path:
            # Create a mock that returns a path that doesn't exist
            mock_path.return_value.parent.__truediv__.return_value.__truediv__.return_value.exists.return_value = False
            # We need to mock __file__ to point to a nonexistent location
            # Since Path(__file__).parent / "content" / "rules" is used

            # Use a different approach - mock the internal path construction
            import claudecodeoptimizer.config as config_module

            original_file = config_module.__file__

            # Temporarily change __file__ to point somewhere without rules
            config_module.__file__ = str(tmp_path / "nonexistent" / "config.py")

            result = _get_rules_count()

            # Restore
            config_module.__file__ = original_file

        assert result == (0, 0)

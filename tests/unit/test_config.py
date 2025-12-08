"""Unit tests for config module."""

from pathlib import Path
from unittest.mock import patch

from claudecodeoptimizer.config import (
    AGENTS_DIR,
    CCO_UNIVERSAL_PATTERN,
    CLAUDE_DIR,
    COMMANDS_DIR,
    SUBPROCESS_TIMEOUT,
    VERSION,
    get_cco_agents,
    get_cco_commands,
    get_content_path,
    get_standards_breakdown,
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
            "<!-- CCO_CONTEXT_START -->content<!-- CCO_CONTEXT_END -->",
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

    def test_get_standards_count(self):
        """Test get_standards_count returns tuple of counts."""
        standards, categories = get_standards_count()
        assert isinstance(standards, int)
        assert isinstance(categories, int)
        assert standards > 0
        assert categories > 0

    def test_get_standards_count_missing_file(self, tmp_path):
        """Test get_standards_count returns (0, 0) when standards file doesn't exist."""
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
            from claudecodeoptimizer.config import get_standards_count

            result = get_standards_count()
            assert result == (0, 0)

    def test_get_content_path(self):
        """Test get_content_path returns correct path for subdirectory."""
        result = get_content_path("slash-commands")
        assert isinstance(result, Path)
        assert result.name == "slash-commands"
        assert "content" in str(result)

    def test_get_content_path_various_subdirs(self):
        """Test get_content_path works for all expected subdirectories."""
        for subdir in [
            "slash-commands",
            "agent-templates",
            "standards",
            "statusline",
            "permissions",
        ]:
            result = get_content_path(subdir)
            assert result.name == subdir

    def test_get_standards_breakdown(self):
        """Test get_standards_breakdown returns correct structure."""
        result = get_standards_breakdown()
        assert isinstance(result, dict)
        assert "universal" in result
        assert "ai_specific" in result
        assert "cco_specific" in result
        assert "project_specific" in result
        assert "total" in result
        # Total should be sum of all categories
        assert result["total"] == (
            result["universal"]
            + result["ai_specific"]
            + result["cco_specific"]
            + result["project_specific"]
        )

    def test_get_standards_breakdown_no_cco_specific_split(self, tmp_path):
        """Test get_standards_breakdown when CCO-Specific section doesn't exist (line 114)."""
        # This tests line 114: when ai_and_cco split returns only 1 part
        # (file has AI-Specific but no CCO-Specific section)

        # Create test file structure
        standards_dir = tmp_path / "content" / "standards"
        standards_dir.mkdir(parents=True)

        # Create mock file with AI-Specific but NO CCO-Specific section
        standards_file = standards_dir / "cco-standards.md"
        standards_file.write_text(
            "# Universal Standards\n| * Rule1 | Desc |\n| * Rule2 | Desc |\n\n"
            "# AI-Specific Standards\n| * AIRule1 | Desc |\n| * AIRule2 | Desc |\n"
        )

        # We need to test the actual function with a modified file
        # The simplest way is to temporarily modify the actual file and restore it
        import importlib

        from claudecodeoptimizer import config

        # Get the actual standards file path
        actual_file = Path(config.__file__).parent / "content" / "standards" / "cco-standards.md"
        original_content = actual_file.read_text(encoding="utf-8")

        try:
            # Temporarily replace with content that has no CCO-Specific section
            # Using new table format: | * Standard | Rule |
            test_content = "# Universal Standards\n| * Rule1 | Desc |\n\n# AI-Specific Standards\n| * AIRule1 | Desc |\n"
            actual_file.write_text(test_content, encoding="utf-8")

            # Reload to pick up changes
            importlib.reload(config)
            result = config.get_standards_breakdown()

            # Should have ai_specific counted (line 114 executed)
            assert result["ai_specific"] == 1
            assert result["cco_specific"] == 0
        finally:
            # Restore original content
            actual_file.write_text(original_content, encoding="utf-8")
            importlib.reload(config)

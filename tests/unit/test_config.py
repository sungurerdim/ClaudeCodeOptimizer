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
    load_json_file,
    save_json_file,
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
        assert "adaptive" in result
        assert "total" in result
        # Total should be sum of all categories
        # Note: tools key removed - tool rules are embedded in templates
        assert result["total"] == (result["core"] + result["ai"] + result["adaptive"])

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


class TestJSONUtilities:
    """Test JSON utility functions with edge cases."""

    def test_load_json_missing_file(self, tmp_path: Path):
        """Test load_json_file returns empty dict for missing file."""
        missing = tmp_path / "nonexistent.json"
        result = load_json_file(missing)
        assert result == {}

    def test_load_json_invalid_json(self, tmp_path: Path):
        """Test load_json_file returns empty dict for invalid JSON."""
        invalid = tmp_path / "invalid.json"
        invalid.write_text("{ not valid json }", encoding="utf-8")
        result = load_json_file(invalid)
        assert result == {}

    def test_load_json_empty_file(self, tmp_path: Path):
        """Test load_json_file returns empty dict for empty file."""
        empty = tmp_path / "empty.json"
        empty.write_text("", encoding="utf-8")
        result = load_json_file(empty)
        assert result == {}

    def test_load_json_unicode_content(self, tmp_path: Path):
        """Test load_json_file handles unicode characters correctly."""
        import json

        unicode_data = {"message": "Hello 世界 🌍", "author": "Привет"}
        unicode_file = tmp_path / "unicode.json"
        unicode_file.write_text(json.dumps(unicode_data), encoding="utf-8")

        result = load_json_file(unicode_file)
        assert result["message"] == "Hello 世界 🌍"
        assert result["author"] == "Привет"

    def test_load_json_valid_file(self, tmp_path: Path):
        """Test load_json_file loads valid JSON correctly."""
        import json

        data = {"key": "value", "number": 42, "nested": {"a": 1}}
        valid = tmp_path / "valid.json"
        valid.write_text(json.dumps(data), encoding="utf-8")

        result = load_json_file(valid)
        assert result == data

    def test_save_json_creates_file(self, tmp_path: Path):
        """Test save_json_file creates new file correctly."""
        import json

        data = {"test": "data", "number": 123}
        output = tmp_path / "output.json"

        save_json_file(output, data)

        assert output.exists()
        content = json.loads(output.read_text(encoding="utf-8"))
        assert content == data

    def test_save_json_overwrites_existing(self, tmp_path: Path):
        """Test save_json_file overwrites existing file."""
        import json

        output = tmp_path / "existing.json"
        output.write_text('{"old": "data"}', encoding="utf-8")

        new_data = {"new": "data"}
        save_json_file(output, new_data)

        content = json.loads(output.read_text(encoding="utf-8"))
        assert content == new_data
        assert "old" not in content

    def test_save_json_write_error(self, tmp_path: Path):
        """Test save_json_file raises RuntimeError on write failure."""
        import pytest

        # Create a directory with the same name to cause write failure
        bad_path = tmp_path / "directory"
        bad_path.mkdir()

        with pytest.raises(RuntimeError, match="Failed to write JSON"):
            save_json_file(bad_path, {"data": "test"})

    def test_save_json_unicode_content(self, tmp_path: Path):
        """Test save_json_file handles unicode correctly."""
        import json

        data = {"emoji": "🎉", "chinese": "中文", "russian": "Русский"}
        output = tmp_path / "unicode_out.json"

        save_json_file(output, data)

        content = json.loads(output.read_text(encoding="utf-8"))
        assert content["emoji"] == "🎉"
        assert content["chinese"] == "中文"

"""Unit tests for cco_status module."""

from unittest.mock import patch

from claudecodeoptimizer.cco_status import (
    count_files,
    has_rules,
    main,
    print_status,
)


class TestCountFiles:
    """Test count_files function."""

    def test_count_empty(self, tmp_path):
        """Test counting when no files."""
        with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                counts = count_files()
                assert counts["commands"] == 0
                assert counts["agents"] == 0

    def test_count_with_files(self, tmp_path):
        """Test counting with CCO files."""
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "agents" / "cco-agent-scan.md").touch()

        with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                counts = count_files()
                assert counts["commands"] == 1
                assert counts["agents"] == 1


class TestHasRules:
    """Test has_rules function."""

    def test_no_claude_md(self, tmp_path):
        """Test when CLAUDE.md doesn't exist."""
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_rules() is False

    def test_with_rules(self, tmp_path):
        """Test when CLAUDE.md has rules."""
        tmp_path.mkdir(exist_ok=True)
        (tmp_path / "CLAUDE.md").write_text(
            "<!-- CCO_RULES_START -->\nrules\n<!-- CCO_RULES_END -->"
        )

        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_rules() is True


class TestPrintStatus:
    """Test print_status function."""

    def test_not_installed(self, tmp_path):
        """Test when not installed."""
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                    assert print_status() == 1


class TestMain:
    """Test main function."""

    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_returns_status(self, mock_print):
        """Test main returns status code."""
        mock_print.return_value = 0
        assert main() == 0

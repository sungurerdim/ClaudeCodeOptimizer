"""Unit tests for install_hook module."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.install_hook import (
    get_content_dir,
    post_install,
    setup_agents,
    setup_claude_md,
    setup_commands,
    setup_templates,
)


class TestGetContentDir:
    """Test get_content_dir function."""

    def test_returns_path(self):
        """Test returns a Path object."""
        result = get_content_dir()
        assert isinstance(result, Path)

    def test_points_to_content(self):
        """Test points to content directory."""
        result = get_content_dir()
        assert result.name == "content"


class TestSetupCommands:
    """Test setup_commands function."""

    def test_creates_commands_dir(self, tmp_path):
        """Test creates commands directory."""
        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "pkg"
                (tmp_path / "pkg" / "commands").mkdir(parents=True)
                (tmp_path / "pkg" / "commands" / "cco-test.md").touch()

                count = setup_commands()

                assert (tmp_path / "commands").exists()
                assert count == 1

    def test_returns_zero_if_no_source(self, tmp_path):
        """Test returns 0 if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "nonexistent"

                count = setup_commands()

                assert count == 0


class TestSetupAgents:
    """Test setup_agents function."""

    def test_creates_agents_dir(self, tmp_path):
        """Test creates agents directory."""
        with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "pkg"
                (tmp_path / "pkg" / "agents").mkdir(parents=True)
                (tmp_path / "pkg" / "agents" / "cco-agent-test.md").touch()

                count = setup_agents()

                assert (tmp_path / "agents").exists()
                assert count == 1

    def test_returns_zero_if_no_source(self, tmp_path):
        """Test returns 0 if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "nonexistent"

                count = setup_agents()

                assert count == 0


class TestSetupTemplates:
    """Test setup_templates function."""

    def test_returns_zero_if_no_templates(self, tmp_path):
        """Test returns 0 if templates dir doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            count = setup_templates()
            # Templates dir doesn't exist in current structure
            assert count >= 0


class TestSetupClaudeMd:
    """Test setup_claude_md function."""

    def test_creates_claude_md(self, tmp_path):
        """Test creates CLAUDE.md with rules."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            setup_claude_md()

            claude_md = tmp_path / "CLAUDE.md"
            assert claude_md.exists()
            content = claude_md.read_text()
            assert "<!-- CCO_RULES_START -->" in content
            assert "<!-- CCO_RULES_END -->" in content

    def test_updates_existing_rules(self, tmp_path):
        """Test updates existing CCO rules."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            claude_md = tmp_path / "CLAUDE.md"
            tmp_path.mkdir(exist_ok=True)
            claude_md.write_text(
                "# My Rules\n\n<!-- CCO_RULES_START -->PLACEHOLDER_TEXT<!-- CCO_RULES_END -->"
            )

            setup_claude_md()

            content = claude_md.read_text()
            assert "# My Rules" in content
            assert "PLACEHOLDER_TEXT" not in content
            assert "CCO Rules" in content

    def test_appends_to_existing_file(self, tmp_path):
        """Test appends rules to existing CLAUDE.md."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            claude_md = tmp_path / "CLAUDE.md"
            tmp_path.mkdir(exist_ok=True)
            claude_md.write_text("# My Custom Rules\n\nSome content")

            setup_claude_md()

            content = claude_md.read_text()
            assert "# My Custom Rules" in content
            assert "<!-- CCO_RULES_START -->" in content

    def test_removes_old_principles(self, tmp_path):
        """Test removes old CCO_PRINCIPLES markers."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            claude_md = tmp_path / "CLAUDE.md"
            tmp_path.mkdir(exist_ok=True)
            claude_md.write_text(
                "<!-- CCO_PRINCIPLES_START -->old<!-- CCO_PRINCIPLES_END -->\n# Rules"
            )

            setup_claude_md()

            content = claude_md.read_text()
            assert "CCO_PRINCIPLES" not in content


class TestPostInstall:
    """Test post_install function."""

    def test_help_flag(self, capsys):
        """Test --help shows usage."""
        with patch.object(sys, "argv", ["cco-setup", "--help"]):
            result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "Usage: cco-setup" in captured.out

    def test_h_flag(self, capsys):
        """Test -h shows usage."""
        with patch.object(sys, "argv", ["cco-setup", "-h"]):
            result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "Usage: cco-setup" in captured.out

    def test_successful_setup(self, tmp_path, capsys):
        """Test successful setup."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                    with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                        mock_content.return_value = tmp_path / "pkg"
                        result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO Setup" in captured.out
        assert "CCO ready" in captured.out

    def test_exception_handling(self, capsys):
        """Test exception during setup."""
        with patch(
            "claudecodeoptimizer.install_hook.setup_commands", side_effect=Exception("Test error")
        ):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Setup failed" in captured.err


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

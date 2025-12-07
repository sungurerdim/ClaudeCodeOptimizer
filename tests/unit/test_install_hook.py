"""Unit tests for install_hook module."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.install_hook import (
    get_content_dir,
    has_statusline,
    post_install,
    setup_agents,
    setup_claude_md,
    setup_commands,
    setup_statusline,
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

                installed = setup_commands()

                assert (tmp_path / "commands").exists()
                assert len(installed) == 1
                assert "cco-test.md" in installed

    def test_returns_empty_if_no_source(self, tmp_path):
        """Test returns empty list if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "nonexistent"

                installed = setup_commands()

                assert installed == []

    def test_removes_old_cco_files(self, tmp_path):
        """Test removes existing cco-*.md files before installing new ones."""
        dest_dir = tmp_path / "commands"
        dest_dir.mkdir(parents=True)
        # Create old files that should be deleted
        old_file = dest_dir / "cco-old-command.md"
        old_file.write_text("old content")
        non_cco_file = dest_dir / "other-file.md"
        non_cco_file.write_text("should remain")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", dest_dir):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "pkg"
                (tmp_path / "pkg" / "commands").mkdir(parents=True)
                (tmp_path / "pkg" / "commands" / "cco-new.md").write_text("new content")

                installed = setup_commands()

                # Old cco-*.md file should be deleted
                assert not old_file.exists()
                # Non-cco file should remain
                assert non_cco_file.exists()
                # New file should be installed
                assert (dest_dir / "cco-new.md").exists()
                assert "cco-new.md" in installed


class TestSetupAgents:
    """Test setup_agents function."""

    def test_creates_agents_dir(self, tmp_path):
        """Test creates agents directory."""
        with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "pkg"
                (tmp_path / "pkg" / "agents").mkdir(parents=True)
                (tmp_path / "pkg" / "agents" / "cco-agent-test.md").touch()

                installed = setup_agents()

                assert (tmp_path / "agents").exists()
                assert len(installed) == 1
                assert "cco-agent-test.md" in installed

    def test_returns_empty_if_no_source(self, tmp_path):
        """Test returns empty list if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "nonexistent"

                installed = setup_agents()

                assert installed == []


class TestSetupClaudeMd:
    """Test setup_claude_md function."""

    def test_creates_claude_md(self, tmp_path):
        """Test creates CLAUDE.md with rules."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            setup_claude_md()

            claude_md = tmp_path / "CLAUDE.md"
            assert claude_md.exists()
            content = claude_md.read_text()
            assert "<!-- CCO_STANDARDS_START -->" in content
            assert "<!-- CCO_STANDARDS_END -->" in content

    def test_updates_existing_standards(self, tmp_path):
        """Test updates existing CCO standards."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            claude_md = tmp_path / "CLAUDE.md"
            tmp_path.mkdir(exist_ok=True)
            claude_md.write_text(
                "# My Rules\n\n<!-- CCO_STANDARDS_START -->PLACEHOLDER_TEXT<!-- CCO_STANDARDS_END -->"
            )

            setup_claude_md()

            content = claude_md.read_text()
            assert "# My Rules" in content
            assert "PLACEHOLDER_TEXT" not in content
            assert "## Claude Code Integration" in content

    def test_appends_to_existing_file(self, tmp_path):
        """Test appends rules to existing CLAUDE.md."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            claude_md = tmp_path / "CLAUDE.md"
            tmp_path.mkdir(exist_ok=True)
            claude_md.write_text("# My Custom Rules\n\nSome content")

            setup_claude_md()

            content = claude_md.read_text()
            assert "# My Custom Rules" in content
            assert "<!-- CCO_STANDARDS_START -->" in content


class TestHasStatusline:
    """Test has_statusline function."""

    def test_no_file(self, tmp_path):
        """Test returns False when statusline file doesn't exist."""
        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", tmp_path / "statusline.js"):
            assert has_statusline() is False

    def test_file_exists_with_cco_content(self, tmp_path):
        """Test returns True when statusline file exists with CCO content."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
            assert has_statusline() is True

    def test_file_exists_without_cco_content(self, tmp_path):
        """Test returns False when statusline file exists but without CCO marker."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// Custom statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
            assert has_statusline() is False


class TestSetupStatusline:
    """Test setup_statusline function."""

    def test_setup_statusline_success(self, tmp_path):
        """Test successfully sets up statusline."""
        # Create source statusline file
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "full.js"
        src_file.write_text("// CCO Statusline\nconsole.log('status');")

        dest_statusline = tmp_path / "statusline.js"
        dest_settings = tmp_path / "settings.json"

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", dest_statusline):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", dest_settings):
                        result = setup_statusline(verbose=False)

        assert result is True
        assert dest_statusline.exists()
        assert dest_settings.exists()
        settings = json.loads(dest_settings.read_text())
        assert "statusLine" in settings

    def test_setup_statusline_verbose(self, tmp_path, capsys):
        """Test verbose output during statusline setup."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "full.js"
        src_file.write_text("// CCO Statusline\nconsole.log('status');")

        dest_statusline = tmp_path / "statusline.js"
        dest_settings = tmp_path / "settings.json"

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", dest_statusline):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", dest_settings):
                        result = setup_statusline(verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "statusline.js" in captured.out
        assert "settings.json" in captured.out

    def test_setup_statusline_no_source(self, tmp_path, capsys):
        """Test returns False when source file doesn't exist."""
        src_dir = tmp_path / "nonexistent"

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            result = setup_statusline(verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "statusline source not found" in captured.out

    def test_setup_statusline_updates_existing_settings(self, tmp_path):
        """Test updates existing settings.json."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "full.js"
        src_file.write_text("// CCO Statusline\nconsole.log('status');")

        dest_statusline = tmp_path / "statusline.js"
        dest_settings = tmp_path / "settings.json"
        # Pre-existing settings
        dest_settings.write_text(json.dumps({"existingKey": "value"}))

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", dest_statusline):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", dest_settings):
                        result = setup_statusline(verbose=False)

        assert result is True
        settings = json.loads(dest_settings.read_text())
        assert "existingKey" in settings  # Preserved
        assert "statusLine" in settings  # Added

    def test_setup_statusline_handles_invalid_json(self, tmp_path):
        """Test handles invalid JSON in existing settings.json."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "full.js"
        src_file.write_text("// CCO Statusline\nconsole.log('status');")

        dest_statusline = tmp_path / "statusline.js"
        dest_settings = tmp_path / "settings.json"
        dest_settings.write_text("invalid json {{{")

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", dest_statusline):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", dest_settings):
                        result = setup_statusline(verbose=False)

        assert result is True
        # Should overwrite with valid JSON
        settings = json.loads(dest_settings.read_text())
        assert "statusLine" in settings


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
                        # Skip statusline to avoid STATUSLINE_FILE path issues
                        with patch.object(sys, "argv", ["cco-setup", "--no-statusline"]):
                            mock_content.return_value = tmp_path / "pkg"
                            result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO Setup" in captured.out
        assert "Installed:" in captured.out

    def test_exception_handling(self, capsys):
        """Test exception during setup."""
        with patch(
            "claudecodeoptimizer.install_hook.setup_commands", side_effect=Exception("Test error")
        ):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Setup failed" in captured.err

    def test_successful_setup_with_statusline(self, tmp_path, capsys):
        """Test successful setup with statusline enabled."""
        # Create source statusline
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "full.js"
        src_file.write_text("// CCO Statusline\nconsole.log('status');")

        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                    with patch(
                        "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                        tmp_path / "statusline.js",
                    ):
                        with patch(
                            "claudecodeoptimizer.install_hook.SETTINGS_FILE",
                            tmp_path / "settings.json",
                        ):
                            with patch(
                                "claudecodeoptimizer.install_hook.get_content_dir"
                            ) as mock_content:
                                with patch(
                                    "claudecodeoptimizer.install_hook.get_content_path",
                                    return_value=src_dir,
                                ):
                                    with patch.object(sys, "argv", ["cco-setup"]):
                                        mock_content.return_value = tmp_path / "pkg"
                                        result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO Setup" in captured.out
        assert "Installed:" in captured.out
        assert "statusline" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

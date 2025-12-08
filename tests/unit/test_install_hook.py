"""Unit tests for install_hook module."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.install_hook import (
    clean_previous_installation,
    get_content_dir,
    post_install,
    setup_agents,
    setup_claude_md,
    setup_commands,
    setup_local_permissions,
    setup_local_statusline,
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


class TestCleanPreviousInstallation:
    """Test clean_previous_installation function."""

    def test_removes_cco_commands(self, tmp_path):
        """Test removes cco-*.md files from commands directory."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-old.md").write_text("old command")
        (commands_dir / "cco-another.md").write_text("another old")
        (commands_dir / "other.md").write_text("keep this")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", commands_dir):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        assert result["commands"] == 2
        assert not (commands_dir / "cco-old.md").exists()
        assert not (commands_dir / "cco-another.md").exists()
        assert (commands_dir / "other.md").exists()  # non-cco file preserved

    def test_removes_cco_agents(self, tmp_path):
        """Test removes cco-*.md files from agents directory."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "cco-agent-old.md").write_text("old agent")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", agents_dir):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        assert result["agents"] == 1
        assert not (agents_dir / "cco-agent-old.md").exists()

    def test_removes_cco_markers_from_claude_md(self, tmp_path):
        """Test removes CCO markers from CLAUDE.md."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My Rules\n\n<!-- CCO_STANDARDS_START -->\nOld content\n<!-- CCO_STANDARDS_END -->\n\nKeep this"
        )

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        assert result["standards"] == 1
        content = claude_md.read_text()
        assert "<!-- CCO_STANDARDS_START -->" not in content
        assert "Keep this" in content

    def test_removes_legacy_settings_keys(self, tmp_path):
        """Test removes legacy CCO keys from settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(
            json.dumps(
                {
                    "existingKey": "keep",
                    "_cco_managed": True,
                    "_cco_version": "1.0.0",
                    "cco_config": {"old": "config"},
                }
            )
        )

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", settings_file):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        assert result["settings_keys"] == 3
        settings = json.loads(settings_file.read_text())
        assert "existingKey" in settings
        assert "_cco_managed" not in settings
        assert "_cco_version" not in settings
        assert "cco_config" not in settings

    def test_removes_cco_statusline(self, tmp_path):
        """Test removes CCO statusline.js."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('old');")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
                            result = clean_previous_installation(verbose=False)

        assert result["statusline"] == 1
        assert not statusline.exists()

    def test_preserves_non_cco_statusline(self, tmp_path):
        """Test preserves non-CCO statusline.js."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// Custom statusline\nconsole.log('custom');")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
                            result = clean_previous_installation(verbose=False)

        assert result["statusline"] == 0
        assert statusline.exists()

    def test_handles_nonexistent_dirs(self, tmp_path):
        """Test handles nonexistent directories gracefully."""
        with patch(
            "claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "nonexistent_commands"
        ):
            with patch(
                "claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "nonexistent_agents"
            ):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path / "nonexistent"):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        assert result["commands"] == 0
        assert result["agents"] == 0
        assert result["standards"] == 0

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output during cleanup."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-old.md").write_text("old")
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", commands_dir):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch(
                        "claudecodeoptimizer.install_hook.SETTINGS_FILE", tmp_path / "settings.json"
                    ):
                        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
                            clean_previous_installation(verbose=True)

        captured = capsys.readouterr()
        assert "Cleaning previous installation" in captured.out
        assert "Removed 1 command" in captured.out
        assert "Removed old statusline" in captured.out

    def test_handles_invalid_settings_json(self, tmp_path):
        """Test handles invalid JSON in settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text("invalid json {{{")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", settings_file):
                        with patch(
                            "claudecodeoptimizer.install_hook.STATUSLINE_FILE",
                            tmp_path / "statusline.js",
                        ):
                            result = clean_previous_installation(verbose=False)

        # Should not crash, just skip settings cleanup
        assert result["settings_keys"] == 0

    def test_full_cleanup_scenario(self, tmp_path, capsys):
        """Test complete cleanup with all components present."""
        # Setup old installation
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-tune.md").write_text("old tune")
        (commands_dir / "cco-audit.md").write_text("old audit")

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "cco-agent-analyze.md").write_text("old agent")

        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# User content\n\n<!-- CCO_STANDARDS_START -->\nOld\n<!-- CCO_STANDARDS_END -->"
        )

        settings_file = tmp_path / "settings.json"
        settings_file.write_text(
            json.dumps(
                {
                    "statusLine": {"type": "command"},
                    "_cco_managed": True,
                    "_cco_version": "1.0.0",
                }
            )
        )

        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('old');")

        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", commands_dir):
            with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", agents_dir):
                with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
                    with patch("claudecodeoptimizer.install_hook.SETTINGS_FILE", settings_file):
                        with patch("claudecodeoptimizer.install_hook.STATUSLINE_FILE", statusline):
                            result = clean_previous_installation(verbose=True)

        # Verify all old components removed
        assert result["commands"] == 2
        assert result["agents"] == 1
        assert result["standards"] == 1
        assert result["settings_keys"] == 2  # _cco_managed and _cco_version
        assert result["statusline"] == 1

        # Files should be removed or cleaned
        assert not list(commands_dir.glob("cco-*.md"))
        assert not list(agents_dir.glob("cco-*.md"))
        assert "CCO_STANDARDS_START" not in claude_md.read_text()
        assert not statusline.exists()

        # Settings should be cleaned
        settings = json.loads(settings_file.read_text())
        assert "_cco_managed" not in settings
        assert "statusLine" in settings  # This is preserved by design


class TestSetupCommands:
    """Test setup_commands function."""

    def test_creates_commands_dir(self, tmp_path):
        """Test creates commands directory."""
        with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                mock_content.return_value = tmp_path / "pkg"
                (tmp_path / "pkg" / "slash-commands").mkdir(parents=True)
                (tmp_path / "pkg" / "slash-commands" / "cco-test.md").touch()

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
                (tmp_path / "pkg" / "slash-commands").mkdir(parents=True)
                (tmp_path / "pkg" / "slash-commands" / "cco-new.md").write_text("new content")

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
                (tmp_path / "pkg" / "agent-templates").mkdir(parents=True)
                (tmp_path / "pkg" / "agent-templates" / "cco-agent-test.md").touch()

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
            assert "## Integration" in content

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


class TestSetupLocalStatusline:
    """Test setup_local_statusline function."""

    def test_success(self, tmp_path):
        """Test successfully sets up local statusline."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "full.js").write_text("// CCO Statusline\nconsole.log('full');")
        (src_dir / "minimal.js").write_text("// CCO Statusline\nconsole.log('minimal');")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "full", verbose=False)

        assert result is True
        assert (project_path / ".claude" / "statusline.js").exists()
        assert (project_path / ".claude" / "settings.json").exists()
        settings = json.loads((project_path / ".claude" / "settings.json").read_text())
        assert settings["statusLine"]["command"] == "node .claude/statusline.js"

    def test_minimal_mode(self, tmp_path):
        """Test minimal statusline mode."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "minimal.js").write_text("// CCO Statusline\nconsole.log('minimal');")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "minimal", verbose=False)

        assert result is True
        content = (project_path / ".claude" / "statusline.js").read_text()
        assert "minimal" in content

    def test_invalid_mode(self, tmp_path, capsys):
        """Test returns False for invalid mode."""

        project_path = tmp_path / "project"
        project_path.mkdir()

        result = setup_local_statusline(project_path, "invalid", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid mode" in captured.out

    def test_source_not_found(self, tmp_path, capsys):
        """Test returns False when source file doesn't exist."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch(
            "claudecodeoptimizer.install_hook.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "full", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Statusline source not found" in captured.out

    def test_preserves_existing_settings(self, tmp_path):
        """Test preserves existing settings.json content."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text(json.dumps({"existingKey": "value"}))

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "full", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert settings["existingKey"] == "value"
        assert "statusLine" in settings

    def test_handles_invalid_json(self, tmp_path):
        """Test handles invalid JSON in existing settings."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text("invalid json {{{")

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "full", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert "statusLine" in settings

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_statusline

            result = setup_local_statusline(project_path, "full", verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "statusline.js" in captured.out
        assert "full mode" in captured.out
        assert "settings.json" in captured.out


class TestSetupLocalPermissions:
    """Test setup_local_permissions function."""

    def test_success(self, tmp_path):
        """Test successfully sets up local permissions."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        perm_data = {"permissions": {"allow": ["Read(./**)"], "deny": []}}
        (src_dir / "balanced.json").write_text(json.dumps(perm_data))

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_permissions

            result = setup_local_permissions(project_path, "balanced", verbose=False)

        assert result is True
        settings = json.loads((project_path / ".claude" / "settings.json").read_text())
        assert "permissions" in settings
        assert settings["_cco_managed"] is True

    def test_all_levels(self, tmp_path):
        """Test all permission levels work."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)

        for level in ("safe", "balanced", "permissive", "full"):
            perm_data = {"permissions": {"allow": [f"{level}_perm"]}}
            (src_dir / f"{level}.json").write_text(json.dumps(perm_data))

            project_path = tmp_path / f"project_{level}"
            project_path.mkdir()

            with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
                from claudecodeoptimizer.install_hook import setup_local_permissions

                result = setup_local_permissions(project_path, level, verbose=False)

            assert result is True

    def test_invalid_level(self, tmp_path, capsys):
        """Test returns False for invalid level."""
        from claudecodeoptimizer.install_hook import setup_local_permissions

        project_path = tmp_path / "project"
        project_path.mkdir()

        result = setup_local_permissions(project_path, "invalid", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid level" in captured.out

    def test_source_not_found(self, tmp_path, capsys):
        """Test returns False when source file doesn't exist."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch(
            "claudecodeoptimizer.install_hook.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
            from claudecodeoptimizer.install_hook import setup_local_permissions

            result = setup_local_permissions(project_path, "balanced", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Permissions source not found" in captured.out

    def test_invalid_json_source(self, tmp_path, capsys):
        """Test returns False for invalid JSON in source."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text("invalid json {{{")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_permissions

            result = setup_local_permissions(project_path, "balanced", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid permissions JSON" in captured.out

    def test_preserves_existing_settings(self, tmp_path):
        """Test preserves existing settings.json content."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text(json.dumps({"permissions": {"allow": []}}))

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text(
            json.dumps({"existingKey": "value", "statusLine": {"type": "command"}})
        )

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_permissions

            result = setup_local_permissions(project_path, "balanced", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert settings["existingKey"] == "value"
        assert settings["statusLine"]["type"] == "command"
        assert "permissions" in settings

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text(json.dumps({"permissions": {}}))

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            from claudecodeoptimizer.install_hook import setup_local_permissions

            result = setup_local_permissions(project_path, "balanced", verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "settings.json" in captured.out
        assert "permissions: balanced" in captured.out

    def test_handles_invalid_json_in_existing_settings(self, tmp_path):
        """Test handles invalid JSON in existing settings.json."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text(json.dumps({"permissions": {"allow": []}}))

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text("invalid json {{{")

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            result = setup_local_permissions(project_path, "balanced", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert "permissions" in settings
        assert settings["_cco_managed"] is True


class TestRunLocalMode:
    """Test _run_local_mode function."""

    def test_nonexistent_path(self, tmp_path, capsys):
        """Test error for nonexistent path."""
        with patch.object(sys, "argv", ["cco-setup", "--local", str(tmp_path / "nonexistent")]):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.err

    def test_not_a_directory(self, tmp_path, capsys):
        """Test error when path is not a directory."""
        file_path = tmp_path / "file.txt"
        file_path.touch()

        with patch.object(sys, "argv", ["cco-setup", "--local", str(file_path)]):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Not a directory" in captured.err

    def test_creates_claude_dir_only(self, tmp_path, capsys):
        """Test creates .claude directory when no options specified."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch.object(sys, "argv", ["cco-setup", "--local", str(project_path)]):
            result = post_install()

        assert result == 0
        assert (project_path / ".claude").exists()
        captured = capsys.readouterr()
        assert "Created:" in captured.out

    def test_with_statusline(self, tmp_path, capsys):
        """Test local mode with statusline option."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch.object(
                sys, "argv", ["cco-setup", "--local", str(project_path), "--statusline", "full"]
            ):
                result = post_install()

        assert result == 0
        assert (project_path / ".claude" / "statusline.js").exists()
        captured = capsys.readouterr()
        assert "Statusline:" in captured.out

    def test_with_permissions(self, tmp_path, capsys):
        """Test local mode with permissions option."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text(json.dumps({"permissions": {}}))

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.install_hook.get_content_path", return_value=src_dir):
            with patch.object(
                sys,
                "argv",
                ["cco-setup", "--local", str(project_path), "--permissions", "balanced"],
            ):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "Permissions:" in captured.out

    def test_with_both_options(self, tmp_path, capsys):
        """Test local mode with both statusline and permissions."""
        statusline_dir = tmp_path / "pkg" / "statusline"
        statusline_dir.mkdir(parents=True)
        (statusline_dir / "minimal.js").write_text("// CCO Statusline")

        perm_dir = tmp_path / "pkg" / "permissions"
        perm_dir.mkdir(parents=True)
        (perm_dir / "safe.json").write_text(json.dumps({"permissions": {}}))

        project_path = tmp_path / "project"
        project_path.mkdir()

        def mock_content_path(subdir):
            if subdir == "statusline":
                return statusline_dir
            return perm_dir

        with patch(
            "claudecodeoptimizer.install_hook.get_content_path", side_effect=mock_content_path
        ):
            with patch.object(
                sys,
                "argv",
                [
                    "cco-setup",
                    "--local",
                    str(project_path),
                    "--statusline",
                    "minimal",
                    "--permissions",
                    "safe",
                ],
            ):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "Statusline:" in captured.out
        assert "Permissions:" in captured.out
        assert "Local setup complete" in captured.out

    def test_failure_returns_error_code(self, tmp_path, capsys):
        """Test returns error code on failure."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Use invalid source path to trigger failure
        with patch(
            "claudecodeoptimizer.install_hook.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
            with patch.object(
                sys, "argv", ["cco-setup", "--local", str(project_path), "--statusline", "full"]
            ):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "completed with errors" in captured.err

    def test_permissions_failure(self, tmp_path, capsys):
        """Test returns error code when permissions fail."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Use invalid source path to trigger permissions failure
        with patch(
            "claudecodeoptimizer.install_hook.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
            with patch.object(
                sys,
                "argv",
                ["cco-setup", "--local", str(project_path), "--permissions", "balanced"],
            ):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "completed with errors" in captured.err


class TestPostInstallValidation:
    """Test post_install argument validation."""

    def test_statusline_requires_local(self, capsys):
        """Test --statusline without --local raises error."""
        with patch.object(sys, "argv", ["cco-setup", "--statusline", "full"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 2  # argparse error code
        captured = capsys.readouterr()
        assert "require --local" in captured.err

    def test_permissions_requires_local(self, capsys):
        """Test --permissions without --local raises error."""
        with patch.object(sys, "argv", ["cco-setup", "--permissions", "balanced"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "require --local" in captured.err


class TestPostInstall:
    """Test post_install function."""

    def test_help_flag(self, capsys):
        """Test --help shows usage."""
        with patch.object(sys, "argv", ["cco-setup", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "cco-setup" in captured.out

    def test_h_flag(self, capsys):
        """Test -h shows usage."""
        with patch.object(sys, "argv", ["cco-setup", "-h"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "cco-setup" in captured.out

    def test_successful_setup(self, tmp_path, capsys):
        """Test successful setup."""
        with patch("claudecodeoptimizer.install_hook.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.install_hook.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.install_hook.AGENTS_DIR", tmp_path / "agents"):
                    with patch("claudecodeoptimizer.install_hook.get_content_dir") as mock_content:
                        with patch.object(sys, "argv", ["cco-setup"]):
                            mock_content.return_value = tmp_path / "pkg"
                            result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO Setup" in captured.out
        assert "Installed:" in captured.out
        # Statusline is no longer installed by cco-setup
        assert "statusline" not in captured.out.lower() or "cco-tune" in captured.out

    def test_exception_handling(self, tmp_path, capsys):
        """Test exception during setup."""
        with patch.object(sys, "argv", ["cco-setup"]):
            with patch(
                "claudecodeoptimizer.install_hook.setup_commands",
                side_effect=Exception("Test error"),
            ):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Setup failed" in captured.err

    def test_help_mentions_cco_tune(self, capsys):
        """Test help mentions cco-tune for statusline/permissions."""
        with patch.object(sys, "argv", ["cco-setup", "--help"]):
            with pytest.raises(SystemExit):
                post_install()

        captured = capsys.readouterr()
        assert "cco-tune" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

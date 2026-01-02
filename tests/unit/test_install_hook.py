"""Unit tests for install_hook module."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from claudecodeoptimizer.config import get_content_path
from claudecodeoptimizer.install import (
    clean_previous_installation,
    setup_agents,
    setup_commands,
)
from claudecodeoptimizer.install_hook import post_install
from claudecodeoptimizer.local import (
    setup_local_permissions,
    setup_local_statusline,
)


class TestGetContentPath:
    """Test get_content_path function."""

    def test_returns_path(self):
        """Test returns a Path object."""
        result = get_content_path()
        assert isinstance(result, Path)

    def test_points_to_content(self):
        """Test points to content directory."""
        result = get_content_path()
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

        result = clean_previous_installation(verbose=False, target_dir=tmp_path)

        assert result["commands"] == 2
        assert not (commands_dir / "cco-old.md").exists()
        assert not (commands_dir / "cco-another.md").exists()
        assert (commands_dir / "other.md").exists()  # non-cco file preserved

    def test_removes_cco_agents(self, tmp_path):
        """Test removes cco-*.md files from agents directory."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "cco-agent-old.md").write_text("old agent")

        result = clean_previous_installation(verbose=False, target_dir=tmp_path)

        assert result["agents"] == 1
        assert not (agents_dir / "cco-agent-old.md").exists()

    def test_removes_cco_markers_from_claude_md(self, tmp_path):
        """Test removes CCO markers from CLAUDE.md."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My Rules\n\n<!-- CCO_STANDARDS_START -->\nOld content\n<!-- CCO_STANDARDS_END -->\n\nKeep this"
        )

        result = clean_previous_installation(verbose=False, target_dir=tmp_path)

        assert result["rules"] >= 1
        content = claude_md.read_text()
        assert "<!-- CCO_STANDARDS_START -->" not in content
        assert "Keep this" in content

    def test_removes_cco_rules_only(self, tmp_path):
        """Test removes only CCO rule files, preserves custom rules during cleanup."""
        # Setup: old rules in root, current rules in cco/ subdir
        rules_root = tmp_path / "rules"
        rules_root.mkdir()
        cco_subdir = rules_root / "cco"
        cco_subdir.mkdir()

        # Old format - in root
        (rules_root / "cco-core.md").write_text("# Old Core")
        (rules_root / "cco-ai.md").write_text("# Old AI")
        # Custom user rule (should be preserved)
        (rules_root / "custom-rule.md").write_text("# Custom")
        # Current format - in cco/ subdir
        (cco_subdir / "core.md").write_text("# New Core")
        (cco_subdir / "ai.md").write_text("# New AI")

        result = clean_previous_installation(verbose=False, target_dir=tmp_path)

        # Both old (root) and new (cco/) files should be removed
        assert result["rules"] >= 4  # 2 old + 2 new (may include cco-adaptive.md too)
        # Custom rule should be preserved
        assert (rules_root / "custom-rule.md").exists()
        # Old format files removed
        assert not (rules_root / "cco-core.md").exists()
        assert not (rules_root / "cco-ai.md").exists()
        # New format files removed
        assert not (cco_subdir / "core.md").exists()
        assert not (cco_subdir / "ai.md").exists()

    def test_handles_nonexistent_dirs(self, tmp_path):
        """Test handles nonexistent directories gracefully."""
        # Use a fresh tmp_path subdirectory that doesn't exist
        nonexistent = tmp_path / "nonexistent"
        result = clean_previous_installation(verbose=False, target_dir=nonexistent)

        assert result["commands"] == 0
        assert result["agents"] == 0
        assert result["rules"] == 0

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output during cleanup."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-old.md").write_text("old")

        clean_previous_installation(verbose=True, target_dir=tmp_path)

        captured = capsys.readouterr()
        assert "Cleaning previous installation" in captured.out
        assert "Commands (1):" in captured.out
        assert "cco-old.md" in captured.out

    def test_full_cleanup_scenario(self, tmp_path, capsys):
        """Test complete cleanup with all components present."""
        # Setup old installation
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "cco-config.md").write_text("old tune")
        (commands_dir / "cco-optimize.md").write_text("old audit")

        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "cco-agent-analyze.md").write_text("old agent")

        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# User content\n\n<!-- CCO_STANDARDS_START -->\nOld\n<!-- CCO_STANDARDS_END -->"
        )

        result = clean_previous_installation(verbose=True, target_dir=tmp_path)

        # Verify all old components removed
        assert result["commands"] == 2
        assert result["agents"] == 1
        assert result["rules"] >= 1

        # Files should be removed or cleaned
        assert not any(commands_dir.glob("cco-*.md"))
        assert not any(agents_dir.glob("cco-*.md"))
        assert "CCO_STANDARDS_START" not in claude_md.read_text()


class TestSetupCommands:
    """Test setup_commands function."""

    def test_creates_commands_dir(self, tmp_path):
        """Test creates commands directory."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "pkg" / subdir if subdir else tmp_path / "pkg"
            )
            (tmp_path / "pkg" / "command-templates").mkdir(parents=True)
            (tmp_path / "pkg" / "command-templates" / "cco-test.md").touch()

            installed = setup_commands(target_dir=tmp_path)

            assert (tmp_path / "commands").exists()
            assert len(installed) == 1
            assert "cco-test.md" in installed

    def test_returns_empty_if_no_source(self, tmp_path):
        """Test returns empty list if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "nonexistent" / subdir
                if subdir
                else tmp_path / "nonexistent"
            )

            installed = setup_commands(target_dir=tmp_path)

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

        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "pkg" / subdir if subdir else tmp_path / "pkg"
            )
            (tmp_path / "pkg" / "command-templates").mkdir(parents=True)
            (tmp_path / "pkg" / "command-templates" / "cco-new.md").write_text("new content")

            installed = setup_commands(target_dir=tmp_path)

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
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "pkg" / subdir if subdir else tmp_path / "pkg"
            )
            (tmp_path / "pkg" / "agent-templates").mkdir(parents=True)
            (tmp_path / "pkg" / "agent-templates" / "cco-agent-test.md").touch()

            installed = setup_agents(target_dir=tmp_path)

            assert (tmp_path / "agents").exists()
            assert len(installed) == 1
            assert "cco-agent-test.md" in installed

    def test_returns_empty_if_no_source(self, tmp_path):
        """Test returns empty list if source dir doesn't exist."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "nonexistent" / subdir
                if subdir
                else tmp_path / "nonexistent"
            )

            installed = setup_agents(target_dir=tmp_path)

            assert installed == []


class TestCleanClaudeMd:
    """Test clean_claude_md function - cleans old CCO markers from CLAUDE.md."""

    def test_cleans_old_markers(self, tmp_path):
        """Test cleans old CCO markers from CLAUDE.md."""
        from claudecodeoptimizer.install import clean_claude_md

        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My Rules\n\n<!-- CCO_STANDARDS_START -->Old content<!-- CCO_STANDARDS_END -->\n\nKeep this"
        )

        removed = clean_claude_md(verbose=False, target_dir=tmp_path)

        assert removed == 1
        content = claude_md.read_text()
        assert "# My Rules" in content
        assert "Keep this" in content
        assert "CCO_STANDARDS_START" not in content

    def test_cleans_old_markers_verbose(self, tmp_path, capsys):
        """Test cleans old CCO markers with verbose output."""
        from claudecodeoptimizer.install import clean_claude_md

        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My Rules\n\n<!-- CCO_STANDARDS_START -->Old content<!-- CCO_STANDARDS_END -->\n\nKeep this"
        )

        removed = clean_claude_md(verbose=True, target_dir=tmp_path)

        assert removed == 1
        captured = capsys.readouterr()
        assert "CLAUDE.md: cleaned" in captured.out
        assert "old CCO marker" in captured.out

    def test_removes_empty_file(self, tmp_path):
        """Test removes CLAUDE.md if empty after cleaning."""
        from claudecodeoptimizer.install import clean_claude_md

        claude_md = tmp_path / "CLAUDE.md"
        # File with only CCO content
        claude_md.write_text("<!-- CCO_CORE_START -->Content<!-- CCO_CORE_END -->")

        removed = clean_claude_md(verbose=False, target_dir=tmp_path)

        assert removed == 1
        # File should be deleted since it's empty
        assert not claude_md.exists()

    def test_no_markers_to_clean(self, tmp_path):
        """Test handles file with no CCO markers."""
        from claudecodeoptimizer.install import clean_claude_md

        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# My Custom Rules\n\nSome content")

        removed = clean_claude_md(verbose=False, target_dir=tmp_path)

        assert removed == 0
        content = claude_md.read_text()
        assert "# My Custom Rules" in content


class TestSetupLocalStatusline:
    """Test setup_local_statusline function."""

    def test_success(self, tmp_path):
        """Test successfully sets up local statusline."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("// CCO Statusline\nconsole.log('cco-full');")
        (src_dir / "cco-minimal.js").write_text("// CCO Statusline\nconsole.log('cco-minimal');")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project_path, "cco-full", verbose=False)

        assert result is True
        assert (project_path / ".claude" / "cco-statusline.js").exists()
        assert (project_path / ".claude" / "settings.json").exists()
        settings = json.loads((project_path / ".claude" / "settings.json").read_text())
        assert settings["statusLine"]["command"] == "node .claude/cco-statusline.js"

    def test_minimal_mode(self, tmp_path):
        """Test minimal statusline mode."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-minimal.js").write_text("// CCO Statusline\nconsole.log('cco-minimal');")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project_path, "cco-minimal", verbose=False)

        assert result is True
        content = (project_path / ".claude" / "cco-statusline.js").read_text()
        assert "cco-minimal" in content

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
            "claudecodeoptimizer.local.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
            result = setup_local_statusline(project_path, "cco-full", verbose=True)

        assert result is False
        captured = capsys.readouterr()
        assert "Statusline source not found" in captured.out

    def test_preserves_existing_settings(self, tmp_path):
        """Test preserves existing settings.json content."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text(json.dumps({"existingKey": "value"}))

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project_path, "cco-full", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert settings["existingKey"] == "value"
        assert "statusLine" in settings

    def test_handles_invalid_json(self, tmp_path):
        """Test handles invalid JSON in existing settings."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        local_claude = project_path / ".claude"
        local_claude.mkdir(parents=True)
        (local_claude / "settings.json").write_text("invalid json {{{")

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project_path, "cco-full", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert "statusLine" in settings

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_statusline(project_path, "cco-full", verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "cco-statusline.js" in captured.out
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

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
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

            with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
                result = setup_local_permissions(project_path, level, verbose=False)

            assert result is True

    def test_invalid_level(self, tmp_path, capsys):
        """Test returns False for invalid level."""

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
            "claudecodeoptimizer.local.get_content_path",
            return_value=tmp_path / "nonexistent",
        ):
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

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
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

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
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

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
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

        with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
            result = setup_local_permissions(project_path, "balanced", verbose=False)

        assert result is True
        settings = json.loads((local_claude / "settings.json").read_text())
        assert "permissions" in settings
        assert settings["_cco_managed"] is True


class TestRunLocalMode:
    """Test _run_local_mode function."""

    def test_nonexistent_path(self, tmp_path, capsys):
        """Test error for nonexistent path."""
        with patch.object(sys, "argv", ["cco-install", "--local", str(tmp_path / "nonexistent")]):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.err

    def test_not_a_directory(self, tmp_path, capsys):
        """Test error when path is not a directory."""
        file_path = tmp_path / "file.txt"
        file_path.touch()

        with patch.object(sys, "argv", ["cco-install", "--local", str(file_path)]):
            result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Not a directory" in captured.err

    def test_creates_claude_dir_only(self, tmp_path, capsys):
        """Test creates .claude directory when no options specified."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch.object(sys, "argv", ["cco-install", "--local", str(project_path)]):
                result = post_install()

        assert result == 0
        assert (project_path / ".claude").exists()
        captured = capsys.readouterr()
        assert "Created:" in captured.out

    def test_with_statusline(self, tmp_path, capsys):
        """Test local mode with statusline option."""
        src_dir = tmp_path / "pkg" / "statusline"
        src_dir.mkdir(parents=True)
        (src_dir / "cco-full.js").write_text("// CCO Statusline")

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
                with patch.object(
                    sys,
                    "argv",
                    ["cco-install", "--local", str(project_path), "--statusline", "cco-full"],
                ):
                    result = post_install()

        assert result == 0
        assert (project_path / ".claude" / "cco-statusline.js").exists()
        captured = capsys.readouterr()
        assert "Statusline:" in captured.out

    def test_with_permissions(self, tmp_path, capsys):
        """Test local mode with permissions option."""
        src_dir = tmp_path / "pkg" / "permissions"
        src_dir.mkdir(parents=True)
        (src_dir / "balanced.json").write_text(json.dumps({"permissions": {}}))

        project_path = tmp_path / "project"
        project_path.mkdir()

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch("claudecodeoptimizer.local.get_content_path", return_value=src_dir):
                with patch.object(
                    sys,
                    "argv",
                    ["cco-install", "--local", str(project_path), "--permissions", "balanced"],
                ):
                    result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "Permissions:" in captured.out

    def test_with_both_options(self, tmp_path, capsys):
        """Test local mode with both statusline and permissions."""
        statusline_dir = tmp_path / "pkg" / "statusline"
        statusline_dir.mkdir(parents=True)
        (statusline_dir / "cco-minimal.js").write_text("// CCO Statusline")

        perm_dir = tmp_path / "pkg" / "permissions"
        perm_dir.mkdir(parents=True)
        (perm_dir / "safe.json").write_text(json.dumps({"permissions": {}}))

        project_path = tmp_path / "project"
        project_path.mkdir()

        def mock_content_path(subdir):
            if subdir == "statusline":
                return statusline_dir
            return perm_dir

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch("claudecodeoptimizer.local.get_content_path", side_effect=mock_content_path):
                with patch.object(
                    sys,
                    "argv",
                    [
                        "cco-install",
                        "--local",
                        str(project_path),
                        "--statusline",
                        "cco-minimal",
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
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch(
                "claudecodeoptimizer.local.get_content_path",
                return_value=tmp_path / "nonexistent",
            ):
                with patch.object(
                    sys,
                    "argv",
                    ["cco-install", "--local", str(project_path), "--statusline", "cco-full"],
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
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            with patch(
                "claudecodeoptimizer.local.get_content_path",
                return_value=tmp_path / "nonexistent",
            ):
                with patch.object(
                    sys,
                    "argv",
                    ["cco-install", "--local", str(project_path), "--permissions", "balanced"],
                ):
                    result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "completed with errors" in captured.err

    def test_path_traversal_rejected(self, tmp_path, capsys):
        """Test path outside home/cwd is rejected."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Mock both home and cwd to be different from tmp_path
        fake_home = Path("/nonexistent/home")
        fake_cwd = Path("/nonexistent/cwd")

        with patch("pathlib.Path.home", return_value=fake_home):
            with patch("pathlib.Path.cwd", return_value=fake_cwd):
                with patch.object(sys, "argv", ["cco-install", "--local", str(project_path)]):
                    result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Path must be within home directory or current working directory" in captured.err


class TestPostInstallValidation:
    """Test post_install argument validation."""

    def test_statusline_requires_local(self, capsys):
        """Test --statusline without --local raises error."""
        with patch.object(sys, "argv", ["cco-install", "--statusline", "cco-full"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 2  # argparse error code
        captured = capsys.readouterr()
        assert "require --local" in captured.err

    def test_permissions_requires_local(self, capsys):
        """Test --permissions without --local raises error."""
        with patch.object(sys, "argv", ["cco-install", "--permissions", "balanced"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "require --local" in captured.err


class TestDryRunMode:
    """Test --dry-run mode for install_hook."""

    def test_dry_run_shows_preview(self, tmp_path, capsys):
        """Test --dry-run shows what would be installed without making changes."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            # Setup mock content paths
            pkg_path = tmp_path / "pkg"
            (pkg_path / "command-templates").mkdir(parents=True)
            (pkg_path / "command-templates" / "cco-test.md").write_text("# Test")
            (pkg_path / "agent-templates").mkdir(parents=True)
            (pkg_path / "agent-templates" / "cco-agent-test.md").write_text("# Agent")
            (pkg_path / "rules").mkdir(parents=True)
            (pkg_path / "rules" / "cco-core.md").write_text("# Core")

            mock_content.side_effect = lambda subdir="": pkg_path / subdir if subdir else pkg_path
            with patch.object(sys, "argv", ["cco-install", "--dry-run", "--dir", str(tmp_path)]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "Would clean previous installation" in captured.out
        assert "Would install" in captured.out
        assert "This was a dry run" in captured.out

    def test_dry_run_no_changes(self, tmp_path, capsys):
        """Test --dry-run does not create any files."""
        target = tmp_path / "target"
        # Don't create target - dry run shouldn't create it

        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            pkg_path = tmp_path / "pkg"
            (pkg_path / "command-templates").mkdir(parents=True)
            mock_content.side_effect = lambda subdir="": pkg_path / subdir if subdir else pkg_path
            with patch.object(sys, "argv", ["cco-install", "--dry-run", "--dir", str(target)]):
                result = post_install()

        assert result == 0
        # Target directory should NOT be created in dry-run mode
        assert not target.exists()

    def test_dry_run_previews_files(self, tmp_path, capsys):
        """Test --dry-run lists files that would be installed."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            pkg_path = tmp_path / "pkg"
            (pkg_path / "command-templates").mkdir(parents=True)
            (pkg_path / "command-templates" / "cco-config.md").write_text("# Config")
            (pkg_path / "command-templates" / "cco-status.md").write_text("# Status")
            (pkg_path / "agent-templates").mkdir(parents=True)
            (pkg_path / "rules").mkdir(parents=True)
            (pkg_path / "rules" / "cco-core.md").write_text("# Core")
            (pkg_path / "rules" / "cco-ai.md").write_text("# AI")

            mock_content.side_effect = lambda subdir="": pkg_path / subdir if subdir else pkg_path
            with patch.object(sys, "argv", ["cco-install", "--dry-run", "--dir", str(tmp_path)]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        # Check that files are listed
        assert "+ cco-config.md" in captured.out
        assert "+ cco-status.md" in captured.out
        # Rules preview shows cco/core.md format
        assert "+ cco/core.md" in captured.out
        assert "+ cco/ai.md" in captured.out

    def test_dry_run_footer_message(self, tmp_path, capsys):
        """Test --dry-run shows footer with instructions."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            pkg_path = tmp_path / "pkg"
            pkg_path.mkdir(parents=True)
            mock_content.side_effect = lambda subdir="": pkg_path / subdir if subdir else pkg_path
            with patch.object(sys, "argv", ["cco-install", "--dry-run", "--dir", str(tmp_path)]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "No changes were made" in captured.out
        assert "Run without --dry-run" in captured.out


class TestPathAndCatUtilities:
    """Test --path and --cat utility options."""

    def test_path_existing_file(self, tmp_path, capsys):
        """Test --path returns path of existing file."""
        with patch("claudecodeoptimizer.install_hook.get_content_path") as mock_content:
            content_path = tmp_path / "content"
            content_path.mkdir(parents=True)
            (content_path / "rules" / "cco-adaptive.md").mkdir(parents=True)
            (content_path / "rules" / "cco-adaptive.md").rmdir()
            rules_dir = content_path / "rules"
            rules_dir.mkdir(exist_ok=True)
            (rules_dir / "cco-adaptive.md").write_text("# Adaptive")

            mock_content.return_value = content_path
            with patch.object(sys, "argv", ["cco-install", "--path", "rules/cco-adaptive.md"]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "cco-adaptive.md" in captured.out

    def test_path_nonexistent_file(self, tmp_path, capsys):
        """Test --path returns error for nonexistent file."""
        with patch("claudecodeoptimizer.install_hook.get_content_path") as mock_content:
            content_path = tmp_path / "content"
            content_path.mkdir(parents=True)
            mock_content.return_value = content_path

            with patch.object(sys, "argv", ["cco-install", "--path", "nonexistent.md"]):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Path not found" in captured.err

    def test_cat_existing_file(self, tmp_path, capsys):
        """Test --cat outputs file content."""
        with patch("claudecodeoptimizer.install_hook.get_content_path") as mock_content:
            content_path = tmp_path / "content"
            rules_dir = content_path / "rules"
            rules_dir.mkdir(parents=True)
            (rules_dir / "cco-adaptive.md").write_text("# Adaptive Rules\n\nContent here")

            mock_content.return_value = content_path
            with patch.object(sys, "argv", ["cco-install", "--cat", "rules/cco-adaptive.md"]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "# Adaptive Rules" in captured.out
        assert "Content here" in captured.out

    def test_cat_nonexistent_file(self, tmp_path, capsys):
        """Test --cat returns error for nonexistent file."""
        with patch("claudecodeoptimizer.install_hook.get_content_path") as mock_content:
            content_path = tmp_path / "content"
            content_path.mkdir(parents=True)
            mock_content.return_value = content_path

            with patch.object(sys, "argv", ["cco-install", "--cat", "nonexistent.md"]):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_cat_directory_returns_error(self, tmp_path, capsys):
        """Test --cat returns error when path is a directory."""
        with patch("claudecodeoptimizer.install_hook.get_content_path") as mock_content:
            content_path = tmp_path / "content"
            (content_path / "rules").mkdir(parents=True)

            mock_content.return_value = content_path
            with patch.object(sys, "argv", ["cco-install", "--cat", "rules"]):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err


class TestDirWithNonexistentTarget:
    """Test --dir with non-existent target directory."""

    def test_dir_creates_nonexistent_target(self, tmp_path, capsys):
        """Test --dir creates target directory if it doesn't exist."""
        target = tmp_path / "new_claude_dir"
        assert not target.exists()

        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            pkg_path = tmp_path / "pkg"
            (pkg_path / "command-templates").mkdir(parents=True)
            (pkg_path / "command-templates" / "cco-test.md").write_text("# Test")
            mock_content.side_effect = lambda subdir="": pkg_path / subdir if subdir else pkg_path
            with patch.object(sys, "argv", ["cco-install", "--dir", str(target)]):
                result = post_install()

        assert result == 0
        assert target.exists()
        assert (target / "commands").exists()


class TestPostInstall:
    """Test post_install function."""

    def test_help_flag(self, capsys):
        """Test --help shows usage."""
        with patch.object(sys, "argv", ["cco-install", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "cco-install" in captured.out

    def test_h_flag(self, capsys):
        """Test -h shows usage."""
        with patch.object(sys, "argv", ["cco-install", "-h"]):
            with pytest.raises(SystemExit) as exc_info:
                post_install()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "cco-install" in captured.out

    def test_successful_setup(self, tmp_path, capsys):
        """Test successful setup with --dir."""
        with patch("claudecodeoptimizer.install.get_content_path") as mock_content:
            mock_content.side_effect = (
                lambda subdir="": tmp_path / "pkg" / subdir if subdir else tmp_path / "pkg"
            )
            with patch.object(sys, "argv", ["cco-install", "--dir", str(tmp_path)]):
                result = post_install()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO Setup" in captured.out
        assert "Installed:" in captured.out
        # Statusline is no longer installed by cco-install
        assert "statusline" not in captured.out.lower() or "cco-config" in captured.out

    def test_exception_handling(self, tmp_path, capsys):
        """Test exception during setup."""
        with patch.object(sys, "argv", ["cco-install", "--dir", str(tmp_path)]):
            with patch(
                "claudecodeoptimizer.install_hook.setup_commands",
                side_effect=RuntimeError("Test error"),
            ):
                result = post_install()

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err

    def test_help_mentions_cco_tune(self, capsys):
        """Test help mentions cco-config for statusline/permissions."""
        with patch.object(sys, "argv", ["cco-install", "--help"]):
            with pytest.raises(SystemExit):
                post_install()

        captured = capsys.readouterr()
        assert "cco-config" in captured.out


class TestSetupRules:
    """Test setup_rules function (installs to cco/ subdirectory)."""

    def test_setup_rules_creates_directory(self, tmp_path):
        """Test setup_rules creates cco/ subdirectory and copies files with new names."""
        from claudecodeoptimizer.install import setup_rules

        # Create source rules in content dir (source files have cco- prefix)
        src_rules = tmp_path / "content" / "rules"
        src_rules.mkdir(parents=True)
        (src_rules / "cco-core.md").write_text("# Core Rules")
        (src_rules / "cco-ai.md").write_text("# AI Rules")
        # Note: tools.md and adaptive.md are NOT installed globally anymore
        # They stay in the package for on-demand loading by commands

        with patch(
            "claudecodeoptimizer.install.get_content_path",
            side_effect=lambda subdir="": tmp_path / "content" / subdir
            if subdir
            else tmp_path / "content",
        ):
            result = setup_rules(verbose=False, target_dir=tmp_path)

        rules_dir = tmp_path / "rules" / "cco"
        assert rules_dir.exists()
        # Files are renamed (cco-core.md -> core.md)
        assert (rules_dir / "core.md").exists()
        assert (rules_dir / "ai.md").exists()
        # tools.md and adaptive.md are NOT installed globally
        assert not (rules_dir / "tools.md").exists()
        assert not (rules_dir / "adaptive.md").exists()
        assert result["core"] == 1
        assert result["ai"] == 1
        assert result["total"] == 2

    def test_setup_rules_verbose_output(self, tmp_path, capsys):
        """Test setup_rules verbose output shows cco/ prefix."""
        from claudecodeoptimizer.install import setup_rules

        src_rules = tmp_path / "content" / "rules"
        src_rules.mkdir(parents=True)
        (src_rules / "cco-core.md").write_text("# Core")

        with patch(
            "claudecodeoptimizer.install.get_content_path",
            side_effect=lambda subdir="": tmp_path / "content" / subdir
            if subdir
            else tmp_path / "content",
        ):
            setup_rules(verbose=True, target_dir=tmp_path)

        captured = capsys.readouterr()
        # Output now shows "cco/core.md" instead of "cco-core.md"
        assert "+ cco/core.md" in captured.out

    def test_setup_rules_removes_old_cco_files_only(self, tmp_path):
        """Test setup_rules removes existing CCO rule files in cco/ subdir."""
        from claudecodeoptimizer.install import setup_rules

        src_rules = tmp_path / "content" / "rules"
        src_rules.mkdir(parents=True)
        (src_rules / "cco-core.md").write_text("# New Core")

        # cco/ subdirectory with existing files
        rules_dir = tmp_path / "rules" / "cco"
        rules_dir.mkdir(parents=True)
        (rules_dir / "core.md").write_text("# Old Core")
        (rules_dir / "custom-rule.md").write_text("# Custom Rule")

        with patch(
            "claudecodeoptimizer.install.get_content_path",
            side_effect=lambda subdir="": tmp_path / "content" / subdir
            if subdir
            else tmp_path / "content",
        ):
            setup_rules(verbose=False, target_dir=tmp_path)

        # Custom rule preserved, CCO rule updated
        assert (rules_dir / "custom-rule.md").exists()
        assert (rules_dir / "core.md").exists()
        assert (rules_dir / "core.md").read_text() == "# New Core"

    def test_setup_rules_no_source_dir(self, tmp_path):
        """Test setup_rules returns empty when source doesn't exist."""
        from claudecodeoptimizer.install import setup_rules

        with patch(
            "claudecodeoptimizer.install.get_content_path",
            side_effect=lambda subdir="": tmp_path / "nonexistent" / subdir
            if subdir
            else tmp_path / "nonexistent",
        ):
            result = setup_rules(verbose=False, target_dir=tmp_path)

        # adaptive.md is no longer installed globally
        assert result == {"core": 0, "ai": 0, "tools": 0, "total": 0}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

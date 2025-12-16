"""Unit tests for cco_uninstall module."""

import json
import subprocess
import sys
from unittest.mock import MagicMock, patch

from claudecodeoptimizer.ui import display_removal_plan
from claudecodeoptimizer.uninstall import _execute_removal, main
from claudecodeoptimizer.uninstall.detection import (
    detect_install_method,
    has_cco_statusline,
    has_claude_md_rules,
    list_cco_files,
)
from claudecodeoptimizer.uninstall.removal import (
    remove_cco_files,
    remove_claude_md_rules,
    remove_statusline,
    uninstall_package,
)


class TestDetectInstallMethod:
    @patch("subprocess.run")
    def test_detect_pipx(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="claudecodeoptimizer")
        assert detect_install_method() == "pipx"

    @patch("subprocess.run")
    def test_detect_none(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        assert detect_install_method() is None

    @patch("subprocess.run")
    def test_detect_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 5)
        assert detect_install_method() is None

    @patch("subprocess.run")
    def test_detect_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert detect_install_method() is None


class TestListCcoFiles:
    def test_list_empty(self, tmp_path):
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.uninstall.detection.get_cco_commands", return_value=[]):
                with patch("claudecodeoptimizer.uninstall.detection.get_cco_agents", return_value=[]):
                    files = list_cco_files()
                    assert files["commands"] == []
                    assert files["agents"] == []

    def test_list_with_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file = tmp_path / "commands" / "cco-config.md"
        agent_file = tmp_path / "agents" / "cco-agent-analyze.md"
        cmd_file.touch()
        agent_file.touch()
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            with patch(
                "claudecodeoptimizer.uninstall.detection.get_cco_commands", return_value=[cmd_file]
            ):
                with patch(
                    "claudecodeoptimizer.uninstall.detection.get_cco_agents", return_value=[agent_file]
                ):
                    files = list_cco_files()
                    assert files["commands"] == ["cco-config.md"]
                    assert files["agents"] == ["cco-agent-analyze.md"]


class TestHasClaudeMdRules:
    def test_no_file(self, tmp_path):
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            assert has_claude_md_rules() == []

    def test_with_rules(self, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->")
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            sections = has_claude_md_rules()
            # Universal pattern returns "CCO Content (N section(s))"
            assert len(sections) == 1
            assert "CCO Content" in sections[0]


class TestRemoveCcoFiles:
    def test_remove_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        cco_file = tmp_path / "commands" / "cco-config.md"
        user_file = tmp_path / "commands" / "user-custom.md"
        cco_file.touch()
        user_file.touch()
        with patch("claudecodeoptimizer.uninstall.removal.CLAUDE_DIR", tmp_path):
            with patch(
                "claudecodeoptimizer.uninstall.removal.get_cco_commands", return_value=[cco_file]
            ):
                with patch("claudecodeoptimizer.uninstall.removal.get_cco_agents", return_value=[]):
                    removed = remove_cco_files(verbose=False)
        assert removed["commands"] == 1
        assert not cco_file.exists()
        assert user_file.exists()

    def test_remove_files_verbose(self, tmp_path, capsys):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file = tmp_path / "commands" / "cco-config.md"
        agent_file = tmp_path / "agents" / "cco-agent.md"
        cmd_file.touch()
        agent_file.touch()
        with patch("claudecodeoptimizer.uninstall.removal.CLAUDE_DIR", tmp_path):
            with patch(
                "claudecodeoptimizer.uninstall.removal.get_cco_commands", return_value=[cmd_file]
            ):
                with patch(
                    "claudecodeoptimizer.uninstall.removal.get_cco_agents", return_value=[agent_file]
                ):
                    removed = remove_cco_files(verbose=True)
        assert removed["commands"] == 1
        assert removed["agents"] == 1


class TestRemoveClaudeMdRules:
    def test_no_file(self, tmp_path):
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.uninstall.removal.CLAUDE_DIR", tmp_path):
                removed = remove_claude_md_rules()
                assert removed == []

    def test_remove_rules(self, tmp_path, capsys):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My\n<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->\nOther"
        )
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.uninstall.removal.CLAUDE_DIR", tmp_path):
                removed = remove_claude_md_rules(verbose=True)
        # Universal pattern returns "CCO Content (N section(s))"
        assert len(removed) == 1
        assert "CCO Content" in removed[0]


class TestUninstallPackage:
    @patch("subprocess.run")
    def test_uninstall_pip(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert uninstall_package("pip") is True

    @patch("subprocess.run")
    def test_uninstall_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        assert uninstall_package("pip") is False

    @patch("subprocess.run")
    def test_uninstall_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 30)
        assert uninstall_package("pip") is False

    @patch("subprocess.run")
    def test_uninstall_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert uninstall_package("pip") is False


class TestHasCcoStatusline:
    """Test has_cco_statusline function."""

    def test_no_file(self, tmp_path):
        """Test returns False when statusline file doesn't exist."""
        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", tmp_path / "statusline.js"):
            assert has_cco_statusline() is False

    def test_file_exists_with_cco_content(self, tmp_path):
        """Test returns True when statusline file exists with CCO content."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", statusline):
            assert has_cco_statusline() is True

    def test_file_exists_without_cco_content(self, tmp_path):
        """Test returns False when statusline file exists but without CCO marker."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// Custom statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", statusline):
            assert has_cco_statusline() is False


class TestRemoveStatusline:
    """Test remove_statusline function."""

    def test_remove_statusline_file(self, tmp_path):
        """Test removes statusline.js when it's a CCO file."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"statusLine": {"type": "command"}}))

        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.uninstall.removal.STATUSLINE_FILE", statusline):
                with patch("claudecodeoptimizer.uninstall.removal.SETTINGS_FILE", settings):
                    result = remove_statusline(verbose=False)

        assert result is True
        assert not statusline.exists()
        # Check settings.json was updated
        updated_settings = json.loads(settings.read_text())
        assert "statusLine" not in updated_settings

    def test_remove_statusline_verbose(self, tmp_path, capsys):
        """Test verbose output during statusline removal."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"statusLine": {"type": "command"}}))

        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.uninstall.removal.STATUSLINE_FILE", statusline):
                with patch("claudecodeoptimizer.uninstall.removal.SETTINGS_FILE", settings):
                    result = remove_statusline(verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "cco-statusline.js" in captured.out
        assert "statusLine removed" in captured.out

    def test_no_statusline_to_remove(self, tmp_path):
        """Test returns False when nothing to remove."""
        with patch(
            "claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", tmp_path / "nonexistent.js"
        ):
            with patch(
                "claudecodeoptimizer.uninstall.removal.STATUSLINE_FILE", tmp_path / "nonexistent.js"
            ):
                with patch(
                    "claudecodeoptimizer.uninstall.removal.SETTINGS_FILE", tmp_path / "nonexistent.json"
                ):
                    result = remove_statusline(verbose=False)
        assert result is False

    def test_settings_json_decode_error(self, tmp_path):
        """Test handles invalid JSON in settings.json gracefully."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        settings = tmp_path / "settings.json"
        settings.write_text("not valid json {{{")

        with patch("claudecodeoptimizer.uninstall.detection.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.uninstall.removal.STATUSLINE_FILE", statusline):
                with patch("claudecodeoptimizer.uninstall.removal.SETTINGS_FILE", settings):
                    result = remove_statusline(verbose=False)

        assert result is True  # Statusline file was removed
        assert not statusline.exists()


class TestHasCcoPermissions:
    """Test has_cco_permissions function."""

    def test_no_file(self, tmp_path):
        """Test returns False when settings.json doesn't exist."""
        from claudecodeoptimizer.uninstall.detection import has_cco_permissions

        result = has_cco_permissions(tmp_path / "settings.json")
        assert result is False

    def test_with_cco_marker(self, tmp_path):
        """Test returns True when CCO marker is present."""
        from claudecodeoptimizer.uninstall.detection import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"_cco_managed": True, "permissions": {}}))
        result = has_cco_permissions(settings)
        assert result is True

    def test_with_meta_in_permissions(self, tmp_path):
        """Test returns True when _meta is in permissions."""
        from claudecodeoptimizer.uninstall.detection import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(
            json.dumps({"permissions": {"_meta": {"level": "balanced"}, "allow": []}})
        )
        result = has_cco_permissions(settings)
        assert result is True

    def test_without_cco_content(self, tmp_path):
        """Test returns False when no CCO markers present."""
        from claudecodeoptimizer.uninstall.detection import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"permissions": {"allow": []}}))
        result = has_cco_permissions(settings)
        assert result is False

    def test_invalid_json(self, tmp_path):
        """Test returns False on invalid JSON."""
        from claudecodeoptimizer.uninstall.detection import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text("invalid json {{{")
        result = has_cco_permissions(settings)
        assert result is False


class TestRemovePermissions:
    """Test remove_permissions function."""

    def test_remove_permissions(self, tmp_path):
        """Test removes permissions from settings.json."""
        from claudecodeoptimizer.uninstall.removal import remove_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(
            json.dumps({"_cco_managed": True, "permissions": {"allow": []}, "other": "data"})
        )
        result = remove_permissions(settings, verbose=False)
        assert result is True

        content = json.loads(settings.read_text())
        assert "permissions" not in content
        assert "_cco_managed" not in content
        assert content["other"] == "data"

    def test_no_file(self, tmp_path):
        """Test returns False when file doesn't exist."""
        from claudecodeoptimizer.uninstall.removal import remove_permissions

        result = remove_permissions(tmp_path / "nonexistent.json", verbose=False)
        assert result is False

    def test_remove_permissions_verbose(self, tmp_path, capsys):
        """Test verbose output during permissions removal."""
        from claudecodeoptimizer.uninstall.removal import remove_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"permissions": {"allow": []}}))
        result = remove_permissions(settings, verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "permissions removed" in captured.out

    def test_invalid_json(self, tmp_path):
        """Test returns False on invalid JSON."""
        from claudecodeoptimizer.uninstall.removal import remove_permissions

        settings = tmp_path / "settings.json"
        settings.write_text("invalid json {{{")
        result = remove_permissions(settings, verbose=False)
        assert result is False


class TestHasRulesDirOld:
    """Test has_rules_dir_old function (old root-level rules)."""

    def test_no_dir(self, tmp_path):
        """Test returns False when old rules root doesn't exist."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir_old

        with patch("claudecodeoptimizer.uninstall.detection.OLD_RULES_ROOT", tmp_path / "nonexistent"):
            result = has_rules_dir_old()
        assert result is False

    def test_empty_dir(self, tmp_path):
        """Test returns False when rules dir exists but has no CCO files."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir_old

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "custom-rule.md").write_text("# Custom")  # Not a CCO file
        with patch("claudecodeoptimizer.uninstall.detection.OLD_RULES_ROOT", rules_dir):
            result = has_rules_dir_old()
        assert result is False

    def test_with_old_cco_rules(self, tmp_path):
        """Test returns True when old CCO rule files exist in root."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir_old

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "cco-core.md").write_text("# Old Core")
        with patch("claudecodeoptimizer.uninstall.detection.OLD_RULES_ROOT", rules_dir):
            result = has_rules_dir_old()
        assert result is True


class TestRemoveRulesDirOld:
    """Test remove_rules_dir_old function (old root-level rules)."""

    def test_no_dir(self, tmp_path):
        """Test returns False when no rules dir exists."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir_old

        with patch("claudecodeoptimizer.uninstall.removal.OLD_RULES_ROOT", tmp_path / "nonexistent"):
            result = remove_rules_dir_old(verbose=False)
        assert result is False

    def test_remove_old_cco_rules(self, tmp_path, capsys):
        """Test removes old CCO rule files from root."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir_old

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "cco-core.md").write_text("# Old Core")
        (rules_dir / "cco-ai.md").write_text("# Old AI")
        (rules_dir / "custom-rule.md").write_text("# Keep")

        with patch("claudecodeoptimizer.uninstall.removal.OLD_RULES_ROOT", rules_dir):
            result = remove_rules_dir_old(verbose=True)

        assert result is True
        assert not (rules_dir / "cco-core.md").exists()
        assert not (rules_dir / "cco-ai.md").exists()
        assert (rules_dir / "custom-rule.md").exists()
        captured = capsys.readouterr()
        assert "old CCO files" in captured.out

    def test_no_cco_files_to_remove(self, tmp_path):
        """Test returns False when no CCO files exist."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir_old

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "custom-rule.md").write_text("# Custom")

        with patch("claudecodeoptimizer.uninstall.removal.OLD_RULES_ROOT", rules_dir):
            result = remove_rules_dir_old(verbose=False)
        assert result is False


class TestHasClaudeMdRulesLargeFile:
    """Test has_claude_md_rules with large file safety check."""

    def test_large_file_skipped(self, tmp_path):
        """Test returns special message for files larger than MAX_CLAUDE_MD_SIZE."""
        claude_md = tmp_path / "CLAUDE.md"
        # Create a file larger than 1MB would be too slow, so mock the stat
        claude_md.write_text("small content")

        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.uninstall.detection.MAX_CLAUDE_MD_SIZE", 5):  # 5 bytes limit
                result = has_claude_md_rules()

        assert len(result) == 1
        assert "too large" in result[0]


class TestHasRulesDir:
    """Test has_rules_dir function."""

    def test_no_dir(self, tmp_path):
        """Test returns False when rules dir doesn't exist."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir

        with patch("claudecodeoptimizer.uninstall.detection.RULES_DIR", tmp_path / "nonexistent"):
            result = has_rules_dir()
        assert result is False

    def test_empty_dir(self, tmp_path):
        """Test returns False when rules dir exists but is empty."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        with patch("claudecodeoptimizer.uninstall.detection.RULES_DIR", rules_dir):
            result = has_rules_dir()
        assert result is False

    def test_with_cco_rules(self, tmp_path):
        """Test returns True when rules dir has CCO rule files (core.md in cco/)."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir

        # Rules are in ~/.claude/rules/cco/{core,ai}.md
        rules_dir = tmp_path / "rules" / "cco"
        rules_dir.mkdir(parents=True)
        (rules_dir / "core.md").write_text("# Core Rules")
        with patch("claudecodeoptimizer.uninstall.detection.RULES_DIR", rules_dir):
            result = has_rules_dir()
        assert result is True

    def test_with_non_cco_rules_only(self, tmp_path):
        """Test returns False when rules dir has only non-CCO .md files."""
        from claudecodeoptimizer.uninstall.detection import has_rules_dir

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "custom-rule.md").write_text("# Custom Rule")
        with patch("claudecodeoptimizer.uninstall.detection.RULES_DIR", rules_dir):
            result = has_rules_dir()
        assert result is False


class TestRemoveRulesDir:
    """Test remove_rules_dir function."""

    def test_remove_cco_rules_only(self, tmp_path, capsys):
        """Test removes only CCO rule files from cco/ subdir."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir

        # Rules are in ~/.claude/rules/cco/{core,ai}.md
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)
        (cco_dir / "core.md").write_text("# Core")
        (cco_dir / "ai.md").write_text("# AI")
        (cco_dir / "custom-rule.md").write_text("# Custom")  # User file in cco/ dir

        with patch("claudecodeoptimizer.uninstall.removal.RULES_DIR", cco_dir):
            result = remove_rules_dir(verbose=True)

        assert result is True
        # Directory still exists with custom rule (cco/ not empty)
        assert cco_dir.exists()
        assert not (cco_dir / "core.md").exists()
        assert not (cco_dir / "ai.md").exists()
        assert (cco_dir / "custom-rule.md").exists()
        captured = capsys.readouterr()
        assert "rules/cco/ (2 files)" in captured.out

    def test_no_dir_to_remove(self, tmp_path):
        """Test returns False when no rules dir exists."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir

        with patch("claudecodeoptimizer.uninstall.removal.RULES_DIR", tmp_path / "nonexistent"):
            result = remove_rules_dir(verbose=False)
        assert result is False

    def test_remove_empty_cco_dir(self, tmp_path, capsys):
        """Test removes empty cco/ directory after all CCO files removed."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir

        # Create cco/ dir with only CCO files
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)
        (cco_dir / "core.md").write_text("# Core")
        (cco_dir / "ai.md").write_text("# AI")

        with patch("claudecodeoptimizer.uninstall.removal.RULES_DIR", cco_dir):
            result = remove_rules_dir(verbose=True)

        assert result is True
        # Directory should be removed since it's empty
        assert not cco_dir.exists()

    def test_no_cco_files_returns_false(self, tmp_path):
        """Test returns False when cco/ dir exists but has no CCO files."""
        from claudecodeoptimizer.uninstall.removal import remove_rules_dir

        # Create cco/ dir with only non-CCO files
        cco_dir = tmp_path / "rules" / "cco"
        cco_dir.mkdir(parents=True)
        (cco_dir / "custom-rule.md").write_text("# Custom")

        with patch("claudecodeoptimizer.uninstall.removal.RULES_DIR", cco_dir):
            result = remove_rules_dir(verbose=False)

        assert result is False
        # Directory should still exist
        assert cco_dir.exists()
        assert (cco_dir / "custom-rule.md").exists()


class TestDisplayRemovalPlan:
    """Test display_removal_plan function."""

    def test_display_with_rules_dir(self, capsys):
        """Test displays rules directory section when present (cco/ subdir)."""
        display_removal_plan(
            method=None,
            commands=[],
            agents=[],
            rules=[],
            rules_dir=True,
            rules_dir_old=False,
            statusline=False,
            permissions=False,
            total=1,
        )
        captured = capsys.readouterr()
        assert "Rules directory:" in captured.out
        assert "~/.claude/rules/cco/" in captured.out

    def test_display_with_statusline(self, capsys):
        """Test displays statusline section when present."""
        display_removal_plan(
            method=None,
            commands=[],
            agents=[],
            rules=[],
            rules_dir=False,
            rules_dir_old=False,
            statusline=True,
            permissions=False,
            total=1,
        )
        captured = capsys.readouterr()
        assert "Settings (~/.claude/):" in captured.out
        assert "cco-statusline.js" in captured.out
        assert "settings.json" in captured.out

    def test_display_with_permissions(self, capsys):
        """Test displays permissions section when present."""
        display_removal_plan(
            method=None,
            commands=[],
            agents=[],
            rules=[],
            rules_dir=False,
            rules_dir_old=False,
            statusline=False,
            permissions=True,
            total=1,
        )
        captured = capsys.readouterr()
        assert "Settings (~/.claude/):" in captured.out
        assert "permissions" in captured.out

    def test_display_with_rules_dir_old(self, capsys):
        """Test displays rules_dir_old section when present (old root-level)."""
        display_removal_plan(
            method=None,
            commands=[],
            agents=[],
            rules=[],
            rules_dir=False,
            rules_dir_old=True,
            statusline=False,
            permissions=False,
            total=1,
        )
        captured = capsys.readouterr()
        assert "Rules directory:" in captured.out
        assert "old files" in captured.out


class TestExecuteRemoval:
    """Test _execute_removal function."""

    def test_execute_with_rules_dir(self, capsys):
        """Test executes rules directory removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": True,
            "rules_dir_old": False,
            "statusline": False,
            "permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.uninstall.remove_rules_dir") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing rules directory" in captured.out

    def test_execute_with_statusline(self, capsys):
        """Test executes statusline removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "rules_dir_old": False,
            "statusline": True,
            "permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.uninstall.remove_statusline") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing settings" in captured.out

    def test_execute_with_permissions(self, capsys):
        """Test executes permissions removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "rules_dir_old": False,
            "statusline": False,
            "permissions": True,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.uninstall.remove_permissions") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing settings" in captured.out

    def test_execute_with_rules_dir_old(self, capsys):
        """Test executes rules_dir_old removal when present (old root-level)."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "rules_dir_old": True,
            "statusline": False,
            "permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.uninstall.remove_rules_dir_old") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing rules directory" in captured.out


class TestHasClaudeMdRulesNoMatches:
    """Test has_claude_md_rules when no CCO markers found."""

    def test_file_without_cco_markers(self, tmp_path):
        """Test returns empty list when file has no CCO markers."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nSome content without CCO markers")
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            result = has_claude_md_rules()
        assert result == []


class TestRemoveClaudeMdRulesNoMatches:
    """Test remove_claude_md_rules when no CCO markers found."""

    def test_file_without_cco_markers(self, tmp_path):
        """Test returns empty list when file has no CCO markers."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nSome content without CCO markers")
        with patch("claudecodeoptimizer.uninstall.detection.CLAUDE_DIR", tmp_path):
            result = remove_claude_md_rules(verbose=False)
        assert result == []


class TestMain:
    """Test main function - cco-uninstall only handles global ~/.claude/ files."""

    @patch("claudecodeoptimizer.uninstall.has_cco_permissions")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir_old")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir")
    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    @patch("claudecodeoptimizer.uninstall.list_cco_files")
    @patch("claudecodeoptimizer.uninstall.has_claude_md_rules")
    @patch("claudecodeoptimizer.uninstall.has_cco_statusline")
    def test_not_installed(
        self,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        mock_rules_dir_old,
        mock_permissions,
        capsys,
    ):
        mock_detect.return_value = None
        mock_list.return_value = {"agents": [], "commands": []}
        mock_rules.return_value = []
        mock_rules_dir.return_value = False
        mock_rules_dir_old.return_value = False
        mock_statusline.return_value = False
        mock_permissions.return_value = False
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "not installed" in captured.out

    @patch("claudecodeoptimizer.uninstall.has_cco_permissions")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir_old")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir")
    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    @patch("claudecodeoptimizer.uninstall.list_cco_files")
    @patch("claudecodeoptimizer.uninstall.has_claude_md_rules")
    @patch("claudecodeoptimizer.uninstall.has_cco_statusline")
    @patch("builtins.input")
    def test_cancelled(
        self,
        mock_input,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        mock_rules_dir_old,
        mock_permissions,
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"agents": ["a.md"], "commands": ["c.md"]}
        mock_rules.return_value = ["CCO Rules"]
        mock_rules_dir.return_value = False
        mock_rules_dir_old.return_value = False
        mock_statusline.return_value = False
        mock_permissions.return_value = False
        mock_input.return_value = "n"
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("claudecodeoptimizer.uninstall.has_cco_permissions")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir_old")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir")
    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    @patch("claudecodeoptimizer.uninstall.list_cco_files")
    @patch("claudecodeoptimizer.uninstall.has_claude_md_rules")
    @patch("claudecodeoptimizer.uninstall.has_cco_statusline")
    @patch("claudecodeoptimizer.uninstall.uninstall_package")
    @patch("claudecodeoptimizer.uninstall.remove_cco_files")
    @patch("claudecodeoptimizer.uninstall.remove_claude_md_rules")
    @patch("builtins.input")
    def test_full_removal(
        self,
        mock_input,
        mock_rm_rules,
        mock_rm_files,
        mock_uninstall,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        mock_rules_dir_old,
        mock_permissions,
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": ["c.md"], "agents": ["a.md"]}
        mock_rules.return_value = ["CCO Rules"]
        mock_rules_dir.return_value = False
        mock_rules_dir_old.return_value = False
        mock_statusline.return_value = False
        mock_permissions.return_value = False
        mock_input.return_value = "y"
        mock_uninstall.return_value = True
        mock_rm_files.return_value = {"commands": 1, "agents": 1}
        mock_rm_rules.return_value = ["CCO Rules"]
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "removed successfully" in captured.out

    @patch("claudecodeoptimizer.uninstall.has_cco_permissions")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir_old")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir")
    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    @patch("claudecodeoptimizer.uninstall.list_cco_files")
    @patch("claudecodeoptimizer.uninstall.has_claude_md_rules")
    @patch("claudecodeoptimizer.uninstall.has_cco_statusline")
    @patch("claudecodeoptimizer.uninstall.uninstall_package")
    @patch("claudecodeoptimizer.uninstall.remove_cco_files")
    @patch("claudecodeoptimizer.uninstall.remove_claude_md_rules")
    def test_full_removal_with_yes_flag(
        self,
        mock_rm_rules,
        mock_rm_files,
        mock_uninstall,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        mock_rules_dir_old,
        mock_permissions,
        capsys,
    ):
        """Test -y flag skips confirmation prompt."""
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": ["c.md"], "agents": ["a.md"]}
        mock_rules.return_value = ["CCO Rules"]
        mock_rules_dir.return_value = False
        mock_rules_dir_old.return_value = False
        mock_statusline.return_value = False
        mock_permissions.return_value = False
        mock_uninstall.return_value = True
        mock_rm_files.return_value = {"commands": 1, "agents": 1}
        mock_rm_rules.return_value = ["CCO Rules"]
        # No mock_input needed - should not be called with -y flag
        with patch.object(sys, "argv", ["cco-uninstall", "-y"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "removed successfully" in captured.out

    @patch("claudecodeoptimizer.uninstall.has_cco_permissions")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir_old")
    @patch("claudecodeoptimizer.uninstall.has_rules_dir")
    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    @patch("claudecodeoptimizer.uninstall.list_cco_files")
    @patch("claudecodeoptimizer.uninstall.has_claude_md_rules")
    @patch("claudecodeoptimizer.uninstall.has_cco_statusline")
    @patch("claudecodeoptimizer.uninstall.uninstall_package")
    @patch("builtins.input")
    def test_package_removal_failure(
        self,
        mock_input,
        mock_uninstall,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        mock_rules_dir_old,
        mock_permissions,
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": [], "agents": []}
        mock_rules.return_value = []
        mock_rules_dir.return_value = False
        mock_rules_dir_old.return_value = False
        mock_statusline.return_value = False
        mock_permissions.return_value = False
        mock_input.return_value = "y"
        mock_uninstall.return_value = False
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Failed to remove package" in captured.out

    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    def test_keyboard_interrupt(self, mock_detect, capsys):
        mock_detect.side_effect = KeyboardInterrupt()
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 130
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("claudecodeoptimizer.uninstall.detect_install_method")
    def test_exception(self, mock_detect, capsys):
        mock_detect.side_effect = Exception("Test error")
        with patch.object(sys, "argv", ["cco-uninstall"]):
            result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err

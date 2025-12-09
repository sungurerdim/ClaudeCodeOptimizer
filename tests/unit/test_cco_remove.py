"""Unit tests for cco_remove module."""

import json
import subprocess
from unittest.mock import MagicMock, patch

from claudecodeoptimizer.cco_remove import (
    _display_removal_plan,
    _execute_removal,
    detect_install_method,
    has_cco_statusline,
    has_claude_md_standards,
    list_cco_files,
    main,
    remove_cco_files,
    remove_claude_md_standards,
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
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.get_cco_commands", return_value=[]):
                with patch("claudecodeoptimizer.cco_remove.get_cco_agents", return_value=[]):
                    files = list_cco_files()
                    assert files["commands"] == []
                    assert files["agents"] == []

    def test_list_with_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file = tmp_path / "commands" / "cco-tune.md"
        agent_file = tmp_path / "agents" / "cco-agent-analyze.md"
        cmd_file.touch()
        agent_file.touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.get_cco_commands", return_value=[cmd_file]):
                with patch(
                    "claudecodeoptimizer.cco_remove.get_cco_agents", return_value=[agent_file]
                ):
                    files = list_cco_files()
                    assert files["commands"] == ["cco-tune.md"]
                    assert files["agents"] == ["cco-agent-analyze.md"]


class TestHasClaudeMdRules:
    def test_no_file(self, tmp_path):
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            assert has_claude_md_standards() == []

    def test_with_rules(self, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            sections = has_claude_md_standards()
            # Universal pattern returns "CCO Content (N section(s))"
            assert len(sections) == 1
            assert "CCO Content" in sections[0]


class TestRemoveCcoFiles:
    def test_remove_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        cco_file = tmp_path / "commands" / "cco-tune.md"
        user_file = tmp_path / "commands" / "user-custom.md"
        cco_file.touch()
        user_file.touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.get_cco_commands", return_value=[cco_file]):
                with patch("claudecodeoptimizer.cco_remove.get_cco_agents", return_value=[]):
                    removed = remove_cco_files(verbose=False)
        assert removed["commands"] == 1
        assert not cco_file.exists()
        assert user_file.exists()

    def test_remove_files_verbose(self, tmp_path, capsys):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file = tmp_path / "commands" / "cco-tune.md"
        agent_file = tmp_path / "agents" / "cco-agent.md"
        cmd_file.touch()
        agent_file.touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.get_cco_commands", return_value=[cmd_file]):
                with patch(
                    "claudecodeoptimizer.cco_remove.get_cco_agents", return_value=[agent_file]
                ):
                    removed = remove_cco_files(verbose=True)
        assert removed["commands"] == 1
        assert removed["agents"] == 1


class TestRemoveClaudeMdRules:
    def test_no_file(self, tmp_path):
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            removed = remove_claude_md_standards()
            assert removed == []

    def test_remove_rules(self, tmp_path, capsys):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# My\n<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->\nOther"
        )
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            removed = remove_claude_md_standards(verbose=True)
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
        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", tmp_path / "statusline.js"):
            assert has_cco_statusline() is False

    def test_file_exists_with_cco_content(self, tmp_path):
        """Test returns True when statusline file exists with CCO content."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", statusline):
            assert has_cco_statusline() is True

    def test_file_exists_without_cco_content(self, tmp_path):
        """Test returns False when statusline file exists but without CCO marker."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// Custom statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", statusline):
            assert has_cco_statusline() is False


class TestRemoveStatusline:
    """Test remove_statusline function."""

    def test_remove_statusline_file(self, tmp_path):
        """Test removes statusline.js when it's a CCO file."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"statusLine": {"type": "command"}}))

        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.cco_remove.SETTINGS_FILE", settings):
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

        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.cco_remove.SETTINGS_FILE", settings):
                result = remove_statusline(verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "statusline.js" in captured.out
        assert "statusLine removed" in captured.out

    def test_no_statusline_to_remove(self, tmp_path):
        """Test returns False when nothing to remove."""
        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", tmp_path / "nonexistent.js"):
            with patch(
                "claudecodeoptimizer.cco_remove.SETTINGS_FILE", tmp_path / "nonexistent.json"
            ):
                result = remove_statusline(verbose=False)
        assert result is False

    def test_settings_json_decode_error(self, tmp_path):
        """Test handles invalid JSON in settings.json gracefully."""
        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        settings = tmp_path / "settings.json"
        settings.write_text("not valid json {{{")

        with patch("claudecodeoptimizer.cco_remove.STATUSLINE_FILE", statusline):
            with patch("claudecodeoptimizer.cco_remove.SETTINGS_FILE", settings):
                result = remove_statusline(verbose=False)

        assert result is True  # Statusline file was removed
        assert not statusline.exists()


class TestHasCcoPermissions:
    """Test has_cco_permissions function."""

    def test_no_file(self, tmp_path):
        """Test returns False when settings.json doesn't exist."""
        from claudecodeoptimizer.cco_remove import has_cco_permissions

        result = has_cco_permissions(tmp_path / "settings.json")
        assert result is False

    def test_with_cco_marker(self, tmp_path):
        """Test returns True when CCO marker is present."""
        from claudecodeoptimizer.cco_remove import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"_cco_managed": True, "permissions": {}}))
        result = has_cco_permissions(settings)
        assert result is True

    def test_with_meta_in_permissions(self, tmp_path):
        """Test returns True when _meta is in permissions."""
        from claudecodeoptimizer.cco_remove import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(
            json.dumps({"permissions": {"_meta": {"level": "balanced"}, "allow": []}})
        )
        result = has_cco_permissions(settings)
        assert result is True

    def test_without_cco_content(self, tmp_path):
        """Test returns False when no CCO markers present."""
        from claudecodeoptimizer.cco_remove import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"permissions": {"allow": []}}))
        result = has_cco_permissions(settings)
        assert result is False

    def test_invalid_json(self, tmp_path):
        """Test returns False on invalid JSON."""
        from claudecodeoptimizer.cco_remove import has_cco_permissions

        settings = tmp_path / "settings.json"
        settings.write_text("invalid json {{{")
        result = has_cco_permissions(settings)
        assert result is False


class TestRemovePermissions:
    """Test remove_permissions function."""

    def test_remove_permissions(self, tmp_path):
        """Test removes permissions from settings.json."""
        from claudecodeoptimizer.cco_remove import remove_permissions

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
        from claudecodeoptimizer.cco_remove import remove_permissions

        result = remove_permissions(tmp_path / "nonexistent.json", verbose=False)
        assert result is False

    def test_remove_permissions_verbose(self, tmp_path, capsys):
        """Test verbose output during permissions removal."""
        from claudecodeoptimizer.cco_remove import remove_permissions

        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"permissions": {"allow": []}}))
        result = remove_permissions(settings, verbose=True)

        assert result is True
        captured = capsys.readouterr()
        assert "permissions removed" in captured.out

    def test_invalid_json(self, tmp_path):
        """Test returns False on invalid JSON."""
        from claudecodeoptimizer.cco_remove import remove_permissions

        settings = tmp_path / "settings.json"
        settings.write_text("invalid json {{{")
        result = remove_permissions(settings, verbose=False)
        assert result is False


class TestHasLocalCcoStatusline:
    """Test has_local_cco_statusline function."""

    def test_no_file(self, tmp_path):
        """Test returns False when local statusline doesn't exist."""
        from claudecodeoptimizer.cco_remove import has_local_cco_statusline

        with patch(
            "claudecodeoptimizer.cco_remove.LOCAL_STATUSLINE_FILE", tmp_path / "statusline.js"
        ):
            result = has_local_cco_statusline()
        assert result is False

    def test_with_cco_content(self, tmp_path):
        """Test returns True when local statusline has CCO marker."""
        from claudecodeoptimizer.cco_remove import has_local_cco_statusline

        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.cco_remove.LOCAL_STATUSLINE_FILE", statusline):
            result = has_local_cco_statusline()
        assert result is True


class TestRemoveLocalStatusline:
    """Test remove_local_statusline function."""

    def test_remove_local_statusline(self, tmp_path, capsys):
        """Test removes local statusline.js."""
        from claudecodeoptimizer.cco_remove import remove_local_statusline

        statusline = tmp_path / "statusline.js"
        statusline.write_text("// CCO Statusline\nconsole.log('test');")
        with patch("claudecodeoptimizer.cco_remove.LOCAL_STATUSLINE_FILE", statusline):
            result = remove_local_statusline(verbose=True)

        assert result is True
        assert not statusline.exists()
        captured = capsys.readouterr()
        assert ".claude/statusline.js" in captured.out

    def test_no_local_statusline(self, tmp_path):
        """Test returns False when no local statusline to remove."""
        from claudecodeoptimizer.cco_remove import remove_local_statusline

        with patch(
            "claudecodeoptimizer.cco_remove.LOCAL_STATUSLINE_FILE", tmp_path / "nonexistent.js"
        ):
            result = remove_local_statusline(verbose=False)
        assert result is False


class TestHasRulesDir:
    """Test has_rules_dir function."""

    def test_no_dir(self, tmp_path):
        """Test returns False when rules dir doesn't exist."""
        from claudecodeoptimizer.cco_remove import has_rules_dir

        with patch("claudecodeoptimizer.cco_remove.RULES_DIR", tmp_path / "nonexistent"):
            result = has_rules_dir()
        assert result is False

    def test_empty_dir(self, tmp_path):
        """Test returns False when rules dir exists but is empty."""
        from claudecodeoptimizer.cco_remove import has_rules_dir

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        with patch("claudecodeoptimizer.cco_remove.RULES_DIR", rules_dir):
            result = has_rules_dir()
        assert result is False

    def test_with_rules(self, tmp_path):
        """Test returns True when rules dir has .md files."""
        from claudecodeoptimizer.cco_remove import has_rules_dir

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "core.md").write_text("# Core Rules")
        with patch("claudecodeoptimizer.cco_remove.RULES_DIR", rules_dir):
            result = has_rules_dir()
        assert result is True


class TestRemoveRulesDir:
    """Test remove_rules_dir function."""

    def test_remove_rules_dir(self, tmp_path, capsys):
        """Test removes rules directory."""
        from claudecodeoptimizer.cco_remove import remove_rules_dir

        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "core.md").write_text("# Core")
        (rules_dir / "ai.md").write_text("# AI")

        with patch("claudecodeoptimizer.cco_remove.RULES_DIR", rules_dir):
            result = remove_rules_dir(verbose=True)

        assert result is True
        assert not rules_dir.exists()
        captured = capsys.readouterr()
        assert "rules/ (2 files)" in captured.out

    def test_no_dir_to_remove(self, tmp_path):
        """Test returns False when no rules dir exists."""
        from claudecodeoptimizer.cco_remove import remove_rules_dir

        with patch("claudecodeoptimizer.cco_remove.RULES_DIR", tmp_path / "nonexistent"):
            result = remove_rules_dir(verbose=False)
        assert result is False


class TestDisplayRemovalPlan:
    """Test _display_removal_plan function."""

    def test_display_with_rules_dir(self, capsys):
        """Test displays rules directory section when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": True,
            "statusline": False,
            "permissions": False,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        _display_removal_plan(items)
        captured = capsys.readouterr()
        assert "Rules directory:" in captured.out
        assert "~/.claude/rules/" in captured.out

    def test_display_with_statusline(self, capsys):
        """Test displays statusline section when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "statusline": True,
            "permissions": False,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        _display_removal_plan(items)
        captured = capsys.readouterr()
        assert "Global (~/.claude/):" in captured.out
        assert "statusline.js" in captured.out
        assert "settings.json" in captured.out

    def test_display_with_permissions(self, capsys):
        """Test displays permissions section when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "statusline": False,
            "permissions": True,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        _display_removal_plan(items)
        captured = capsys.readouterr()
        assert "Global (~/.claude/):" in captured.out
        assert "permissions" in captured.out

    def test_display_with_local_items(self, capsys):
        """Test displays local section when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "statusline": False,
            "permissions": False,
            "local_statusline": True,
            "local_permissions": True,
            "total_files": 0,
            "total": 2,
        }
        _display_removal_plan(items)
        captured = capsys.readouterr()
        assert "Local (./.claude/):" in captured.out
        assert "statusline.js" in captured.out
        assert "permissions" in captured.out


class TestExecuteRemoval:
    """Test _execute_removal function."""

    def test_execute_with_rules_dir(self, capsys):
        """Test executes rules directory removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": True,
            "statusline": False,
            "permissions": False,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.cco_remove.remove_rules_dir") as mock_remove:
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
            "statusline": True,
            "permissions": False,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.cco_remove.remove_statusline") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing global settings" in captured.out

    def test_execute_with_permissions(self, capsys):
        """Test executes permissions removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "statusline": False,
            "permissions": True,
            "local_statusline": False,
            "local_permissions": False,
            "total_files": 0,
            "total": 1,
        }
        with patch("claudecodeoptimizer.cco_remove.remove_permissions") as mock_remove:
            mock_remove.return_value = True
            _execute_removal(items)

        mock_remove.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing global settings" in captured.out

    def test_execute_with_local_items(self, capsys):
        """Test executes local removal when present."""
        items = {
            "method": None,
            "files": {"commands": [], "agents": []},
            "rules": [],
            "rules_dir": False,
            "statusline": False,
            "permissions": False,
            "local_statusline": True,
            "local_permissions": True,
            "total_files": 0,
            "total": 2,
        }
        with patch("claudecodeoptimizer.cco_remove.remove_local_statusline") as mock_statusline:
            with patch("claudecodeoptimizer.cco_remove.remove_permissions") as mock_permissions:
                mock_statusline.return_value = True
                mock_permissions.return_value = True
                _execute_removal(items)

        mock_statusline.assert_called_once()
        mock_permissions.assert_called_once()
        captured = capsys.readouterr()
        assert "Removing local settings" in captured.out


class TestHasClaudeMdStandardsNoMatches:
    """Test has_claude_md_standards when no CCO markers found."""

    def test_file_without_cco_markers(self, tmp_path):
        """Test returns empty list when file has no CCO markers."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nSome content without CCO markers")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            result = has_claude_md_standards()
        assert result == []


class TestRemoveClaudeMdStandardsNoMatches:
    """Test remove_claude_md_standards when no CCO markers found."""

    def test_file_without_cco_markers(self, tmp_path):
        """Test returns empty list when file has no CCO markers."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nSome content without CCO markers")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            result = remove_claude_md_standards(verbose=False)
        assert result == []


class TestMain:
    @patch("claudecodeoptimizer.cco_remove.has_rules_dir")
    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_rules")
    @patch("claudecodeoptimizer.cco_remove.has_cco_statusline")
    def test_not_installed(
        self, mock_statusline, mock_rules, mock_list, mock_detect, mock_rules_dir, capsys
    ):
        mock_detect.return_value = None
        mock_list.return_value = {"agents": [], "commands": []}
        mock_rules.return_value = []
        mock_rules_dir.return_value = False
        mock_statusline.return_value = False
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "not installed" in captured.out

    @patch("claudecodeoptimizer.cco_remove.has_rules_dir")
    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_rules")
    @patch("claudecodeoptimizer.cco_remove.has_cco_statusline")
    @patch("builtins.input")
    def test_cancelled(
        self,
        mock_input,
        mock_statusline,
        mock_rules,
        mock_list,
        mock_detect,
        mock_rules_dir,
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"agents": ["a.md"], "commands": ["c.md"]}
        mock_rules.return_value = ["CCO Rules"]
        mock_rules_dir.return_value = False
        mock_statusline.return_value = False
        mock_input.return_value = "n"
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("claudecodeoptimizer.cco_remove.has_rules_dir")
    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_rules")
    @patch("claudecodeoptimizer.cco_remove.has_cco_statusline")
    @patch("claudecodeoptimizer.cco_remove.uninstall_package")
    @patch("claudecodeoptimizer.cco_remove.remove_cco_files")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_md_rules")
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
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": ["c.md"], "agents": ["a.md"]}
        mock_rules.return_value = ["CCO Rules"]
        mock_rules_dir.return_value = False
        mock_statusline.return_value = False
        mock_input.return_value = "y"
        mock_uninstall.return_value = True
        mock_rm_files.return_value = {"commands": 1, "agents": 1}
        mock_rm_rules.return_value = ["CCO Rules"]
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "removed successfully" in captured.out

    @patch("claudecodeoptimizer.cco_remove.has_rules_dir")
    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_rules")
    @patch("claudecodeoptimizer.cco_remove.has_cco_statusline")
    @patch("claudecodeoptimizer.cco_remove.uninstall_package")
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
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": [], "agents": []}
        mock_rules.return_value = []
        mock_rules_dir.return_value = False
        mock_statusline.return_value = False
        mock_input.return_value = "y"
        mock_uninstall.return_value = False
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Failed to remove package" in captured.out

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    def test_keyboard_interrupt(self, mock_detect, capsys):
        mock_detect.side_effect = KeyboardInterrupt()
        result = main()
        assert result == 130
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    def test_exception(self, mock_detect, capsys):
        mock_detect.side_effect = Exception("Test error")
        result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err

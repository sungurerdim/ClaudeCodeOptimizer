"""Unit tests for cco_remove module."""

import subprocess
from unittest.mock import MagicMock, patch

from claudecodeoptimizer.cco_remove import (
    detect_install_method,
    has_claude_md_standards,
    list_cco_files,
    main,
    remove_cco_files,
    remove_claude_md_standards,
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
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    files = list_cco_files()
                    assert files["commands"] == []
                    assert files["agents"] == []

    def test_list_with_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "agents" / "cco-agent-scan.md").touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    files = list_cco_files()
                    assert files["commands"] == ["cco-help.md"]
                    assert files["agents"] == ["cco-agent-scan.md"]


class TestHasClaudeMdRules:
    def test_no_file(self, tmp_path):
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            assert has_claude_md_standards() == []

    def test_with_rules(self, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            sections = has_claude_md_standards()
            assert "CCO Standards" in sections

    def test_with_principles(self, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("<!-- CCO_PRINCIPLES_START -->old<!-- CCO_PRINCIPLES_END -->")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            sections = has_claude_md_standards()
            assert "CCO Principles (legacy)" in sections


class TestRemoveCcoFiles:
    def test_remove_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "commands" / "user-custom.md").touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
                    removed = remove_cco_files(verbose=False)
        assert removed["commands"] == 1
        assert not (tmp_path / "commands" / "cco-help.md").exists()
        assert (tmp_path / "commands" / "user-custom.md").exists()

    def test_remove_files_verbose(self, tmp_path, capsys):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "agents" / "cco-agent.md").touch()
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_remove.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_remove.AGENTS_DIR", tmp_path / "agents"):
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
        assert "CCO Standards" in removed

    def test_remove_principles(self, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("<!-- CCO_PRINCIPLES_START -->old<!-- CCO_PRINCIPLES_END -->")
        with patch("claudecodeoptimizer.cco_remove.CLAUDE_DIR", tmp_path):
            removed = remove_claude_md_standards(verbose=False)
        assert "CCO Principles (legacy)" in removed


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


class TestMain:
    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_standards")
    def test_not_installed(self, mock_standards, mock_list, mock_detect, capsys):
        mock_detect.return_value = None
        mock_list.return_value = {"agents": [], "commands": []}
        mock_standards.return_value = []
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "not installed" in captured.out

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_standards")
    @patch("builtins.input")
    def test_cancelled(self, mock_input, mock_standards, mock_list, mock_detect, capsys):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"agents": ["a.md"], "commands": ["c.md"]}
        mock_standards.return_value = ["CCO Standards"]
        mock_input.return_value = "n"
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_standards")
    @patch("claudecodeoptimizer.cco_remove.uninstall_package")
    @patch("claudecodeoptimizer.cco_remove.remove_cco_files")
    @patch("claudecodeoptimizer.cco_remove.remove_claude_md_standards")
    @patch("builtins.input")
    def test_full_removal(
        self,
        mock_input,
        mock_rm_rules,
        mock_rm_files,
        mock_uninstall,
        mock_standards,
        mock_list,
        mock_detect,
        capsys,
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": ["c.md"], "agents": ["a.md"]}
        mock_standards.return_value = ["CCO Standards"]
        mock_input.return_value = "y"
        mock_uninstall.return_value = True
        mock_rm_files.return_value = {"commands": 1, "agents": 1}
        mock_rm_rules.return_value = ["CCO Standards"]
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "removed successfully" in captured.out

    @patch("claudecodeoptimizer.cco_remove.detect_install_method")
    @patch("claudecodeoptimizer.cco_remove.list_cco_files")
    @patch("claudecodeoptimizer.cco_remove.has_claude_md_standards")
    @patch("claudecodeoptimizer.cco_remove.uninstall_package")
    @patch("builtins.input")
    def test_package_removal_failure(
        self, mock_input, mock_uninstall, mock_standards, mock_list, mock_detect, capsys
    ):
        mock_detect.return_value = "pip"
        mock_list.return_value = {"commands": [], "agents": []}
        mock_standards.return_value = []
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

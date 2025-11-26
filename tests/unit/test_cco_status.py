"""Unit tests for cco_status module."""

import subprocess
import sys
from unittest.mock import patch

from claudecodeoptimizer.cco_status import (
    check_claude_md,
    count_components,
    count_files,
    get_claude_dir,
    get_version_info,
    has_rules,
    main,
    print_status,
)


class TestCountFiles:
    def test_count_empty(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                counts = count_files()
                assert counts["commands"] == 0
                assert counts["agents"] == 0

    def test_count_with_files(self, tmp_path):
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
    def test_no_claude_md(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_rules() is False

    def test_with_rules(self, tmp_path):
        tmp_path.mkdir(exist_ok=True)
        (tmp_path / "CLAUDE.md").write_text("<!-- CCO_RULES_START -->rules<!-- CCO_RULES_END -->")
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_rules() is True


class TestPrintStatus:
    def test_not_installed(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                    assert print_status() == 1

    def test_installed(self, tmp_path, capsys):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "commands" / "cco-help.md").touch()
        (tmp_path / "commands" / "cco-audit.md").touch()
        (tmp_path / "agents" / "cco-agent-scan.md").touch()
        (tmp_path / "CLAUDE.md").write_text("<!-- CCO_RULES_START -->rules<!-- CCO_RULES_END -->")
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
                with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                    result = print_status()
        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "Commands: 2" in captured.out
        assert "Agents: 1" in captured.out
        assert "Rules: yes" in captured.out


class TestMain:
    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_returns_status(self, mock_print):
        mock_print.return_value = 0
        assert main() == 0

    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_keyboard_interrupt(self, mock_print):
        mock_print.side_effect = KeyboardInterrupt()
        assert main() == 130

    @patch("claudecodeoptimizer.cco_status.print_status")
    def test_main_exception(self, mock_print, capsys):
        mock_print.side_effect = Exception("Test error")
        result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err


class TestBackwardsCompatFunctions:
    def test_get_claude_dir(self):
        result = get_claude_dir()
        assert result.name == ".claude"

    def test_count_components(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.COMMANDS_DIR", tmp_path / "commands"):
            with patch("claudecodeoptimizer.cco_status.AGENTS_DIR", tmp_path / "agents"):
                result = count_components(tmp_path)
                assert "commands" in result
                assert "agents" in result

    def test_get_version_info(self):
        info = get_version_info()
        assert "version" in info
        assert "install_method" in info
        assert "python_version" in info
        assert "platform" in info

    def test_check_claude_md(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            result = check_claude_md(tmp_path)
            assert result is False


class TestModuleExecution:
    def test_main_module_execution(self):
        result = subprocess.run(
            [sys.executable, "-m", "claudecodeoptimizer.cco_status"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode in [0, 1]

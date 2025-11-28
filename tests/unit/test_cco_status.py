"""Unit tests for cco_status module."""

import subprocess
import sys
from unittest.mock import patch

from claudecodeoptimizer.cco_status import (
    count_files,
    has_standards,
    main,
    print_status,
)


class TestCountFiles:
    def test_count_empty(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.get_cco_commands", return_value=[]):
            with patch("claudecodeoptimizer.cco_status.get_cco_agents", return_value=[]):
                counts = count_files()
                assert counts["commands"] == 0
                assert counts["agents"] == 0

    def test_count_with_files(self, tmp_path):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file = tmp_path / "commands" / "cco-help.md"
        cmd_file.touch()
        agent_file = tmp_path / "agents" / "cco-agent-scan.md"
        agent_file.touch()
        with patch("claudecodeoptimizer.cco_status.get_cco_commands", return_value=[cmd_file]):
            with patch("claudecodeoptimizer.cco_status.get_cco_agents", return_value=[agent_file]):
                counts = count_files()
                assert counts["commands"] == 1
                assert counts["agents"] == 1


class TestHasRules:
    def test_no_claude_md(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_standards() is False

    def test_with_rules(self, tmp_path):
        tmp_path.mkdir(exist_ok=True)
        (tmp_path / "CLAUDE.md").write_text(
            "<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->"
        )
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            assert has_standards() is True


class TestPrintStatus:
    def test_not_installed(self, tmp_path):
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            with patch("claudecodeoptimizer.cco_status.get_cco_commands", return_value=[]):
                with patch("claudecodeoptimizer.cco_status.get_cco_agents", return_value=[]):
                    assert print_status() == 1

    def test_installed(self, tmp_path, capsys):
        (tmp_path / "commands").mkdir()
        (tmp_path / "agents").mkdir()
        cmd_file1 = tmp_path / "commands" / "cco-help.md"
        cmd_file1.touch()
        cmd_file2 = tmp_path / "commands" / "cco-audit.md"
        cmd_file2.touch()
        agent_file = tmp_path / "agents" / "cco-agent-scan.md"
        agent_file.touch()
        (tmp_path / "CLAUDE.md").write_text(
            "<!-- CCO_STANDARDS_START -->standards<!-- CCO_STANDARDS_END -->"
        )
        with patch("claudecodeoptimizer.cco_status.CLAUDE_DIR", tmp_path):
            with patch(
                "claudecodeoptimizer.cco_status.get_cco_commands",
                return_value=[cmd_file1, cmd_file2],
            ):
                with patch(
                    "claudecodeoptimizer.cco_status.get_cco_agents", return_value=[agent_file]
                ):
                    result = print_status()
        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "Commands: 2" in captured.out
        assert "Agents: 1" in captured.out
        assert "Standards: yes" in captured.out


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


class TestModuleExecution:
    def test_main_module_execution(self):
        result = subprocess.run(
            [sys.executable, "-m", "claudecodeoptimizer.cco_status"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode in [0, 1]

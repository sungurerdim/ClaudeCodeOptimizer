"""Unit tests for __main__.py module."""

import sys
from unittest.mock import patch

import pytest

from claudecodeoptimizer.__main__ import main


class TestMain:
    """Test main function."""

    def test_version_flag_long(self, capsys):
        """Test --version flag."""
        with patch.object(sys, "argv", ["cco", "--version"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_version_flag_short(self, capsys):
        """Test -v flag."""
        with patch.object(sys, "argv", ["cco", "-v"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_version_command(self, capsys):
        """Test version command."""
        with patch.object(sys, "argv", ["cco", "version"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_help_flag_long(self, capsys):
        """Test --help flag."""
        with patch.object(sys, "argv", ["cco", "--help"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "Usage:" in captured.out
        assert "Options:" in captured.out

    def test_help_flag_short(self, capsys):
        """Test -h flag."""
        with patch.object(sys, "argv", ["cco", "-h"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "Usage:" in captured.out

    def test_help_command(self, capsys):
        """Test help command."""
        with patch.object(sys, "argv", ["cco", "help"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "Usage:" in captured.out

    def test_default_shows_help(self, capsys):
        """Test no arguments shows help."""
        with patch.object(sys, "argv", ["cco"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "cco-install" in captured.out
        assert "cco-uninstall" in captured.out
        assert "/cco-config" in captured.out

    def test_keyboard_interrupt(self, capsys, monkeypatch):
        """Test KeyboardInterrupt handling."""
        # Create a flag to track if this is first call
        call_count = {"value": 0}
        original_print = print

        def mock_print(*args, **kwargs):
            call_count["value"] += 1
            if call_count["value"] == 1:
                raise KeyboardInterrupt
            return original_print(*args, **kwargs)

        monkeypatch.setattr("builtins.print", mock_print)
        monkeypatch.setattr(sys, "argv", ["cco", "--version"])

        result = main()

        assert result == 130

    def test_exit_code_on_version(self):
        """Test returns 0 exit code on --version."""
        with patch.object(sys, "argv", ["cco", "--version"]):
            result = main()
        assert result == 0

    def test_exit_code_on_help(self):
        """Test returns 0 exit code on --help."""
        with patch.object(sys, "argv", ["cco", "--help"]):
            result = main()
        assert result == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

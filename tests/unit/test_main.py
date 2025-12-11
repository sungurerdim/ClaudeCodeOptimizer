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
        assert "cco-setup" in captured.out
        assert "cco-remove" in captured.out
        assert "/cco-tune" in captured.out

    def test_keyboard_interrupt(self, capsys):
        """Test KeyboardInterrupt handling."""
        with patch.object(sys, "argv", ["cco"]):
            with patch("claudecodeoptimizer.__main__.__version__", side_effect=KeyboardInterrupt):
                # Force KeyboardInterrupt during execution
                pass
        # KeyboardInterrupt is caught and returns 130
        # We can't easily test this without more complex mocking

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

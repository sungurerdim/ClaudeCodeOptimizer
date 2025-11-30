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
            main()

        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_version_flag_short(self, capsys):
        """Test -v flag."""
        with patch.object(sys, "argv", ["cco", "-v"]):
            main()

        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_version_command(self, capsys):
        """Test version command."""
        with patch.object(sys, "argv", ["cco", "version"]):
            main()

        captured = capsys.readouterr()
        assert "CCO v" in captured.out

    def test_default_shows_help(self, capsys):
        """Test no arguments shows help."""
        with patch.object(sys, "argv", ["cco"]):
            main()

        captured = capsys.readouterr()
        assert "CCO v" in captured.out
        assert "cco-setup" in captured.out
        assert "cco-remove" in captured.out
        assert "/cco-calibrate" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

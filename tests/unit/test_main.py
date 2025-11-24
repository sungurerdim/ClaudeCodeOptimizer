"""Unit tests for __main__.py module

Tests the module entry point and version display.
Target Coverage: 100%
"""

import sys
from unittest.mock import patch

import pytest

from claudecodeoptimizer.__main__ import main


class TestMain:
    """Test main function"""

    @patch("builtins.print")
    def test_main_version_flag_long(self, mock_print):
        """Test main with --version flag"""
        with patch.object(sys, "argv", ["claudecodeoptimizer", "--version"]):
            main()

        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "ClaudeCodeOptimizer v" in printed_text
        assert "Architecture: Stateless" in printed_text

    @patch("builtins.print")
    def test_main_version_flag_short(self, mock_print):
        """Test main with -v flag"""
        with patch.object(sys, "argv", ["claudecodeoptimizer", "-v"]):
            main()

        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "ClaudeCodeOptimizer v" in printed_text

    @patch("builtins.print")
    def test_main_version_command(self, mock_print):
        """Test main with version command"""
        with patch.object(sys, "argv", ["claudecodeoptimizer", "version"]):
            main()

        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "ClaudeCodeOptimizer v" in printed_text

    @patch("builtins.print")
    def test_main_default_help(self, mock_print):
        """Test main without arguments shows help"""
        with patch.object(sys, "argv", ["claudecodeoptimizer"]):
            main()

        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        assert "ClaudeCodeOptimizer" in printed_text
        assert "Usage:" in printed_text
        assert "/cco-help" in printed_text

    @patch("builtins.print")
    def test_main_unknown_arg(self, mock_print):
        """Test main with unknown argument shows help"""
        with patch.object(sys, "argv", ["claudecodeoptimizer", "unknown"]):
            main()

        printed_text = " ".join(
            [str(call.args[0]) for call in mock_print.call_args_list if call.args]
        )
        # Should show default help for unknown arguments
        assert "ClaudeCodeOptimizer" in printed_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

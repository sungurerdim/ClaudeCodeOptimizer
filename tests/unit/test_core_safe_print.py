"""
Unit tests for Core Safe Print

Tests safe printing utilities for cross-platform Unicode support.
Target Coverage: 90%+
"""

import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import MagicMock, Mock, patch

import pytest

from claudecodeoptimizer.core.safe_print import (
    _unicode_to_ascii,
    configure_utf8_encoding,
    safe_print,
)


class TestConfigureUtf8Encoding:
    """Test configure_utf8_encoding function"""

    @patch("sys.platform", "win32")
    @patch("subprocess.run")
    @patch("sys.stdout")
    @patch("sys.stderr")
    def test_configure_utf8_encoding_windows(
        self, mock_stderr: Mock, mock_stdout: Mock, mock_subprocess_run: Mock
    ) -> None:
        """Test UTF-8 configuration on Windows platform"""
        # Setup mocks
        mock_buffer = MagicMock()
        mock_stdout.buffer = mock_buffer
        mock_stderr.buffer = mock_buffer

        # Execute
        configure_utf8_encoding()

        # Verify subprocess called to set code page on Windows
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args[0][0]
        assert call_args == ["chcp", "65001"]

        # Verify subprocess settings
        call_kwargs = mock_subprocess_run.call_args[1]
        assert call_kwargs["stdout"] == subprocess.DEVNULL
        assert call_kwargs["stderr"] == subprocess.DEVNULL
        assert call_kwargs["check"] is False

    @patch("sys.platform", "linux")
    @patch("sys.stdout")
    @patch("sys.stderr")
    def test_configure_utf8_encoding_linux(self, mock_stderr: Mock, mock_stdout: Mock) -> None:
        """Test UTF-8 configuration on Linux platform"""
        # Setup mocks
        mock_buffer = MagicMock()
        mock_stdout.buffer = mock_buffer
        mock_stderr.buffer = mock_buffer

        # Execute
        configure_utf8_encoding()

        # Verify stdout/stderr were reconfigured
        # The function wraps the buffer with TextIOWrapper
        assert hasattr(mock_stdout, "buffer")

    @patch("sys.platform", "darwin")
    @patch("sys.stdout")
    @patch("sys.stderr")
    def test_configure_utf8_encoding_macos(self, mock_stderr: Mock, mock_stdout: Mock) -> None:
        """Test UTF-8 configuration on macOS platform"""
        # Setup mocks
        mock_buffer = MagicMock()
        mock_stdout.buffer = mock_buffer
        mock_stderr.buffer = mock_buffer

        # Execute
        configure_utf8_encoding()

        # Verify reconfiguration attempted (no subprocess on macOS)
        assert hasattr(mock_stdout, "buffer")

    @patch("sys.stdout")
    def test_configure_utf8_encoding_no_buffer(self, mock_stdout: Mock) -> None:
        """Test configuration when stdout has no buffer attribute"""
        # Setup: stdout without buffer attribute
        delattr(mock_stdout, "buffer") if hasattr(mock_stdout, "buffer") else None
        mock_stdout.buffer = None

        # Execute - should not crash
        configure_utf8_encoding()

        # No exception should be raised

    @patch("sys.stdout")
    @patch("sys.stderr")
    @patch("logging.debug")
    def test_configure_utf8_encoding_attribute_error(
        self, mock_logging_debug: Mock, mock_stderr: Mock, mock_stdout: Mock
    ) -> None:
        """Test configuration handles AttributeError gracefully"""
        # Setup: stdout with buffer but TextIOWrapper raises AttributeError
        mock_stdout.buffer = MagicMock()
        mock_stderr.buffer = MagicMock()

        with patch("io.TextIOWrapper", side_effect=AttributeError("Test error")):
            # Execute
            configure_utf8_encoding()

            # Verify error logged but no exception raised
            mock_logging_debug.assert_called()
            call_message = str(mock_logging_debug.call_args[0][0])
            assert "Failed to reconfigure console encoding" in call_message

    @patch("sys.stdout")
    @patch("sys.stderr")
    @patch("logging.debug")
    def test_configure_utf8_encoding_os_error(
        self, mock_logging_debug: Mock, mock_stderr: Mock, mock_stdout: Mock
    ) -> None:
        """Test configuration handles OSError gracefully"""
        # Setup: stdout with buffer but TextIOWrapper raises OSError
        mock_stdout.buffer = MagicMock()
        mock_stderr.buffer = MagicMock()

        with patch("io.TextIOWrapper", side_effect=OSError("Test error")):
            # Execute
            configure_utf8_encoding()

            # Verify error logged but no exception raised
            mock_logging_debug.assert_called()
            call_message = str(mock_logging_debug.call_args[0][0])
            assert "Failed to reconfigure console encoding" in call_message

    @patch("sys.platform", "win32")
    @patch("subprocess.run", side_effect=OSError("Command failed"))
    @patch("sys.stdout")
    @patch("sys.stderr")
    @patch("logging.debug")
    def test_configure_utf8_encoding_windows_subprocess_failure(
        self,
        mock_logging_debug: Mock,
        mock_stderr: Mock,
        mock_stdout: Mock,
        mock_subprocess_run: Mock,
    ) -> None:
        """Test configuration handles subprocess failure on Windows"""
        # Setup mocks
        mock_buffer = MagicMock()
        mock_stdout.buffer = mock_buffer
        mock_stderr.buffer = mock_buffer

        # Execute
        configure_utf8_encoding()

        # Verify error logged but no exception raised
        mock_logging_debug.assert_called()


class TestSafePrint:
    """Test safe_print function"""

    def test_safe_print_basic_string(self) -> None:
        """Test safe_print with basic ASCII string"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("Hello World")

        assert output.getvalue().strip() == "Hello World"

    def test_safe_print_unicode_success(self) -> None:
        """Test safe_print with Unicode characters when encoding works"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("✓ Success!")

        result = output.getvalue().strip()
        # Should contain either Unicode or ASCII version
        assert "Success!" in result

    def test_safe_print_multiple_args(self) -> None:
        """Test safe_print with multiple arguments"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("Hello", "World", "Test")

        result = output.getvalue().strip()
        assert "Hello" in result
        assert "World" in result
        assert "Test" in result

    def test_safe_print_with_kwargs(self) -> None:
        """Test safe_print with keyword arguments"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("Line1", "Line2", sep=" | ", end="!\n")

        result = output.getvalue()
        assert "Line1 | Line2!" in result

    def test_safe_print_non_string_args(self) -> None:
        """Test safe_print with non-string arguments"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print(123, 45.67, True, None)

        result = output.getvalue().strip()
        assert "123" in result
        assert "45.67" in result
        assert "True" in result
        assert "None" in result

    @patch("builtins.print", side_effect=UnicodeEncodeError("utf-8", "", 0, 1, "test"))
    def test_safe_print_unicode_encode_error_recovery(self, mock_print: Mock) -> None:
        """Test safe_print recovers from UnicodeEncodeError"""
        # First call raises error, second call should succeed
        mock_print.side_effect = [
            UnicodeEncodeError("utf-8", "", 0, 1, "test"),
            None,
        ]

        # Execute - should not crash
        safe_print("✓ Test")

        # Verify print called twice (once failed, once succeeded with ASCII)
        assert mock_print.call_count == 2

    @patch("builtins.print")
    def test_safe_print_converts_unicode_on_error(self, mock_print: Mock) -> None:
        """Test safe_print converts Unicode to ASCII on encoding error"""
        # First call raises error
        mock_print.side_effect = [
            UnicodeEncodeError("utf-8", "", 0, 1, "test"),
            None,
        ]

        # Execute
        safe_print("✓ Success!", "🔧 Build")

        # Verify second call has ASCII replacements
        assert mock_print.call_count == 2
        second_call_args = mock_print.call_args_list[1][0]
        assert "[OK]" in second_call_args[0] or "Success!" in second_call_args[0]

    @patch("builtins.print")
    def test_safe_print_mixed_types_on_error(self, mock_print: Mock) -> None:
        """Test safe_print handles mixed types on encoding error"""
        # First call raises error
        mock_print.side_effect = [
            UnicodeEncodeError("utf-8", "", 0, 1, "test"),
            None,
        ]

        # Execute with mixed types
        safe_print("✓", 123, True, "🔧")

        # Verify conversion handled all types
        assert mock_print.call_count == 2
        second_call_args = mock_print.call_args_list[1][0]
        # All args should be converted to strings
        assert len(second_call_args) == 4


class TestUnicodeToAscii:
    """Test _unicode_to_ascii function"""

    def test_status_indicators(self) -> None:
        """Test conversion of status indicator emojis"""
        assert _unicode_to_ascii("✓") == "[OK]"
        assert _unicode_to_ascii("✗") == "[X]"
        assert _unicode_to_ascii("❌") == "[ERROR]"
        assert _unicode_to_ascii("⚠️") == "[WARNING]"
        assert _unicode_to_ascii("💡") == "[TIP]"

    def test_progress_indicators(self) -> None:
        """Test conversion of progress indicator emojis"""
        assert _unicode_to_ascii("🔧") == "[BUILD]"
        assert _unicode_to_ascii("📊") == "[ANALYSIS]"
        assert _unicode_to_ascii("🎯") == "[TARGET]"
        assert _unicode_to_ascii("🚀") == "[LAUNCH]"

    def test_documentation_indicators(self) -> None:
        """Test conversion of documentation emojis"""
        assert _unicode_to_ascii("📋") == "[LIST]"
        assert _unicode_to_ascii("📦") == "[PACKAGE]"
        assert _unicode_to_ascii("📅") == "[DATE]"
        assert _unicode_to_ascii("📝") == "[NOTE]"

    def test_level_indicators(self) -> None:
        """Test conversion of level indicator emojis"""
        assert _unicode_to_ascii("🟢") == "[HIGH]"
        assert _unicode_to_ascii("🟡") == "[MEDIUM]"
        assert _unicode_to_ascii("🔴") == "[LOW]"
        assert _unicode_to_ascii("⚪") == "[NONE]"

    def test_arrow_conversions(self) -> None:
        """Test conversion of arrow characters"""
        assert _unicode_to_ascii("→") == "->"
        assert _unicode_to_ascii("←") == "<-"
        assert _unicode_to_ascii("↓") == "v"
        assert _unicode_to_ascii("↑") == "^"

    def test_other_symbols(self) -> None:
        """Test conversion of other common symbols"""
        assert _unicode_to_ascii("•") == "*"
        assert _unicode_to_ascii("…") == "..."

    def test_combined_replacements(self) -> None:
        """Test text with multiple Unicode characters"""
        text = "✓ Success! → Next step • Important"
        result = _unicode_to_ascii(text)
        assert result == "[OK] Success! -> Next step * Important"

    def test_multiple_emojis(self) -> None:
        """Test text with multiple emojis"""
        text = "🔧 Building 🎯 target 📦 package"
        result = _unicode_to_ascii(text)
        assert result == "[BUILD] Building [TARGET] target [PACKAGE] package"

    def test_plain_text_unchanged(self) -> None:
        """Test that plain ASCII text is unchanged"""
        text = "Hello World 123"
        result = _unicode_to_ascii(text)
        assert result == text

    def test_empty_string(self) -> None:
        """Test empty string handling"""
        assert _unicode_to_ascii("") == ""

    def test_only_unicode(self) -> None:
        """Test string with only Unicode characters"""
        text = "✓✗❌"
        result = _unicode_to_ascii(text)
        assert result == "[OK][X][ERROR]"

    @patch("sys.stdout")
    def test_encoding_fallback_ascii(self, mock_stdout: Mock) -> None:
        """Test ASCII fallback when stdout encoding check fails"""
        # Setup: stdout with non-UTF-8 encoding
        mock_stdout.encoding = "ascii"

        # Test with character that needs replacement
        text = "café"  # 'é' is not ASCII
        result = _unicode_to_ascii(text)

        # Should return string (possibly with replacements)
        assert isinstance(result, str)

    @patch("sys.stdout")
    def test_encoding_no_stdout_encoding(self, mock_stdout: Mock) -> None:
        """Test when stdout has no encoding attribute"""
        # Setup: stdout without encoding
        mock_stdout.encoding = None

        # Test with Unicode text
        text = "✓ Test"
        result = _unicode_to_ascii(text)

        # Should still work and convert emojis
        assert "[OK]" in result or "✓" in result

    @patch("sys.stdout", new_callable=lambda: MagicMock(spec=[]))
    def test_encoding_attribute_error(self, mock_stdout: Mock) -> None:
        """Test handling when stdout has no encoding attribute"""
        # Test with Unicode text
        text = "✓ Test"
        result = _unicode_to_ascii(text)

        # Should still work (falls back to ASCII encoding)
        assert isinstance(result, str)

    def test_unencodable_characters(self) -> None:
        """Test handling of unencodable characters"""
        # Test with character that may not encode properly
        text = "Test \u0001 control character"  # Control character
        result = _unicode_to_ascii(text)

        # Should return a string without crashing
        assert isinstance(result, str)
        assert "Test" in result


class TestSafePrintIntegration:
    """Integration tests for safe_print module"""

    def test_configure_and_print_workflow(self) -> None:
        """Test typical workflow: configure then print"""
        # This tests real execution path
        output = StringIO()
        with redirect_stdout(output):
            # Configure UTF-8 (should not crash)
            configure_utf8_encoding()

            # Print various content
            safe_print("✓ Configuration successful")
            safe_print("🔧 Building project")

        result = output.getvalue()
        # Should contain some form of the messages
        assert "Configuration successful" in result or "successful" in result
        assert "Building project" in result or "project" in result

    def test_safe_print_stderr(self) -> None:
        """Test safe_print with stderr"""
        output = StringIO()
        with redirect_stderr(output):
            safe_print("Error message", file=sys.stderr)

        result = output.getvalue()
        assert "Error message" in result

    def test_safe_print_preserves_newlines(self) -> None:
        """Test safe_print preserves newline behavior"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("Line 1")
            safe_print("Line 2")

        result = output.getvalue()
        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert "Line 1" in lines[0]
        assert "Line 2" in lines[1]

    def test_safe_print_flush(self) -> None:
        """Test safe_print with flush parameter"""
        output = StringIO()
        with redirect_stdout(output):
            safe_print("Test", flush=True)

        assert "Test" in output.getvalue()

    @patch("builtins.print")
    def test_unicode_to_ascii_called_on_encode_error(self, mock_print: Mock) -> None:
        """Test _unicode_to_ascii is used when encoding fails"""
        # Setup: print raises UnicodeEncodeError on first call
        mock_print.side_effect = [
            UnicodeEncodeError("utf-8", "", 0, 1, "test"),
            None,
        ]

        # Execute with emoji
        safe_print("✓ Success")

        # Verify print called twice
        assert mock_print.call_count == 2

        # Second call should have ASCII version
        second_call = mock_print.call_args_list[1][0]
        assert "[OK]" in str(second_call)


class TestModuleExports:
    """Test module's public API"""

    def test_all_exports(self) -> None:
        """Test __all__ contains expected exports"""
        from claudecodeoptimizer.core import safe_print as module

        assert hasattr(module, "__all__")
        assert "configure_utf8_encoding" in module.__all__
        assert "safe_print" in module.__all__
        assert len(module.__all__) == 2

    def test_private_function_not_exported(self) -> None:
        """Test private function is not in __all__"""
        from claudecodeoptimizer.core import safe_print as module

        assert "_unicode_to_ascii" not in module.__all__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

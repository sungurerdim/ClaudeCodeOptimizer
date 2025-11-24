"""Unit tests for core/safe_print.py

Tests UTF-8 encoding configuration and safe printing utilities.
Target Coverage: 95%+
"""

from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.core.safe_print import (
    _unicode_to_ascii,
    configure_utf8_encoding,
    safe_print,
)


class TestConfigureUtf8Encoding:
    """Test configure_utf8_encoding function"""

    def test_configure_doesnt_crash(self):
        """Test that configure_utf8_encoding doesn't crash"""
        # This test just verifies the function doesn't raise exceptions
        # Actual behavior is platform-dependent and hard to test without
        # interfering with pytest's output capture
        try:
            configure_utf8_encoding()
        except Exception as e:
            pytest.fail(f"configure_utf8_encoding() raised {e}")

    @patch("sys.stdout")
    def test_configure_handles_attribute_error(self, mock_stdout: MagicMock):
        """Test that AttributeError is caught and handled (lines 41-47, 53-55)"""
        # Remove buffer attribute to trigger AttributeError
        mock_stdout.configure_mock(**{"buffer": None})
        delattr(mock_stdout, "buffer")

        # Should not raise exception
        try:
            configure_utf8_encoding()
        except AttributeError:
            pytest.fail("configure_utf8_encoding() should catch AttributeError")

    @patch("sys.stdout")
    @patch("sys.platform", "win32")
    def test_configure_handles_os_error(self, mock_stdout: MagicMock):
        """Test that OSError is caught and handled (lines 41-47, 53-55)"""
        # Mock stdout.buffer to exist but raise OSError when accessed
        mock_buffer = MagicMock()
        mock_stdout.buffer = mock_buffer

        # Make TextIOWrapper raise OSError to simulate system-level error
        with patch("io.TextIOWrapper", side_effect=OSError("Cannot reconfigure")):
            # Should not raise exception
            try:
                configure_utf8_encoding()
            except OSError:
                pytest.fail("configure_utf8_encoding() should catch OSError")


class TestSafePrint:
    """Test safe_print function"""

    @patch("builtins.print")
    def test_safe_print_success(self, mock_print: MagicMock):
        """Test safe_print with normal string"""
        safe_print("Hello, world!")

        mock_print.assert_called_once_with("Hello, world!")

    @patch("builtins.print")
    def test_safe_print_unicode(self, mock_print: MagicMock):
        """Test safe_print with Unicode characters"""
        safe_print("✓ Success!")

        mock_print.assert_called_once_with("✓ Success!")

    @patch("builtins.print")
    def test_safe_print_multiple_args(self, mock_print: MagicMock):
        """Test safe_print with multiple arguments"""
        safe_print("Status:", "✓", "Done")

        mock_print.assert_called_once_with("Status:", "✓", "Done")

    @patch("builtins.print")
    def test_safe_print_with_kwargs(self, mock_print: MagicMock):
        """Test safe_print with keyword arguments"""
        safe_print("Message", end="", sep="-")

        mock_print.assert_called_once_with("Message", end="", sep="-")

    @patch("builtins.print")
    def test_safe_print_unicode_encode_error(self, mock_print: MagicMock):
        """Test safe_print fallback when UnicodeEncodeError occurs"""
        # First call raises UnicodeEncodeError, second succeeds
        mock_print.side_effect = [UnicodeEncodeError("utf-8", "✓", 0, 1, "test"), None]

        safe_print("✓ Success!")

        # Should be called twice (first fails, second with ASCII)
        assert mock_print.call_count == 2
        # Second call should have ASCII version
        second_call_args = mock_print.call_args_list[1][0]
        assert "[OK]" in second_call_args[0]

    @patch("builtins.print")
    def test_safe_print_non_string_args(self, mock_print: MagicMock):
        """Test safe_print with non-string arguments"""
        # First call raises error, second succeeds
        mock_print.side_effect = [UnicodeEncodeError("utf-8", "test", 0, 1, "test"), None]

        safe_print(123, True, None)

        # Should convert non-strings to strings
        assert mock_print.call_count == 2

    @patch("builtins.print")
    def test_safe_print_mixed_args(self, mock_print: MagicMock):
        """Test safe_print with mixed string and non-string arguments"""
        mock_print.side_effect = [UnicodeEncodeError("utf-8", "✓", 0, 1, "test"), None]

        safe_print("Status: ✓", 42, True)

        assert mock_print.call_count == 2
        second_call = mock_print.call_args_list[1][0]
        assert "[OK]" in second_call[0]
        assert "42" in second_call
        assert "True" in second_call


class TestUnicodeToAscii:
    """Test _unicode_to_ascii function"""

    def test_convert_checkmark(self):
        """Test conversion of checkmark"""
        result = _unicode_to_ascii("✓ Success")
        assert result == "[OK] Success"

    def test_convert_error_mark(self):
        """Test conversion of error mark"""
        result = _unicode_to_ascii("✗ Failed")
        assert result == "[X] Failed"

    def test_convert_emoji_warning(self):
        """Test conversion of warning emoji"""
        result = _unicode_to_ascii("⚠️ Warning")
        assert "[WARNING]" in result

    def test_convert_emoji_error(self):
        """Test conversion of error emoji"""
        result = _unicode_to_ascii("❌ Error")
        assert result == "[ERROR] Error"

    def test_convert_build_emoji(self):
        """Test conversion of build emoji"""
        result = _unicode_to_ascii("🔧 Building")
        assert result == "[BUILD] Building"

    def test_convert_analysis_emoji(self):
        """Test conversion of analysis emoji"""
        result = _unicode_to_ascii("📊 Analyzing")
        assert result == "[ANALYSIS] Analyzing"

    def test_convert_arrows(self):
        """Test conversion of arrow characters"""
        result = _unicode_to_ascii("→ Next → Step")
        assert result == "-> Next -> Step"

    def test_convert_bullet(self):
        """Test conversion of bullet point"""
        result = _unicode_to_ascii("• Item 1")
        assert result == "* Item 1"

    def test_convert_ellipsis(self):
        """Test conversion of ellipsis"""
        result = _unicode_to_ascii("Loading…")
        assert result == "Loading..."

    def test_convert_multiple_unicode(self):
        """Test conversion of multiple Unicode characters"""
        result = _unicode_to_ascii("✓ Success → Next • Item")
        assert result == "[OK] Success -> Next * Item"

    def test_convert_no_unicode(self):
        """Test with plain ASCII text"""
        result = _unicode_to_ascii("Plain ASCII text")
        assert result == "Plain ASCII text"

    def test_convert_level_indicators(self):
        """Test conversion of level indicator emojis"""
        high = _unicode_to_ascii("🟢 High priority")
        medium = _unicode_to_ascii("🟡 Medium priority")
        low = _unicode_to_ascii("🔴 Low priority")

        assert high == "[HIGH] High priority"
        assert medium == "[MEDIUM] Medium priority"
        assert low == "[LOW] Low priority"

    def test_convert_documentation_emojis(self):
        """Test conversion of documentation emojis"""
        result = _unicode_to_ascii("📋 List 📦 Package 📝 Note")
        assert result == "[LIST] List [PACKAGE] Package [NOTE] Note"

    @patch("sys.stdout")
    def test_convert_with_encoding_error(self, mock_stdout: MagicMock):
        """Test fallback when encoding check fails"""
        mock_stdout.encoding = "ascii"

        # Text with Unicode that can't be encoded in ASCII
        result = _unicode_to_ascii("Test ✓ 你好")

        # Should handle gracefully (replace non-ASCII with ?)
        assert "Test" in result
        assert "[OK]" in result

    @patch("sys.stdout")
    def test_convert_with_no_encoding_attribute(self, mock_stdout: MagicMock):
        """Test when stdout has no encoding attribute"""
        delattr(mock_stdout, "encoding")

        result = _unicode_to_ascii("✓ Test")

        # Should use UTF-8 fallback
        assert "[OK]" in result

    def test_convert_all_replacements(self):
        """Test all emoji replacements are working"""
        test_cases = {
            "✓": "[OK]",
            "✗": "[X]",
            "❌": "[ERROR]",
            "⚠️": "[WARNING]",
            "💡": "[TIP]",
            "🔧": "[BUILD]",
            "📊": "[ANALYSIS]",
            "🎯": "[TARGET]",
            "🚀": "[LAUNCH]",
            "📋": "[LIST]",
            "📦": "[PACKAGE]",
            "📅": "[DATE]",
            "📝": "[NOTE]",
            "🟢": "[HIGH]",
            "🟡": "[MEDIUM]",
            "🔴": "[LOW]",
            "⚪": "[NONE]",
            "→": "->",
            "←": "<-",
            "↓": "v",
            "↑": "^",
            "•": "*",
            "…": "...",
        }

        for unicode_char, expected_ascii in test_cases.items():
            result = _unicode_to_ascii(f"Test {unicode_char} End")
            assert expected_ascii in result, f"Failed to convert {unicode_char}"


class TestModuleExports:
    """Test module exports"""

    def test_all_exports(self):
        """Test __all__ exports"""
        from claudecodeoptimizer.core import safe_print as module

        assert hasattr(module, "__all__")
        assert "configure_utf8_encoding" in module.__all__
        assert "safe_print" in module.__all__

    def test_functions_importable(self):
        """Test that all functions can be imported"""
        from claudecodeoptimizer.core.safe_print import (
            configure_utf8_encoding,
            safe_print,
        )

        assert callable(configure_utf8_encoding)
        assert callable(safe_print)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=claudecodeoptimizer.core.safe_print"])

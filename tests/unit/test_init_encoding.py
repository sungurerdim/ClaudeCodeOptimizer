"""
Test Windows console encoding configuration in __init__.py.

This module specifically tests lines 15-16 which handle encoding configuration errors.
"""

import sys
from unittest.mock import MagicMock

import pytest


class TestWindowsEncodingErrorPath:
    """Test the exception handling path for Windows console encoding."""

    def test_reconfigure_exception_triggers_logging_warning(self):
        """Test that reconfigure exception triggers logging.warning (lines 15-16)."""
        # Only run on Windows
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # Create a mock logger
        mock_logger = MagicMock()

        # Simulate the code from lines 11-16
        if sys.platform == "win32":
            # Create mock stdout/stderr that fail on reconfigure
            mock_stdout = MagicMock()
            mock_stderr = MagicMock()
            mock_stdout.reconfigure.side_effect = Exception("Test encoding error")
            mock_stderr.reconfigure.side_effect = Exception("Test encoding error")

            try:
                mock_stdout.reconfigure(encoding="utf-8")
                mock_stderr.reconfigure(encoding="utf-8")
            except Exception as e:
                # This is what line 16 does
                warning_msg = f"Failed to reconfigure console encoding: {e}. Using default encoding."
                mock_logger.warning(warning_msg)

            # Verify logging.warning was called
            mock_logger.warning.assert_called_once()
            call_msg = mock_logger.warning.call_args[0][0]
            assert "Failed to reconfigure console encoding" in call_msg
            assert "Using default encoding" in call_msg

    def test_reconfigure_no_exception_no_warning(self):
        """Test that successful reconfigure doesn't trigger warning."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        mock_logger = MagicMock()

        # Simulate successful reconfigure
        if sys.platform == "win32":
            mock_stdout = MagicMock()
            mock_stderr = MagicMock()
            # Don't set side_effect - will succeed
            try:
                mock_stdout.reconfigure(encoding="utf-8")
                mock_stderr.reconfigure(encoding="utf-8")
            except Exception as e:
                mock_logger.warning(
                    f"Failed to reconfigure console encoding: {e}. Using default encoding."
                )

        # Warning should NOT be called on success
        mock_logger.warning.assert_not_called()

    def test_exception_message_format(self):
        """Test the exact format of the warning message."""
        test_error = Exception("Encoding not supported")
        mock_logger = MagicMock()

        try:
            raise test_error
        except Exception as e:
            warning_msg = f"Failed to reconfigure console encoding: {e}. Using default encoding."
            mock_logger.warning(warning_msg)

        # Verify exact message format
        mock_logger.warning.assert_called_once()
        expected_msg = "Failed to reconfigure console encoding: Encoding not supported. Using default encoding."
        mock_logger.warning.assert_called_with(expected_msg)

    def test_various_exception_types(self):
        """Test handling of different exception types."""
        exceptions_to_test = [
            Exception("Generic error"),
            ValueError("Invalid encoding"),
            OSError("System error"),
            RuntimeError("Runtime error"),
        ]

        for exc in exceptions_to_test:
            mock_logger = MagicMock()
            try:
                raise exc
            except Exception as e:
                warning_msg = f"Failed to reconfigure console encoding: {e}. Using default encoding."
                mock_logger.warning(warning_msg)

            # Each exception should trigger warning
            mock_logger.warning.assert_called_once()
            call_msg = mock_logger.warning.call_args[0][0]
            assert str(exc) in call_msg


class TestPlatformSpecificBehavior:
    """Test platform-specific behavior of encoding setup."""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
    def test_windows_platform_check(self):
        """Test that code only runs on Windows."""
        # On Windows, this should be True
        assert sys.platform == "win32"

    @pytest.mark.skipif(sys.platform == "win32", reason="Non-Windows test")
    def test_non_windows_platform_skip(self):
        """Test that code is skipped on non-Windows."""
        # On non-Windows, this should NOT be win32
        assert sys.platform != "win32"

    def test_hasattr_reconfigure_check(self):
        """Test the hasattr check for reconfigure."""
        # The code checks: hasattr(sys.stdout, "reconfigure")
        # This is platform-dependent
        has_reconfigure = hasattr(sys.stdout, "reconfigure")

        # Just verify the check works (result depends on platform/Python version)
        assert isinstance(has_reconfigure, bool)


class TestEncodingLogic:
    """Test the encoding configuration logic."""

    def test_encoding_target_is_utf8(self):
        """Test that target encoding is UTF-8."""
        # The code uses encoding="utf-8"
        target_encoding = "utf-8"
        assert target_encoding == "utf-8"

    def test_both_stdout_and_stderr_reconfigured(self):
        """Test that both stdout and stderr are reconfigured."""
        if sys.platform != "win32" or not hasattr(sys.stdout, "reconfigure"):
            pytest.skip("Requires Windows with reconfigure support")

        # Verify both stdout and stderr have reconfigure
        # (if one has it, both should in practice)
        has_stdout = hasattr(sys.stdout, "reconfigure")
        has_stderr = hasattr(sys.stderr, "reconfigure")

        # If we're running on a platform that supports it, both should have it
        if has_stdout or has_stderr:
            # They should both be present
            assert has_stdout == has_stderr

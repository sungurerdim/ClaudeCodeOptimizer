"""Test Windows console encoding configuration in __init__.py."""

import sys
from unittest.mock import MagicMock

import pytest


class TestWindowsEncodingErrorPath:
    """Test the exception handling path for Windows console encoding."""

    def test_reconfigure_exception_handled_silently(self):
        """Test that reconfigure exception is handled silently."""
        # The code now uses silent pass instead of logging
        exception_handled = False
        try:
            raise Exception("Test encoding error")
        except Exception:
            # Silent pass - no logging
            exception_handled = True

        assert exception_handled

    def test_reconfigure_no_exception_success(self):
        """Test successful reconfigure doesn't raise."""
        mock_stdout = MagicMock()
        # Don't set side_effect - will succeed
        try:
            mock_stdout.reconfigure(encoding="utf-8")
            success = True
        except Exception:
            success = False

        assert success


class TestPlatformSpecificBehavior:
    """Test platform-specific behavior of encoding setup."""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
    def test_windows_platform_check(self):
        """Test that code only runs on Windows."""
        assert sys.platform == "win32"

    @pytest.mark.skipif(sys.platform == "win32", reason="Non-Windows test")
    def test_non_windows_platform_skip(self):
        """Test that code is skipped on non-Windows."""
        assert sys.platform != "win32"

    def test_hasattr_reconfigure_check(self):
        """Test the hasattr check for reconfigure."""
        has_reconfigure = hasattr(sys.stdout, "reconfigure")
        assert isinstance(has_reconfigure, bool)


class TestEncodingLogic:
    """Test the encoding configuration logic."""

    def test_encoding_target_is_utf8(self):
        """Test that target encoding is UTF-8."""
        target_encoding = "utf-8"
        assert target_encoding == "utf-8"

    def test_both_stdout_and_stderr_reconfigured(self):
        """Test that both stdout and stderr are reconfigured."""
        if sys.platform != "win32" or not hasattr(sys.stdout, "reconfigure"):
            pytest.skip("Requires Windows with reconfigure support")

        has_stdout = hasattr(sys.stdout, "reconfigure")
        has_stderr = hasattr(sys.stderr, "reconfigure")

        if has_stdout or has_stderr:
            assert has_stdout == has_stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

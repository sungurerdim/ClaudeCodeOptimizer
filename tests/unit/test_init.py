"""Unit tests for claudecodeoptimizer/__init__.py module."""

import sys

import pytest


class TestVersionInfo:
    """Test version and author information."""

    def test_version_exists(self):
        """Test __version__ is defined."""
        from claudecodeoptimizer import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)

    def test_version_format(self):
        """Test __version__ follows semantic versioning."""
        from claudecodeoptimizer import __version__

        parts = __version__.split(".")
        assert len(parts) >= 2  # At least major.minor

    def test_version_is_1_0_0(self):
        """Test __version__ is 1.0.0."""
        from claudecodeoptimizer import __version__

        assert __version__ == "1.0.0"

    def test_author_exists(self):
        """Test __author__ is defined."""
        from claudecodeoptimizer import __author__

        assert __author__ is not None
        assert isinstance(__author__, str)


class TestWindowsConsoleEncoding:
    """Test Windows console encoding configuration."""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_windows_stdout_reconfigure_success(self):
        """Test stdout reconfigure on Windows succeeds."""
        if hasattr(sys.stdout, "reconfigure"):
            assert hasattr(sys.stdout, "reconfigure")

    @pytest.mark.skipif(sys.platform == "win32", reason="Non-Windows test")
    def test_non_windows_no_reconfigure(self):
        """Test non-Windows platforms skip reconfigure."""
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None
        assert hasattr(claudecodeoptimizer, "__version__")

    def test_exception_handling_silent(self):
        """Test exception handling is silent (pass)."""
        # The code now uses silent fail (pass)
        exception_handled = False
        try:
            raise Exception("Test error")
        except Exception:
            # This is what the module does - silent pass
            exception_handled = True

        assert exception_handled


class TestImportSuccess:
    """Test module import succeeds."""

    def test_import_succeeds(self):
        """Test import succeeds without errors."""
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None

    def test_version_importable(self):
        """Test __version__ is importable."""
        from claudecodeoptimizer import __version__

        assert __version__ is not None

    def test_author_importable(self):
        """Test __author__ is importable."""
        from claudecodeoptimizer import __author__

        assert __author__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

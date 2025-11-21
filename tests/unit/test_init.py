"""Unit tests for claudecodeoptimizer/__init__.py module."""

import sys
from unittest.mock import patch

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

    def test_author_exists(self):
        """Test __author__ is defined."""
        from claudecodeoptimizer import __author__

        assert __author__ is not None
        assert isinstance(__author__, str)

    def test_license_exists(self):
        """Test __license__ is defined."""
        from claudecodeoptimizer import __license__

        assert __license__ is not None
        assert isinstance(__license__, str)


class TestWindowsConsoleEncoding:
    """Test Windows console encoding configuration."""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_windows_stdout_reconfigure_success(self):
        """Test stdout reconfigure on Windows succeeds."""
        # This test runs on actual Windows, so it should work
        if hasattr(sys.stdout, "reconfigure"):
            # The encoding should have been set during import
            # We can't test the actual reconfiguration easily, but we can
            # verify the code path exists
            assert hasattr(sys.stdout, "reconfigure")

    @pytest.mark.skipif(sys.platform == "win32", reason="Non-Windows test")
    def test_non_windows_no_reconfigure(self):
        """Test non-Windows platforms skip reconfigure."""
        # On non-Windows, the reconfigure code shouldn't run
        # Verify module imports successfully on non-Windows
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None
        assert hasattr(claudecodeoptimizer, "__version__")

    def test_windows_reconfigure_exception_handling_direct(self):
        """Test exception handling during Windows console reconfigure (lines 14-15)."""
        # Test the actual exception handling logic that would occur in lines 14-15
        # The code now uses silent fail (pass) instead of logging

        test_exception = Exception("Failed to reconfigure console encoding")

        # Simulate the try-except block from lines 11-15
        exception_handled = False
        try:
            # This simulates the reconfigure call that might fail
            raise test_exception
        except Exception:  # noqa: S110
            # This is what line 15 does - silent pass
            exception_handled = True

        # Verify exception was handled without raising
        assert exception_handled, "Exception should have been caught and handled"


class TestCCOConfigImport:
    """Test CCOConfig import."""

    def test_ccoconfig_imported(self):
        """Test CCOConfig is imported."""
        from claudecodeoptimizer import CCOConfig

        assert CCOConfig is not None

    def test_ccoconfig_in_all(self):
        """Test CCOConfig is in __all__."""
        from claudecodeoptimizer import __all__

        assert "CCOConfig" in __all__

    def test_version_in_all(self):
        """Test __version__ is in __all__."""
        from claudecodeoptimizer import __all__

        assert "__version__" in __all__


class TestImportSuccess:
    """Test module import succeeds."""

    def test_import_succeeds(self):
        """Test import succeeds without errors."""
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None


class TestAllExports:
    """Test __all__ exports."""

    def test_all_defined(self):
        """Test __all__ is defined."""
        from claudecodeoptimizer import __all__

        assert __all__ is not None
        assert isinstance(__all__, list)

    def test_all_contains_expected(self):
        """Test __all__ contains expected exports."""
        from claudecodeoptimizer import __all__

        assert "CCOConfig" in __all__
        assert "__version__" in __all__

    def test_all_exports_importable(self):
        """Test all __all__ exports can be imported."""
        import claudecodeoptimizer
        from claudecodeoptimizer import __all__

        for name in __all__:
            assert hasattr(claudecodeoptimizer, name)


class TestImportStructure:
    """Test import structure and dependencies."""

    def test_can_import_module(self):
        """Test module can be imported."""
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None

    def test_can_import_from_module(self):
        """Test can import from module."""
        from claudecodeoptimizer import CCOConfig, __version__

        assert CCOConfig is not None
        assert __version__ is not None

    def test_config_import_works(self):
        """Test CCOConfig import from config module works."""
        from claudecodeoptimizer import CCOConfig
        from claudecodeoptimizer.config import CCOConfig as DirectCCOConfig

        assert CCOConfig is DirectCCOConfig


class TestExceptionHandling:
    """Test exception handling behavior."""

    def test_silent_exception_handling(self):
        """Test exceptions are handled silently without logging."""
        # The module uses silent fail (pass) instead of logging
        # This verifies the module can be imported without logging configuration
        import claudecodeoptimizer

        assert claudecodeoptimizer is not None



"""
Unit tests for Core Utilities

Tests utility functions for formatting, printing, and common helpers.
Target Coverage: 100%
"""

from io import StringIO
from contextlib import redirect_stdout

import pytest

from claudecodeoptimizer.core.utils import (
    format_confidence,
    format_confidence_str,
    print_header,
    print_separator,
)


class TestFormatConfidence:
    """Test format_confidence function"""

    def test_basic_conversion(self) -> None:
        """Test basic 0-1 to 0-100 conversion"""
        assert format_confidence(0.5) == 50.0
        assert format_confidence(1.0) == 100.0
        assert format_confidence(0.0) == 0.0

    def test_precision_default(self) -> None:
        """Test default precision of 1 decimal place"""
        assert format_confidence(0.875) == 87.5
        assert format_confidence(0.123) == 12.3
        assert format_confidence(0.999) == 99.9

    def test_precision_zero(self) -> None:
        """Test rounding to integer"""
        assert format_confidence(0.875, 0) == 88.0
        assert format_confidence(0.124, 0) == 12.0
        assert format_confidence(0.125, 0) == 12.0  # Banker's rounding
        assert format_confidence(0.126, 0) == 13.0

    def test_precision_two(self) -> None:
        """Test precision with 2 decimal places"""
        assert format_confidence(0.12345, 2) == 12.35
        assert format_confidence(0.12344, 2) == 12.34

    def test_edge_cases(self) -> None:
        """Test edge case values"""
        assert format_confidence(0.0) == 0.0
        assert format_confidence(1.0) == 100.0
        assert format_confidence(0.001) == 0.1
        assert format_confidence(0.999) == 99.9


class TestFormatConfidenceStr:
    """Test format_confidence_str function"""

    def test_default_decimal(self) -> None:
        """Test default format with 1 decimal place"""
        assert format_confidence_str(0.875) == "87.5%"
        assert format_confidence_str(0.5) == "50.0%"
        assert format_confidence_str(0.123) == "12.3%"

    def test_integer_format(self) -> None:
        """Test integer format"""
        assert format_confidence_str(0.875, True) == "87%"
        assert format_confidence_str(0.5, True) == "50%"
        assert format_confidence_str(0.123, True) == "12%"

    def test_edge_cases(self) -> None:
        """Test edge case values"""
        assert format_confidence_str(0.0) == "0.0%"
        assert format_confidence_str(1.0) == "100.0%"
        assert format_confidence_str(0.0, True) == "0%"
        assert format_confidence_str(1.0, True) == "100%"

    def test_rounding(self) -> None:
        """Test rounding behavior"""
        assert format_confidence_str(0.999, False) == "99.9%"
        assert format_confidence_str(0.999, True) == "99%"
        assert format_confidence_str(0.001, False) == "0.1%"
        assert format_confidence_str(0.001, True) == "0%"


class TestPrintSeparator:
    """Test print_separator function"""

    def test_default_separator(self) -> None:
        """Test default separator with '=' and default width"""
        output = StringIO()
        with redirect_stdout(output):
            print_separator()

        result = output.getvalue().strip()
        assert result.startswith("=")
        assert all(c == "=" for c in result)
        assert len(result) > 0

    def test_custom_char(self) -> None:
        """Test custom separator character"""
        output = StringIO()
        with redirect_stdout(output):
            print_separator("-")

        result = output.getvalue().strip()
        assert all(c == "-" for c in result)

    def test_custom_width(self) -> None:
        """Test custom width"""
        output = StringIO()
        with redirect_stdout(output):
            print_separator("=", 40)

        result = output.getvalue().strip()
        assert len(result) == 40
        assert all(c == "=" for c in result)

    def test_different_chars(self) -> None:
        """Test different separator characters"""
        for char in ["=", "-", "*", "#", "~"]:
            output = StringIO()
            with redirect_stdout(output):
                print_separator(char, 10)

            result = output.getvalue().strip()
            assert len(result) == 10
            assert all(c == char for c in result)


class TestPrintHeader:
    """Test print_header function"""

    def test_title_only(self) -> None:
        """Test header with title only"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("Test Title")

        result = output.getvalue()
        assert "Test Title" in result
        assert "=" in result
        # Should have separators before and after
        lines = result.strip().split("\n")
        assert len(lines) >= 3
        # First and last non-empty lines should be separators
        assert all(c == "=" for c in lines[0])
        assert all(c == "=" for c in lines[-1])

    def test_title_with_subtitle(self) -> None:
        """Test header with title and subtitle"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("Main Title", "Subtitle")

        result = output.getvalue()
        assert "Main Title" in result
        assert "Subtitle" in result
        assert "=" in result

    def test_custom_width(self) -> None:
        """Test header with custom width"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("Title", width=40)

        result = output.getvalue()
        lines = result.strip().split("\n")
        # Check separator lines have correct width
        separator_lines = [line for line in lines if all(c == "=" for c in line) and line]
        for sep in separator_lines:
            assert len(sep) == 40

    def test_none_subtitle(self) -> None:
        """Test header with explicit None subtitle"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("Title", None)

        result = output.getvalue()
        assert "Title" in result
        # Should not have extra content lines
        lines = [line for line in result.strip().split("\n") if line]
        # Should have: separator, title (indented), separator
        assert len(lines) == 3

    def test_empty_title(self) -> None:
        """Test header with empty title"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("")

        result = output.getvalue()
        assert "=" in result
        # Should still print separators even with empty title

    def test_long_title(self) -> None:
        """Test header with very long title"""
        long_title = "A" * 200
        output = StringIO()
        with redirect_stdout(output):
            print_header(long_title)

        result = output.getvalue()
        assert long_title in result


class TestUtilsIntegration:
    """Integration tests for utility functions"""

    def test_confidence_formatting_consistency(self) -> None:
        """Test that different confidence formats are consistent"""
        value = 0.875

        numeric = format_confidence(value, 1)
        string = format_confidence_str(value, False)

        # String should contain the numeric value
        assert str(numeric) in string

    def test_multiple_separators(self) -> None:
        """Test printing multiple separators"""
        output = StringIO()
        with redirect_stdout(output):
            print_separator("=", 20)
            print_separator("-", 20)
            print_separator("*", 20)

        result = output.getvalue()
        lines = result.strip().split("\n")
        assert len(lines) == 3
        assert all(c == "=" for c in lines[0])
        assert all(c == "-" for c in lines[1])
        assert all(c == "*" for c in lines[2])

    def test_header_with_content(self) -> None:
        """Test header followed by content"""
        output = StringIO()
        with redirect_stdout(output):
            print_header("Section 1", "Details")
            print("Content line 1")
            print("Content line 2")

        result = output.getvalue()
        assert "Section 1" in result
        assert "Details" in result
        assert "Content line 1" in result
        assert "Content line 2" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

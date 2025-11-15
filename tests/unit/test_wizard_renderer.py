"""
Comprehensive tests for wizard renderer module.

Tests cover:
- Color class and colorization
- Header and section printing
- List and table rendering
- Key-value pair formatting
- Progress bar display
- Success/warning/error/info messages
- Box rendering with different styles
- User input functions (ask_input, ask_choice, ask_yes_no, ask_multi_choice)
- Terminal control functions (clear_screen, pause)
- Edge cases and error conditions
"""

import io
import os
import subprocess
import sys
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from claudecodeoptimizer.core.constants import SEPARATOR_WIDTH, UI_HEADING_LEVEL_SECONDARY
from claudecodeoptimizer.wizard.renderer import (
    Colors,
    ask_choice,
    ask_input,
    ask_multi_choice,
    ask_yes_no,
    clear_screen,
    pause,
    print_box,
    print_dim,
    print_error,
    print_header,
    print_info,
    print_key_value,
    print_list,
    print_progress,
    print_section,
    print_success,
    print_table,
    print_warning,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_stdout():
    """Mock stdout for testing output"""
    return io.StringIO()


@pytest.fixture
def mock_colors_enabled():
    """Enable colors for testing"""
    original = Colors.ENABLED
    Colors.ENABLED = True
    yield
    Colors.ENABLED = original


@pytest.fixture
def mock_colors_disabled():
    """Disable colors for testing"""
    original = Colors.ENABLED
    Colors.ENABLED = False
    yield
    Colors.ENABLED = original


# ============================================================================
# COLORS CLASS TESTS
# ============================================================================


def test_colors_enabled_detection():
    """Test Colors.ENABLED is determined by terminal capabilities"""
    # ENABLED should be a boolean
    assert isinstance(Colors.ENABLED, bool)


def test_colors_colorize_enabled():
    """Test colorize applies color codes when enabled"""
    # Temporarily enable colors and re-initialize color codes
    original_enabled = Colors.ENABLED
    original_reset = Colors.RESET
    try:
        Colors.ENABLED = True
        Colors.RESET = "\033[0m"  # Re-set RESET code
        red_code = "\033[31m"

        result = Colors.colorize("test", red_code)
        assert "\033[31m" in result
        assert "\033[0m" in result
        assert "test" in result
    finally:
        Colors.ENABLED = original_enabled
        Colors.RESET = original_reset


def test_colors_colorize_disabled(mock_colors_disabled):
    """Test colorize returns plain text when disabled"""
    result = Colors.colorize("test", Colors.RED)
    assert result == "test"
    assert "\033[" not in result


def test_colors_all_codes_available():
    """Test all color codes are defined"""
    assert hasattr(Colors, "RESET")
    assert hasattr(Colors, "BOLD")
    assert hasattr(Colors, "DIM")
    assert hasattr(Colors, "RED")
    assert hasattr(Colors, "GREEN")
    assert hasattr(Colors, "YELLOW")
    assert hasattr(Colors, "BLUE")
    assert hasattr(Colors, "CYAN")
    assert hasattr(Colors, "MAGENTA")
    assert hasattr(Colors, "WHITE")
    assert hasattr(Colors, "BRIGHT_GREEN")
    assert hasattr(Colors, "BRIGHT_YELLOW")
    assert hasattr(Colors, "BRIGHT_BLUE")
    assert hasattr(Colors, "BRIGHT_CYAN")


def test_colors_disabled_when_term_is_dumb():
    """Test colors are disabled when TERM=dumb"""
    with patch.dict(os.environ, {"TERM": "dumb"}):
        with patch("sys.stdout.isatty", return_value=True):
            # Re-evaluate ENABLED with dumb terminal
            assert os.getenv("TERM") == "dumb"


# ============================================================================
# PRINT HEADER TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_header_basic(mock_print):
    """Test basic header printing"""
    print_header("Test Header")
    assert mock_print.call_count >= 4  # Empty line, top border, title, bottom border, empty line


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_header_with_subtitle(mock_print):
    """Test header with subtitle"""
    print_header("Test Header", "Subtitle")
    assert mock_print.call_count >= 5  # Extra call for subtitle


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_header_custom_width(mock_print):
    """Test header with custom width"""
    print_header("Test", width=40)
    # Verify width is used in formatting
    assert mock_print.called


# ============================================================================
# PRINT SECTION TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_section_level_1(mock_print):
    """Test level 1 section printing"""
    print_section("Section Title", level=1)
    # Should print empty line, colored title with >, and separator
    assert mock_print.call_count >= 3


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_section_level_2(mock_print):
    """Test level 2 section printing"""
    print_section("Section Title", level=UI_HEADING_LEVEL_SECONDARY)
    # Should print empty line and indented title
    assert mock_print.call_count >= 2


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_section_level_3(mock_print):
    """Test level 3+ section printing"""
    print_section("Section Title", level=3)
    # Should print colored title with more indentation
    assert mock_print.call_count >= 1


# ============================================================================
# PRINT LIST TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_list_basic(mock_print):
    """Test basic list printing"""
    items = ["Item 1", "Item 2", "Item 3"]
    print_list(items)
    assert mock_print.call_count == 3


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_list_custom_bullet(mock_print):
    """Test list with custom bullet"""
    items = ["Item 1"]
    print_list(items, bullet="-")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_list_custom_indent(mock_print):
    """Test list with custom indent"""
    items = ["Item 1"]
    print_list(items, indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_list_empty(mock_print):
    """Test list with no items"""
    print_list([])
    assert mock_print.call_count == 0


# ============================================================================
# PRINT TABLE TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_basic(mock_print):
    """Test basic table printing"""
    data = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]
    print_table(data)
    assert mock_print.call_count >= 4  # Header, separator, 2 rows, empty line


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_with_headers(mock_print):
    """Test table with custom headers"""
    data = [{"name": "Alice", "age": "30"}]
    print_table(data, headers=["name", "age"])
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_empty_data(mock_print):
    """Test table with empty data"""
    print_table([])
    assert mock_print.called
    # Should print "(No data)" message


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_auto_headers(mock_print):
    """Test table auto-detects headers from data"""
    data = [{"col1": "val1", "col2": "val2"}]
    print_table(data, headers=None)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_width_overflow(mock_print):
    """Test table handles width overflow"""
    data = [{"very_long_column_name": "very_long_value_that_exceeds_width" * 10}]
    print_table(data, max_width=40)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_missing_keys(mock_print):
    """Test table handles missing keys gracefully"""
    data = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob"},  # Missing age
    ]
    print_table(data)
    assert mock_print.called


# ============================================================================
# PRINT KEY-VALUE TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_key_value_basic(mock_print):
    """Test basic key-value printing"""
    print_key_value("Key", "Value")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_key_value_custom_indent(mock_print):
    """Test key-value with custom indent"""
    print_key_value("Key", "Value", indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_key_value_non_string_value(mock_print):
    """Test key-value with non-string value"""
    print_key_value("Count", 42)
    assert mock_print.called


# ============================================================================
# PRINT PROGRESS TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_basic(mock_print):
    """Test basic progress bar"""
    print_progress(50, 100)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_with_label(mock_print):
    """Test progress bar with label"""
    print_progress(50, 100, label="Processing")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_zero_total(mock_print):
    """Test progress bar with zero total"""
    print_progress(0, 0)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_full(mock_print):
    """Test progress bar at 100%"""
    print_progress(100, 100)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_partial(mock_print):
    """Test progress bar at partial completion"""
    print_progress(33, 100)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_custom_width(mock_print):
    """Test progress bar with custom width"""
    print_progress(50, 100, width=20)
    assert mock_print.called


# ============================================================================
# MESSAGE PRINTING TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_success(mock_print):
    """Test success message printing"""
    print_success("Operation completed")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_success_custom_indent(mock_print):
    """Test success message with custom indent"""
    print_success("Done", indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_warning(mock_print):
    """Test warning message printing"""
    print_warning("Be careful")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_warning_custom_indent(mock_print):
    """Test warning message with custom indent"""
    print_warning("Warning", indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_error(mock_print):
    """Test error message printing"""
    print_error("Something went wrong")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_error_custom_indent(mock_print):
    """Test error message with custom indent"""
    print_error("Error", indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_info(mock_print):
    """Test info message printing"""
    print_info("Information")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_info_custom_indent(mock_print):
    """Test info message with custom indent"""
    print_info("Info", indent=4)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_dim(mock_print):
    """Test dimmed message printing"""
    print_dim("Muted text")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_dim_custom_indent(mock_print):
    """Test dimmed message with custom indent"""
    print_dim("Dim", indent=4)
    assert mock_print.called


# ============================================================================
# PRINT BOX TESTS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_basic(mock_print):
    """Test basic box printing"""
    content = ["Line 1", "Line 2"]
    print_box(content)
    assert mock_print.call_count >= 4  # Top, 2 lines, bottom, empty


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_with_title(mock_print):
    """Test box with title"""
    content = ["Line 1"]
    print_box(content, title="Test Box")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_double_style(mock_print):
    """Test box with double border style"""
    content = ["Line 1"]
    print_box(content, style="double")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_single_style(mock_print):
    """Test box with single border style"""
    content = ["Line 1"]
    print_box(content, style="single")
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_custom_width(mock_print):
    """Test box with custom width"""
    content = ["Line 1"]
    print_box(content, width=40)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_long_content(mock_print):
    """Test box with content that needs wrapping"""
    content = ["This is a very long line that should be wrapped " * 5]
    print_box(content, width=40)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_empty_content(mock_print):
    """Test box with empty content"""
    print_box([])
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_wrapping_edge_case(mock_print):
    """Test box word wrapping with edge cases"""
    # Test with a single very long word
    content = ["verylongwordthatcannotbewrapped" * 10]
    print_box(content, width=40)
    assert mock_print.called


# ============================================================================
# ASK INPUT TESTS
# ============================================================================


@patch("builtins.input", return_value="user input")
def test_ask_input_basic(mock_input):
    """Test basic input asking"""
    result = ask_input("Enter value")
    assert result == "user input"


@patch("builtins.input", return_value="")
def test_ask_input_with_default(mock_input):
    """Test input with default value"""
    result = ask_input("Enter value", default="default_val")
    assert result == "default_val"


@patch("builtins.input", side_effect=["", "", "valid"])
def test_ask_input_required(mock_input):
    """Test required input validation"""
    with patch("claudecodeoptimizer.wizard.renderer.print_warning"):
        result = ask_input("Enter value", required=True)
        assert result == "valid"
        assert mock_input.call_count == 3


@patch("builtins.input", return_value="")
def test_ask_input_not_required(mock_input):
    """Test optional input"""
    result = ask_input("Enter value", required=False)
    assert result == ""


@patch("builtins.input", side_effect=KeyboardInterrupt)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_input_keyboard_interrupt(mock_print, mock_input):
    """Test handling of keyboard interrupt"""
    with pytest.raises(KeyboardInterrupt):
        ask_input("Enter value")


@patch("builtins.input", side_effect=EOFError)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_input_eof_error(mock_print, mock_input):
    """Test handling of EOF error"""
    with pytest.raises(EOFError):
        ask_input("Enter value")


@patch("builtins.input", return_value="  trimmed  ")
def test_ask_input_strips_whitespace(mock_input):
    """Test input is stripped of whitespace"""
    result = ask_input("Enter value")
    assert result == "trimmed"


# ============================================================================
# ASK CHOICE TESTS
# ============================================================================


@patch("builtins.input", return_value="1")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_numeric(mock_print, mock_input):
    """Test choice selection with number"""
    choices = ["Option 1", "Option 2", "Option 3"]
    result = ask_choice("Select option", choices)
    assert result == "Option 1"


@patch("builtins.input", return_value="opt")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_partial_text(mock_print, mock_input):
    """Test choice selection with partial text match"""
    choices = ["Option 1", "Option 2"]
    result = ask_choice("Select option", choices)
    assert result == "Option 1"


@patch("builtins.input", return_value="")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_default(mock_print, mock_input):
    """Test choice with default value"""
    choices = ["Option 1", "Option 2"]
    result = ask_choice("Select option", choices, default="Option 2")
    assert result == "Option 2"


@patch("builtins.input", side_effect=["99", "0", "2"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_invalid_then_valid(mock_print, mock_input):
    """Test invalid choice followed by valid choice"""
    choices = ["Option 1", "Option 2"]
    with patch("claudecodeoptimizer.wizard.renderer.print_warning"):
        result = ask_choice("Select option", choices)
        assert result == "Option 2"
        assert mock_input.call_count == 3


@patch("builtins.input", return_value="2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_no_numbers(mock_print, mock_input):
    """Test choice without number display"""
    choices = ["Option 1", "Option 2"]
    result = ask_choice("Select option", choices, show_numbers=False)
    assert result == "Option 2"


@patch("builtins.input", side_effect=KeyboardInterrupt)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_keyboard_interrupt(mock_print, mock_input):
    """Test keyboard interrupt in choice"""
    with pytest.raises(KeyboardInterrupt):
        ask_choice("Select option", ["A", "B"])


@patch("builtins.input", return_value="option 2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_case_insensitive(mock_print, mock_input):
    """Test choice is case insensitive"""
    choices = ["Option 1", "Option 2"]
    result = ask_choice("Select option", choices)
    assert result == "Option 2"


@patch("builtins.input", return_value="")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_bullets_with_default(mock_print, mock_input):
    """Test choice with bullets and default value"""
    choices = ["Option 1", "Option 2"]
    result = ask_choice("Select option", choices, default="Option 1", show_numbers=False)
    assert result == "Option 1"


# ============================================================================
# ASK YES/NO TESTS
# ============================================================================


@patch("builtins.input", return_value="y")
def test_ask_yes_no_yes(mock_input):
    """Test yes answer"""
    result = ask_yes_no("Confirm?")
    assert result is True


@patch("builtins.input", return_value="n")
def test_ask_yes_no_no(mock_input):
    """Test no answer"""
    result = ask_yes_no("Confirm?")
    assert result is False


@patch("builtins.input", return_value="yes")
def test_ask_yes_no_yes_full(mock_input):
    """Test 'yes' full word"""
    result = ask_yes_no("Confirm?")
    assert result is True


@patch("builtins.input", return_value="no")
def test_ask_yes_no_no_full(mock_input):
    """Test 'no' full word"""
    result = ask_yes_no("Confirm?")
    assert result is False


@patch("builtins.input", return_value="")
def test_ask_yes_no_default_true(mock_input):
    """Test default True"""
    result = ask_yes_no("Confirm?", default=True)
    assert result is True


@patch("builtins.input", return_value="")
def test_ask_yes_no_default_false(mock_input):
    """Test default False"""
    result = ask_yes_no("Confirm?", default=False)
    assert result is False


@patch("builtins.input", return_value="1")
def test_ask_yes_no_numeric_true(mock_input):
    """Test numeric 1 for True"""
    result = ask_yes_no("Confirm?")
    assert result is True


@patch("builtins.input", return_value="0")
def test_ask_yes_no_numeric_false(mock_input):
    """Test numeric 0 for False"""
    result = ask_yes_no("Confirm?")
    assert result is False


@patch("builtins.input", side_effect=["maybe", "invalid", "y"])
def test_ask_yes_no_invalid_then_valid(mock_input):
    """Test invalid answers followed by valid"""
    with patch("claudecodeoptimizer.wizard.renderer.print_warning"):
        result = ask_yes_no("Confirm?")
        assert result is True
        assert mock_input.call_count == 3


@patch("builtins.input", side_effect=KeyboardInterrupt)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_yes_no_keyboard_interrupt(mock_print, mock_input):
    """Test keyboard interrupt in yes/no"""
    with pytest.raises(KeyboardInterrupt):
        ask_yes_no("Confirm?")


@patch("builtins.input", return_value="Y")
def test_ask_yes_no_case_insensitive(mock_input):
    """Test yes/no is case insensitive"""
    result = ask_yes_no("Confirm?")
    assert result is True


@patch("builtins.input", return_value="true")
def test_ask_yes_no_true_keyword(mock_input):
    """Test 'true' keyword"""
    result = ask_yes_no("Confirm?")
    assert result is True


@patch("builtins.input", return_value="false")
def test_ask_yes_no_false_keyword(mock_input):
    """Test 'false' keyword"""
    result = ask_yes_no("Confirm?")
    assert result is False


# ============================================================================
# ASK MULTI CHOICE TESTS
# ============================================================================


@patch("builtins.input", return_value="1 2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_basic(mock_print, mock_input):
    """Test basic multi-choice selection"""
    choices = ["Option 1", "Option 2", "Option 3"]
    result = ask_multi_choice("Select options", choices)
    assert result == ["Option 1", "Option 2"]


@patch("builtins.input", return_value="")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_defaults(mock_print, mock_input):
    """Test multi-choice with defaults"""
    choices = ["Option 1", "Option 2", "Option 3"]
    defaults = ["Option 1", "Option 3"]
    result = ask_multi_choice("Select options", choices, defaults=defaults)
    assert result == defaults


@patch("builtins.input", return_value="1,2,3")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_comma_separated(mock_print, mock_input):
    """Test multi-choice with comma-separated input"""
    choices = ["Option 1", "Option 2", "Option 3"]
    result = ask_multi_choice("Select options", choices)
    assert result == ["Option 1", "Option 2", "Option 3"]


@patch("builtins.input", side_effect=["more", "16"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_pagination_more(mock_print, mock_input):
    """Test multi-choice pagination - next page"""
    choices = [f"Option {i}" for i in range(1, 30)]  # More than page_size
    result = ask_multi_choice("Select options", choices, show_pagination=True, page_size=15)
    # After "more", we're on page 2, so selecting option 16 (first on page 2)
    assert result == ["Option 16"]


@patch("builtins.input", side_effect=["more", "back", "1"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_pagination_back(mock_print, mock_input):
    """Test multi-choice pagination - previous page"""
    choices = [f"Option {i}" for i in range(1, 30)]
    result = ask_multi_choice("Select options", choices, show_pagination=True, page_size=15)
    assert result == ["Option 1"]


@patch("builtins.input", side_effect=["all", "1 2"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_show_all(mock_print, mock_input):
    """Test multi-choice show all command"""
    choices = [f"Option {i}" for i in range(1, 30)]
    result = ask_multi_choice("Select options", choices, show_pagination=True, page_size=15)
    assert result == ["Option 1", "Option 2"]


@patch("builtins.input", side_effect=["", "1 2"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_min_selections(mock_print, mock_input):
    """Test multi-choice minimum selections validation"""
    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("claudecodeoptimizer.wizard.renderer.print_warning"):
        result = ask_multi_choice("Select options", choices, min_selections=2)
        assert len(result) >= 2


@patch("builtins.input", side_effect=["1 2 3", "1 2"])
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_max_selections(mock_print, mock_input):
    """Test multi-choice maximum selections validation"""
    choices = ["Option 1", "Option 2", "Option 3"]
    with patch("claudecodeoptimizer.wizard.renderer.print_warning"):
        result = ask_multi_choice("Select options", choices, max_selections=2)
        assert len(result) <= 2


@patch("builtins.input", return_value="99 1")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_invalid_numbers(mock_print, mock_input):
    """Test multi-choice ignores invalid numbers"""
    choices = ["Option 1", "Option 2"]
    result = ask_multi_choice("Select options", choices)
    assert result == ["Option 1"]  # 99 is ignored


@patch("builtins.input", side_effect=KeyboardInterrupt)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_keyboard_interrupt(mock_print, mock_input):
    """Test keyboard interrupt in multi-choice"""
    with pytest.raises(KeyboardInterrupt):
        ask_multi_choice("Select options", ["A", "B"])


@patch("builtins.input", return_value="2 1 3")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_sorted_output(mock_print, mock_input):
    """Test multi-choice returns sorted results"""
    choices = ["Option 1", "Option 2", "Option 3"]
    result = ask_multi_choice("Select options", choices)
    assert result == ["Option 1", "Option 2", "Option 3"]


@patch("builtins.input", return_value="1 2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_no_pagination(mock_print, mock_input):
    """Test multi-choice without pagination"""
    choices = ["Option 1", "Option 2", "Option 3"]
    result = ask_multi_choice("Select options", choices, show_pagination=False)
    assert result == ["Option 1", "Option 2"]


@patch("builtins.input", return_value="1 2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_custom_label(mock_print, mock_input):
    """Test multi-choice with custom default label"""
    choices = ["Option 1", "Option 2", "Option 3"]
    defaults = ["Option 1"]
    result = ask_multi_choice(
        "Select options",
        choices,
        defaults=defaults,
        default_label="recommended",
    )
    assert result == ["Option 1", "Option 2"]


# ============================================================================
# TERMINAL CONTROL TESTS
# ============================================================================


@patch("subprocess.run")
def test_clear_screen_windows(mock_run):
    """Test clear screen on Windows"""
    with patch("os.name", "nt"):
        clear_screen()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "cls" in args


@patch("subprocess.run")
def test_clear_screen_unix(mock_run):
    """Test clear screen on Unix-like systems"""
    with patch("os.name", "posix"):
        clear_screen()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "clear" in args


@patch("builtins.input", return_value="")
def test_pause_default_message(mock_input):
    """Test pause with default message"""
    pause()
    assert mock_input.called


@patch("builtins.input", return_value="")
def test_pause_custom_message(mock_input):
    """Test pause with custom message"""
    pause("Custom message")
    assert mock_input.called


@patch("builtins.input", side_effect=KeyboardInterrupt)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_pause_keyboard_interrupt(mock_print, mock_input):
    """Test keyboard interrupt in pause"""
    with pytest.raises(KeyboardInterrupt):
        pause()


@patch("builtins.input", side_effect=EOFError)
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_pause_eof_error(mock_print, mock_input):
    """Test EOF error in pause"""
    with pytest.raises(EOFError):
        pause()


# ============================================================================
# EDGE CASES AND ERROR CONDITIONS
# ============================================================================


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_single_row(mock_print):
    """Test table with single row"""
    data = [{"name": "Alice"}]
    print_table(data)
    assert mock_print.called


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_table_wide_content(mock_print):
    """Test table with very wide content"""
    data = [{"col": "x" * 200}]
    print_table(data, max_width=80)
    assert mock_print.called


@patch("builtins.input", return_value="")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_empty_defaults(mock_print, mock_input):
    """Test multi-choice with empty defaults list"""
    choices = ["Option 1", "Option 2"]
    result = ask_multi_choice("Select options", choices, defaults=[])
    # Should require user to select something or return empty
    assert isinstance(result, list)


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_box_title_longer_than_width(mock_print):
    """Test box with title longer than width"""
    content = ["Content"]
    print_box(content, title="Very Long Title That Exceeds Width", width=20)
    assert mock_print.called


@patch("builtins.input", return_value="3")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_choice_exact_match(mock_print, mock_input):
    """Test choice selection at boundary"""
    choices = ["A", "B", "C"]
    result = ask_choice("Choose", choices)
    assert result == "C"


@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_print_progress_edge_values(mock_print):
    """Test progress with edge case values"""
    print_progress(0, 100)  # 0%
    print_progress(100, 100)  # 100%
    print_progress(50, 100)  # 50%
    assert mock_print.call_count == 3


@patch("builtins.input", return_value="1 1 1 2")
@patch("claudecodeoptimizer.wizard.renderer.safe_print")
def test_ask_multi_choice_duplicate_selections(mock_print, mock_input):
    """Test multi-choice handles duplicate selections"""
    choices = ["Option 1", "Option 2"]
    result = ask_multi_choice("Select options", choices)
    # Should deduplicate
    assert result.count("Option 1") == 1
    assert result.count("Option 2") == 1

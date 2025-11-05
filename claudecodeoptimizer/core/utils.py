"""
Utility functions for ClaudeCodeOptimizer.

Common helper functions to reduce code duplication (P002 - DRY Enforcement).
"""

from typing import Optional

from .constants import CONFIDENCE_SCALE, SEPARATOR_WIDTH


def format_confidence(value: float, precision: int = 1) -> float:
    """
    Convert 0-1 confidence value to 0-100 percentage scale.

    Args:
        value: Confidence value between 0 and 1
        precision: Number of decimal places (default: 1)

    Returns:
        Confidence as percentage (0-100) rounded to specified precision

    Examples:
        >>> format_confidence(0.875, 1)
        87.5
        >>> format_confidence(0.875, 0)
        88.0
    """
    return round(value * CONFIDENCE_SCALE, precision)


def format_confidence_str(value: float, use_int: bool = False) -> str:
    """
    Convert 0-1 confidence to percentage string with % sign.

    Args:
        value: Confidence value between 0 and 1
        use_int: If True, use integer percentage (default: False uses 1 decimal)

    Returns:
        Formatted percentage string (e.g., "87.5%" or "88%")

    Examples:
        >>> format_confidence_str(0.875, False)
        '87.5%'
        >>> format_confidence_str(0.875, True)
        '88%'
    """
    if use_int:
        return f"{int(value * CONFIDENCE_SCALE)}%"
    return f"{format_confidence(value, 1)}%"


def print_separator(char: str = "=", width: Optional[int] = None) -> None:
    """
    Print a separator line.

    Args:
        char: Character to use for separator (default: "=")
        width: Width of separator (default: SEPARATOR_WIDTH from constants)

    Examples:
        >>> print_separator()
        ================================================================================
        >>> print_separator("-", 40)
        ----------------------------------------
    """
    if width is None:
        width = SEPARATOR_WIDTH
    print(char * width)


def print_header(title: str, subtitle: Optional[str] = None, width: Optional[int] = None) -> None:
    """
    Print a formatted header with separator lines.

    Args:
        title: Header title text
        subtitle: Optional subtitle text
        width: Width of header (default: SEPARATOR_WIDTH from constants)

    Examples:
        >>> print_header("CCO Status")
        ================================================================================
          CCO Status
        ================================================================================

        >>> print_header("CCO Status", "Project Analysis")
        ================================================================================
          CCO Status
          Project Analysis
        ================================================================================
    """
    if width is None:
        width = SEPARATOR_WIDTH

    print()
    print_separator("=", width)
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print_separator("=", width)
    print()


__all__ = [
    "format_confidence",
    "format_confidence_str",
    "print_separator",
    "print_header",
]

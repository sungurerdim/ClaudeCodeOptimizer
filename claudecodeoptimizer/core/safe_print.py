"""
Safe printing utilities for cross-platform Unicode support.

Ensures proper UTF-8 encoding for emojis and special characters across all platforms.
Automatically handles console encoding configuration with error recovery.
"""

import sys
from typing import Any


def configure_utf8_encoding() -> None:
    """
    Configure console for UTF-8 encoding across all platforms.

    Fixes UnicodeEncodeError when printing emojis and Unicode characters.
    Must be called early in program execution, before any print() calls.

    Automatically detects platform and applies appropriate configuration:
    - Reconfigures stdout/stderr with UTF-8 encoding
    - Enables error replacement instead of crashes
    - Sets console code page on platforms that require it
    """
    try:
        import io

        # Only reconfigure if stdout has a buffer (not already wrapped)
        if hasattr(sys.stdout, "buffer"):
            # Set console code page to UTF-8 on platforms that use code pages
            if sys.platform == "win32":
                import subprocess

                subprocess.run(  # noqa: S603
                    ["chcp", "65001"],  # noqa: S607 - chcp is built-in Windows command
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )

            # Reconfigure stdout/stderr with UTF-8 encoding
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer,
                encoding="utf-8",
                errors="replace",  # Replace unencodable chars instead of crashing
                line_buffering=True,
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer,
                encoding="utf-8",
                errors="replace",
                line_buffering=True,
            )
    except (AttributeError, OSError):
        # If reconfiguration fails, continue with default encoding
        pass


def safe_print(*args: object, **kwargs: Any) -> None:  # noqa: ANN401
    """
    Print with automatic error recovery for encoding issues on all platforms.

    If UTF-8 encoding fails, automatically converts:
    - Emojis to ASCII equivalents (🔧 -> [BUILD])
    - Special Unicode to basic characters (✓ -> [OK])

    Usage:
        safe_print("✓ Success!")      # Works everywhere
        safe_print("🔧 Building...")   # Works everywhere
    """
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Convert to ASCII-safe version
        safe_args: list[str] = []
        for arg in args:
            if isinstance(arg, str):
                safe_args.append(_unicode_to_ascii(arg))
            else:
                safe_args.append(str(arg))
        print(*safe_args, **kwargs)


def _unicode_to_ascii(text: str) -> str:
    """
    Convert Unicode characters to ASCII equivalents for consoles without UTF-8 support.

    Maps common emojis and special characters to readable ASCII alternatives.
    """
    # Emoji replacements
    replacements = {
        # Status indicators
        "✓": "[OK]",
        "✗": "[X]",
        "❌": "[ERROR]",
        "⚠️": "[WARNING]",
        "💡": "[TIP]",
        # Progress indicators
        "🔧": "[BUILD]",
        "📊": "[ANALYSIS]",
        "🎯": "[TARGET]",
        "🚀": "[LAUNCH]",
        # Documentation
        "📋": "[LIST]",
        "📦": "[PACKAGE]",
        "📅": "[DATE]",
        "📝": "[NOTE]",
        # Levels
        "🟢": "[HIGH]",
        "🟡": "[MEDIUM]",
        "🔴": "[LOW]",
        "⚪": "[NONE]",
        # Other common
        "→": "->",
        "←": "<-",
        "↓": "v",
        "↑": "^",
        "•": "*",
        "…": "...",
    }

    result = text
    for unicode_char, ascii_equiv in replacements.items():
        result = result.replace(unicode_char, ascii_equiv)

    # Final fallback: encode with 'replace' error handling
    try:
        result.encode(sys.stdout.encoding or "utf-8")
        return result
    except (UnicodeEncodeError, AttributeError):
        # Last resort: ASCII-only
        return result.encode("ascii", errors="replace").decode("ascii")


__all__ = ["configure_utf8_encoding", "safe_print"]

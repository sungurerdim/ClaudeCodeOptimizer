"""
Safe printing utilities for cross-platform Unicode support.

Ensures proper UTF-8 encoding for emojis and special characters across all platforms.
Automatically handles console encoding configuration with error recovery.
"""

import re
import sys
from typing import Any

# Pre-built replacement map (module-level constant for single initialization)
# Multi-char replacements require regex, single-char can use translate
_UNICODE_REPLACEMENTS = {
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

# Pre-compiled regex pattern for O(n) single-pass replacement
_UNICODE_PATTERN = re.compile("|".join(re.escape(k) for k in _UNICODE_REPLACEMENTS))


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
    # Skip reconfiguration during pytest execution to avoid interfering with pytest's capture
    if "pytest" in sys.modules:
        return

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
    Uses pre-compiled regex for O(n) single-pass replacement instead of O(n*m) sequential.
    """
    # Single-pass replacement using pre-compiled pattern (O(n) vs O(n*m))
    result = _UNICODE_PATTERN.sub(lambda m: _UNICODE_REPLACEMENTS[m.group()], text)

    # Final fallback: encode with 'replace' error handling
    try:
        result.encode(sys.stdout.encoding or "utf-8")
        return result
    except (UnicodeEncodeError, AttributeError):
        # Last resort: ASCII-only
        return result.encode("ascii", errors="replace").decode("ascii")


__all__ = ["configure_utf8_encoding", "safe_print"]

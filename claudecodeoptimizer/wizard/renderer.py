"""
CLI Rendering Utilities - CCO 2.5 Wizard

Simple text-based UI components using pure stdlib.
No external dependencies (rich, questionary, etc.)
Optional ANSI color support for better UX.
"""

import os
import sys
from typing import Any, Dict, List, Optional

from ..core.constants import SEPARATOR_WIDTH, UI_HEADING_LEVEL_SECONDARY
from ..core.safe_print import safe_print
from ..core.utils import format_confidence


class Colors:
    """ANSI color codes (optional - degrades gracefully)"""

    # Check if terminal supports colors
    ENABLED = sys.stdout.isatty() and os.getenv("TERM") not in ["dumb", None]

    # Color codes
    RESET = "\033[0m" if ENABLED else ""
    BOLD = "\033[1m" if ENABLED else ""
    DIM = "\033[2m" if ENABLED else ""

    # Foreground colors
    BLACK = "\033[30m" if ENABLED else ""
    RED = "\033[31m" if ENABLED else ""
    GREEN = "\033[32m" if ENABLED else ""
    YELLOW = "\033[33m" if ENABLED else ""
    BLUE = "\033[34m" if ENABLED else ""
    MAGENTA = "\033[35m" if ENABLED else ""
    CYAN = "\033[36m" if ENABLED else ""
    WHITE = "\033[37m" if ENABLED else ""

    # Bright colors
    BRIGHT_GREEN = "\033[92m" if ENABLED else ""
    BRIGHT_YELLOW = "\033[93m" if ENABLED else ""
    BRIGHT_BLUE = "\033[94m" if ENABLED else ""
    BRIGHT_CYAN = "\033[96m" if ENABLED else ""

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text if enabled"""
        if not cls.ENABLED:
            return text
        return f"{color}{text}{cls.RESET}"


def print_header(title: str, subtitle: Optional[str] = None, width: int = SEPARATOR_WIDTH) -> None:
    """Print a formatted header section"""
    c = Colors

    safe_print()
    safe_print(c.colorize("=" * width, c.CYAN))
    safe_print(c.colorize(f"{title:^{width}}", c.BOLD + c.BRIGHT_CYAN))
    if subtitle:
        safe_print(c.colorize(f"{subtitle:^{width}}", c.DIM + c.CYAN))
    safe_print(c.colorize("=" * width, c.CYAN))
    safe_print()


def print_section(title: str, level: int = 1) -> None:
    """Print a section header"""
    c = Colors

    if level == 1:
        safe_print()
        safe_print(c.colorize(f"> {title}", c.BOLD + c.BRIGHT_BLUE))
        safe_print(c.colorize("-" * (len(title) + 3), c.BLUE))
    elif level == UI_HEADING_LEVEL_SECONDARY:
        safe_print()
        safe_print(c.colorize(f"  {title}", c.BRIGHT_CYAN))
    else:
        safe_print(c.colorize(f"    {title}", c.CYAN))


def print_list(items: List[str], bullet: str = "*", indent: int = 2) -> None:
    """Print a bulleted list"""
    c = Colors
    prefix = " " * indent

    for item in items:
        safe_print(f"{prefix}{c.colorize(bullet, c.GREEN)} {item}")


def print_table(
    data: List[Dict[str, Any]],
    headers: Optional[List[str]] = None,
    max_width: int = SEPARATOR_WIDTH,
) -> None:
    """Print a formatted table"""
    c = Colors

    if not data:
        safe_print(c.colorize("  (No data)", c.DIM))
        return

    # Auto-detect headers if not provided
    if headers is None:
        headers = list(data[0].keys())

    # Calculate column widths
    col_widths = {h: len(h) for h in headers}
    for row in data:
        for header in headers:
            value = str(row.get(header, ""))
            col_widths[header] = max(col_widths[header], len(value))

    # Limit column widths to avoid overflow
    total_width = sum(col_widths.values()) + len(headers) * 3
    if total_width > max_width:
        # Scale down proportionally
        scale = (max_width - len(headers) * 3) / sum(col_widths.values())
        col_widths = {h: max(10, int(w * scale)) for h, w in col_widths.items()}

    # Print header
    header_row = " | ".join(
        [c.colorize(h[: col_widths[h]].ljust(col_widths[h]), c.BOLD + c.CYAN) for h in headers],
    )
    safe_print(f"  {header_row}")

    # Print separator
    separator = "-+-".join(["-" * col_widths[h] for h in headers])
    safe_print(f"  {c.colorize(separator, c.BLUE)}")

    # Print rows
    for row in data:
        row_str = " | ".join(
            [str(row.get(h, ""))[: col_widths[h]].ljust(col_widths[h]) for h in headers],
        )
        safe_print(f"  {row_str}")

    safe_print()


def print_key_value(key: str, value: Any, indent: int = 2) -> None:
    """Print key-value pair"""
    c = Colors
    prefix = " " * indent
    key_str = c.colorize(f"{key}:", c.BOLD + c.CYAN)
    safe_print(f"{prefix}{key_str} {value}")


def print_progress(
    current: int,
    total: int,
    label: Optional[str] = None,
    width: int = 40,
) -> None:
    """Print a progress bar"""
    c = Colors

    percent = current / total if total > 0 else 0
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)

    if label:
        safe_print(
            f"\r{label} [{c.colorize(bar, c.GREEN)}] {int(format_confidence(percent, 0))}%",
            end="",
            flush=True,
        )
    else:
        safe_print(
            f"\r[{c.colorize(bar, c.GREEN)}] {int(format_confidence(percent, 0))}%",
            end="",
            flush=True,
        )


def print_success(message: str, indent: int = 2) -> None:
    """Print a success message"""
    c = Colors
    prefix = " " * indent
    icon = c.colorize("[OK]", c.BRIGHT_GREEN)
    safe_print(f"{prefix}{icon} {c.colorize(message, c.GREEN)}")


def print_warning(message: str, indent: int = 2) -> None:
    """Print a warning message"""
    c = Colors
    prefix = " " * indent
    icon = c.colorize("[!]", c.BRIGHT_YELLOW)
    safe_print(f"{prefix}{icon} {c.colorize(message, c.YELLOW)}")


def print_error(message: str, indent: int = 2) -> None:
    """Print an error message"""
    c = Colors
    prefix = " " * indent
    icon = c.colorize("[X]", c.RED)
    safe_print(f"{prefix}{icon} {c.colorize(message, c.RED)}")


def print_info(message: str, indent: int = 2) -> None:
    """Print an info message"""
    c = Colors
    prefix = " " * indent
    icon = c.colorize("[i]", c.BRIGHT_CYAN)
    safe_print(f"{prefix}{icon} {message}")


def print_dim(message: str, indent: int = 2) -> None:
    """Print a dimmed/muted message"""
    c = Colors
    prefix = " " * indent
    safe_print(f"{prefix}{c.colorize(message, c.DIM)}")


def print_box(
    content: List[str],
    title: Optional[str] = None,
    width: int = SEPARATOR_WIDTH,
    style: str = "single",
) -> None:
    """Print content in a box"""
    c = Colors

    # Box drawing characters (ASCII)
    if style == "double":
        top_left, top_right = "+", "+"
        bottom_left, bottom_right = "+", "+"
        horizontal, vertical = "=", "|"
    else:  # single
        top_left, top_right = "+", "+"
        bottom_left, bottom_right = "+", "+"
        horizontal, vertical = "-", "|"

    # Calculate inner width
    inner_width = width - 4

    # Print top border
    if title:
        title_len = len(title)
        left_pad = (inner_width - title_len - 2) // 2
        right_pad = inner_width - title_len - 2 - left_pad
        top_line = f"{top_left}{horizontal * left_pad} {c.colorize(title, c.BOLD + c.CYAN)} {horizontal * right_pad}{top_right}"
    else:
        top_line = f"{top_left}{horizontal * inner_width}{top_right}"

    safe_print(c.colorize(top_line, c.CYAN))

    # Print content
    for line in content:
        # Wrap long lines
        if len(line) > inner_width:
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= inner_width:
                    current_line += word + " "
                else:
                    safe_print(
                        c.colorize(f"{vertical} ", c.CYAN)
                        + current_line.ljust(inner_width)
                        + c.colorize(f" {vertical}", c.CYAN),
                    )
                    current_line = word + " "
            if current_line:
                safe_print(
                    c.colorize(f"{vertical} ", c.CYAN)
                    + current_line.ljust(inner_width)
                    + c.colorize(f" {vertical}", c.CYAN),
                )
        else:
            safe_print(
                c.colorize(f"{vertical} ", c.CYAN)
                + line.ljust(inner_width)
                + c.colorize(f" {vertical}", c.CYAN),
            )

    # Print bottom border
    bottom_line = f"{bottom_left}{horizontal * inner_width}{bottom_right}"
    safe_print(c.colorize(bottom_line, c.CYAN))
    safe_print()


def ask_input(
    prompt: str,
    default: Optional[str] = None,
    required: bool = True,
) -> str:
    """Ask for user input with optional default"""
    c = Colors

    if default:
        prompt_str = f"{prompt} [{c.colorize(default, c.DIM)}]: "
    else:
        prompt_str = f"{prompt}: "

    while True:
        try:
            value = input(f"  {prompt_str}").strip()

            if not value and default:
                return default

            if not value and required:
                print_warning("This field is required. Please provide a value.")
                continue

            return value
        except (KeyboardInterrupt, EOFError):
            safe_print()
            raise


def ask_choice(
    prompt: str,
    choices: List[str],
    default: Optional[str] = None,
    show_numbers: bool = True,
) -> str:
    """Ask user to choose from a list"""
    c = Colors

    safe_print()
    safe_print(f"  {c.colorize(prompt, c.BOLD)}")
    safe_print()

    # Print choices
    for i, choice in enumerate(choices, 1):
        if show_numbers:
            num = c.colorize(f"{i}.", c.BRIGHT_BLUE)
            if choice == default:
                safe_print(f"    {num} {choice} {c.colorize('(default)', c.DIM + c.GREEN)}")
            else:
                safe_print(f"    {num} {choice}")
        else:
            bullet = c.colorize("•", c.GREEN)
            if choice == default:
                safe_print(f"    {bullet} {choice} {c.colorize('(default)', c.DIM + c.GREEN)}")
            else:
                safe_print(f"    {bullet} {choice}")

    safe_print()

    # Get input
    while True:
        try:
            if default:
                prompt_str = f"  Enter choice (1-{len(choices)}) [{c.colorize(default, c.DIM)}]: "
            else:
                prompt_str = f"  Enter choice (1-{len(choices)}): "

            value = input(prompt_str).strip()

            # Handle default
            if not value and default:
                return default

            # Handle numeric input
            if value.isdigit():
                idx = int(value) - 1
                if 0 <= idx < len(choices):
                    return choices[idx]

            # Handle text input (partial match)
            for choice in choices:
                if choice.lower().startswith(value.lower()):
                    return choice

            print_warning(f"Invalid choice. Please enter a number between 1 and {len(choices)}.")
        except (KeyboardInterrupt, EOFError):
            safe_print()
            raise


def ask_yes_no(
    prompt: str,
    default: Optional[bool] = None,
) -> bool:
    """Ask a yes/no question"""
    c = Colors

    if default is True:
        suffix = f"[{c.colorize('Y', c.BOLD + c.GREEN)}/n]"
    elif default is False:
        suffix = f"[y/{c.colorize('N', c.BOLD + c.RED)}]"
    else:
        suffix = "[y/n]"

    while True:
        try:
            value = input(f"  {prompt} {suffix}: ").strip().lower()

            if not value and default is not None:
                return default

            if value in ["y", "yes", "true", "1"]:
                return True
            elif value in ["n", "no", "false", "0"]:
                return False
            else:
                print_warning("Please enter 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            safe_print()
            raise


def ask_multi_choice(
    prompt: str,
    choices: List[str],
    defaults: Optional[List[str]] = None,
    min_selections: int = 0,
    max_selections: Optional[int] = None,
    show_pagination: bool = True,
    page_size: int = 15,
    default_label: str = "detected",
) -> List[str]:
    """Ask user to select multiple items from a list"""
    c = Colors

    safe_print()
    safe_print(f"  {c.colorize(prompt, c.BOLD)}")
    safe_print(
        f"  {c.colorize('Enter numbers to customize selection, or press Enter to use defaults', c.DIM)}",
    )
    commands_text = 'Commands: "more" (next page), "back" (prev page), "all" (show all)'
    safe_print(f"  {c.colorize(commands_text, c.DIM)}")
    safe_print()

    defaults = defaults or []

    # Pagination for long lists
    total_choices = len(choices)
    current_page = 0
    max_pages = (total_choices + page_size - 1) // page_size if show_pagination else 1

    def show_choices(page: int = 0) -> None:
        """Display choices for current page"""
        start_idx = page * page_size if show_pagination else 0
        end_idx = min(start_idx + page_size, total_choices) if show_pagination else total_choices

        # Print choices with checkbox-style markers
        for i in range(start_idx, end_idx):
            choice = choices[i]
            num = c.colorize(f"{i + 1}.", c.BRIGHT_BLUE)
            checkbox = "[✓]" if choice in defaults else "[ ]"
            checkbox_colored = c.colorize(checkbox, c.GREEN if choice in defaults else c.DIM)

            if choice in defaults:
                safe_print(
                    f"    {checkbox_colored} {num} {choice} {c.colorize(f'({default_label})', c.DIM + c.GREEN)}",
                )
            else:
                safe_print(f"    {checkbox_colored} {num} {choice}")

        # Show pagination info
        if show_pagination and max_pages > 1:
            safe_print()
            safe_print(
                f"  {c.colorize(f'Showing {start_idx + 1}-{end_idx} of {total_choices}', c.DIM)}",
            )
            if page < max_pages - 1:
                more_msg = 'Type "more" to see next page'
                safe_print(f"  {c.colorize(more_msg, c.DIM)}")

    # Show first page
    show_choices(current_page)

    safe_print()

    # Get input
    while True:
        try:
            if defaults:
                default_nums = [str(choices.index(d) + 1) for d in defaults if d in choices]
                default_str = ", ".join(default_nums)
                prompt_str = f"  Enter choices [{c.colorize(default_str, c.DIM)}]: "
            else:
                prompt_str = "  Enter choices: "

            value = input(prompt_str).strip().lower()

            # Handle pagination commands
            if value == "more" and current_page < max_pages - 1:
                current_page += 1
                safe_print()
                show_choices(current_page)
                safe_print()
                continue
            elif value == "back" and current_page > 0:
                current_page -= 1
                safe_print()
                show_choices(current_page)
                safe_print()
                continue
            elif value == "all":
                # Show all choices at once
                safe_print()
                for i, choice in enumerate(choices, 1):
                    num = c.colorize(f"{i}.", c.BRIGHT_BLUE)
                    checkbox = "[✓]" if choice in defaults else "[ ]"
                    checkbox_colored = c.colorize(
                        checkbox,
                        c.GREEN if choice in defaults else c.DIM,
                    )
                    marker = (
                        c.colorize(f"({default_label})", c.DIM + c.GREEN)
                        if choice in defaults
                        else ""
                    )
                    safe_print(f"    {checkbox_colored} {num} {choice} {marker}")
                safe_print()
                continue

            # Handle default
            if not value and defaults:
                return defaults

            # Parse input
            selected_indices = set()
            for part in value.replace(",", " ").split():
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(choices):
                        selected_indices.add(idx)

            selected = [choices[i] for i in sorted(selected_indices)]

            # Validate selection count
            if len(selected) < min_selections:
                print_warning(f"Please select at least {min_selections} items.")
                continue

            if max_selections and len(selected) > max_selections:
                print_warning(f"Please select at most {max_selections} items.")
                continue

            return selected
        except (KeyboardInterrupt, EOFError):
            safe_print()
            raise


def clear_screen() -> None:
    """Clear the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def pause(message: str = "Press Enter to continue...") -> None:
    """Pause and wait for user input"""
    c = Colors
    try:
        input(f"\n  {c.colorize(message, c.DIM)}")
    except (KeyboardInterrupt, EOFError):
        safe_print()
        raise

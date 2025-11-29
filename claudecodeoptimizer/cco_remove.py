"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import re
import subprocess
import sys

from .config import (
    CCO_MARKER_PATTERNS,
    CLAUDE_DIR,
    SUBPROCESS_TIMEOUT,
    get_cco_agents,
    get_cco_commands,
)


def detect_install_method() -> str | None:
    """Detect pip/pipx/uv installation."""
    for cmd, args in [
        ("pipx", ["list"]),
        ("uv", ["tool", "list"]),
        ("pip", ["show", "claudecodeoptimizer"]),
    ]:
        try:
            result = subprocess.run(
                [cmd] + args, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT
            )
            if "claudecodeoptimizer" in result.stdout:
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return None


def list_cco_files() -> dict[str, list[str]]:
    """List CCO files in ~/.claude/ by category."""
    files: dict[str, list[str]] = {"commands": [], "agents": []}
    files["commands"] = sorted(f.name for f in get_cco_commands())
    files["agents"] = sorted(f.name for f in get_cco_agents())
    return files


def has_claude_md_standards() -> list[str]:
    """Check which CCO sections exist in CLAUDE.md."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []
    content = claude_md.read_text(encoding="utf-8")
    sections = []
    if "<!-- CCO_STANDARDS_START -->" in content:
        sections.append("CCO Standards")
    return sections


def remove_cco_files(verbose: bool = True) -> dict[str, int]:
    """Remove CCO files with detailed output."""
    removed = {"commands": 0, "agents": 0}

    # Commands
    for f in get_cco_commands():
        f.unlink()
        removed["commands"] += 1
        if verbose:
            print(f"  - {f.name}")

    # Agents
    for f in get_cco_agents():
        f.unlink()
        removed["agents"] += 1
        if verbose:
            print(f"  - {f.name}")

    return removed


def remove_claude_md_standards(verbose: bool = True) -> list[str]:
    """Remove CCO standards from CLAUDE.md with detailed output."""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if not claude_md.exists():
        return []

    content = claude_md.read_text(encoding="utf-8")
    removed = []

    # Remove CCO standards marker
    pattern, flags = CCO_MARKER_PATTERNS["standards"]
    if re.search(pattern, content, flags=flags):
        content = re.sub(pattern, "", content, flags=flags)
        removed.append("CCO Standards")

    if removed:
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md.write_text(content, encoding="utf-8")
        if verbose:
            for section in removed:
                print(f"  - {section}")

    return removed


def uninstall_package(method: str) -> bool:
    """Uninstall CCO package."""
    cmds = {
        "pipx": ["pipx", "uninstall", "claudecodeoptimizer"],
        "uv": ["uv", "tool", "uninstall", "claudecodeoptimizer"],
        "pip": ["pip", "uninstall", "-y", "claudecodeoptimizer"],
    }
    try:
        result = subprocess.run(cmds[method], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def main() -> int:
    """CLI entry point."""
    try:
        method = detect_install_method()
        files = list_cco_files()
        standards = has_claude_md_standards()
        total_files = sum(len(f) for f in files.values())

        if not method and total_files == 0 and not standards:
            print("CCO is not installed.")
            return 0

        # Show what will be removed
        print("\n" + "=" * 50)
        print("CCO Uninstall")
        print("=" * 50)
        print(f"\nLocation: {CLAUDE_DIR}\n")

        if method:
            print("Package:")
            print(f"  claudecodeoptimizer ({method})")
            print()

        # Print file categories
        categories = [
            ("Commands", files["commands"]),
            ("Agents", files["agents"]),
            ("CLAUDE.md sections", standards),
        ]
        for title, items in categories:
            if items:
                print(f"{title}:")
                for item in items:
                    print(f"  - {item}")
                print()

        # Summary
        print("=" * 50)
        print("Summary")
        print("=" * 50)
        if method:
            print("  Package:   1")
        print(f"  Commands:  {len(files['commands'])}")
        print(f"  Agents:    {len(files['agents'])}")
        print(f"  Standards: {len(standards)} sections in CLAUDE.md")
        print()

        # Confirmation
        confirm = input("Remove all CCO components? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return 0

        print()

        # Remove package
        if method:
            print("Removing package...")
            if uninstall_package(method):
                print("  Package removed")
            else:
                print("  Failed to remove package")
            print()

        # Remove files
        if total_files > 0:
            print("Removing files...")
            remove_cco_files()
            print()

        # Remove standards
        if standards:
            print("Removing CLAUDE.md sections...")
            remove_claude_md_standards()
            print()

        print("=" * 50)
        print("CCO removed successfully.")
        print("=" * 50)
        print()
        return 0

    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

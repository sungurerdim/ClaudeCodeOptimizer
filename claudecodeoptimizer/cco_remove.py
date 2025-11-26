"""CCO Remove - Uninstall CCO files from ~/.claude/"""

import re
import subprocess
import sys

from .config import AGENTS_DIR, CLAUDE_DIR, COMMANDS_DIR


def detect_install_method() -> str | None:
    """Detect pip/pipx/uv installation."""
    for cmd, args in [
        ("pipx", ["list"]),
        ("uv", ["tool", "list"]),
        ("pip", ["show", "claudecodeoptimizer"]),
    ]:
        try:
            result = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=5)
            if "claudecodeoptimizer" in result.stdout:
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return None


def count_cco_files() -> dict[str, int]:
    """Count CCO files in ~/.claude/"""
    counts = {"agents": 0, "commands": 0, "templates": 0}
    if AGENTS_DIR.exists():
        counts["agents"] = sum(1 for _ in AGENTS_DIR.glob("cco-*.md"))
    if COMMANDS_DIR.exists():
        counts["commands"] = sum(1 for _ in COMMANDS_DIR.glob("cco-*.md"))
    counts["templates"] = sum(1 for _ in CLAUDE_DIR.glob("*.cco"))
    return counts


def remove_cco_files() -> int:
    """Remove CCO files, return count deleted."""
    deleted = 0
    for pattern, path in [
        ("cco-*.md", AGENTS_DIR),
        ("cco-*.md", COMMANDS_DIR),
        ("*.cco", CLAUDE_DIR),
    ]:
        if path.exists():
            for f in path.glob(pattern):
                f.unlink()
                deleted += 1

    # Clean CLAUDE.md markers
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        content = re.sub(
            r"<!-- CCO_RULES_START -->.*?<!-- CCO_RULES_END -->\n?", "", content, flags=re.DOTALL
        )
        content = re.sub(
            r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?",
            "",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(r"\n{3,}", "\n\n", content)
        claude_md.write_text(content, encoding="utf-8")

    return deleted


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
        counts = count_cco_files()
        total = sum(counts.values())

        if not method and total == 0:
            print("CCO is not installed.")
            return 0

        # Show what will be removed
        print("\nCCO Uninstall")
        print("-" * 40)
        if method:
            print(f"Package: claudecodeoptimizer ({method})")
        if total > 0:
            print(f"Files: {total} in ~/.claude/")
        print()

        # Simple confirmation
        confirm = input("Remove CCO? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return 0

        # Remove
        if method:
            print("Removing package...")
            if uninstall_package(method):
                print("  Package removed")
            else:
                print("  Failed to remove package")

        if total > 0:
            deleted = remove_cco_files()
            print(f"  Removed {deleted} files")

        print("\nCCO removed.")
        return 0

    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

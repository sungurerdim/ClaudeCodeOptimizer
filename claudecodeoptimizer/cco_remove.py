"""
CCO Remove - Complete uninstallation

Safely removes CCO package and global ~/.claude/ directory.
"""

import re
import subprocess
import sys
from pathlib import Path

from .config import get_claude_dir


def detect_package_install() -> str | None:
    """
    Detect how CCO was installed.

    Returns:
        Installation method ('pip', 'pipx', 'uv') or None
    """
    # Check pipx
    try:
        result = subprocess.run(["pipx", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "claudecodeoptimizer" in result.stdout:
            return "pipx"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check uv
    try:
        result = subprocess.run(["uv", "tool", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "claudecodeoptimizer" in result.stdout:
            return "uv"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check pip
    try:
        result = subprocess.run(
            ["pip", "show", "claudecodeoptimizer"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return "pip"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return None


def count_cco_files(claude_dir: Path) -> dict[str, int]:
    """
    Count CCO files in ~/.claude/

    Returns:
        Dictionary with file counts per category
    """
    counts = {
        "agents": 0,
        "commands": 0,
        "skills": 0,
        "principles": 0,
        "principles_cco_u": 0,
        "principles_cco_c": 0,
        "templates": 0,
        "standards": 0,
    }

    if not claude_dir.exists():
        return counts

    # Count agents
    agents_dir = claude_dir / "agents"
    if agents_dir.exists():
        counts["agents"] = sum(1 for _ in agents_dir.glob("cco-*.md"))

    # Count commands
    commands_dir = claude_dir / "commands"
    if commands_dir.exists():
        counts["commands"] = sum(1 for _ in commands_dir.glob("cco-*.md"))

    # Count skills
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        counts["skills"] = sum(1 for _ in skills_dir.glob("cco-skill-*.md"))

    # Count principles - single pass instead of 4 iterations over list
    principles_dir = claude_dir / "principles"
    if principles_dir.exists():
        for p in principles_dir.glob("*.md"):
            if p.name == "PRINCIPLES.md":
                continue
            counts["principles"] += 1
            # Check prefix in single pass (O(n) vs O(4n))
            if p.name.startswith("cco-principle-u-"):
                counts["principles_cco_u"] += 1
            elif p.name.startswith("cco-principle-c-"):
                counts["principles_cco_c"] += 1

    # Count templates
    # Count standards (cco-*.md)
    counts["standards"] = sum(
        1
        for f in claude_dir.glob("cco-*.md")
        if f.name in ("cco-standards.md", "cco-patterns.md", "cco-tech-detection.md")
    )
    counts["templates"] = sum(1 for _ in claude_dir.glob("*.cco"))

    return counts


def get_package_location() -> str | None:
    """Get CCO package installation location."""
    try:
        result = subprocess.run(
            ["pip", "show", "claudecodeoptimizer"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Location:"):
                    return line.split(":", 1)[1].strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def show_removal_preview(
    install_method: str | None, package_location: str | None, counts: dict[str, int]
) -> None:
    """Show what will be deleted."""
    print("=" * 60)
    print("CCO UNINSTALL - PREVIEW")
    print("=" * 60)
    print()
    print("The following will be PERMANENTLY DELETED:")
    print()

    if install_method:
        print("PACKAGE:")
        print(f"  • claudecodeoptimizer (installed via {install_method})")
        if package_location:
            print(f"    Location: {package_location}")
        print()

    total_files = sum(counts.values())
    if total_files > 0:
        print("-" * 60)
        print("GLOBAL DIRECTORY (~/.claude/)")
        print("-" * 60)
        print()
        if counts["agents"] > 0:
            print(f"  • Agents: {counts['agents']} files")
        if counts["commands"] > 0:
            print(f"  • Commands: {counts['commands']} files")
        if counts["skills"] > 0:
            print(f"  • Skills: {counts['skills']} files")
        if counts["principles"] > 0:
            print(f"  • Principles: {counts['principles']} files")
            print(f"    - cco-principle-u-*: {counts['principles_cco_u']} (Universal)")
            print(f"    - cco-principle-c-*: {counts['principles_cco_c']} (Claude)")
        if counts["templates"] > 0:
            print(f"  • Templates: {counts['templates']} files")
            print("    - settings.json.cco (Claude Code configuration)")
            print("    - statusline.js.cco (Status line script)")
        print()
        print("-" * 60)
        print(f"  Total: {total_files} files in ~/.claude/")
        print("-" * 60)
        print()

    print("CLAUDE.MD:")
    print("  • CCO principle markers will be removed from ~/.claude/CLAUDE.md")
    print("  • Your other content in CLAUDE.md will be preserved")
    print()
    print("PROJECT FILES:")
    print("  • NONE - Zero-pollution architecture")
    print("  • Your project files are NOT affected")
    print()
    print("WHAT WILL NOT BE DELETED:")
    print("  • Your code and project files")
    print("  • Git history")
    print("  • Other Python packages")
    print("  • IDE configurations")
    print("  • Non-CCO files in ~/.claude/ (preserved)")
    print("  • Folder structure in ~/.claude/ (preserved)")
    print()
    print("=" * 60)
    print()


def confirm_deletion() -> bool:
    """Ask user for deletion confirmation."""
    print("⚠️  PERMANENT DELETION: This will remove ALL CCO files.")
    print("⚠️  This action CANNOT be undone.")
    print()
    response = input("Type 'yes-delete-cco' to confirm deletion: ").strip()
    return response == "yes-delete-cco"


def remove_package(install_method: str) -> bool:
    """
    Uninstall CCO package.

    Returns:
        True if successful, False otherwise
    """
    try:
        if install_method == "pipx":
            result = subprocess.run(
                ["pipx", "uninstall", "claudecodeoptimizer"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        elif install_method == "uv":
            result = subprocess.run(
                ["uv", "tool", "uninstall", "claudecodeoptimizer"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        else:  # pip
            result = subprocess.run(
                ["pip", "uninstall", "-y", "claudecodeoptimizer"],
                capture_output=True,
                text=True,
                timeout=30,
            )

        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"Error uninstalling package: {e}", file=sys.stderr)
        return False


def remove_cco_files(claude_dir: Path) -> dict[str, int]:
    """
    Remove only CCO files, preserving all user content and folders.

    Only removes files with cco-* prefix. Never deletes folders (even empty ones)
    to preserve user's directory structure.
    """
    deleted = {
        "agents": 0,
        "commands": 0,
        "skills": 0,
        "principles": 0,
        "standards": 0,
        "templates": 0,
    }

    if not claude_dir.exists():
        return deleted

    # Remove agents (cco-*.md only, preserve folder)
    agents_dir = claude_dir / "agents"
    if agents_dir.exists():
        for f in agents_dir.glob("cco-*.md"):
            f.unlink()
            deleted["agents"] += 1

    # Remove commands (cco-*.md only, preserve folder)
    commands_dir = claude_dir / "commands"
    if commands_dir.exists():
        for f in commands_dir.glob("cco-*.md"):
            f.unlink()
            deleted["commands"] += 1

    # Remove skills (cco-skill-*.md only, preserve folders)
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        for f in skills_dir.rglob("cco-skill-*.md"):
            f.unlink()
            deleted["skills"] += 1

    # Remove principles (cco-principle-*.md only, preserve folder)
    principles_dir = claude_dir / "principles"
    if principles_dir.exists():
        for f in principles_dir.glob("cco-principle-u-*.md"):
            f.unlink()
            deleted["principles"] += 1
        for f in principles_dir.glob("cco-principle-c-*.md"):
            f.unlink()
            deleted["principles"] += 1

    # Remove standards (cco-*.md in root only)
    for f in claude_dir.glob("cco-*.md"):
        if f.is_file():
            f.unlink()
            deleted["standards"] += 1

    # Remove templates (*.cco files only)
    for f in claude_dir.glob("*.cco"):
        f.unlink()
        deleted["templates"] += 1

    _remove_claude_md_markers(claude_dir)
    return deleted


def _remove_claude_md_markers(claude_dir: Path) -> None:
    """
    Remove CCO markers from CLAUDE.md while preserving all user content.

    Only removes the CCO_PRINCIPLES_START/END markers and content between them.
    Never deletes the file - preserves user's other settings and content.
    """
    claude_md = claude_dir / "CLAUDE.md"
    if not claude_md.exists():
        return

    file_content = claude_md.read_text(encoding="utf-8")

    # Only remove CCO markers and content between them
    # Pattern matches: <!-- CCO_PRINCIPLES_START --> ... <!-- CCO_PRINCIPLES_END --> + optional newlines
    pattern = r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?"
    new_content = re.sub(pattern, "", file_content, flags=re.DOTALL)

    # Clean up excessive blank lines (more than 2 consecutive) but preserve structure
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    # Write back content (even if empty - never delete user's CLAUDE.md)
    claude_md.write_text(new_content, encoding="utf-8")


def verify_removal(install_method: str | None) -> dict[str, bool]:
    """
    Verify CCO was removed completely.

    Returns:
        Dictionary with verification results
    """
    results = {
        "package_removed": True,
        "files_removed": True,
    }

    # Check package
    if install_method:
        check_result = detect_package_install()
        results["package_removed"] = check_result is None

    # Check CCO files
    claude_dir = get_claude_dir()
    if claude_dir.exists():
        cco_files = count_cco_files(claude_dir)
        total = sum(cco_files.values())
        results["files_removed"] = total == 0

    return results


def main() -> int:
    """CLI entry point for cco-remove."""
    try:
        claude_dir = get_claude_dir()

        # Detect installation
        install_method = detect_package_install()
        package_location = get_package_location() if install_method else None
        counts = count_cco_files(claude_dir)

        # Check if anything to remove
        total_files = sum(counts.values())
        if not install_method and total_files == 0:
            print("[INFO] CCO is not installed")
            print()
            print("Nothing to remove:")
            print("  • Package: not found")
            print(f"  • Directory: {claude_dir} has no CCO files")
            return 0

        # Show preview
        show_removal_preview(install_method, package_location, counts)

        # Confirm
        if not confirm_deletion():
            print()
            print("[CANCELLED] CCO removal cancelled by user")
            return 0

        print()
        print("Removing CCO...")
        print()

        # Remove package
        package_removed = True
        if install_method:
            print(f"Uninstalling package ({install_method})...")
            package_removed = remove_package(install_method)
            if package_removed:
                print("  ✓ Package uninstalled")
            else:
                print("  ✗ Failed to uninstall package")

        # Remove CCO files (selective, preserves user content)
        files_removed = True
        deleted = {
            "agents": 0,
            "commands": 0,
            "skills": 0,
            "principles": 0,
            "standards": 0,
            "templates": 0,
        }
        if total_files > 0:
            print("Removing CCO files...")
            deleted = remove_cco_files(claude_dir)
            total_deleted = sum(deleted.values())
            if total_deleted > 0:
                print(f"  [OK] Removed {total_deleted} CCO files")
            files_removed = total_deleted == total_files

        # Verify
        print()
        print("Verifying removal...")
        results = verify_removal(install_method)

        if results["package_removed"] and results.get("files_removed", files_removed):
            print()
            print("=" * 60)
            print("CCO UNINSTALL COMPLETE")
            print("=" * 60)
            print()
            print("REMOVED:")
            if install_method:
                print(f"  ✓ Package: claudecodeoptimizer ({install_method})")
            if total_files > 0:
                if deleted["agents"] > 0:
                    print(f"  [OK] Agents: {deleted['agents']} files")
                if deleted["commands"] > 0:
                    print(f"  [OK] Commands: {deleted['commands']} files")
                if deleted["skills"] > 0:
                    print(f"  [OK] Skills: {deleted['skills']} files")
                if deleted["principles"] > 0:
                    print(f"  [OK] Principles: {deleted['principles']} files")
                if deleted["standards"] > 0:
                    print(f"  [OK] Standards: {deleted['standards']} files")
                if deleted["templates"] > 0:
                    print(f"  [OK] Templates: {deleted['templates']} files")
                print("  [OK] CLAUDE.md markers removed")
            print()
            print("-" * 60)
            print(f"  Total: {sum(deleted.values())} files deleted")
            print("-" * 60)
            print()
            print("CCO has been completely removed from your system.")
            print("Your non-CCO files in ~/.claude/ were preserved.")
            print()
            print("TO REINSTALL:")
            print("  pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git")
            print("  cco-setup")
            return 0
        else:
            print()
            print("[ERROR] Removal incomplete")
            if not results["package_removed"]:
                print("  ✗ Package still installed")
            if not results.get("files_removed", files_removed):
                print("  [FAIL] Some CCO files still present in ~/.claude/")
            return 1

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

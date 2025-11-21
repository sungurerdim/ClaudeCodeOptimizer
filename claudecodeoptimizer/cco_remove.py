"""
CCO Remove - Complete uninstallation

Safely removes CCO package and global ~/.claude/ directory.
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_claude_dir() -> Path:
    """Get ~/.claude/ directory path."""
    return Path.home() / ".claude"


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
        "principles_u": 0,
        "principles_c": 0,
        "principles_p": 0,
        "templates": 0,
    }

    if not claude_dir.exists():
        return counts

    # Count agents
    agents_dir = claude_dir / "agents"
    if agents_dir.exists():
        counts["agents"] = len(list(agents_dir.glob("cco-*.md")))

    # Count commands
    commands_dir = claude_dir / "commands"
    if commands_dir.exists():
        counts["commands"] = len(list(commands_dir.glob("cco-*.md")))

    # Count skills
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        counts["skills"] = len(list(skills_dir.glob("cco-skill-*.md")))

    # Count principles
    principles_dir = claude_dir / "principles"
    if principles_dir.exists():
        all_principles = list(principles_dir.glob("*.md"))
        # Exclude PRINCIPLES.md summary
        all_principles = [p for p in all_principles if p.name != "PRINCIPLES.md"]
        counts["principles"] = len(all_principles)
        counts["principles_u"] = len([p for p in all_principles if p.name.startswith("U_")])
        counts["principles_c"] = len([p for p in all_principles if p.name.startswith("C_")])
        counts["principles_p"] = len([p for p in all_principles if p.name.startswith("P_")])

    # Count templates
    counts["templates"] = len(list(claude_dir.glob("*.cco")))

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
            print(f"    - U_*.md: {counts['principles_u']} (Universal principles)")
            print(f"    - C_*.md: {counts['principles_c']} (Claude guidelines)")
            print(f"    - P_*.md: {counts['principles_p']} (Project principles)")
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


def backup_claude_dir(claude_dir: Path) -> Path | None:
    """
    Create backup of ~/.claude/ directory.

    Returns:
        Backup path if successful, None otherwise
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = claude_dir.parent / f".claude.backup-{timestamp}"

    try:
        shutil.copytree(claude_dir, backup_path)
        return backup_path
    except Exception as e:
        print(f"Warning: Could not create backup: {e}", file=sys.stderr)
        return None


def remove_claude_dir(claude_dir: Path, create_backup: bool = False) -> tuple[bool, Path | None]:
    """
    Remove ~/.claude/ directory.

    Args:
        claude_dir: Path to ~/.claude/
        create_backup: Whether to create backup before deletion

    Returns:
        (success, backup_path) tuple
    """
    backup_path = None

    if create_backup:
        backup_path = backup_claude_dir(claude_dir)

    try:
        shutil.rmtree(claude_dir)
        return True, backup_path
    except Exception as e:
        print(f"Error removing directory: {e}", file=sys.stderr)
        return False, backup_path


def verify_removal(install_method: str | None) -> dict[str, bool]:
    """
    Verify CCO was removed completely.

    Returns:
        Dictionary with verification results
    """
    results = {
        "package_removed": True,
        "directory_removed": True,
    }

    # Check package
    if install_method:
        check_result = detect_package_install()
        results["package_removed"] = check_result is None

    # Check directory
    claude_dir = get_claude_dir()
    if claude_dir.exists():
        cco_files = count_cco_files(claude_dir)
        total = sum(cco_files.values())
        results["directory_removed"] = total == 0

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

        # Remove directory
        directory_removed = True
        backup_path = None
        if total_files > 0:
            print("Removing global directory...")
            directory_removed, backup_path = remove_claude_dir(claude_dir, create_backup=False)
            if directory_removed:
                print("  ✓ Directory removed")
                if backup_path:
                    print(f"  ✓ Backup created: {backup_path}")
            else:
                print("  ✗ Failed to remove directory")

        # Verify
        print()
        print("Verifying removal...")
        results = verify_removal(install_method)

        if results["package_removed"] and results["directory_removed"]:
            print()
            print("=" * 60)
            print("CCO UNINSTALL COMPLETE")
            print("=" * 60)
            print()
            print("REMOVED:")
            if install_method:
                print(f"  ✓ Package: claudecodeoptimizer ({install_method})")
            if total_files > 0:
                print(f"  ✓ Agents: {counts['agents']} files deleted")
                print(f"  ✓ Commands: {counts['commands']} files deleted")
                print(f"  ✓ Skills: {counts['skills']} files deleted")
                print(f"  ✓ Principles: {counts['principles']} files deleted")
                print(f"  ✓ Templates: {counts['templates']} files deleted")
            print()
            print("-" * 60)
            print(f"  Total: {total_files} files deleted")
            print("-" * 60)
            print()
            print("CCO has been completely removed from your system.")
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
            if not results["directory_removed"]:
                print("  ✗ CCO files still present in ~/.claude/")
            return 1

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

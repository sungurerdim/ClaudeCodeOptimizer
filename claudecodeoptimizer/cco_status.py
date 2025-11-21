"""
CCO Status - Installation health check

Verifies CCO installation and shows available components.
"""

import sys
from pathlib import Path


def get_claude_dir() -> Path:
    """Get ~/.claude/ directory path."""
    return Path.home() / ".claude"


def count_components(claude_dir: Path) -> dict[str, int]:
    """
    Count CCO components in ~/.claude/

    Returns:
        Dictionary with component counts
    """
    counts = {
        "commands": 0,
        "principles": 0,
        "principles_c": 0,
        "principles_u": 0,
        "principles_p": 0,
        "skills": 0,
        "agents": 0,
    }

    if not claude_dir.exists():
        return counts

    # Count commands
    commands_dir = claude_dir / "commands"
    if commands_dir.exists():
        counts["commands"] = len(list(commands_dir.glob("cco-*.md")))

    # Count principles
    principles_dir = claude_dir / "principles"
    if principles_dir.exists():
        all_principles = list(principles_dir.glob("*.md"))
        # Exclude PRINCIPLES.md summary file
        all_principles = [p for p in all_principles if p.name != "PRINCIPLES.md"]
        counts["principles"] = len(all_principles)
        counts["principles_c"] = len([p for p in all_principles if p.name.startswith("C_")])
        counts["principles_u"] = len([p for p in all_principles if p.name.startswith("U_")])
        counts["principles_p"] = len([p for p in all_principles if p.name.startswith("P_")])

    # Count skills
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        counts["skills"] = len(list(skills_dir.glob("cco-skill-*.md")))

    # Count agents
    agents_dir = claude_dir / "agents"
    if agents_dir.exists():
        counts["agents"] = len(list(agents_dir.glob("cco-agent-*.md")))

    return counts


def get_version_info() -> dict[str, str]:
    """Get CCO version and installation info."""
    try:
        from claudecodeoptimizer import __version__

        version = __version__
    except ImportError:
        version = "unknown"

    # Detect installation method
    install_method = "unknown"
    try:
        import subprocess

        # Check pipx
        result = subprocess.run(["pipx", "list"], capture_output=True, text=True, timeout=2)
        if "claudecodeoptimizer" in result.stdout:
            install_method = "pipx"
        else:
            # Check pip
            result = subprocess.run(
                ["pip", "show", "claudecodeoptimizer"], capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                install_method = "pip"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return {
        "version": version,
        "install_method": install_method,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
    }


def check_claude_md(claude_dir: Path) -> bool:
    """Check if CLAUDE.md has CCO principle markers."""
    claude_md = claude_dir / "CLAUDE.md"
    if not claude_md.exists():
        return False

    try:
        content = claude_md.read_text(encoding="utf-8")
        return "CCO_PRINCIPLES_START" in content and "CCO_PRINCIPLES_END" in content
    except Exception:
        return False


def print_status() -> int:
    """
    Print CCO installation status.

    Returns:
        Exit code (0 = success, 1 = not installed, 2 = incomplete)
    """
    claude_dir = get_claude_dir()

    # Check if directory exists
    if not claude_dir.exists():
        print("[ERROR] CCO not installed")
        print()
        print(f"Directory {claude_dir} not found.")
        print()
        print("Install:")
        print("1. pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git")
        print("2. cco-setup")
        return 1

    # Count components
    counts = count_components(claude_dir)
    version_info = get_version_info()
    has_claude_md = check_claude_md(claude_dir)

    # Determine health status
    health = "Good"
    exit_code = 0

    if counts["commands"] == 0 or counts["principles"] == 0:
        health = "Incomplete installation"
        exit_code = 2

    # Print status
    print("# CCO Installation Status")
    print()
    print(f"[{'OK' if exit_code == 0 else 'ERROR'}] Health: {health}")
    print(f"[OK] Location: {claude_dir}")
    print()
    print("---")
    print()
    print("## Components")
    print()
    print(f"**Commands ({counts['commands']} core):**")
    if counts["commands"] > 0:
        print("- Discovery: help, status")
        print("- Critical: audit, fix, generate")
        print("- Productivity: optimize, commit, implement, slim")
        print("- Management: update, remove")
    else:
        print("  [ERROR] No commands found - run cco-setup")
    print()
    print(f"**Principles ({counts['principles']}):**")
    print(f"- {counts['principles_c']} Claude Guidelines (C_*) - Always active")
    print(f"- {counts['principles_u']} Universal (U_*) - Always active")
    print(f"- {counts['principles_p']} Project (P_*) - Progressive loading via skills")
    print()
    print(f"**Skills ({counts['skills']} - Auto-Activate on Demand):**")
    if counts["skills"] > 0:
        print("  Available: security, testing, database, CI/CD, performance, and more")
        print("  Skills auto-activate via Claude's semantic matching")
    else:
        print("  [WARNING] No skills found")
    print()
    print(f"**Agents ({counts['agents']} - Parallel Execution):**")
    if counts["agents"] > 0:
        print("- cco-agent-audit (Haiku - Fast scanning)")
        print("- cco-agent-fix (Sonnet - Accurate fixes)")
        print("- cco-agent-generate (Sonnet - Code generation)")
    else:
        print("  [WARNING] No agents found")
    print()
    print("---")
    print()
    print("## Architecture")
    print()
    print("**Zero Pollution:**")
    print(f"- Global storage: {claude_dir} (all projects share)")
    print("- Project storage: ZERO files created")
    print("- Updates: One command updates all projects")
    print()
    print("**Progressive Loading:**")
    print(
        f"- Always loaded: Baseline principles ({counts['principles_c']} C_ + {counts['principles_u']} U_)"
    )
    print(f"- Auto-activated: {counts['skills']} skills via semantic matching")
    print()
    print("**CLAUDE.md Integration:**")
    if has_claude_md:
        print(f"  [OK] {claude_dir}/CLAUDE.md configured with CCO principles")
    else:
        print(f"  [WARNING] {claude_dir}/CLAUDE.md not configured")
    print()
    print("---")
    print()
    print("## Version Info")
    print()
    print(f"**CCO Version:** {version_info['version']}")
    print(f"**Installation Method:** {version_info['install_method']}")
    print(f"**Python Version:** {version_info['python_version']}")
    print(f"**Platform:** {version_info['platform']}")
    print()
    print("---")
    print()

    if exit_code == 0:
        print("[OK] CCO is ready!")
        print("All components installed and available.")
        print()
        print("Next: /cco-help (command reference) or /cco-audit (project health)")
    else:
        print("[ERROR] Installation incomplete")
        print()
        print("Fix: Run cco-setup to repair installation")

    return exit_code


def main() -> int:
    """CLI entry point for cco-status."""
    try:
        return print_status()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

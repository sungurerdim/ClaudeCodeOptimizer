#!/usr/bin/env python3
"""
ClaudeCodeOptimizer - Quick Remote Installer

Single command installation without git clone.

Usage:
    curl -sSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py | python3

Or:
    python3 -c "$(curl -fsSL https://raw.githubusercontent.com/sungurerdim/ClaudeCodeOptimizer/main/quick-install.py)"

What it does:
    1. Installs directly from GitHub
    2. Runs cco-setup automatically
    3. Verifies installation
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Quick installer from GitHub."""
    print("=" * 60)
    print("ClaudeCodeOptimizer - Quick Install")
    print("=" * 60)

    # Check Python version

    print(f"\n[OK] Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check if package is already installed
    print("\n> Checking existing installation...")
    check_result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "claudecodeoptimizer"],
        capture_output=True,
        text=True,
    )

    if check_result.returncode == 0:
        # Package is installed, remove it first
        print("[NOTICE] Existing installation found, removing...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "uninstall", "-y", "claudecodeoptimizer"],
                check=True,
                capture_output=True,
                text=True,
            )
            print("[OK] Previous installation removed")
        except subprocess.CalledProcessError as e:
            print("[ERROR] Removal failed:")
            print(e.stderr)
            return 1

    # Install directly from GitHub
    github_url = "git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git"

    print("\n> Installing from GitHub...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", github_url],
            check=True,
            capture_output=True,
            text=True,
        )
        print("[OK] Package installed")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Installation failed:")
        print(e.stderr)
        return 1

    # Run setup
    print("\n> Setting up ~/.claude/ directory...")
    try:
        subprocess.run(
            [sys.executable, "-m", "claudecodeoptimizer.install_hook"],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("[ERROR] Setup failed")
        print("\nTry manually: cco-setup")
        return 1

    # Verify
    print("\n" + "=" * 60)
    print("Verifying installation...")
    print("=" * 60)

    claude_dir = Path.home() / ".claude"
    commands_dir = claude_dir / "commands"
    agents_dir = claude_dir / "agents"

    cmd_count = len(list(commands_dir.glob("cco-*.md"))) if commands_dir.exists() else 0
    agent_count = len(list(agents_dir.glob("cco-*.md"))) if agents_dir.exists() else 0

    print(f"\n[OK] Commands: {cmd_count}")
    print(f"[OK] Agents: {agent_count}")
    print(f"[OK] Location: {claude_dir}")

    print("\n" + "=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Open/Restart Claude Code")
    print("  2. Try: /cco-help")
    print("=" * 60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

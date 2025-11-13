# Installation Guide

## Requirements

- **Python 3.11+** - Core runtime
- **Claude Code** - Required for all features (commands, UI, agents)
- **Git** - Recommended for workflow features and history analysis

## Installation

### Global Installation

```bash
# From PyPI (coming soon)
pip install claudecodeoptimizer

# From source (development)
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer
cd ClaudeCodeOptimizer
pip install -e ".[dev]"
```

**What happens during installation:**

1. Installs Python package from PyPI
2. Deploys principles, guides, commands, and skills from `content/` to `~/.cco/`:
   - `commands/` - 28 command files (from content/commands/)
   - `principles/` - 83 principle files (14 universal + 69 project-specific) (from content/principles/)
   - `guides/` - 5 comprehensive guides (from content/guides/)
   - `skills/` - 23 skill files (18 language-specific + 5 cross-language) (from content/skills/)
   - `agents/` - 3 task-specific agents (from content/agents/)
   - `templates/` - Optional template files (reference only):
     - `settings.json.template` - Claude Code settings example
     - Other project templates (.editorconfig, .pre-commit-config.yaml, etc.)
   - `projects/` - Project registry directory (empty initially)
3. Creates `config.json` with global configuration
4. Creates `.installed` marker file
5. Adds `/cco-init` and `/cco-remove` to global `~/.claude/commands/`
6. CCO now available in **all Claude Code sessions**

## Project Initialization

### Quick Start

From within any Claude Code session:

```bash
# Quick mode (AI auto-detects, 10 seconds)
/cco-init

# Interactive mode (user confirms each decision, 2-5 minutes)
/cco-init --mode=interactive
```

### What Happens During Initialization

**Phase 1: Analysis & Detection**

1. Reads project files (README, existing CLAUDE.md, package files, config files)
2. Analyzes git history (if available) for team size and activity patterns
3. Detects system context (OS, shell, locale)
4. Detects project characteristics:
   - Languages (Python, JavaScript/TypeScript, Go, Rust, etc.)
   - Frameworks (FastAPI, Django, React, Next.js, etc.)
   - Tools (Docker, pytest, eslint, GitHub Actions, etc.)
   - Project type (API, web app, CLI, library, etc.)
   - Team size (solo, small, medium, large, enterprise)
   - Maturity level (prototype, MVP, beta, production, legacy)

**Phase 2: Decision & Selection**

Interactive mode: user confirms; Quick mode: auto-decided

5. Determines development philosophy (move fast, balanced, quality-first)
6. Selects testing strategy (basic, standard, comprehensive)
7. Selects security level (basic, standard, strict, paranoid)
8. Selects git workflow (main-only, GitHub Flow, Git Flow)
9. Selects documentation level (minimal, standard, comprehensive)
10. Chooses applicable principles from 83 total (14 universal always + 20-40 project-specific = 34-54 total)
11. Chooses relevant commands from 28 available (typically 8-15 selected)
12. Chooses relevant guides (verification, security, performance, etc.)
13. Chooses language-specific skills based on detected languages

**Phase 3: File Generation**

14. Creates `.claude/` directory structure using preference order (symlink → hardlink → copy):
    - `.claude/principles/` - Links to principles:
      - All universal principles (U001-U014, 14 files, always)
      - Selected project principles (P001-P069, 20-40 files, AI-selected)
    - `.claude/commands/` - Links to selected global commands (8-15 from 28 available)
    - `.claude/guides/` - Links to relevant guides
    - `.claude/skills/` - Links to language skills
    - `.claude/agents/` - Links to task agents (if any)
15. Generates/updates `CLAUDE.md`:
    - If no existing CLAUDE.md: Creates minimal guide with principle references
    - If existing CLAUDE.md: Appends CCO section (preserves existing content)
    - No user approval needed (append-only, uninstall-safe)
16. Reference: see `~/.cco/templates/settings.json.template` for Claude Code settings example (optional, not deployed)
17. Updates `.gitignore` to exclude CCO-generated temp files (if applicable)

**Phase 4: Registration**

18. Creates project registry at `~/.cco/projects/<project-name>.json` with:
    - Detection results
    - Selected principles (universal + project-specific), commands, guides, skills
    - Command overrides (for dynamic loading)
    - Wizard mode used
    - Initialization timestamp
19. Displays completion summary with next steps

## Platform-Specific Notes

### Windows

#### Linking Strategy

CCO uses a **preference order** when creating links: symlink → hardlink → copy.

> **See**: [Architecture → Linking Strategy](architecture.md#linking-strategy) for details

#### Recommended Setup

**Option 1: Use WSL2** (Windows Subsystem for Linux) - Best experience:

```bash
# Install WSL2 (PowerShell as Admin)
wsl --install

# Install Ubuntu
wsl --install -d Ubuntu

# Use CCO inside WSL
cd /mnt/d/GitHub/YourProject
pip install claudecodeoptimizer
/cco-init
```

**Option 2: Native Windows with Developer Mode:**

- Open Settings → Update & Security → For Developers
- Enable "Developer Mode"
- Restart if prompted
- CCO can now create symlinks

#### Path Handling

- Windows paths (`D:\GitHub\project`) work correctly
- Git commands handle forward slashes automatically
- Spaces in paths supported

#### Known Limitations

- **Network drives:** Symlinks often fail, CCO uses copies automatically
- **OneDrive/Dropbox:** Symlinks may not sync (keep `~/.cco/` local)
- **Antivirus:** May block symlinks (whitelist `~/.cco/`)

### macOS / Linux

Full symlink support out of the box - no special setup needed.

```bash
pip install claudecodeoptimizer
/cco-init
```

**Storage:** Global at `~/.cco/`, project at `.claude/` (symlinks to global)

### Network Drives & Cloud Storage

- **Network drives (NAS, SMB, NFS):** Symlinks may fail, CCO falls back to copies automatically. Use local drive for `~/.cco/`.
- **Cloud storage (OneDrive, Dropbox, Google Drive):** Keep `~/.cco/` local, projects can be in cloud folders. Each device runs `/cco-init` separately.

### Troubleshooting

#### "Permission denied" creating symlinks (Windows)

```bash
# Solution 1: Enable Developer Mode (see Windows section above)
# Solution 2: Run terminal as Administrator (one time)
# Solution 3: Use WSL2 (recommended)
```

#### Symlinks showing as text files

```bash
# Check if symlink creation succeeded
ls -la .claude/commands/  # Should show -> arrows

# If not, CCO fell back to copies (still works, minor duplication)
```

#### CCO commands not found

```bash
# Ensure global commands installed
ls ~/.claude/commands/cco-*

# If missing, reinstall
pip install --force-reinstall claudecodeoptimizer
```

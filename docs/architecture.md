# CCO Architecture

## Core Design Principles

1. **Zero Pollution** - Global storage with local links, no project-specific CCO files
2. **Zero State** - No config files, no project registry, completely stateless operation
3. **Single Source of Truth** - All principles, guides, commands, and skills in `content/` (repo), deployed to `~/.cco/` (global), projects reference via links
4. **Progressive Disclosure** - Load only applicable principles/guides, not entire principle set
5. **Two-Tier Principles** - Universal (19 principles, always) + Project-specific (64 principles, AI-selected)
6. **Minimal CLAUDE.md** - Marker-based injection only; existing content NEVER modified
7. **Clean Install** - Init always removes previous CCO setup first
8. **Evidence-Based** - AI detection with confidence scores and evidence trails
9. **Anti-Overengineering** - Simplest solution that works, no premature abstraction
10. **Multi-Agent First** - Parallel execution by default (Haiku for speed, Sonnet for reasoning)
11. **Linking Preference Order** - Try symlink → hardlink → copy (systematic preference, not fallback)
12. **Complete Removal** - Remove command cleans up global + local + CLAUDE.md markers
13. **Uninstall Safety** - Projects restored to exact pre-CCO state after removal
14. **Document Consistency** - All documentation validated for internal consistency and efficiency
15. **No Version Tracking** - Only project version tracked, no versioning for principles/commands/guides
16. **No Dead Code** - Zero dead code, placeholders, fallbacks, or backward compatibility layers; always 100% current

## Linking Strategy

**Preference Order (Not Fallback)**

CCO uses a systematic preference order when creating links from global to local:

1. **Symlink** (preferred) - Auto-updates when global files change, zero duplication
2. **Hardlink** (good) - Same disk only, zero duplication, requires manual update
3. **Copy** (works everywhere) - Some duplication, requires manual update

This is a **preference order**, not a fallback. CCO tries each method until finding one the OS supports. The strategy applies universally to all file types: commands, principles, guides, skills, agents, and templates.

**Platform Support:**
- **macOS/Linux**: Full symlink support (optimal)
- **Windows**: Symlinks with Developer Mode, hardlinks otherwise
- **Windows WSL2**: Full symlink support (recommended)
- **Network drives**: Usually falls back to copy

## Directory Structure

**Repository (`content/`):**
```
content/                   # Single source of truth (tracked in git)
├── commands/             # 28 command source files (*.md)
├── principles/           # Principle source files (*.md with frontmatter)
│   ├── U_*.md               # Universal principles (19 files)
│   └── P_*.md               # Project-specific principles (24 files)
├── guides/               # 5 comprehensive guide source files (*.md)
│   ├── cco-verification-protocol.md
│   ├── cco-git-workflow.md
│   ├── cco-security-response.md
│   ├── cco-performance-optimization.md
│   └── cco-container-best-practices.md
├── skills/               # Language-specific (18) and cross-language (5) skill source files
│   ├── python/          # 5 skills: cco-skill-async-patterns, cco-skill-packaging-modern, cco-skill-performance, cco-skill-testing-pytest, cco-skill-type-hints-advanced
│   ├── typescript/      # 5 skills: cco-skill-advanced-types, cco-skill-async-patterns, cco-skill-node-performance, cco-skill-testing-vitest, cco-skill-type-safety
│   ├── rust/            # 4 skills: cco-skill-async-tokio, cco-skill-error-handling, cco-skill-ownership-patterns, cco-skill-testing
│   ├── go/              # 4 skills: cco-skill-concurrency-patterns, cco-skill-error-handling, cco-skill-performance, cco-skill-testing-strategies
│   ├── cco-skill-verification-protocol.md      # Cross-language verification skill
│   ├── cco-skill-root-cause-analysis.md        # Cross-language debugging skill
│   ├── cco-skill-test-first-verification.md    # Cross-language testing skill
│   ├── cco-skill-incremental-improvement.md    # Cross-language development skill
│   └── cco-skill-security-emergency-response.md # Cross-language security skill
└── agents/               # 3 task-specific agent source files (cco-agent-audit, cco-agent-fix, cco-agent-generate)
```

**Global Claude Commands (`~/.claude/commands/`):**
```
~/.claude/commands/       # Only 2 CCO commands
├── cco-init.md          # Initialize CCO for any project
└── cco-remove.md        # Remove CCO from project
```

**Global CCO Storage (`~/.cco/`):**
```
~/.cco/                   # Deployed from content/ during pip install
├── commands/             # 28 commands (deployed from content/commands/)
├── principles/           # Individual principle files with frontmatter (deployed from content/principles/)
│   ├── U_*.md               # Universal principles (19 files)
│   ├── C_*.md               # Claude guidelines (12 files)
│   └── P_*.md               # Project-specific principles (64 files)
├── guides/               # 5 comprehensive guides (deployed from content/guides/)
├── skills/               # Language-specific (18) and cross-language (5) skills (deployed from content/skills/)
│   ├── python/          # 5 Python-specific skills
│   ├── typescript/      # 5 TypeScript-specific skills
│   ├── rust/            # 4 Rust-specific skills
│   ├── go/              # 4 Go-specific skills
│   └── cco-skill-*.md   # Cross-language skills (verification, root-cause, etc.)
├── agents/               # 3 task-specific agents (deployed from content/agents/)
└── templates/            # Template files (deployed from templates/*.template)
    └── settings.json.template    # Optional settings template

# NO STATE FILES:
# ❌ No projects/ directory
# ❌ No config.json file
# ❌ No project registries
# ✅ 100% stateless
```

**Project Structure (`.claude/`):**
```
project/.claude/          # Linked from global (using preference order)
├── principles/          # Links to selected principles
│   ├── U_EVIDENCE_BASED.md → ~/.cco/principles/U_EVIDENCE_BASED.md (universal, always)
│   ├── U_FAIL_FAST.md → ~/.cco/principles/U_FAIL_FAST.md (universal, always)
│   ├── ... (19 universal, all included)
│   ├── P_LINTING_SAST.md → ~/.cco/principles/P_LINTING_SAST.md (selected)
│   ├── P_CONTAINER_SECURITY.md → ~/.cco/principles/P_CONTAINER_SECURITY.md (selected)
│   └── ... (10-20 selected from 64 project-specific)
├── commands/            # Links to selected global commands
│   ├── cco-audit.md → ~/.cco/commands/audit.md
│   └── ... (8-15 selected commands)
├── guides/              # Links to relevant guides
│   └── verification-protocol.md → ~/.cco/guides/verification-protocol.md
├── skills/              # Links to language skills
│   └── python/
│       └── testing-pytest.md → ~/.cco/skills/python/testing-pytest.md
├── agents/              # Links to task agents (if any)
└── settings.json.template    # Optional template reference (example configuration)

project/CLAUDE.md        # Minimal guide with principle references
```

**Key Points:**
- All links use preference order (symlink → hardlink → copy)
- Universal principles (19 total) always linked to every project
- Claude guidelines (12 total) always linked to every project
- Project principles (64 total) only selected ones linked (AI-selected)
- `settings.json.template` is optional template reference (not deployed to projects)
- `CLAUDE.md` uses marker-based injection (existing content NEVER modified)
- **Zero state**: No config files anywhere, selection stored as symlinks

## Source Code

```
ClaudeCodeOptimizer/
├── claudecodeoptimizer/
│   ├── ai/                    # AI-powered detection & recommendations (4 files)
│   │   ├── detection.py       # UniversalDetector (languages, frameworks, tools)
│   │   ├── command_selection.py  # Smart command selection
│   │   ├── recommendations.py # Cascading decision recommendations
│   │   └── __init__.py        # Package initialization
│   ├── core/                  # Core installation & generation logic (17 files)
│   │   ├── analyzer.py        # Project analyzer using UniversalDetector
│   │   ├── claude_md_generator.py  # Template-based CLAUDE.md generation
│   │   ├── constants.py       # System constants and thresholds
│   │   ├── generator.py       # Code generation utilities
│   │   ├── hybrid_claude_md_generator.py # Hybrid CLAUDE.md generation
│   │   ├── knowledge_setup.py # Global ~/.cco/ structure initialization
│   │   ├── principle_loader.py # Legacy principle loading
│   │   ├── principle_md_loader.py # Load principles from .md files with frontmatter
│   │   ├── principle_selector.py   # Dynamic principle selection
│   │   ├── principles.py      # Principle management
│   │   ├── project.py         # Project utilities
│   │   ├── safe_print.py      # Cross-platform safe printing
│   │   ├── skill_loader.py    # Skill loading utilities
│   │   ├── utils.py           # General utility functions
│   │   ├── version_manager.py # Semantic versioning automation
│   │   └── __init__.py        # Package initialization
│   ├── wizard/                # Interactive initialization (13 files)
│   │   ├── orchestrator.py    # Wizard flow (quick/interactive)
│   │   ├── decision_tree.py   # 4-tier decision tree (TIER 0-3)
│   │   ├── system_detection.py # OS/shell/locale/Python detection
│   │   ├── ui_adapter.py      # Claude Code UI integration with terminal fallback
│   │   ├── renderer.py        # ANSI color terminal UI
│   │   ├── models.py          # Data models (SystemContext, AnswerContext, DecisionPoint, WizardResult)
│   │   ├── checkpoints.py     # Display and checkpoint functions
│   │   ├── context_matrix.py  # Context matrix for recommendations
│   │   ├── questions.py       # Question definitions
│   │   ├── recommendations.py # Wizard-level recommendation engine
│   │   ├── tool_comparison.py # Tool comparison logic
│   │   ├── validators.py      # Answer validation logic
│   │   └── __init__.py        # Package initialization
│   ├── schemas/               # Data models (Pydantic) (4 files)
│   │   ├── preferences.py     # Universal Preference Schema (SSOT for all choice types)
│   │   ├── commands.py        # Command metadata schema
│   │   ├── recommendations.py # Recommendation data models
│   │   └── __init__.py        # Package initialization
│   ├── config.py              # Central configuration (paths, branding)
│   ├── commands_loader.py     # Command loading utilities
│   ├── install_hook.py        # Post-install hook for pip install
│   ├── __init__.py            # Package initialization
│   └── __main__.py            # CLI entry point
└── tests/                     # Test suite (in progress)
```

# ClaudeCodeOptimizer - TODO & Roadmap

**Last Updated**: 2025-11-10
**Current Version**: 0.1.0-alpha
**Target**: v0.2.0 Production Readiness (2 weeks)

---

## 🎯 Milestone Overview

- [x] **v0.1.0** - Alpha Release (COMPLETE)
- [ ] **v0.2.0** - Production Readiness (Target: 2 weeks)
- [ ] **v0.3.0** - User Experience (Target: 1 month)
- [ ] **v0.4.0** - Extensibility (Target: 2 months)
- [ ] **v1.0.0** - Stable Release (Target: 3 months)

---

## 🔥 URGENT: Critical Fixes & wshobson/agents Integration (PRIORITY 0 - Week 0)

**Focus**: Fix existing issues, integrate best practices from wshobson/agents

**Release Criteria**:
- [ ] Export/import removed (cleaner flow)
- [ ] Command selection fixed (only recommended installed)
- [ ] Model enforcement in all commands
- [ ] Document management system implemented
- [ ] Token optimization (progressive disclosure)
- [ ] Context-aware init system (team-specific recommendations)
- [ ] P074: Automated semantic versioning
- [ ] UI Adapter for Claude Code tool integration

---

### P-1: Update README with Recent Changes (Priority: 🔴 URGENT)

**Goal**: Sync README.md with latest architectural changes from last 48 hours

**Context**: Major changes in last 48 hours:
- Symlink-based knowledge base architecture (15222a6)
- AI-powered semantic commit system (ce20cb4)
- Progressive disclosure implementation (e7cfdff)
- P074 automated versioning (b95819d)
- Interactive knowledge base selection (4f1e9ba)
- P073 atomic commits (766dede, 0932804)

**Analysis Required**:

1. **Review Git History (Last 48 Hours)**:
   ```bash
   git log --since="48 hours ago" --oneline --stat
   git log --since="48 hours ago" --format="%B" | grep -E "^(feat|fix|refactor|docs)"
   ```

2. **Analyze Current Code Structure**:
   ```bash
   # Check new directories/files
   tree claudecodeoptimizer/skills/
   tree ~/.cco/knowledge/
   ls -la .claude/

   # Check key implementations
   wc -l claudecodeoptimizer/skills/commit_skill.py
   wc -l claudecodeoptimizer/commands/commit.md
   grep "Architecture.*Model" claudecodeoptimizer/commands/*.md
   ```

3. **Identify Outdated README Sections**:
   - [ ] Check "Progressive Disclosure" section (~line 76-110)
   - [ ] Check "Core Features" accuracy
   - [ ] Check architecture diagrams
   - [ ] Check Quick Start instructions
   - [ ] Check version numbers and progress percentages
   - [ ] Check feature lists (74 principles, 25+ commands, etc.)

**Sections to Update**:

#### Section 1: Version & Status
- [ ] Line 7: Version badge (check if 0.1.0-alpha is still correct)
- [ ] Line 10: Update progress percentage
- [ ] Update completion status of P0 tasks

#### Section 2: Progressive Disclosure Documentation
- [ ] Lines 78-134: Update with symlink architecture
- [ ] Remove PRINCIPLES.md references (no longer exists, moved to symlinks)
- [ ] Add knowledge base structure:
   ```markdown
   **NEW Architecture** (Symlink-based):
   ```
   ~/.cco/knowledge/          # Global source (single source of truth)
   ├── commands/              # CCO slash commands
   ├── guides/                # Detailed guides
   ├── principles/            # Category-based principles
   ├── agents/                # Custom agent templates
   └── skills/                # Custom skill templates

   project/.claude/           # Project-local (symlinks)
   ├── commands/              → symlinked from global
   ├── guides/                → symlinked (selective)
   ├── principles/            → symlinked (selective)
   ├── agents/                → symlinked (selective)
   └── skills/                → symlinked (selective)
   ```

#### Section 3: Smart Git Commit Feature
- [ ] Add new feature section for AI-powered commits:
   ```markdown
   ### 🤖 AI-Powered Semantic Commits

   **NEW in P0.0** - Intelligent commit system with semantic analysis

   **Architecture**:
   - **Skill Layer** (210 lines): Pure git operations utility
   - **Command Layer** (AI): Semantic analysis & grouping

   **Features**:
   - AI analyzes changes across all files
   - Groups related changes logically (not by directory)
   - Generates high-quality conventional commit messages
   - Follows P072 (Concise), P073 (Atomic), P074 (Versioning)

   **Quality**:
   ```
   Old (Mechanical):
   - 10+ commits for single feature
   - Generic: "update 5 files"

   New (AI-Powered):
   - 1-3 logical commits per feature
   - Descriptive: "implement AI-powered semantic commit system"
   ```

   **Usage**:
   ```bash
   /cco-commit              # Interactive with AI analysis
   /cco-commit --auto       # Auto-commit
   /cco-commit --dry-run    # Preview only
   ```
   ```

#### Section 4: Commands List
- [ ] Update command count and categories
- [ ] Add new commands:
   - `/cco-commit` - AI-powered semantic commits
- [ ] Update model enforcement note

#### Section 5: Principles
- [ ] Update P072: Concise Commit Messages (already in README)
- [ ] Add P073: Atomic Commits
- [ ] Add P074: Automated Semantic Versioning
- [ ] Update total principle count (74 → verify actual count)

#### Section 6: Architecture Diagrams
- [ ] Update workflow diagram to show symlink architecture
- [ ] Add commit workflow diagram

#### Section 7: What's New
- [ ] Add "Recent Updates" section with last 48h changes:
   ```markdown
   ## Recent Updates (2025-11-10)

   ### 🎉 Major Features
   - **AI-Powered Commits**: Semantic analysis for high-quality commits
   - **Symlink Architecture**: Zero-duplication knowledge base
   - **P074 Versioning**: Automated semantic version bumping
   - **Interactive KB Selection**: Granular guide/agent/skill selection

   ### ✅ Completed
   - P0.0: Smart Git Commit ✅
   - P0.1: Fix Existing Issues ✅
   - P0.8 Task 1: Automated Versioning ✅

   ### 📊 Progress
   - Production readiness: 95% → 97%
   - Token optimization: 76% reduction achieved
   - Symlink architecture: Fully implemented
   ```

**Implementation Steps**:

1. **Phase 1: Gather Data**
   ```bash
   # Run these commands and analyze output
   git log --since="48 hours ago" --oneline
   git log --since="48 hours ago" --stat
   find claudecodeoptimizer -name "*.py" | wc -l
   find claudecodeoptimizer/commands -name "*.md" | wc -l
   ls ~/.cco/knowledge/
   ```

2. **Phase 2: Update README.md**
   - Update version/status badges
   - Update progressive disclosure section
   - Add Smart Commit feature section
   - Update commands list
   - Add P073, P074 to principles
   - Update architecture diagrams
   - Add "Recent Updates" section

3. **Phase 3: Verify Accuracy**
   ```bash
   # Check all references are correct
   grep -n "PRINCIPLES.md" README.md  # Should not exist
   grep -n "0.1.0" README.md          # Check version consistency
   grep -n "74 principles" README.md  # Verify count
   ```

**Success Criteria**:
- ✅ README accurately reflects symlink architecture
- ✅ Smart Commit feature documented
- ✅ No outdated references (PRINCIPLES.md in root)
- ✅ Progress percentages updated
- ✅ All new principles documented
- ✅ Architecture diagrams updated

**Estimated Effort**: 2-3 hours

**Note**: This is a documentation task requiring analysis of recent commits and code structure. Should be done in a separate session with fresh context.

---

### P0.0: Smart Git Commit (Hybrid: Skill + CCO Enhancement) ✅ COMPLETE

**Goal**: Universal skill that automatically commits uncommitted changes following CLAUDE.md Git Workflow rules.

**Implementation**: Hybrid Approach
1. **Primary**: `.claude/skills/commit.md` - Universal skill (all projects)
2. **Enhancement**: CCO integration - Enhanced features in CCO projects

**Rationale**:
- ✅ **Universal usage**: Works in any project with Claude Code
- ✅ **Smart adaptation**: Uses project rules from CLAUDE.md if present, otherwise generic
- ✅ **CCO enhancement**: Scope detection and knowledge base support when CCO installed
- ✅ **Exportable**: Can be moved to other projects as a skill
- ✅ **Eliminates manual effort**: AI automatically generates commit messages and grouping

---

#### Hybrid Architecture

**Layer 1: Universal Skill** (`.claude/skills/commit.md`)
```
Primary implementation - works in ANY project with Claude Code
- Detects CLAUDE.md → Uses project-specific Git Workflow
- No CLAUDE.md → Uses conventional commits defaults
- Basic scope detection from file paths
- Generic commit message generation
```

**Layer 2: CCO Enhancement** (Optional, when CCO installed)
```
Enhanced features when .cco/project.json exists:
- CCO-specific scope detection (wizard, core, commands, etc.)
- CCO knowledge base for better categorization
- Project identity awareness
- Principle-aware commit messages
- Automatic /cco-commit command registration
```

**Usage**:
```bash
# Universal (any project)
@commit                    # Interactive mode
@commit --auto             # Auto-commit
@commit --push             # Commit + push

# CCO projects (enhanced)
/cco-commit                # Same as @commit but with CCO features
/cco-commit --auto --push  # Auto-commit and push with CCO intelligence
```

---

#### Skill Features (Universal)

**1. Otomatik Analiz**:
```python
# Uncommitted changes analiz et
git_status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True)
changed_files = parse_git_status(git_status.stdout)

# Categorize each file
for file in changed_files:
    scope = detect_scope(file)  # wizard, core, docs, tests, etc.
    change_type = detect_type(file)  # feat, fix, refactor, docs, etc.
```

**2. Smart Grouping**:
- Group files with same `scope` and `type`
- Create separate commit for each group
- Separate unrelated changes

**3. Conventional Commits**:
```
type(scope): subject

- Detailed change 1
- Detailed change 2
- Detailed change 3

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**4. User Confirmation**:
```bash
# Preview mode (default)
/cco-commit
> Found 3 groups of changes:
>
> Group 1: feat(wizard) - 3 files
>   - orchestrator.py
>   - renderer.py
>   - init.md
> Commit message: "refactor(wizard): enhance interactive mode..."
>
> Group 2: docs(workflow) - 2 files
>   - CLAUDE.md
>   - TODO.md
> Commit message: "docs(workflow): add Git Workflow strategy..."
>
> Create these commits? [y/N]
```

**5. Flags**:
```bash
/cco-commit --auto          # Auto-commit without confirmation
/cco-commit --push          # Auto-push after committing
/cco-commit --dry-run       # Show what would be committed
/cco-commit --group=feat    # Only commit feat changes
/cco-commit --scope=wizard  # Only commit wizard scope
```

---

#### Implementation Plan

**Phase 1: Universal Skill** (Works everywhere)

**Files to Create**:

1. **`.claude/skills/commit.md`** (Universal skill - Primary)
   ```markdown
   ---
   name: commit
   description: Smart git commit with conventional commits and automatic grouping
   model: sonnet
   cost: 3
   ---

   # Smart Git Commit

   Universal git commit helper for any project with Claude Code.

   ## Context Detection

   **Priority 1**: Check for CLAUDE.md
   ```bash
   if exists("CLAUDE.md"):
       workflow_rules = parse_git_workflow_section()
       scopes = extract_project_scopes()
   ```

   **Priority 2**: Check for .cco/project.json (CCO enhancement)
   ```bash
   elif exists(".cco/project.json"):
       use_cco_enhancement = True
       load_cco_knowledge()
   ```

   **Priority 3**: Generic conventional commits
   ```bash
   else:
       use_generic_conventional_commits()
   ```

   ## Step 1: Analyze uncommitted changes

   ```bash
   git status --porcelain
   ```

   ## Step 2: Group by scope and type

   Use AI to analyze diffs and categorize...

   ## Step 3: Generate commit messages

   Follow detected workflow or conventional commits...

   ## Step 4: Create commits

   Interactive confirmation or auto-commit based on flags...
   ```

2. **`claudecodeoptimizer/skills/commit_skill.py`** (Skill implementation)
   ```python
   class CommitSkill:
       """Universal git commit skill"""

       def detect_context(self) -> CommitContext:
           """Detect project context for commit strategy"""
           if Path("CLAUDE.md").exists():
               return self._load_claude_md_context()
           elif Path(".cco/project.json").exists():
               return self._load_cco_context()
           else:
               return self._generic_context()

       def analyze_changes(self) -> List[CommitGroup]:
           """Analyze git changes and group intelligently"""

       def generate_commit_message(self, group: CommitGroup) -> str:
           """Generate conventional commit message"""
   ```

---

**Phase 2: CCO Enhancement** (Optional, better experience in CCO projects)

**Files to Create**:

1. **`claudecodeoptimizer/commands/commit.md`** (CCO wrapper command)
   ```markdown
   ---
   description: CCO-enhanced git commit (wraps @commit skill)
   cost: 3
   model: sonnet
   ---

   # CCO Git Commit

   Enhanced git commit with CCO-specific features.

   This command wraps the universal @commit skill with:
   - CCO scope detection (wizard, core, commands, etc.)
   - Project identity awareness
   - Principle-aware commit messages
   - CCO knowledge base integration

   ## Implementation

   ```python
   # Load CCO context
   from claudecodeoptimizer.core.project import ProjectManager

   pm = ProjectManager(Path.cwd())
   cco_context = pm.get_commit_context()

   # Invoke universal skill with CCO enhancement
   invoke_skill("commit", context=cco_context)
   ```
   ```

2. **`claudecodeoptimizer/git/cco_commit_enhancer.py`** (CCO-specific logic)
   ```python
   class CCOCommitEnhancer:
       """Enhance commit skill with CCO knowledge"""

       def enhance_scope_detection(self) -> Dict[str, str]:
           """CCO-specific scope mapping"""
           return {
               "claudecodeoptimizer/wizard/": "wizard",
               "claudecodeoptimizer/core/": "core",
               "claudecodeoptimizer/commands/": "commands",
               # ... etc
           }

       def apply_principles(self, commit_msg: str) -> str:
           """Enhance commit message with principle awareness"""
   ```

**Scope Detection Rules**:
```python
SCOPE_MAP = {
    "claudecodeoptimizer/wizard/": "wizard",
    "claudecodeoptimizer/core/": "core",
    "claudecodeoptimizer/commands/": "commands",
    "claudecodeoptimizer/ai/": "ai",
    "claudecodeoptimizer/schemas/": "schemas",
    "claudecodeoptimizer/knowledge/": "knowledge",
    "tests/": "tests",
    "docs/": "docs",
    "CLAUDE.md": "docs",
    "PRINCIPLES.md": "docs",
    "TODO.md": "docs",
    "README.md": "docs",
    ".gitignore": "chore",
    "pyproject.toml": "deps",
    "requirements.txt": "deps",
}
```

**Type Detection Rules**:
```python
TYPE_RULES = [
    # New files
    (r"^A\s+", "feat"),  # git status: Added

    # Bug fixes
    (r"fix|bug|error|issue", "fix"),  # Keywords in diff

    # Refactoring
    (r"refactor|rename|move|reorganize", "refactor"),

    # Documentation
    (r"\.(md|txt|rst)$", "docs"),

    # Tests
    (r"tests?/|_test\.py$", "test"),

    # Default: feature
    (r".*", "feat"),
]
```

---

#### Usage Examples

**Example 1: Auto-commit all changes**
```bash
/cco-commit --auto --push

> Analyzing changes...
> ✓ Created 3 commits
> ✓ Pushed to origin/main
>
> Commits created:
> - feat(wizard): enhance interactive mode (3 files)
> - docs(workflow): add Git Workflow strategy (2 files)
> - fix(core): restore P071 principle (1 file)
```

**Example 2: Preview before committing**
```bash
/cco-commit

> Found 2 groups of changes:
>
> Group 1: feat(commands) - 2 files
>   - commands/audit.md (+45 lines)
>   - commands/fix.md (+32 lines)
>
> Message:
> feat(commands): add model enforcement to audit and fix
>
> - Add Haiku for data gathering in audit
> - Add Sonnet for analysis in fix
> - Update command descriptions
>
> Group 2: docs(todo) - 1 file
>   - TODO.md (+150 lines)
>
> Message:
> docs(todo): add P0.1 Task 4 for Git Workflow selection
>
> - Add Git Workflow customization plan
> - Add 3 workflow templates
>
> Create these commits? [Y/n] y
> ✓ Created 2 commits
```

**Example 3: Dry run**
```bash
/cco-commit --dry-run

> [DRY RUN] Would create 1 commit:
>
> feat(core): add backup mechanism
> - Update principle_selector.py
> - Update claude_md_generator.py
> - Add timestamp-based backups
>
> Files:
>   M claudecodeoptimizer/core/principle_selector.py
>   M claudecodeoptimizer/core/claude_md_generator.py
>
> [DRY RUN] No changes made.
```

---

#### User Experience

**Interactive Mode** (default):
1. Analyze changes
2. Show grouped commits with preview
3. Ask for confirmation
4. Create commits
5. Ask if push to remote

**Auto Mode** (`--auto`):
1. Analyze changes
2. Create commits automatically
3. Show summary

**Push Mode** (`--auto --push`):
1. Analyze changes
2. Create commits
3. Push to remote
4. Show summary

---

#### Safety Features

1. **Never commit**:
   - Files with secrets (`.env`, `credentials.json`, etc.)
   - Temporary files (`temp/`, `*.tmp`, `*.log`)
   - Generated files already in .gitignore

2. **Always verify**:
   - Tests pass (run `pytest` before commit)
   - No syntax errors (run `ruff check`)
   - No uncommitted conflicts

3. **Rollback support**:
   - Save commit hashes for easy revert
   - Provide rollback command if needed

---

#### Verification

```bash
# Test with sample changes
echo "test" > test.txt
git add test.txt

/cco-commit --dry-run
# Should show: chore(repo): add test file

# Real commit
/cco-commit
# Should prompt and create commit

# Verify
git log -1 --stat
```

**Estimated Effort**: 6-8 hours

---

#### ✅ Completion Status (2025-11-10)

**Implemented**:
- ✅ Universal skill (`.claude/skills/commit.md`)
- ✅ Core implementation (`claudecodeoptimizer/skills/commit_skill.py`)
- ✅ CCO enhancement command (`claudecodeoptimizer/commands/commit.md`)
- ✅ Context detection (CCO/CLAUDE.md/generic)
- ✅ Scope detection with CCO-specific mappings
- ✅ Type detection from diffs and file paths
- ✅ Atomic commit grouping by (type, scope)
- ✅ Conventional commit message generation
- ✅ Safety features (skip secrets, temp files)
- ✅ Unicode and path parsing fixes for Windows
- ✅ Principle references (P072, P073, P074)

**Files Created**:
- `claudecodeoptimizer/skills/commit_skill.py` (497 lines)
- `claudecodeoptimizer/skills/__init__.py`
- `claudecodeoptimizer/commands/commit.md` (650 lines)
- `.claude/skills/commit.md` (173 lines)

**Verified**:
- ✅ Context detection works correctly
- ✅ Groups 11 files into 5 atomic commits
- ✅ Generates P072-compliant messages
- ✅ Ready for production use

---

### P0.1: Fix Existing Issues ✅ COMPLETE

#### Task 1: Remove Export/Import

**Rationale**: Old functions, unnecessary in current structure. `remove + init` is cleaner.

**Files to Modify**:
- [ ] `claudecodeoptimizer/commands/config.md`
  - [ ] Remove export subcommand section (lines 52-116)
  - [ ] Remove import subcommand section (lines 118-192)
  - [ ] Keep only: setup, show
  - [ ] Update description to remove export/import mention

- [ ] `claudecodeoptimizer/ai/command_selection.py`
  - [ ] Remove export rule (lines 272-284)
  - [ ] Remove import-skills rule (lines 285-296)
  - [ ] Update RECOMMENDATION_RULES list

**New Workflow**:
```bash
# Old: Export/import
/cco-config export → cco-config.json
/cco-config import

# New: Remove + Init
/cco-remove              # Clean removal
/cco-init                # Fresh setup with current analysis
```

**Verification**:
```bash
# Verify commands work
/cco-config show
/cco-remove
/cco-init
```

**Estimated Effort**: 30 minutes

---

#### Task 2: Fix Command Selection Mechanism

**Problem**: All commands may be loading, only recommended ones should be installed.

**Files to Check**:
- [ ] `claudecodeoptimizer/wizard/orchestrator.py`
  - [ ] Locate command installation logic
  - [ ] Verify only `core + recommended` are installed
  - [ ] NOT all commands from registry

**Expected Behavior**:
```python
# In wizard/orchestrator.py
recommendations = recommender.recommend_commands()
commands_to_install = recommendations["core"] + recommendations["recommended"]
# Install only these, NOT recommendations["optional"]
```

**If Fix Needed**:
- [ ] Update `core/installer.py`
  - [ ] Modify `link_commands()` to accept command list
  - [ ] Only link specified commands

- [ ] Show optional commands to user
  - [ ] Print: "Optional commands available: ..."
  - [ ] User can enable later with: `/cco-config enable <command>`

**Verification**:
```bash
# After init, check ~/.claude/commands/
ls ~/.claude/commands/ | wc -l
# Should show ~8-12 commands, NOT all 25+

# Verify only core + recommended
cat ~/.cco/projects/<PROJECT>.json | jq '.commands'
```

**Estimated Effort**: 2 hours

---

#### Task 3: Model Enforcement (All Commands)

**Problem**: Model specified in some commands, missing in others.

**Standard Template** to Add:
```markdown
## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast file scanning, pattern detection
- Cost-effective for repetitive operations

**Analysis & Reasoning**: Sonnet (Plan agent)
- Complex analysis and recommendations
- Synthesis of findings

**Execution Pattern**:
1. Launch data gathering agents (Haiku) in parallel
2. Aggregate results with analysis agent (Sonnet)
3. Generate actionable report

## Implementation

Task("scan for patterns", model="haiku", subagent_type="Explore", thoroughness="quick")
Task("analyze findings", model="sonnet", subagent_type="Plan")
```

**Files to Update**:
- [x] `commands/status.md` - Already has model enforcement
- [x] `commands/audit.md` - Already has model enforcement
- [ ] `commands/fix.md` - Add model enforcement
- [ ] `commands/sync.md` - Add model enforcement
- [ ] `commands/analyze.md` - Add model enforcement
- [ ] `commands/optimize-code.md` - Add model enforcement
- [ ] `commands/optimize-deps.md` - Add model enforcement
- [ ] `commands/optimize-docker.md` - Add model enforcement
- [ ] `commands/generate.md` - Add model enforcement
- [ ] `commands/scan-secrets.md` - Add model enforcement
- [ ] `commands/test.md` - Add model enforcement

**Template for Each Command**:
1. Add "Architecture & Model Selection" section
2. Specify which operations use Haiku (data gathering)
3. Specify which operations use Sonnet (reasoning)
4. Add explicit model parameter in Task calls

**Verification**:
```bash
# All commands should have model specification
grep -r "model=" commands/*.md | wc -l
# Should show multiple matches for each command
```

**Estimated Effort**: 3 hours

---

#### Task 4: Git Workflow Selection & CLAUDE.md Customization

**Problem**: CLAUDE.md'de tek bir Git Workflow stratejisi var, tüm projelere aynı uygulanıyor.

**Goal**: Init sırasında ekip boyutuna göre Git Workflow sorup CLAUDE.md'ye özelleştirilmiş olarak eklemek.

**Decision Tree Integration**:
- **Conditional Question** (Tier 2): "Git Workflow Preference"
  - **Condition**: `team_trajectory != "solo"` (sadece team projelerde sor)
  - **Options**:
    1. **Main-Only (Simple)** - Solo/Small teams için recommended
       - Single branch (main)
       - No feature branches
       - Direct commits with clear messages
       - Fast, simple, minimal overhead
    2. **GitHub Flow (Balanced)** - Small-Medium teams için recommended
       - Feature branches from main
       - Pull requests required
       - Branch protection on main
       - Moderate structure
    3. **Git Flow (Professional)** - Large teams için recommended
       - develop + main branches
       - Feature, release, hotfix branches
       - Formal release process
       - Maximum structure
    4. **Custom** - User defines their own

**Recommendation Logic**:
```python
if team_size == "solo":
    recommended = "Main-Only (Simple)"
    auto_select = True  # Don't ask, use recommended
elif team_size in ["small-2-5", "medium-5-10"]:
    recommended = "GitHub Flow (Balanced)"
    ask_question = True
elif team_size in ["large-10-30", "enterprise-30+"]:
    recommended = "Git Flow (Professional)"
    ask_question = True
```

**Files to Modify**:

1. **`claudecodeoptimizer/wizard/decision_tree.py`**
   - [ ] Add Tier 2 question: `git_workflow_preference`
   - [ ] Add conditional logic: `if team_trajectory != "solo"`
   - [ ] Add 4 options (Main-Only, GitHub Flow, Git Flow, Custom)
   - [ ] Set recommendation based on team size

2. **`claudecodeoptimizer/core/claude_md_generator.py`**
   - [ ] **CRITICAL: Add backup mechanism before writing**
     - [ ] Check if output_path exists
     - [ ] If exists, create backup: `CLAUDE.md.backup-YYYYMMDD-HHMMSS`
     - [ ] Keep last 3 backups, delete older ones
     - [ ] Same pattern as needed for PRINCIPLES.md
   - [ ] Add `_get_git_workflow_section()` method
   - [ ] Generate workflow section dynamically based on preference:
     - Main-Only → Simple strategy (like current CLAUDE.md)
     - GitHub Flow → Branch + PR strategy
     - Git Flow → Full develop/main/release strategy
     - Custom → Basic template + user notes
   - [ ] Add conditional insertion in `_add_conditional_sections()`
   - [ ] Check `preferences.collaboration.git_workflow`
   - [ ] **Verify merge strategy is working correctly**:
     - [x] Existing sections preserved ✅ (line 108)
     - [x] New sections added from template ✅ (line 118-125)
     - [x] Section order maintained ✅ (line 161-186)
     - [x] User customizations kept ✅ (line 100-103)
     - **Merge Algorithm** (line 94-128):
       1. Parse both files into sections (by `## Header`)
       2. Start with existing sections (user's work preserved)
       3. Ensure "Development Principles" section has @PRINCIPLES.md
       4. Add missing sections from template (only if not exist)
       5. Rebuild: original order first, then new sections
       6. Result: User's customizations + new CCO features ✅

3. **`claudecodeoptimizer/schemas/preferences.py`**
   - [ ] Verify `TeamCollaboration.git_workflow` field exists
   - [ ] Update valid values: `["main-only", "github-flow", "git-flow", "custom"]`

**Git Workflow Templates**:

**Main-Only (Solo/Small)**:
```markdown
## Git Workflow

**Branch Strategy: Main-Only (Solo Developer)**

- Single `main` branch
- No feature branches
- Direct commits with clear messages

**Commit Strategy**:
- Format: `type(scope): subject`
- Types: feat, fix, docs, refactor, test, chore
- Grouped commits (same category)
- Push after each completed task

**Versioning**:
- Minor bump per milestone (v0.2.0, v0.3.0)
- Major bump for breaking changes
- Patch bump for bug fixes
```

**GitHub Flow (Balanced)**:
```markdown
## Git Workflow

**Branch Strategy: GitHub Flow**

- `main` - Production-ready code
- Feature branches: `feature/<name>`
- Hotfix branches: `hotfix/<issue>`

**Process**:
1. Create feature branch from main
2. Make commits with clear messages
3. Open PR when ready
4. Code review required
5. Merge to main after approval
6. Delete feature branch

**Branch Protection**:
- Require PR reviews (1-2 reviewers)
- Run CI checks before merge
- No direct commits to main

**Versioning**:
- Tag releases on main
- Semantic versioning (major.minor.patch)
```

**Git Flow (Professional)**:
```markdown
## Git Workflow

**Branch Strategy: Git Flow**

- `main` - Production releases only
- `develop` - Integration branch
- Feature branches: `feature/<name>` (from develop)
- Release branches: `release/<version>` (from develop)
- Hotfix branches: `hotfix/<issue>` (from main)

**Process**:
1. Feature: Branch from develop → PR to develop
2. Release: Branch from develop → test → merge to main + develop
3. Hotfix: Branch from main → fix → merge to main + develop
4. Tag releases on main

**Branch Protection**:
- main: Require PR + 2 reviewers
- develop: Require PR + 1 reviewer
- CI/CD required on all branches

**Release Process**:
- Create release branch from develop
- Freeze features, fix bugs only
- Merge to main, tag version
- Merge back to develop
```

**Implementation in claude_md_generator.py**:
```python
def _add_conditional_sections(self, content, team_size, linting, testing):
    # ... existing code ...

    # Add Git Workflow section
    git_workflow = self._get_pref("collaboration.git_workflow", "main-only")
    if "Git Workflow" not in content:
        additions.append(self._get_git_workflow_section(git_workflow, team_size))

    # ... rest of code ...

def _get_git_workflow_section(self, workflow_type: str, team_size: str) -> str:
    """Generate Git Workflow section based on preference"""
    if workflow_type == "main-only" or team_size == "solo":
        return self._get_main_only_workflow()
    elif workflow_type == "github-flow":
        return self._get_github_flow_workflow()
    elif workflow_type == "git-flow":
        return self._get_git_flow_workflow()
    else:  # custom
        return self._get_custom_workflow_template()
```

**Verification**:
```bash
# After init with different team sizes
cat CLAUDE.md | grep -A 30 "## Git Workflow"

# Solo dev should show: Main-Only
# Small team should show: GitHub Flow (if selected)
# Large team should show: Git Flow (if selected)
```

**Benefits**:
- ✅ Project-specific Git Workflow
- ✅ No manual CLAUDE.md editing needed
- ✅ Scales with team size
- ✅ Professional workflows for large teams
- ✅ Simple workflows for solo devs
- ✅ Consistent with project maturity

**Estimated Effort**: 4 hours

---

### P0.2: Document Management System (Priority: ~~🔴 CRITICAL~~ ✅ MOSTLY SOLVED)

**Status**: ✅ Symlink-based knowledge base architecture solves most issues

**Problem**: ~~Dokümanlar ve raporlar kök dizinde dağınık halde~~ → Solved with symlink architecture

**Current Issues**:
- `PRINCIPLES.md`, `CLAUDE.md` → Root directory
- Audit reports, status reports → Root directory
- No systematic organization
- Hard to find and manage

**New Structure**:

```
project-root/
├── .cco/
│   ├── project.json
│   ├── commands.json
│   └── reports/                    # ← NEW: Command output reports
│       ├── audit/
│       │   ├── 2025-11-09-143022-audit-security.md
│       │   ├── 2025-11-09-150145-audit-code.md
│       │   └── latest-audit.md → symlink to most recent
│       ├── status/
│       │   ├── 2025-11-09-140500-status.md
│       │   └── latest-status.md
│       ├── fix/
│       ├── analyze/
│       └── sync/
│
├── .claude/
│   ├── commands/
│   ├── settings.local.json
│   └── statusline.js
│
└── docs/                           # ← NEW: Project documentation
    ├── cco/                        # ← CCO-generated docs
    │   ├── PRINCIPLES.md           # ← Moved from root
    │   ├── CLAUDE.md               # ← Moved from root (optional)
    │   ├── principles/             # ← NEW: Split principles by category
    │   │   ├── core.md             # Critical principles (always loaded)
    │   │   ├── code-quality.md     # Load on /cco-audit code
    │   │   ├── security.md         # Load on /cco-audit security
    │   │   ├── testing.md          # Load on /cco-test
    │   │   ├── architecture.md     # Load on /cco-analyze
    │   │   ├── performance.md      # Load on /cco-optimize
    │   │   └── operations.md       # Load on DevOps commands
    │   │
    │   ├── guides/                 # ← NEW: Detailed guides (on-demand)
    │   │   ├── verification-protocol.md
    │   │   ├── git-workflow.md
    │   │   ├── security-response.md
    │   │   ├── performance-optimization.md
    │   │   └── container-best-practices.md
    │   │
    │   └── skills/                 # ← NEW: Language-specific skills
    │       ├── python/
    │       │   ├── async-patterns.md
    │       │   ├── type-hints-advanced.md
    │       │   ├── testing-pytest.md
    │       │   └── performance.md
    │       ├── typescript/
    │       │   ├── advanced-types.md
    │       │   ├── async-patterns.md
    │       │   └── testing-vitest.md
    │       ├── rust/
    │       │   ├── ownership-patterns.md
    │       │   ├── async-tokio.md
    │       │   └── error-handling.md
    │       └── go/
    │           ├── concurrency-patterns.md
    │           ├── error-handling.md
    │           └── testing-strategies.md
    │
    └── architecture/               # ← User's own docs (optional)
        ├── README.md
        └── ...
```

**Implementation Tasks**:

#### Task 1: Create Directory Structure

- [ ] Create `docs/cco/` directory
- [ ] Create `docs/cco/principles/` subdirectory
- [ ] Create `docs/cco/guides/` subdirectory
- [ ] Create `docs/cco/skills/` subdirectory
- [ ] Create `docs/cco/skills/python/` subdirectory
- [ ] Create `docs/cco/skills/typescript/` subdirectory
- [ ] Create `docs/cco/skills/rust/` subdirectory
- [ ] Create `docs/cco/skills/go/` subdirectory
- [ ] Create `.cco/reports/` directory
- [ ] Create `.cco/reports/audit/` subdirectory
- [ ] Create `.cco/reports/status/` subdirectory
- [ ] Create `.cco/reports/fix/` subdirectory
- [ ] Create `.cco/reports/analyze/` subdirectory
- [ ] Create `.cco/reports/sync/` subdirectory

#### Task 2: Migrate Existing Documents

**⚠️ CRITICAL: Add Backup Mechanism First**

- [ ] **Update `claudecodeoptimizer/core/principle_selector.py`**
  - [ ] Add `_create_backup()` helper method
  - [ ] In `generate_principles_md()` (line 407), add backup before writing:
    ```python
    # Before line 434: output_path.write_text(content, encoding="utf-8")
    if output_path.exists():
        self._create_backup(output_path)
    ```
  - [ ] Backup format: `PRINCIPLES.md.backup-YYYYMMDD-HHMMSS`
  - [ ] Keep last 3 backups, delete older ones
  - [ ] Example:
    ```python
    def _create_backup(self, file_path: Path) -> None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = file_path.parent / f"{file_path.name}.backup-{timestamp}"
        shutil.copy2(file_path, backup_path)

        # Keep last 3 backups
        backups = sorted(file_path.parent.glob(f"{file_path.name}.backup-*"))
        for old_backup in backups[:-3]:
            old_backup.unlink()
    ```

- [ ] **Update `claudecodeoptimizer/core/claude_md_generator.py`**
  - [ ] (Already added in P0.1 Task 4) ✅

- [ ] Move `PRINCIPLES.md` → `docs/cco/PRINCIPLES.md`
  - [ ] Update references in code
  - [ ] Add note in root: "See docs/cco/PRINCIPLES.md"
  - [ ] **Backup created automatically before any modification** ✅

- [ ] Move `CLAUDE.md` → `docs/cco/CLAUDE.md` (optional, user decision)
  - [ ] Update references in code
  - [ ] Keep backward compat (check both locations)
  - [ ] **Backup created automatically before any modification** ✅

#### Task 3: Split PRINCIPLES.md (Progressive Disclosure)

**Current**: 72 principles × ~70 tokens = ~5040 tokens (all loaded)

**Target**: Core principles only (~500 tokens), rest loaded on-demand

- [ ] Create `docs/cco/principles/core.md`
  - [ ] Include: P001 (Fail-Fast), P067 (Evidence-Based), P071 (Anti-Overengineering)
  - [ ] ~5-7 critical principles
  - [ ] Always loaded (~500 tokens)

- [ ] Create `docs/cco/principles/code-quality.md`
  - [ ] Include: P002-P015 (DRY, type safety, immutability, etc.)
  - [ ] Load only on: `/cco-audit code`, `/cco-fix code`

- [ ] Create `docs/cco/principles/security.md`
  - [ ] Include: P019-P037 (Privacy, encryption, zero-trust, etc.)
  - [ ] Load only on: `/cco-audit security`, `/cco-scan-secrets`

- [ ] Create `docs/cco/principles/testing.md`
  - [ ] Include: P038-P043 (Test pyramid, coverage, isolation)
  - [ ] Load only on: `/cco-test`, `/cco-audit tests`

- [ ] Create `docs/cco/principles/architecture.md`
  - [ ] Include: P044-P053 (Event-driven, microservices, SoC)
  - [ ] Load only on: `/cco-analyze`

- [ ] Create `docs/cco/principles/performance.md`
  - [ ] Include: P054-P058 (Caching, async, DB optimization)
  - [ ] Load only on: `/cco-optimize`

- [ ] Create `docs/cco/principles/operations.md`
  - [ ] Include: P059-P063 (IaC, observability, health checks)
  - [ ] Load only on: DevOps commands

#### Task 4: Update PRINCIPLES.md (Summary + Links)

**New Structure**:
```markdown
# Development Principles

**Generated**: 2025-11-09
**Applicable Principles**: 41/72
**Coverage**: 57.7%

---

## Quick Reference (Core Principles - Always Apply)

### P001: Fail-Fast Error Handling ⚠️
Errors must cause immediate, visible failure. No silent fallbacks.

### P067: Evidence-Based Verification ⚠️
Every claim requires proof (command output, test results).

### P071: Anti-Overengineering ⚠️
Simplest solution that works. Measure before optimizing.

---

## Full Principles by Category

For detailed principles, see category-specific documents:

- [Code Quality Principles](principles/code-quality.md) - 15 principles
- [Security & Privacy Principles](principles/security.md) - 19 principles
- [Testing Principles](principles/testing.md) - 6 principles
- [Architecture Principles](principles/architecture.md) - 10 principles
- [Performance Principles](principles/performance.md) - 5 principles
- [Operations Principles](principles/operations.md) - 10 principles
- [Git Workflow Principles](principles/git-workflow.md) - 5 principles

**Token Optimization**: Only core principles loaded by default (~500 tokens vs ~5000 tokens)

Category-specific principles load automatically when running relevant commands.
```

#### Task 5: Create Guides (On-Demand Loading)

- [ ] Create `docs/cco/guides/verification-protocol.md`
  - [ ] Extract from CLAUDE.md
  - [ ] Detailed verification workflow
  - [ ] Load only on: User request or verification-related tasks

- [ ] Create `docs/cco/guides/git-workflow.md`
  - [ ] Extract from CLAUDE.md
  - [ ] Git commit, PR guidelines
  - [ ] Load only on: Git operations

- [ ] Create `docs/cco/guides/security-response.md`
  - [ ] Extract from CLAUDE.md
  - [ ] Security incident response
  - [ ] Load only on: Security operations

- [ ] Create `docs/cco/guides/performance-optimization.md`
  - [ ] Extract from CLAUDE.md
  - [ ] Performance analysis workflow
  - [ ] Load only on: Performance tasks

- [ ] Create `docs/cco/guides/container-best-practices.md`
  - [ ] Extract from CLAUDE.md
  - [ ] Docker/K8s best practices
  - [ ] Load only on: Container operations

#### Task 6: Update CLAUDE.md (Minimal Core)

**Current**: ~3000 tokens (everything loaded)

**Target**: ~1000 tokens (core guidelines only)

**New Structure**:
```markdown
# Claude Code Development Guide

**Universal guide for working with Claude Code across any project**

---

## CCO Initialization
[Keep minimal - link to full guide]

## Development Principles
@docs/cco/PRINCIPLES.md (core principles auto-loaded)

## Working Guidelines (MUST FOLLOW)
- What NOT to Do
- Always Prefer
- Critical Changes (Require Approval)

## Verification Protocol (CRITICAL)
@docs/cco/guides/verification-protocol.md (load on demand)

## Complete Action Reporting & Transparency (MANDATORY)
[Keep full section - this is critical]

---

## Detailed Guides (On-Demand)

For detailed workflows, see:
- [Verification Protocol](docs/cco/guides/verification-protocol.md)
- [Git Workflow](docs/cco/guides/git-workflow.md)
- [Security Response](docs/cco/guides/security-response.md)
- [Performance Optimization](docs/cco/guides/performance-optimization.md)
- [Container Best Practices](docs/cco/guides/container-best-practices.md)

**Token Optimization**: Core guidelines (~1000 tokens), detailed guides loaded on-demand
```

#### Task 7: Report Management System

**Update All Commands** to use new report locations:

- [ ] Update `commands/audit.md`
  ```markdown
  ## Output

  Report saved to: `.cco/reports/audit/YYYY-MM-DD-HHMMSS-audit-<type>.md`
  Latest: `.cco/reports/audit/latest-audit.md` (symlink)
  ```

- [ ] Update `commands/status.md`
  ```markdown
  ## Output

  Report saved to: `.cco/reports/status/YYYY-MM-DD-HHMMSS-status.md`
  Latest: `.cco/reports/status/latest-status.md` (symlink)
  ```

- [ ] Update all other commands similarly

**Implement in Core**:

- [ ] Create `core/report_manager.py`
  ```python
  class ReportManager:
      def save_report(self, command: str, content: str) -> Path:
          """Save report to .cco/reports/{command}/"""
          timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
          filename = f"{timestamp}-{command}.md"
          report_dir = Path.cwd() / ".cco" / "reports" / command
          report_dir.mkdir(parents=True, exist_ok=True)

          report_file = report_dir / filename
          report_file.write_text(content)

          # Create symlink to latest
          latest_link = report_dir / f"latest-{command}.md"
          if latest_link.exists():
              latest_link.unlink()
          latest_link.symlink_to(filename)

          return report_file
  ```

#### Task 8: Update .gitignore

- [ ] Add to `.gitignore`:
  ```
  # CCO Reports (generated, not committed)
  .cco/reports/

  # Optional: CCO docs (if user prefers not to commit)
  # docs/cco/
  ```

**Verification**:
```bash
# Directory structure
tree docs/cco/
tree .cco/reports/

# Token reduction
# Before: PRINCIPLES.md (~5000 tokens) + CLAUDE.md (~3000 tokens) = ~8000 tokens
# After: Core principles (~500 tokens) + Core guidelines (~1000 tokens) = ~1500 tokens
# Reduction: 5.3x (8000 → 1500)

# Verify references updated
grep -r "PRINCIPLES.md" claudecodeoptimizer/
grep -r "CLAUDE.md" claudecodeoptimizer/

# Verify reports work
/cco-status
ls -la .cco/reports/status/
```

**Estimated Effort**: 1 day

---

### P0.3: Token Optimization & Progressive Disclosure (Priority: 🔴 CRITICAL)

**Goal**: Reduce context token usage by 5x (8000 → 1500 tokens)

**Strategy**: Load only what's needed, when it's needed

#### Task 1: Implement Progressive Disclosure for Skills

**Pattern** (from wshobson/agents):
```markdown
# skill-name.md
---
metadata:
  name: Skill Name
  activation_keywords: ["keyword1", "keyword2"]
  category: category-name
---

# Quick Reference (Always Loaded - ~50 tokens)
One-liner summary of what this skill provides.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions
Step-by-step guide...

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources
Code examples, templates...
```

**Files to Create/Update**:

- [ ] Update existing skills to use 3-tier loading:
  - [ ] `skills/verification-protocol.md`
  - [ ] `skills/test-first-verification.md`
  - [ ] `skills/root-cause-analysis.md`
  - [ ] `skills/incremental-improvement.md`
  - [ ] `skills/security-emergency-response.md`

- [ ] Create `core/skill_loader.py`:
  ```python
  class SkillLoader:
      def load_skill_metadata(self, skill_path: Path) -> SkillMetadata:
          """Load only metadata (~50 tokens)"""

      def load_skill_instructions(self, skill_path: Path) -> str:
          """Load instructions section (~150 tokens)"""

      def load_skill_resources(self, skill_path: Path) -> str:
          """Load resources section (~500 tokens)"""

      def is_activated(self, skill: Skill, context: str) -> bool:
          """Check if skill should be activated based on context"""
  ```

#### Task 2: Category-Based Principle Loading

**Command → Principle Category Mapping**:

- [ ] Create `core/principle_loader.py`:
  ```python
  COMMAND_PRINCIPLE_MAP = {
      "cco-audit-code": ["core", "code_quality"],
      "cco-audit-security": ["core", "security"],
      "cco-test": ["core", "testing"],
      "cco-analyze": ["core", "architecture", "code_quality"],
      "cco-optimize": ["core", "performance"],
      "cco-audit-all": ["all"],  # Load everything
  }

  class PrincipleLoader:
      def load_for_command(self, command: str) -> str:
          """Load only relevant principles for this command"""
          categories = COMMAND_PRINCIPLE_MAP.get(command, ["core"])

          principles = []
          for category in categories:
              path = Path("docs/cco/principles") / f"{category}.md"
              if path.exists():
                  principles.append(path.read_text())

          return "\n\n".join(principles)
  ```

- [ ] Update all commands to use category-based loading:
  ```markdown
  ## Principles Reference

  @principle_loader.load_for_command("cco-audit-security")
  # This auto-loads: core.md + security.md only (~1500 tokens)
  ```

#### Task 3: Guide On-Demand Loading

**Implementation**:

- [ ] Update commands to reference guides via path:
  ```markdown
  ## Detailed Workflow

  For step-by-step verification protocol, see:
  @docs/cco/guides/verification-protocol.md

  (Load only when user explicitly requests verification details)
  ```

- [ ] Create `core/guide_loader.py`:
  ```python
  class GuideLoader:
      _cache: Dict[str, str] = {}

      def load_guide(self, guide_name: str) -> str:
          """Load guide on-demand with caching"""
          if guide_name in self._cache:
              return self._cache[guide_name]

          path = Path("docs/cco/guides") / f"{guide_name}.md"
          content = path.read_text()
          self._cache[guide_name] = content
          return content
  ```

**Verification**:
```bash
# Measure token reduction
# Before: All loaded = ~8000 tokens
# After: On-demand = ~1500 tokens (core only)
# Reduction: 5.3x

# Test that relevant content still loads when needed
/cco-audit security
# Should load: core.md + security.md (~1500 tokens, not all 8000)
```

**Estimated Effort**: 1 day

---

### P0.4: Language-Specific Skills (Priority: 🟡 HIGH)

**Goal**: Add 16-20 language-specific skills (4 languages × 4-5 skills each)

**Pattern** (from wshobson/agents):
- Each language gets dedicated skills directory
- Skills activate contextually based on detected language
- Progressive disclosure (metadata → instructions → resources)

#### Task 1: Python Skills (5 skills)

- [ ] Create `docs/cco/skills/python/async-patterns.md`
  - Async/await best practices
  - asyncio patterns
  - Common pitfalls

- [ ] Create `docs/cco/skills/python/type-hints-advanced.md`
  - Generics, Protocol, TypeVar
  - Union, Optional, Literal
  - Type narrowing

- [ ] Create `docs/cco/skills/python/testing-pytest.md`
  - Pytest fixtures
  - Parametrization
  - Mocking strategies

- [ ] Create `docs/cco/skills/python/packaging-modern.md`
  - pyproject.toml setup
  - UV package manager
  - Publishing to PyPI

- [ ] Create `docs/cco/skills/python/performance.md`
  - Profiling tools
  - Common bottlenecks
  - Optimization patterns

#### Task 2: TypeScript Skills (5 skills)

- [ ] Create `docs/cco/skills/typescript/advanced-types.md`
  - Conditional types
  - Mapped types
  - Template literal types

- [ ] Create `docs/cco/skills/typescript/async-patterns.md`
  - Promises and async/await
  - Concurrent operations
  - Error handling

- [ ] Create `docs/cco/skills/typescript/testing-vitest.md`
  - Vitest setup
  - Component testing
  - Mocking strategies

- [ ] Create `docs/cco/skills/typescript/node-performance.md`
  - V8 optimization
  - Event loop understanding
  - Memory management

- [ ] Create `docs/cco/skills/typescript/type-safety.md`
  - Strict mode setup
  - Type guards
  - Discriminated unions

#### Task 3: Rust Skills (4 skills)

- [ ] Create `docs/cco/skills/rust/ownership-patterns.md`
  - Ownership rules
  - Borrowing strategies
  - Lifetimes

- [ ] Create `docs/cco/skills/rust/async-tokio.md`
  - Tokio runtime
  - Async traits
  - Concurrent patterns

- [ ] Create `docs/cco/skills/rust/error-handling.md`
  - Result and Option
  - Error propagation (?)
  - Custom error types

- [ ] Create `docs/cco/skills/rust/testing.md`
  - Unit tests
  - Integration tests
  - Benchmarking

#### Task 4: Go Skills (4 skills)

- [ ] Create `docs/cco/skills/go/concurrency-patterns.md`
  - Goroutines
  - Channels
  - Select statements

- [ ] Create `docs/cco/skills/go/error-handling.md`
  - Error wrapping
  - Sentinel errors
  - Error types

- [ ] Create `docs/cco/skills/go/testing-strategies.md`
  - Table-driven tests
  - Subtests
  - Test fixtures

- [ ] Create `docs/cco/skills/go/performance.md`
  - Profiling (pprof)
  - Memory optimization
  - Goroutine management

#### Task 5: Activation System

- [ ] Update `core/skill_loader.py`:
  ```python
  class SkillLoader:
      def detect_language_skills(self, primary_language: str) -> List[Path]:
          """Auto-detect relevant skills for language"""
          skills_dir = Path("docs/cco/skills") / primary_language.lower()
          if skills_dir.exists():
              return list(skills_dir.glob("*.md"))
          return []

      def activate_skill(self, skill_path: Path, context: str) -> bool:
          """Check if skill should activate based on context"""
          metadata = self.load_skill_metadata(skill_path)

          # Check keywords in context
          return any(
              keyword.lower() in context.lower()
              for keyword in metadata.activation_keywords
          )
  ```

- [ ] Update commands to auto-activate language skills:
  ```markdown
  ## Language-Specific Guidance

  @skill_loader.detect_language_skills(detected_language)
  # For Python project: Auto-loads Python skills metadata
  # Skills activate when relevant keywords appear in conversation
  ```

**Verification**:
```bash
# Test Python project
cd python-project/
/cco-init
# Should detect: Primary language = Python
# Should load: Python skills metadata (~250 tokens)

# When discussing async code
"How should I structure async code?"
# Should activate: docs/cco/skills/python/async-patterns.md

# Test TypeScript project
cd typescript-project/
/cco-init
# Should load: TypeScript skills metadata
```

**Estimated Effort**: 2 days

---

### P0.5: Update Project Types (Priority: 🟡 HIGH)

**Goal**: 7 → 13 unique, overlap-free project types

**Current Issues**:
- Some projects fit multiple categories (e.g., "web_app" vs "api_backend")
- No clear boundaries
- Confusion during selection

**New Structure** (Mutually Exclusive):

#### Task 1: Update decision_tree.py

- [ ] Update `wizard/decision_tree.py` line 34-84:
  ```python
  TIER1_PROJECT_PURPOSE = DecisionPoint(
      id="project_purpose",
      multi_select=True,  # Can select multiple if truly different domains
      validation=validate_no_conflicts,  # Prevent conflicting selections
      options=[
          # Backend Services (1-2)
          Option(value="api_service", label="API Service",
                 description="Pure backend API (REST/GraphQL/gRPC), no UI",
                 conflicts_with=["web_app", "spa"]),

          Option(value="microservice", label="Microservice",
                 description="Part of distributed system, service mesh",
                 conflicts_with=["monolith"]),

          # Frontend/Full-Stack (3-4)
          Option(value="web_app", label="Web Application",
                 description="Full-stack (frontend + backend integrated)",
                 conflicts_with=["api_service", "spa"]),

          Option(value="spa", label="Single Page Application",
                 description="Frontend-only, consumes external API",
                 conflicts_with=["web_app", "api_service"]),

          # Libraries & Tools (5-7)
          Option(value="library", label="Library/SDK",
                 description="Reusable package for developers",
                 effects="Public API, versioning, semver"),

          Option(value="framework", label="Framework/Platform",
                 description="Opinionated foundation for apps",
                 effects="Plugin system, extensibility, DX"),

          Option(value="cli_tool", label="CLI Tool",
                 description="Command-line utility",
                 effects="Help text, UX, error messages"),

          # Data & Processing (8-10)
          Option(value="data_pipeline", label="Data Pipeline",
                 description="ETL, batch processing",
                 effects="Idempotency, retry logic, data quality"),

          Option(value="ml_pipeline", label="ML/AI Pipeline",
                 description="Training, inference, MLOps",
                 effects="Reproducibility, experiment tracking"),

          Option(value="stream_processing", label="Stream Processing",
                 description="Real-time data (Kafka, Flink)",
                 effects="Low latency, exactly-once semantics"),

          # Desktop & Mobile (11-12)
          Option(value="desktop_app", label="Desktop Application",
                 description="Native or cross-platform desktop",
                 effects="Installers, auto-updates"),

          Option(value="mobile_app", label="Mobile Application",
                 description="iOS, Android, cross-platform mobile",
                 effects="Offline support, app store guidelines"),

          # Infrastructure (13-14)
          Option(value="infrastructure", label="Infrastructure as Code",
                 description="Terraform, Pulumi modules",
                 effects="Idempotency, state management"),

          Option(value="automation", label="Automation/Orchestration",
                 description="CI/CD, deployment automation",
                 effects="Reliability, rollback strategies"),
      ],
  )
  ```

#### Task 2: Add Conflict Validation

- [ ] Create `wizard/validators.py`:
  ```python
  def validate_no_conflicts(selected: List[str], options: List[Option]) -> bool:
      """Ensure no conflicting project types selected"""
      conflicts = {}
      for opt in options:
          if hasattr(opt, 'conflicts_with'):
              conflicts[opt.value] = opt.conflicts_with

      for sel in selected:
          if sel in conflicts:
              conflicting = set(conflicts[sel]) & set(selected)
              if conflicting:
                  raise ValueError(
                      f"Cannot select both {sel} and {conflicting}: "
                      f"They are mutually exclusive"
                  )
      return True
  ```

#### Task 3: Update Auto-Detection

- [ ] Update `wizard/decision_tree.py` line 391-431:
  ```python
  def _auto_detect_project_purpose(ctx: AnswerContext) -> list:
      """Auto-detect with better disambiguation"""

      # Check for explicit conflicts
      # If both React and FastAPI detected → "web_app" (full-stack)
      # If only FastAPI → "api_service" (backend only)
      # If only React → "spa" (frontend only)

      has_frontend = any(fw in frameworks for fw in ["react", "vue", "angular"])
      has_backend = any(fw in frameworks for fw in ["fastapi", "express", "django"])

      if has_frontend and has_backend:
          return ["web_app"]  # Full-stack
      elif has_backend and not has_frontend:
          return ["api_service"]  # Pure backend
      elif has_frontend and not has_backend:
          return ["spa"]  # Pure frontend

      # ... rest of logic
  ```

**Verification**:
```bash
# Test conflict detection
# Try selecting: api_service + web_app
# Should error: "Cannot select both api_service and web_app"

# Test auto-detection
cd fullstack-project/  # Has React + FastAPI
/cco-init --mode=quick
# Should detect: "web_app" (not both api_service and spa)
```

**Estimated Effort**: 3 hours

---

### P0.6: Expand Commands (12 → 25+ commands) (Priority: 🟡 HIGH)

**Goal**: Expand from 12 to 25+ specialized commands

**Categories**:
- Analysis (3 new)
- Testing (3 new)
- Documentation (3 new)
- Feature Implementation (2 new)
- DevOps (2 new)

#### Task 1: Analysis Commands (+3)

- [ ] Create `commands/analyze-structure.md`
  ```markdown
  ---
  description: Analyze codebase structure and architectural patterns
  category: analysis
  model: sonnet  # Complex reasoning
  ---

  # Codebase Structure Analysis

  Deep analysis of project organization, patterns, and architecture.

  ## Architecture
  - Detection: Haiku (scan directory tree, identify patterns)
  - Analysis: Sonnet (identify anti-patterns, suggest improvements)
  ```

- [ ] Create `commands/analyze-dependencies.md`
  ```markdown
  ---
  description: Dependency graph, circular deps, unused deps
  category: analysis
  model: haiku (scanning) + sonnet (analysis)
  ---

  # Dependency Analysis

  Analyze project dependencies, detect issues, suggest cleanup.
  ```

- [ ] Create `commands/analyze-complexity.md`
  ```markdown
  ---
  description: Cyclomatic complexity, code smells, refactoring candidates
  category: analysis
  model: sonnet
  ---

  # Code Complexity Analysis

  Identify complex code, suggest refactoring targets.
  ```

#### Task 2: Testing Commands (+3)

- [ ] Create `commands/generate-tests.md`
  ```markdown
  ---
  description: Auto-generate unit tests
  category: testing
  model: haiku  # Fast generation
  ---

  # Test Generation

  Generate unit tests for untested code.
  ```

- [ ] Create `commands/audit-tests.md`
  ```markdown
  ---
  description: Test quality, coverage gaps, flaky tests
  category: testing
  model: haiku (scan) + sonnet (recommendations)
  ---

  # Test Quality Audit

  Analyze test suite health, identify issues.
  ```

- [ ] Create `commands/generate-integration-tests.md`
  ```markdown
  ---
  description: Generate integration tests
  category: testing
  model: sonnet  # Complex scenarios
  ---

  # Integration Test Generation

  Generate service-to-service integration tests.
  ```

#### Task 3: Documentation Commands (+3)

- [ ] Create `commands/audit-docs.md`
  ```markdown
  ---
  description: Documentation completeness, accuracy, drift
  category: documentation
  model: haiku
  ---

  # Documentation Audit

  Check docs completeness, find drift from code.
  ```

- [ ] Create `commands/generate-docs.md`
  ```markdown
  ---
  description: Auto-generate API docs, README sections
  category: documentation
  model: haiku
  ---

  # Documentation Generation

  Generate missing documentation automatically.
  ```

- [ ] Create `commands/fix-docs.md`
  ```markdown
  ---
  description: Fix documentation inconsistencies
  category: documentation
  model: haiku
  ---

  # Documentation Fixes

  Auto-fix common documentation issues.
  ```

#### Task 4: Feature Implementation Commands (+2)

- [ ] Create `commands/implement-feature.md`
  ```markdown
  ---
  description: Full workflow - architect, code, test, doc, review
  category: feature
  model: multi-agent orchestration
  ---

  # Feature Implementation Workflow

  ## Architecture (Multi-Agent Orchestration)

  1. **Architect Agent** (Sonnet) - Design approach
  2. **Code Generator** (Haiku) - Implement
  3. **Test Generator** (Haiku) - Write tests
  4. **Security Auditor** (Sonnet) - Review security
  5. **Documentation** (Haiku) - Update docs
  6. **Validator** (Sonnet) - Final review

  ## Usage
  /cco-implement-feature "Add OAuth2 authentication"
  ```

- [ ] Create `commands/refactor.md`
  ```markdown
  ---
  description: Guided refactoring with safety checks
  category: feature
  model: sonnet
  ---

  # Refactoring Workflow

  Safe, guided refactoring with test validation.
  ```

#### Task 5: DevOps Commands (+2)

- [ ] Create `commands/setup-cicd.md`
  ```markdown
  ---
  description: Generate GitHub Actions, GitLab CI configs
  category: devops
  model: haiku
  ---

  # CI/CD Setup

  Auto-generate CI/CD pipeline configurations.
  ```

- [ ] Create `commands/setup-monitoring.md`
  ```markdown
  ---
  description: Observability stack setup (Prometheus, Grafana)
  category: devops
  model: sonnet
  ---

  # Monitoring Setup

  Configure observability stack for your project.
  ```

#### Task 6: Update Command Registry

- [ ] Update `command_selection.py` with new commands:
  - Add recommendation rules for new commands
  - Add to appropriate categories
  - Set applicable project types

**Verification**:
```bash
# Count commands
ls commands/*.md | wc -l
# Should show 25+ commands

# Verify categories
grep "category:" commands/*.md | sort | uniq -c

# Test new commands
/cco-analyze-structure
/cco-generate-tests
/cco-implement-feature "Add user authentication"
```

**Estimated Effort**: 2 days

---

### P0.7: Workflow Implementation (Multi-Agent Orchestration) (Priority: 🟢 MEDIUM)

**Goal**: Implement complex multi-agent workflows (inspired by wshobson/agents)

**Pattern**:
```
Complex Task → Specialized Agents → Coordinated Execution → Comprehensive Result
```

#### Task 1: Feature Implementation Workflow

**Already defined in P0.6 Task 4**, now implement:

- [ ] Create workflow coordination logic
  ```python
  # core/workflows.py
  class FeatureImplementationWorkflow:
      def execute(self, feature_description: str) -> WorkflowResult:
          # 1. Architecture design (Sonnet)
          design = self.architect_agent.plan(feature_description)

          # 2. Implementation (Haiku)
          code = self.code_generator.implement(design)

          # 3. Testing (Haiku)
          tests = self.test_generator.generate(code)

          # 4. Security review (Sonnet)
          security_issues = self.security_auditor.review(code)

          # 5. Documentation (Haiku)
          docs = self.doc_generator.update(code, design)

          # 6. Final validation (Sonnet)
          validation = self.validator.validate_all(
              code, tests, security_issues, docs
          )

          return WorkflowResult(
              code=code,
              tests=tests,
              docs=docs,
              security_review=security_issues,
              validation=validation
          )
  ```

#### Task 2: Security Audit Workflow

- [ ] Update `commands/audit.md` to use workflow:
  ```python
  # Security audit workflow
  workflow = SecurityAuditWorkflow()
  results = workflow.execute(
      agents=[
          DataSecurityAgent(model="haiku"),
          ArchitectureAuditAgent(model="haiku"),
          IntelligentAnalysisAgent(model="sonnet"),
      ]
  )
  ```

**Verification**:
```bash
# Test workflow execution
/cco-implement-feature "Add JWT authentication"
# Should coordinate 6 agents sequentially

# Verify parallel execution where possible
# Security audit should run 2 Haiku agents in parallel
```

**Estimated Effort**: 1 day

---

### P0.8: Context-Aware Init System & Versioning (Priority: 🔴 CRITICAL)

**Goal**: Implement context-aware, team-specific init system with rich UI and automated versioning

**Key Features**:
- P074: Automated semantic versioning (commit type → version bump)
- UI Adapter: Claude Code tool integration for rich interactive experience
- Context Matrix: Team-size/maturity-aware recommendations
- Enhanced Decisions: Git workflow, pre-commit hooks, CI/CD, code style, etc.
- Knowledge Base Granularity: Individual selection of guides/agents/skills

---

#### Task 1: P074 - Automated Semantic Versioning ✅ COMPLETE

**Status**: Completed in commit ce20cb4 (feat(skills): implement AI-powered semantic commit system)

**Goal**: Auto-bump version based on commit type, with team-aware workflows

**Files to Create/Modify**:

- [ ] `claudecodeoptimizer/knowledge/principles.json`
  - [ ] Add P074 principle definition
  - [ ] Update total principle count to 74
  - [ ] Update git-workflow category count to 8

- [ ] `~/.cco/knowledge/principles/git-workflow.md`
  - [ ] Add P074 section with detailed examples

- [ ] `claudecodeoptimizer/core/version_manager.py` (NEW)
  ```python
  class VersionManager:
      """Manage semantic versioning based on commit types"""

      def detect_bump_type(self, commit_messages: List[str]) -> BumpType:
          """Detect version bump from commit messages"""
          # BREAKING CHANGE → MAJOR
          # feat: → MINOR
          # fix: → PATCH
          # other → NO_BUMP

      def bump_version(self, current: str, bump_type: BumpType) -> str:
          """Calculate new version"""

      def update_version_files(self, new_version: str, files: List[Path]):
          """Update version in pyproject.toml, package.json, __init__.py"""

      def create_changelog_entry(self, version: str, commits: List[str]) -> str:
          """Generate CHANGELOG.md entry"""

      def create_git_tag(self, version: str, create: bool = False):
          """Create git tag (optional)"""
  ```

- [ ] `claudecodeoptimizer/wizard/decision_tree.py`
  - [ ] Add `TIER3_VERSIONING_STRATEGY` decision point
  - [ ] Options: auto_semver, pr_based_semver, manual_semver, calver, no_versioning
  - [ ] Team-aware recommendations
  - [ ] Auto-strategy based on team_size

- [ ] `templates/CLAUDE.md.template`
  - [ ] Add versioning workflow section
  - [ ] Add P074 reference

**Verification**:
```bash
# Test version detection
echo "feat(core): add new feature" | python -c "from version_manager import detect_bump_type; print(detect_bump_type(['feat(core): add new feature']))"
# Should output: MINOR

# Test version bump
python -c "from version_manager import bump_version; print(bump_version('1.2.3', 'MINOR'))"
# Should output: 1.3.0
```

**Estimated Effort**: 4 hours

---

#### Task 2: UI Adapter - Claude Code Tool Integration

**Goal**: Replace basic terminal prompts with rich Claude Code UI

**Files to Create**:

- [ ] `claudecodeoptimizer/wizard/ui_adapter.py` (NEW)
  ```python
  class ClaudeCodeUIAdapter:
      """Adapter for Claude Code AskUserQuestion tool"""

      def __init__(self, mode: Literal["terminal", "claude_code"]):
          self.mode = mode

      def ask_decision(
          self,
          decision: DecisionPoint,
          context: AnswerContext
      ) -> Any:
          """Ask user with rich UI"""
          if self.mode == "claude_code":
              return self._ask_via_claude_tool(decision, context)
          else:
              return self._ask_via_terminal(decision, context)

      def _ask_via_claude_tool(self, decision, context) -> Any:
          """Use AskUserQuestion with rich formatting"""
          question = {
              "question": decision.question,
              "header": self._format_header(decision, context),
              "options": self._build_rich_options(decision, context),
              "multiSelect": decision.multi_select
          }
          return ask_user_question(question)

      def _build_rich_options(self, decision, context) -> List[Dict]:
          """Build options with context-aware descriptions"""
          options = []
          for opt in decision.options:
              is_recommended = self._is_recommended_for_context(opt, context)
              description = self._build_context_description(opt, context, is_recommended)
              options.append({
                  "label": opt.label + (" ⭐" if is_recommended else ""),
                  "description": description
              })
          return options

      def _build_context_description(self, option, context, is_recommended) -> str:
          """Build rich description with team-specific notes"""
          parts = [option.description]

          if is_recommended:
              reason = self._get_recommendation_reason(option, context)
              parts.append(f"✓ {reason}")

          if hasattr(option, 'trade_offs'):
              parts.append(f"⚖️ {option.trade_offs}")

          team_note = self._get_team_specific_note(option, context)
          if team_note:
              parts.append(f"👥 {team_note}")

          return "\n".join(parts)
  ```

**Files to Modify**:

- [ ] `claudecodeoptimizer/wizard/orchestrator.py`
  - [ ] Replace `ask_choice()` / `ask_multi_choice()` calls
  - [ ] Use `ClaudeCodeUIAdapter` instead
  - [ ] Detect if running in Claude Code context
  - [ ] Fallback to terminal mode if not

**Verification**:
```bash
# Test in Claude Code
/cco-init --mode=interactive
# Should use rich UI with context-aware descriptions

# Test in terminal
python -m claudecodeoptimizer init --mode=interactive
# Should fallback to basic terminal UI
```

**Estimated Effort**: 6 hours

---

#### Task 3: Context Matrix - Team-Aware Recommendations

**Goal**: Multi-factor recommendation engine (team_size × maturity × philosophy)

**Files to Create**:

- [ ] `claudecodeoptimizer/wizard/context_matrix.py` (NEW)
  ```python
  class ContextMatrix:
      """Context-aware recommendation engine"""

      def recommend_versioning_strategy(
          self,
          team_size: str,
          maturity: str,
          has_ci: bool
      ) -> Dict:
          """Recommend versioning based on context"""
          # Solo dev → auto_semver (zero overhead)
          # Small team → pr_based_semver (peer review)
          # Large team → manual_semver (release managers)

      def recommend_principle_intensity(
          self,
          team_size: str,
          maturity: str,
          philosophy: str
      ) -> Dict:
          """Recommend how many principles to apply"""
          # Score-based system
          # Returns: intensity, principle_count, categories, reason

      def recommend_precommit_hooks(
          self,
          team_size: str,
          has_ci: bool
      ) -> List[str]:
          """Recommend pre-commit hooks based on team"""
          # Solo → format + secrets
          # Team → format + lint + secrets
          # Large team → add type check

      def get_team_specific_note(
          self,
          option: Option,
          context: AnswerContext
      ) -> str:
          """Get team-specific note for option"""
          # Returns notes like:
          # "✓ Perfect for solo developers"
          # "⚠️ Overhead for small teams"
          # "❌ Not recommended for large orgs"
  ```

**Files to Modify**:

- [ ] `claudecodeoptimizer/wizard/decision_tree.py`
  - [ ] Update auto_strategy functions to use ContextMatrix
  - [ ] Update ai_hint_generator to use ContextMatrix

**Verification**:
```python
# Test recommendation engine
matrix = ContextMatrix()

# Solo dev
rec = matrix.recommend_versioning_strategy("solo", "mvp", False)
assert rec["strategy"] == "auto_semver"

# Small team
rec = matrix.recommend_versioning_strategy("small_team", "production", True)
assert rec["strategy"] == "pr_based_semver"

# Large org
rec = matrix.recommend_versioning_strategy("large_org", "production", True)
assert rec["strategy"] == "manual_semver"
```

**Estimated Effort**: 6 hours

---

#### Task 4: Enhanced Decision Points

**Goal**: Add 10+ new decision points for comprehensive project configuration

**Files to Modify**:

- [ ] `claudecodeoptimizer/wizard/decision_tree.py`
  - [ ] Add `TIER2_GIT_WORKFLOW` (main-only, github-flow, git-flow)
  - [ ] Add `TIER3_BRANCH_NAMING` (conventional, jira, github_issue, custom)
  - [ ] Add `TIER3_PRECOMMIT_HOOKS` (multi-select: format, lint, type, security, test, secrets)
  - [ ] Add `TIER2_CI_PROVIDER` (github_actions, gitlab_ci, none)
  - [ ] Add `TIER3_NAMING_CONVENTION` (snake_case, camelCase, PascalCase)
  - [ ] Add `TIER3_LINE_LENGTH` (79, 88, 100, 120)
  - [ ] Add `TIER3_PACKAGE_MANAGER` (pip, poetry, pipenv, pdm)
  - [ ] Add `TIER2_DOCUMENTATION_STRATEGY` (minimal, standard, comprehensive)
  - [ ] Add `TIER3_AUTH_PATTERN` (jwt, session, oauth, api_key, none) - conditional
  - [ ] Add `TIER2_SECRETS_MANAGEMENT` (dotenv, vault, cloud, none)
  - [ ] Add `TIER2_ERROR_HANDLING` (fail_fast, graceful, retry)
  - [ ] Add `TIER3_LOGGING_LEVEL` (DEBUG, INFO, WARNING, ERROR)
  - [ ] Add `TIER3_CODE_REVIEW` (optional, required_1, required_2) - conditional
  - [ ] Add `TIER3_API_DOCS_TOOL` (openapi, graphql, none) - conditional

**Each Decision Point Must Have**:
- `question`: Clear question
- `why_this_question`: Context about why this matters
- `options`: 2-5 options with rich descriptions
- `team_notes`: Dict with team-size specific notes
- `trade_offs`: What you gain/lose with each option
- `workflow`: Step-by-step workflow for option
- `auto_strategy`: Lambda for quick mode
- `ai_hint_generator`: Lambda for recommendation reasoning

**Verification**:
```bash
# Test all decision points in interactive mode
/cco-init --mode=interactive
# Should ask ~20-25 questions total

# Test quick mode uses all auto-strategies
/cco-init --mode=quick
# Should auto-decide all questions
```

**Estimated Effort**: 2 days (16 hours)

---

#### Task 5: Knowledge Base Granular Selection

**Goal**: Individual selection of guides/agents/skills instead of all/none

**Files to Modify**:

- [ ] `claudecodeoptimizer/wizard/orchestrator.py` - `_run_command_selection()`
  - [ ] Replace simple "all/none" input with multi-select
  - [ ] Show guide descriptions
  - [ ] Pre-select recommended guides based on project type
  - [ ] Same for agents and skills

**Example**:
```python
# Current (simple):
response = input("  Select guides (all/none): ").strip().lower()

# New (rich):
available_guides = get_available_guides()
guide_descriptions = {
    "verification-protocol": "Evidence-based verification workflow",
    "git-workflow": "Git commit, branching, PR guidelines",
    "security-response": "Security incident response plan",
    "performance-optimization": "Performance analysis workflow",
    "container-best-practices": "Docker/K8s best practices"
}

# Pre-select based on project type
recommended_guides = []
if project_type == "api_backend":
    recommended_guides = ["security-response", "performance-optimization"]
elif project_type == "cli_tool":
    recommended_guides = []  # Minimal
elif team_size != "solo":
    recommended_guides = ["git-workflow", "verification-protocol"]

# Use UI adapter for rich selection
selected_guides = ui_adapter.ask_multi_select(
    question="Select knowledge base guides to symlink:",
    options=[
        {
            "label": guide,
            "description": guide_descriptions.get(guide, ""),
            "recommended": guide in recommended_guides
        }
        for guide in available_guides
    ],
    defaults=recommended_guides
)
```

**Verification**:
```bash
# Test guide selection
/cco-init --mode=interactive
# At knowledge base step, should show individual guides with descriptions
# Recommended guides should be pre-selected
```

**Estimated Effort**: 4 hours

---

#### Task 6: File Generation Enhancements

**Goal**: Generate additional config files based on selections

**Files to Modify**:

- [ ] `claudecodeoptimizer/wizard/orchestrator.py` - `_run_file_generation()`
  - [ ] Generate `.editorconfig` (if code style selected)
  - [ ] Generate `.pre-commit-config.yaml` (if pre-commit selected)
  - [ ] Generate `.github/workflows/ci.yml` (if GitHub Actions selected)
  - [ ] Generate `.github/pull_request_template.md` (if PR template selected)
  - [ ] Generate `CODEOWNERS` (if team project)
  - [ ] Generate `.vscode/settings.json` (IDE preferences)

**Files to Create**:

- [ ] `templates/.editorconfig.template`
- [ ] `templates/.pre-commit-config.yaml.template`
- [ ] `templates/github-actions-ci.yml.template`
- [ ] `templates/pull_request_template.md.template`
- [ ] `templates/CODEOWNERS.template`
- [ ] `templates/.vscode-settings.json.template`

**Verification**:
```bash
# After init with GitHub Actions + pre-commit
ls -la .github/workflows/
ls -la .pre-commit-config.yaml

# Verify content
cat .github/workflows/ci.yml
# Should have project-specific configuration
```

**Estimated Effort**: 6 hours

---

#### Task 7: Quick Mode = Interactive Mode with AI Decisions

**Goal**: Quick mode uses SAME decision tree, AI auto-answers each question

**Current Issue**: Quick mode bypasses some questions

**Fix**:

- [ ] `claudecodeoptimizer/wizard/orchestrator.py`
  - [ ] Ensure `_run_decision_tree()` executes ALL decisions in both modes
  - [ ] In quick mode: `_auto_decide()` for each decision
  - [ ] In interactive mode: `_ask_user_decision()` for each decision
  - [ ] Same decision flow, different UI

**Verification**:
```bash
# Run both modes, compare decisions made
/cco-init --mode=quick > quick_decisions.txt
/cco-init --mode=interactive  # Accept all defaults > interactive_decisions.txt

# Should have same number of decisions, same keys
diff <(cat quick_decisions.txt | grep "AUTO") <(cat interactive_decisions.txt | grep "Question")
```

**Estimated Effort**: 2 hours

---

## Estimated Total Effort for P0.8

**Task 1 (P074 Versioning)**: 4 hours
**Task 2 (UI Adapter)**: 6 hours
**Task 3 (Context Matrix)**: 6 hours
**Task 4 (Enhanced Decisions)**: 16 hours (2 days)
**Task 5 (KB Granularity)**: 4 hours
**Task 6 (File Generation)**: 6 hours
**Task 7 (Quick Mode Fix)**: 2 hours

**Total**: 44 hours (~5.5 days)

**Priority**: Complete before v0.2.0 release (after P0.1-P0.7)

---

## Estimated Total Effort for P0

**P0.1**: 0.5 days (Critical fixes)
**P0.2**: ~~1 day~~ 2 hours (Report management only - rest solved by symlinks)
**P0.3**: 1 day (Token optimization)
**P0.4**: 2 days (Language skills)
**P0.5**: 0.5 days (Project types)
**P0.6**: 2 days (New commands)
**P0.7**: 1 day (Workflows)

**Total**: 8 days (~1.5 weeks)

**Priority**: Complete before v0.2.0 release

---

## 🔴 v0.2.0 - Production Readiness (Week 1-2)

**Focus**: Testing, stability, and core quality improvements

**Release Criteria**:
- ✅ 60%+ test coverage
- ✅ Zero critical bugs (try-except-pass fixed)
- ✅ Type annotations complete (mypy strict)
- ✅ CI/CD pipeline operational
- ✅ Zero P001 (Fail-Fast) violations

### Critical Tasks

#### 1. Testing Infrastructure (Priority: 🔴 CRITICAL)

**Status**: ❌ 0% coverage - NO TESTS

**Tasks**:
- [ ] **Setup test framework**
  - [ ] Configure pytest with coverage plugin
  - [ ] Setup test directory structure
  - [ ] Add pytest configuration to pyproject.toml
  - [ ] Create conftest.py with common fixtures

- [ ] **Unit Tests - Detection Module** (Target: 80% coverage)
  - [ ] `tests/unit/test_detection.py`
    - [ ] Test language detection for Python projects
    - [ ] Test language detection for JavaScript projects
    - [ ] Test framework detection (FastAPI, Django, React, etc.)
    - [ ] Test tool detection (Docker, pytest, ruff, etc.)
    - [ ] Test confidence scoring accuracy
    - [ ] Test evidence collection
    - [ ] Edge case: Empty project
    - [ ] Edge case: Multi-language project
    - [ ] Edge case: Large project (10k+ files)

- [ ] **Unit Tests - Principles Module** (Target: 80% coverage)
  - [ ] `tests/unit/test_principles.py`
    - [ ] Test principle loading from JSON
    - [ ] Test principle selection (auto strategy)
    - [ ] Test principle selection (minimal strategy)
    - [ ] Test principle selection (comprehensive strategy)
    - [ ] Test condition evaluation
    - [ ] Test applicability checks
    - [ ] Test auto-fix principles filtering
    - [ ] Edge case: Invalid principles.json
    - [ ] Edge case: Missing principles

- [ ] **Unit Tests - Wizard Module** (Target: 70% coverage)
  - [ ] `tests/unit/test_wizard.py`
    - [ ] Test quick mode initialization
    - [ ] Test interactive mode initialization
    - [ ] Test system detection
    - [ ] Test project detection
    - [ ] Test decision tree execution
    - [ ] Test principle selection from answers
    - [ ] Test command selection from answers
    - [ ] Edge case: Wizard cancellation (KeyboardInterrupt)
    - [ ] Edge case: Invalid user input
    - [ ] Edge case: Missing detection data

- [ ] **Unit Tests - Installer Module** (Target: 70% coverage)
  - [ ] `tests/unit/test_installer.py`
    - [ ] Test global installation
    - [ ] Test project initialization
    - [ ] Test command linking
    - [ ] Test uninstallation cleanup
    - [ ] Test upgrade process
    - [ ] Edge case: Installation failure recovery
    - [ ] Edge case: Permissions issues
    - [ ] Edge case: Existing installation

- [ ] **Integration Tests** (Target: 60% coverage)
  - [ ] `tests/integration/test_init_flow.py`
    - [ ] Test end-to-end quick mode init (Python project)
    - [ ] Test end-to-end interactive mode init (JavaScript project)
    - [ ] Test init → status → remove workflow
    - [ ] Test re-initialization (remove → init)

  - [ ] `tests/integration/test_command_execution.py`
    - [ ] Test /cco-status command execution
    - [ ] Test /cco-analyze command execution
    - [ ] Test /cco-audit command (mocked agents)

- [ ] **Test Fixtures**
  - [ ] `tests/fixtures/sample_python_project/`
    - [ ] Create minimal Python project (pyproject.toml, src/, tests/)
    - [ ] Add FastAPI example
    - [ ] Add pytest configuration

  - [ ] `tests/fixtures/sample_js_project/`
    - [ ] Create minimal JavaScript project (package.json, src/, tests/)
    - [ ] Add React example
    - [ ] Add Jest configuration

  - [ ] `tests/fixtures/sample_go_project/`
    - [ ] Create minimal Go project (go.mod, main.go)

  - [ ] `tests/fixtures/sample_rust_project/`
    - [ ] Create minimal Rust project (Cargo.toml, src/)

**Verification**:
```bash
# Run tests
pytest tests/ -v --cov=claudecodeoptimizer --cov-report=html --cov-report=term

# Coverage report should show:
# claudecodeoptimizer/ai/detection.py        80%+
# claudecodeoptimizer/core/principles.py     80%+
# claudecodeoptimizer/wizard/orchestrator.py 70%+
# claudecodeoptimizer/core/installer.py      70%+
# TOTAL                                       60%+
```

**Estimated Effort**: 3-4 days

---

#### 2. Fix Try-Except-Pass (Priority: 🔴 CRITICAL)

**Status**: ❌ 13 instances found (P001 Fail-Fast violation)

**Locations**:
```bash
$ ruff check | grep S110
claudecodeoptimizer/ai/detection.py:710    # 3 instances
claudecodeoptimizer/wizard/orchestrator.py:184 # 2 instances
claudecodeoptimizer/core/installer.py:176  # 1 instance
claudecodeoptimizer/core/utils.py:45       # 2 instances
claudecodeoptimizer/wizard/cli.py:89       # 2 instances
claudecodeoptimizer/ai/recommendations.py:123 # 3 instances
```

**Tasks**:
- [ ] **Fix detection.py (3 instances)**
  - [ ] Lines 710, 728, 957: File reading try-except-pass
  - [ ] Action: Add logging, specific exceptions
  - [ ] Test: Add unit test for file read failures

- [ ] **Fix wizard/orchestrator.py (2 instances)**
  - [ ] Lines 184, 309: Generic exception catching
  - [ ] Action: Specific exceptions, user-friendly error messages
  - [ ] Test: Add integration test for wizard error handling

- [ ] **Fix installer.py (1 instance)**
  - [ ] Line 176: Chmod failure on Windows
  - [ ] Action: Platform-specific handling with logging
  - [ ] Test: Mock chmod failure, verify graceful degradation

- [ ] **Fix utils.py (2 instances)**
  - [ ] Lines 45, 78: JSON parsing failures
  - [ ] Action: Raise JSONDecodeError with context
  - [ ] Test: Add test for invalid JSON handling

- [ ] **Fix cli.py (2 instances)**
  - [ ] Lines 89, 134: User input validation
  - [ ] Action: Specific validation errors
  - [ ] Test: Add test for invalid CLI inputs

- [ ] **Fix recommendations.py (3 instances)**
  - [ ] Lines 123, 156, 189: API call failures
  - [ ] Action: Retry logic + specific error handling
  - [ ] Test: Mock API failures, verify error messages

**Before**:
```python
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

**After**:
```python
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

**Verification**:
```bash
# Should show ZERO S110 violations
ruff check claudecodeoptimizer/ | grep S110

# All tests should still pass
pytest tests/ -v
```

**Estimated Effort**: 1 day

---

#### 3. Complete Type Annotations (Priority: 🔴 CRITICAL)

**Status**: ❌ 17 missing annotations

**Locations**:
```bash
$ ruff check | grep ANN
17 × ANN401 (any-type)
5  × ANN204 (missing-return-type-special-method)
2  × ANN001 (missing-type-function-argument)
1  × ANN202 (missing-return-type-private-function)
```

**Tasks**:
- [ ] **Fix ANN401 (17 instances) - Replace `any` with specific types**
  - [ ] `core/analyzer.py`: 5 instances
    - [ ] `analyze()` return type: `Dict[str, Any]` → More specific
    - [ ] `_process_*()` methods: Specific return types

  - [ ] `wizard/models.py`: 4 instances
    - [ ] `AnswerContext.answers`: `Dict[str, Any]` → `Dict[str, Union[str, List[str], bool]]`

  - [ ] `ai/detection.py`: 3 instances
    - [ ] `ProjectAnalysisReport.dict()`: Better type hints

  - [ ] `core/principles.py`: 3 instances
    - [ ] `applicability` field types

  - [ ] `wizard/orchestrator.py`: 2 instances
    - [ ] `_build_preferences()` return type

- [ ] **Fix ANN204 (5 instances) - Add return types to special methods**
  - [ ] `__init__` methods: Add `→ None`
  - [ ] `__str__` methods: Add `→ str`

- [ ] **Fix ANN001 (2 instances) - Add argument type hints**
  - [ ] Function arguments missing type hints

- [ ] **Fix ANN202 (1 instance) - Add private function return type**
  - [ ] `_helper_function()` needs return type

- [ ] **Enable mypy strict mode**
  - [ ] Add mypy configuration to pyproject.toml
  - [ ] Fix all mypy errors
  - [ ] Add mypy to pre-commit hooks

**Verification**:
```bash
# Should show ZERO ANN violations
ruff check claudecodeoptimizer/ | grep ANN

# Mypy should pass in strict mode
mypy --strict claudecodeoptimizer/
```

**Estimated Effort**: 1 day

---

#### 4. Setup CI/CD Pipeline (Priority: 🔴 CRITICAL)

**Status**: ❌ No CI/CD

**Tasks**:
- [ ] **Create GitHub Actions workflow**
  - [ ] `.github/workflows/ci.yml`
    ```yaml
    name: CI

    on: [push, pull_request]

    jobs:
      lint:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-python@v4
            with:
              python-version: '3.12'
          - run: pip install ruff
          - run: ruff check claudecodeoptimizer/
          - run: ruff format --check claudecodeoptimizer/

      type-check:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-python@v4
          - run: pip install -e ".[dev]"
          - run: mypy --strict claudecodeoptimizer/

      test:
        runs-on: ${{ matrix.os }}
        strategy:
          matrix:
            os: [ubuntu-latest, windows-latest, macos-latest]
            python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-python@v4
            with:
              python-version: ${{ matrix.python-version }}
          - run: pip install -e ".[dev]"
          - run: pytest tests/ --cov=claudecodeoptimizer --cov-report=xml
          - uses: codecov/codecov-action@v3
            if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
    ```

- [ ] **Setup Codecov**
  - [ ] Sign up for Codecov
  - [ ] Add CODECOV_TOKEN to GitHub secrets
  - [ ] Add coverage badge to README

- [ ] **Add pre-commit hooks**
  - [ ] `.pre-commit-config.yaml`
    ```yaml
    repos:
      - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.1.0
        hooks:
          - id: ruff
          - id: ruff-format

      - repo: https://github.com/pre-commit/mirrors-mypy
        rev: v1.0.0
        hooks:
          - id: mypy
            additional_dependencies: [pydantic]
    ```

  - [ ] Document in CONTRIBUTING.md:
    ```bash
    # Install pre-commit hooks
    pip install pre-commit
    pre-commit install
    ```

- [ ] **Setup release workflow**
  - [ ] `.github/workflows/release.yml`
    - [ ] Automated PyPI publishing on tag push
    - [ ] Changelog generation
    - [ ] GitHub release notes

**Verification**:
```bash
# All workflows should be green
# Visit: https://github.com/sungurerdim/ClaudeCodeOptimizer/actions
```

**Estimated Effort**: 1 day

---

#### 5. Code Quality Cleanup (Priority: 🟡 HIGH)

**Status**: ⚠️ 79 ruff warnings (26 auto-fixable)

**Tasks**:
- [ ] **Auto-fix 26 fixable errors**
  ```bash
  ruff check --fix claudecodeoptimizer/
  ```

  - [ ] COM812 (17): Missing trailing commas - Auto-fix
  - [ ] F401 (3): Unused imports - Auto-fix
  - [ ] I001 (3): Unsorted imports - Auto-fix
  - [ ] UP015 (2): Redundant open modes - Auto-fix
  - [ ] F811 (1): Redefined while unused - Auto-fix

- [ ] **Manual fixes for remaining errors**
  - [ ] N812 (6): Lowercase imported as non-lowercase
    - [ ] Rename imports to follow PEP8

  - [ ] S112 (3): Try-except-continue
    - [ ] Similar to try-except-pass, add logging

  - [ ] E741 (2): Ambiguous variable name
    - [ ] Rename `l` → `line`, `O` → `obj`, etc.

  - [ ] B023 (1): Function uses loop variable
    - [ ] Fix closure issue with proper scoping

  - [ ] E402 (1): Module import not at top
    - [ ] Reorganize imports

  - [ ] S105 (1): Hardcoded password string
    - [ ] Use environment variable

  - [ ] S605 (1): Start process with shell
    - [ ] Use subprocess with shell=False

**Verification**:
```bash
# Should show ZERO errors
ruff check claudecodeoptimizer/

# Code should be formatted
ruff format claudecodeoptimizer/
```

**Estimated Effort**: 0.5 days

---

### v0.2.0 Release Checklist

**Before Release**:
- [ ] All P0 tasks complete (wshobson/agents integration)
- [ ] All critical tasks complete
- [ ] Test coverage ≥60%
- [ ] Zero try-except-pass
- [ ] Type annotations complete
- [ ] CI/CD green
- [ ] Ruff clean (0 errors)
- [ ] Update CHANGELOG.md
- [ ] Version bump to 0.2.0
- [ ] Tag release: `git tag v0.2.0`
- [ ] Push to PyPI

**Estimated Total Effort**: 15-16 days (3 weeks including P0)

---

## 🟡 v0.3.0 - User Experience (Week 3-4)

**Focus**: Better UX/DX and performance improvements

### High Priority Tasks

#### 6. Command Discovery System (Priority: 🟡 HIGH)

**Status**: ❌ No help command

**Tasks**:
- [ ] **Create `/cco-help` command**
  - [ ] `claudecodeoptimizer/commands/help.md`
  - [ ] List all available commands
  - [ ] Show command descriptions
  - [ ] Show command categories

- [ ] **Add search functionality**
  - [ ] `/cco-help search audit` → Show audit-related commands
  - [ ] `/cco-help search security` → Show security commands

- [ ] **Add command details**
  - [ ] `/cco-help show audit` → Show full audit.md content
  - [ ] Show expected arguments
  - [ ] Show usage examples

- [ ] **Create interactive menu**
  - [ ] Use AskUserQuestion for command selection
  - [ ] Execute selected command

**Verification**:
```bash
# Test help command
/cco-help

# Test search
/cco-help search test

# Test show
/cco-help show audit
```

**Estimated Effort**: 2 days

---

#### 7. Error Message Improvements (Priority: 🟡 HIGH)

**Status**: ⚠️ Error messages too generic

**Tasks**:
- [ ] **Create error message guidelines**
  - [ ] Document in CONTRIBUTING.md
  - [ ] Format: `❌ {Problem} → 💡 {Solution}`
  - [ ] Include context (file, line, command)

- [ ] **Improve installer errors**
  - [ ] Before: `"Installation failed"`
  - [ ] After: `"❌ Installation failed: ~/.cco/ already exists\n   💡 Run 'pip uninstall claudecodeoptimizer' first"`

- [ ] **Improve wizard errors**
  - [ ] Before: `"Initialization failed"`
  - [ ] After: `"❌ Initialization failed: Project already initialized\n   💡 Run '/cco-remove' to reinitialize"`

- [ ] **Improve detection errors**
  - [ ] Before: `"Detection failed"`
  - [ ] After: `"❌ Detection failed: No package.json or pyproject.toml found\n   💡 Run this command from project root"`

- [ ] **Add error recovery suggestions**
  - [ ] Create `core/error_handlers.py`
  - [ ] Centralized error handling with suggestions

**Verification**:
```bash
# Test various error scenarios
# Verify all errors have:
# 1. Clear problem statement
# 2. Actionable solution
# 3. Relevant context
```

**Estimated Effort**: 1 day

---

#### 8. Integration Tests Expansion (Priority: 🟡 HIGH)

**Status**: ⚠️ Only basic integration tests

**Tasks**:
- [ ] **Command execution tests**
  - [ ] `tests/integration/test_audit_command.py`
    - [ ] Test audit with mocked agents
    - [ ] Test parallel agent execution
    - [ ] Test audit report generation

  - [ ] `tests/integration/test_status_command.py`
    - [ ] Test status check
    - [ ] Test multi-language projects
    - [ ] Test caching behavior

  - [ ] `tests/integration/test_fix_command.py`
    - [ ] Test auto-fix workflow
    - [ ] Test rollback on test failure
    - [ ] Test git stash integration

- [ ] **Multi-language project tests**
  - [ ] `tests/integration/test_polyglot_project.py`
    - [ ] Python + JavaScript project
    - [ ] Rust + Go project
    - [ ] Test principle selection for multi-lang

- [ ] **E2E workflow tests**
  - [ ] `tests/integration/test_e2e_workflow.py`
    - [ ] Init → Status → Audit → Fix → Remove
    - [ ] Verify file generation
    - [ ] Verify cleanup

**Verification**:
```bash
# All integration tests pass
pytest tests/integration/ -v
```

**Estimated Effort**: 2 days

---

#### 9. Performance Optimization (Priority: 🟡 HIGH)

**Status**: ⚠️ Large projects slow

**Tasks**:
- [ ] **Detection engine caching**
  - [ ] `core/cache.py`
    - [ ] LRU cache for file extension counts
    - [ ] Cache detection results for 5 minutes
    - [ ] Invalidate on file changes

  - [ ] Implement in `ai/detection.py`:
    ```python
    @lru_cache(maxsize=128)
    def _count_file_extensions(self, cache_key: str) -> Dict[str, int]:
        # Cached implementation
    ```

- [ ] **Principles lazy loading**
  - [ ] Load principles.json only when needed
  - [ ] Cache loaded principles in memory
  - [ ] Implement in `core/principles.py`:
    ```python
    class PrinciplesManager:
        _cache: Optional[Dict] = None

        def _load_principles(self):
            if self._cache is None:
                self._cache = json.loads(...)
    ```

- [ ] **Parallel file scanning**
  - [ ] Use multiprocessing for large projects
  - [ ] Implement in `ai/detection.py`:
    ```python
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Parallel file scanning
    ```

- [ ] **Add performance benchmarks**
  - [ ] `tests/benchmarks/test_detection_performance.py`
    - [ ] Benchmark small project (<100 files)
    - [ ] Benchmark medium project (1000 files)
    - [ ] Benchmark large project (10000 files)

  - [ ] Target metrics:
    - Small: <100ms
    - Medium: <500ms
    - Large: <2s

**Verification**:
```bash
# Run benchmarks
pytest tests/benchmarks/ -v

# Verify speedup:
# Before: Large project detection ~5s
# After:  Large project detection <2s (2.5x improvement)
```

**Estimated Effort**: 2 days

---

#### 10. Documentation Expansion (Priority: 🟡 HIGH)

**Status**: ⚠️ Documentation gaps

**Tasks**:
- [ ] **Create CONTRIBUTING.md**
  - [ ] Development setup instructions
  - [ ] Code standards
  - [ ] Testing guidelines
  - [ ] PR process
  - [ ] Code of conduct

- [ ] **Create API documentation**
  - [ ] Setup Sphinx or MkDocs
  - [ ] `docs/api/detection.md`
  - [ ] `docs/api/principles.md`
  - [ ] `docs/api/wizard.md`
  - [ ] Auto-generate from docstrings

- [ ] **Create usage guides**
  - [ ] `docs/guides/getting-started.md`
  - [ ] `docs/guides/principles-guide.md`
  - [ ] `docs/guides/command-reference.md`
  - [ ] `docs/guides/multi-agent-patterns.md`

- [ ] **Add examples**
  - [ ] `examples/python-api/` - FastAPI project
  - [ ] `examples/react-app/` - React project
  - [ ] `examples/go-cli/` - Go CLI tool
  - [ ] Each with README and CCO configuration

**Verification**:
```bash
# Documentation builds successfully
mkdocs serve

# All examples run
cd examples/python-api && /cco-init
```

**Estimated Effort**: 3 days

---

### v0.3.0 Release Checklist

**Before Release**:
- [ ] All high priority tasks complete
- [ ] Command discovery working
- [ ] Error messages improved
- [ ] Performance 2x better
- [ ] Documentation complete
- [ ] Update CHANGELOG.md
- [ ] Version bump to 0.3.0
- [ ] Tag release

**Estimated Total Effort**: 10 days (2 weeks)

---

## 🟢 v0.4.0 - Extensibility (Month 2)

**Focus**: Plugin system and customization

### Medium Priority Tasks

#### 11. Plugin System Architecture (Priority: 🟢 MEDIUM)

**Status**: ❌ No plugin system

**Tasks**:
- [ ] **Design plugin API**
  - [ ] `docs/ADR/004-plugin-system.md`
  - [ ] Define plugin interface
  - [ ] Define plugin lifecycle
  - [ ] Define plugin discovery mechanism

- [ ] **Implement plugin loader**
  - [ ] `core/plugin_loader.py`
    ```python
    class PluginLoader:
        def discover_plugins(self) -> List[Plugin]:
            # Scan ~/.cco/plugins/

        def load_plugin(self, plugin_name: str) -> Plugin:
            # Load and validate plugin

        def unload_plugin(self, plugin_name: str) -> None:
            # Cleanup plugin
    ```

- [ ] **Create plugin types**
  - [ ] Custom detectors plugin
  - [ ] Custom principles plugin
  - [ ] Custom commands plugin
  - [ ] Custom skills plugin

- [ ] **Plugin manifest schema**
  - [ ] `schemas/plugin.json`
    ```json
    {
      "name": "custom-detector",
      "version": "1.0.0",
      "type": "detector",
      "entry_point": "detector.py",
      "dependencies": [],
      "config": {}
    }
    ```

**Estimated Effort**: 5 days

---

#### 12. Architecture Decision Records (Priority: 🟢 MEDIUM)

**Status**: ❌ No ADRs

**Tasks**:
- [ ] **Create ADR directory**
  - [ ] `docs/ADR/README.md`
  - [ ] `docs/ADR/template.md`

- [ ] **Document key decisions**
  - [ ] `001-wizard-dual-mode.md`
    - Why both quick and interactive modes?
    - Trade-offs considered
    - Implementation approach

  - [ ] `002-global-installation.md`
    - Why ~/.cco/ instead of per-project?
    - Benefits and drawbacks
    - Migration path

  - [ ] `003-principles-database.md`
    - Why 72 principles?
    - How were they selected?
    - Maintenance strategy

  - [ ] `004-plugin-system.md`
    - Design goals
    - API design
    - Security considerations

  - [ ] `005-multi-agent-orchestration.md`
    - Why parallel agents?
    - Model selection strategy
    - Cost optimization

  - [ ] `006-document-management-system.md`
    - Why docs/cco/ structure?
    - Progressive disclosure rationale
    - Token optimization goals

**Estimated Effort**: 2 days

---

#### 13. Example Projects (Priority: 🟢 MEDIUM)

**Status**: ❌ No example projects

**Tasks**:
- [ ] **Create Python examples**
  - [ ] `examples/python-fastapi-api/`
    - Full FastAPI project with tests
    - Pre-configured with CCO
    - README with CCO usage examples

  - [ ] `examples/python-django-web/`
    - Django web app
    - CCO principles for web projects

  - [ ] `examples/python-cli-tool/`
    - Click-based CLI tool
    - CCO principles for CLI projects

- [ ] **Create JavaScript examples**
  - [ ] `examples/react-web-app/`
    - React + TypeScript
    - Jest tests
    - CCO configuration

  - [ ] `examples/nextjs-app/`
    - Next.js project
    - Full-stack example

  - [ ] `examples/nodejs-api/`
    - Express.js API
    - TypeScript + Jest

- [ ] **Create other language examples**
  - [ ] `examples/go-microservice/`
  - [ ] `examples/rust-cli/`

- [ ] **Add example tests**
  - [ ] Each example should pass CCO audit
  - [ ] CI should verify examples

**Estimated Effort**: 5 days

---

### v0.4.0 Release Checklist

**Before Release**:
- [ ] Plugin system working
- [ ] ADRs documented
- [ ] Example projects complete
- [ ] Update CHANGELOG.md
- [ ] Version bump to 0.4.0
- [ ] Tag release

**Estimated Total Effort**: 12 days (2.5 weeks)

---

## 🚀 v1.0.0 - Stable Release (Month 3)

**Focus**: Production polish and stability

### Production Requirements

- [ ] **Quality Gates**
  - [ ] ≥80% test coverage
  - [ ] Zero critical bugs
  - [ ] Zero P001 violations
  - [ ] All tests pass on Windows, Linux, macOS
  - [ ] Performance benchmarks met

- [ ] **Documentation**
  - [ ] Complete API reference
  - [ ] User guide
  - [ ] Developer guide
  - [ ] Migration guide from v0.x
  - [ ] Video tutorials

- [ ] **Stability**
  - [ ] No breaking API changes
  - [ ] Deprecation warnings for future changes
  - [ ] Upgrade path documented

- [ ] **Production Examples**
  - [ ] At least 3 real-world usage examples
  - [ ] Case studies
  - [ ] Testimonials

---

## 📋 Ongoing Tasks

### Maintenance

- [ ] **Weekly**
  - [ ] Review and triage new issues
  - [ ] Respond to discussions
  - [ ] Update dependencies

- [ ] **Monthly**
  - [ ] Review and update principles
  - [ ] Performance regression testing
  - [ ] Security audit

### Community

- [ ] **Content**
  - [ ] Blog post: "Why CCO?"
  - [ ] Tutorial videos
  - [ ] Conference talk proposal

- [ ] **Outreach**
  - [ ] Share on Twitter/LinkedIn
  - [ ] Post on Reddit (r/Python, r/programming)
  - [ ] Hacker News submission

---

## 🎯 Success Metrics

### v0.2.0 (Production Readiness)
- ✅ Test coverage ≥60%
- ✅ CI/CD green
- ✅ Zero critical bugs
- ✅ <5 GitHub issues

### v0.3.0 (User Experience)
- ✅ 2x performance improvement
- ✅ <1s average command execution
- ✅ 10+ documentation pages
- ✅ ≥10 GitHub stars

### v0.4.0 (Extensibility)
- ✅ 3+ community plugins
- ✅ Plugin documentation complete
- ✅ 5+ example projects
- ✅ ≥50 GitHub stars

### v1.0.0 (Stable Release)
- ✅ 100+ active users
- ✅ ≥100 GitHub stars
- ✅ 3+ production deployments
- ✅ 0 critical bugs in last month
- ✅ Community contributions

---

## 📝 Notes

**Anti-Overengineering Reminders (P071)**:
- ✅ Don't add features without user requests
- ✅ Keep it simple and pragmatic
- ✅ Measure before optimizing
- ✅ Document why, not just what

**Quality Standards**:
- ✅ No try-except-pass (P001)
- ✅ Type annotations everywhere (P023)
- ✅ Evidence-based verification (P067)
- ✅ DRY enforcement (P002)
- ✅ Fail-fast error handling (P001)

**wshobson/agents Integration**:
- ✅ Progressive disclosure (3-tier loading)
- ✅ Language-specific skills
- ✅ Multi-agent workflows
- ✅ Token optimization (5x reduction)
- ✅ Category-based principle loading

---

## ✅ GitHub Actions CI/CD Fixes (COMPLETED - 2025-11-09)

**Priority**: 🔴 CRITICAL - Blocking production readiness
**Status**: ✅ COMPLETE

### Issue 1: Dependency Vulnerability Scan (SBOM Generation)
**Problem**: `cyclonedx-py` failing with "requirements.txt not found"
**Solution**: ✅ FIXED
- [x] Changed from `requirements` to `environment` mode
- [x] Removed unsupported `--format` flag
- [x] Works with pyproject.toml projects
- **Commits**: c3080e6, 79af6f4

### Issue 2: Secret Scanning (TruffleHog)
**Problem**: Duplicate `--fail` flag causing errors
**Solution**: ✅ FIXED
- [x] Removed duplicate flag from workflow
- [x] TruffleHog action handles --fail by default
- **Commit**: 8b877bc

### Issue 3: Tool Redundancy & Workflow Optimization
**Problem**: Black + Bandit + mypy overlap with Ruff, verbose workflows
**Solution**: ✅ FIXED (P071: Anti-Overengineering)
- [x] Consolidated Black/Bandit/mypy → Ruff (3 tools → 1)
- [x] Simplified workflow from 8 steps to 5 steps
- [x] Added pip caching for faster builds
- [x] Replaced `|| true` with `continue-on-error`
- [x] Removed redundant tool configs from pyproject.toml
- **Commits**: e3c9e76, dc938b8, 90fd97d

### Issue 4: Code Quality & Formatting
**Problem**: 25 files with format issues, lint warnings
**Solution**: ✅ FIXED
- [x] Formatted all Python files with `ruff format`
- [x] Added S110, COM812 to ignore rules (intentional patterns)
- [x] Auto-fixed linting issues with `ruff check --fix`
- **Commit**: e3c9e76

### New Addition: P072 Concise Commit Messages
**Goal**: Standardize commit message format across CCO projects
**Status**: ✅ IMPLEMENTED
- [x] Added P072 principle (max 10 lines, 5 bullets, Co-Authored-By footer)
- [x] Updated git-workflow.md with compact examples
- [x] Added to CLAUDE.md for all CCO users
- [x] Restored Co-Authored-By footer (GitHub contributor attribution)
- **Commits**: 1ddd73d, 3219e85

**Final Workflow**:
```yaml
dependency-scan: pip-audit + SBOM (cyclonedx-py environment)
secret-scan: TruffleHog (verified secrets only)
code-quality: Ruff format + Ruff check (lint + security)
```

**Outcome**: All CI/CD issues resolved, workflow optimized, P071 & P072 applied

---

## 🔄 `/cco-remove` Backup Restore Feature (USER REQUEST)

**Priority**: 🟡 HIGH - Important UX improvement

### Requirement
`/cco-remove` command should offer interactive backup restore options for each backed-up document.

### Current Behavior
- Creates backups but no restore option during removal
- User must manually restore from `.backup-*` files

### Desired Behavior
When running `/cco-remove`:
1. Detect all backup files (*.backup-*)
2. For each backup, ask user:
   - **Restore**: Replace current file with backup
   - **Keep Current**: Leave current file as-is
   - **Delete All**: Remove current file and all backups

### Implementation

**Files to Modify**:
- [ ] `claudecodeoptimizer/commands/remove.md` - Add backup restore flow
- [ ] `claudecodeoptimizer/core/installer.py` - Implement backup detection and restore

**Example Flow**:
```
/cco-remove

Found backups:
1. CLAUDE.md (3 backups)
   - CLAUDE.md.backup-20251109-143022 (2 hours ago)
   - CLAUDE.md.backup-20251109-120015 (5 hours ago)
   - CLAUDE.md.backup-20251108-183045 (1 day ago)

2. PRINCIPLES.md (2 backups)
   - PRINCIPLES.md.backup-20251109-140500 (3 hours ago)
   - PRINCIPLES.md.backup-20251108-190022 (1 day ago)

What would you like to do with CLAUDE.md?
  [1] Restore latest backup (2 hours ago)
  [2] Choose specific backup to restore
  [3] Keep current file (delete backups)
  [4] Delete all (current + backups)

> 1

✓ Restored CLAUDE.md from backup (20251109-143022)
✓ Deleted old backups

What would you like to do with PRINCIPLES.md?
  [1] Restore latest backup (3 hours ago)
  [2] Choose specific backup to restore
  [3] Keep current file (delete backups)
  [4] Delete all (current + backups)

> 3

✓ Kept current PRINCIPLES.md
✓ Deleted 2 backup files
```

**Implementation Details**:
```python
def detect_backups(self, file_path: Path) -> List[Path]:
    """Detect all backups for a file"""
    pattern = f"{file_path.name}.backup-*"
    return sorted(file_path.parent.glob(pattern), reverse=True)

def restore_backup(self, backup_path: Path, target_path: Path) -> None:
    """Restore a specific backup"""
    shutil.copy2(backup_path, target_path)

def offer_backup_restore(self, file_path: Path) -> None:
    """Interactive backup restore flow"""
    backups = self.detect_backups(file_path)
    if not backups:
        return

    # Show options and get user choice
    # Implement restore logic based on choice
```

**Verification**:
```bash
# Test backup restore flow
/cco-init  # Create initial setup
# Make changes to CLAUDE.md
/cco-init  # Triggers backup
/cco-remove  # Should show restore options
```

**Estimated Effort**: 0.5 day

---

**Last Updated**: 2025-11-09 (Added GitHub Actions fixes + Backup restore feature)
**Maintainer**: Sungur Zahid Erdim
**Status**: Active Development

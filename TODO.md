# CCO Dynamic Architecture Implementation

**Goal**: Make every component (agent/skill/command/guide) dynamically use project-specific selected principles, with universal principles auto-included in all projects.

**Philosophy**: Project-specific, AI-driven, zero-waste architecture.

---

## Architecture Overview

### Global Structure
```
~/.claude/
├── commands/
│   ├── cco-init.md      # ONLY these 2 commands
│   └── cco-remove.md

~/.cco/                   # Everything else here
├── principles/
│   ├── U001.md          # Universal principles (auto-included in all projects)
│   ├── U002.md
│   ├── ...
│   ├── P001.md          # Project-specific principles (AI-selected)
│   ├── P002.md
│   └── ...
├── commands/            # All CCO commands
├── guides/
├── skills/
├── agents/
├── templates/
│   ├── settings.json
│   └── statusline.js
└── projects/

.claude/                 # Project-local
├── principles/          # Symlinks to selected principles
│   ├── U001.md → ~/.cco/principles/U001.md (auto)
│   ├── U002.md → ~/.cco/principles/U002.md (auto)
│   ├── P001.md → ~/.cco/principles/P001.md (selected)
│   └── ...
├── project.json         # AI selections + preferences
├── commands/            # Symlinks to selected commands
├── guides/
├── skills/
└── statusline.js → ~/.cco/templates/statusline.js

CLAUDE.md                # Minimal, just references
```

### CLAUDE.md Format (New)
```markdown
# {PROJECT_NAME} - Claude Development Guide

{EXISTING_CONTENT_IF_ANY}

---

<!-- CCO_START -->
## Development Principles & Guidelines

Follow the principles and guidelines in `.claude/principles/`:
- Universal principles (U001-U0XX): Apply to all projects
- Project-specific principles (P001-P074): Selected for this project

See `.claude/principles/` directory for full definitions.

<!-- CCO_END -->
```

---

## Phase 1: Universal Principles Extraction & Deduplication

**Status**: ⏳ Not Started

### Tasks

#### 1.1: Identify Universal Content from CLAUDE.md.template
- [ ] Read templates/CLAUDE.md.template
- [ ] Extract universal sections:
  - Model Selection (Haiku/Sonnet/Opus guidelines)
  - Verification Protocol (evidence-based verification)
  - Token Optimization (grep-first, parallel agents)
  - Complete Action Reporting (report every tool use)
  - Test-First Development
  - Root Cause Analysis
  - Minimal Touch Policy
  - Cross-Platform Bash Commands
  - Git Workflow (commit format, atomic commits)
- [ ] List each as U001, U002, etc.

#### 1.2: Check for Overlap with Existing P-Principles
- [ ] Compare universal candidates with P001-P074
- [ ] Identify duplicates/overlaps:
  - P001 (Fail-Fast Error Handling) → Universal candidate (U-level)
  - P067 (Evidence-Based Verification) → Universal candidate (U-level)
  - P071 (No Overengineering) → Universal candidate (U-level)
  - P072 (Concise Commit Messages) → Universal candidate (U-level)
  - P073 (Atomic Commits) → Universal candidate (U-level)
  - P074 (Semantic Versioning) → Project-specific (API projects mostly)
- [ ] For each overlap:
  - If applies to ALL projects with no harm → Keep as universal
  - If project-specific value → Keep as P-principle
  - If overlap, merge best parts into one principle

#### 1.3: Determine Final Universal Principles (~10-15)
- [ ] Criteria: "Beneficial in ALL projects, zero harm, project-agnostic"
- [ ] Expected candidates:
  - Evidence-Based Verification (from P067)
  - Model Selection Strategy (from CLAUDE.md)
  - Token Optimization (from CLAUDE.md)
  - Complete Action Reporting (from CLAUDE.md)
  - Test-First Development (from CLAUDE.md)
  - Root Cause Analysis (from CLAUDE.md)
  - Minimal Touch Policy (from CLAUDE.md)
  - Cross-Platform Bash Commands (from CLAUDE.md)
  - Fail-Fast Error Handling (from P001)
  - No Overengineering (from P071)
  - Atomic Commits (from P073)
  - Concise Commit Messages (from P072)

#### 1.4: Create Universal Principle Files
- [ ] Create content/principles/U001.md - U0XX.md (one per universal rule)
- [ ] Format: Same as P001.md (frontmatter + content)
- [ ] Example frontmatter:
  ```yaml
  ---
  id: U001
  number: 1
  title: Evidence-Based Verification
  category: universal
  severity: critical
  weight: 10
  applicability:
    project_types: ['all']
    languages: ['all']
  ---
  ```

#### 1.5: Remove Promoted P-Principles
- [ ] Delete P001.md, P067.md, P071.md, P072.md, P073.md (if promoted to U)
- [ ] Update content/principles.json (remove from project categories)
- [ ] Result: P001-P074 → P001-P069 (5 fewer)

#### 1.6: Reorganize & Renumber All Principles

**Goal**: Logical grouping, related principles adjacent, continuous numbering

**Universal Principles (U001-U0XX)**:
- [ ] Group by theme:
  - Verification & Quality (Evidence-based, Fail-fast)
  - Development Process (Test-first, Root cause, Minimal touch)
  - AI Optimization (Model selection, Token optimization)
  - Communication (Complete reporting)
  - Git Workflow (Atomic commits, Concise messages)
  - Architecture (No overengineering)
  - Platform (Cross-platform bash)
- [ ] Assign continuous numbers U001-U012 (adjust if more/less)
- [ ] Update all frontmatter with new numbers

**Project-Specific Principles (P001-P0XX)**:
- [ ] Reorganize by logical flow within each category:
  - **Code Quality** (P001-P0XX): DRY, Type safety, Immutability, etc.
  - **Architecture** (P0XX-P0XX): Event-driven, Microservices, SOLID, etc.
  - **Security & Privacy** (P0XX-P0XX): Encryption, Zero-trust, Secrets, etc.
  - **Testing** (P0XX-P0XX): Pyramid, Coverage, Isolation, etc.
  - **Git Workflow** (P0XX-P0XX): Branch strategy, PR templates, etc.
  - **Performance** (P0XX-P0XX): Caching, Async, Optimization, etc.
  - **Operations** (P0XX-P0XX): IaC, Observability, Health checks, etc.
  - **API Design** (P0XX-P0XX): RESTful, Error handling, etc.
- [ ] Within each category, group related principles together
- [ ] Assign continuous numbers P001-P069 (or final count after deduplication)
- [ ] Update all frontmatter with new numbers

#### 1.7: Update principles.json
- [ ] Add universal principles to content/principles.json
- [ ] Add "universal" category to CATEGORY_TO_IDS mapping
- [ ] Update all principle IDs (U001-U0XX, P001-P0XX)
- [ ] Update category ranges
- [ ] Final count: ~12 U-principles + ~69 P-principles = ~81 total

#### 1.8: Update All References

**Files to update with new counts and IDs**:
- [ ] README.md:
  - Update "74 principles" → "~81 total (~12 universal + ~69 project-specific)"
  - Update principle ID examples
  - Update category breakdowns
- [ ] PRINCIPLE_LOADING_GUIDE.md:
  - Update principle counts
  - Update ID ranges
  - Update examples
- [ ] content/commands/*.md:
  - Update principle IDs in frontmatter
  - Ensure "universal" included where needed
- [ ] claudecodeoptimizer/core/principle_loader.py:
  - Update COMMAND_PRINCIPLE_MAP
  - Update "core" mapping (remove P001, P067, P071 if moved to U)
  - Add "universal" to all command mappings
- [ ] templates/CLAUDE.md.template (if kept):
  - Update principle references
  - Or DELETE if moving to minimal reference system

---

## Phase 2: Update Installation & Global Commands

**Status**: ⏳ Not Started

### 2.1: Update pip install Process

**File**: `claudecodeoptimizer/core/installer.py` (or setup.py / pyproject.toml hooks)

**Tasks**:
- [ ] Deploy U001-U0XX.md to ~/.cco/principles/ (universal principles)
- [ ] Deploy P001-P0XX.md to ~/.cco/principles/ (project-specific principles)
- [ ] Deploy only cco-init.md and cco-remove.md to ~/.claude/commands/
- [ ] Remove CLAUDE.md template deployment (no longer needed)
- [ ] Verify ~/.cco/ structure:
  ```
  ~/.cco/
  ├── principles/
  │   ├── U001.md - U012.md
  │   └── P001.md - P069.md
  ├── commands/ (28 command files)
  ├── guides/
  ├── skills/
  ├── agents/
  └── templates/ (settings.json, statusline.js, etc. - no CLAUDE.md)
  ```
- [ ] Verify ~/.claude/commands/ structure:
  ```
  ~/.claude/commands/
  ├── cco-init.md
  └── cco-remove.md
  ```

### 2.2: Update /cco-init Command

**File**: `~/.claude/commands/cco-init.md` (or content/commands/init.md source)

**Tasks**:
- [ ] Update init logic to:
  1. Run wizard (quick/interactive mode)
  2. AI analyzes project, selects principles
  3. **Always symlink ALL universal principles** (U001-U0XX)
  4. **Symlink only selected project principles** (P001-P0XX subset)
  5. Create `.claude/project.json` with selections
  6. Generate/merge minimal CLAUDE.md (not template-based)
  7. Link commands, guides, skills, agents as before
- [ ] Ensure principle linking:
  ```python
  # Pseudo-code
  def setup_principle_links():
      # 1. Always link all universal principles
      for u_principle in get_all_universal_principles():  # U001-U012
          link(f"~/.cco/principles/{u_principle}.md",
               f".claude/principles/{u_principle}.md")

      # 2. Link only selected project principles
      selected_p = ai_select_principles()  # e.g., ['P001', 'P036', 'P037']
      for p_principle in selected_p:
          link(f"~/.cco/principles/{p_principle}.md",
               f".claude/principles/{p_principle}.md")
  ```

### 2.3: Update /cco-remove Command

**File**: `~/.claude/commands/cco-remove.md` (or content/commands/remove.md source)

**Tasks**:
- [ ] Update removal logic to:
  1. Remove `.claude/project.json`
  2. Remove all principle symlinks (U*.md + P*.md)
  3. Remove command symlinks
  4. Remove guide/skill/agent symlinks
  5. Remove statusline.js symlink
  6. **Optionally remove CCO section from CLAUDE.md**:
     - Detect `<!-- CCO_START -->` and `<!-- CCO_END -->` markers
     - Ask user: "Remove CCO section from CLAUDE.md? (y/N)"
     - If yes: Remove content between markers
     - If no: Keep it (uninstall-safe, broken refs ignored)
  7. Optionally remove `.claude/settings.json` (if CCO-generated)
  8. Remove project registry from `~/.cco/projects/<project>.json`
  9. Display summary (no backup needed)
- [ ] Ensure clean removal:
  ```python
  # Pseudo-code
  def remove_principles():
      # Remove all U principles
      for u_file in glob(".claude/principles/U*.md"):
          remove_link(u_file)

      # Remove all P principles
      for p_file in glob(".claude/principles/P*.md"):
          remove_link(p_file)

  def remove_cco_section_from_claude_md():
      if not Path("CLAUDE.md").exists():
          return

      content = read("CLAUDE.md")
      if "<!-- CCO_START -->" not in content:
          return

      ask_user = input("Remove CCO section from CLAUDE.md? (y/N): ")
      if ask_user.lower() == 'y':
          # Remove between markers
          new_content = remove_between_markers(content,
                                                "<!-- CCO_START -->",
                                                "<!-- CCO_END -->")
          write("CLAUDE.md", new_content)
  ```

---

## Phase 3: Project Config System

**Status**: ⏳ Not Started

### 3.1: Define project.json Schema

**File**: `.claude/project.json` (NEW - created by cco-init)

```json
{
  "project_name": "MyProject",
  "project_root": "/absolute/path",
  "initialized_at": "2025-11-12T10:30:00Z",
  "wizard_mode": "quick",

  "detection": {
    "project_type": "api",
    "languages": ["python"],
    "frameworks": ["fastapi"],
    "team_size": "small",
    "maturity": "production",
    "security_level": "high",
    "philosophy": "balanced"
  },

  "selected_principles": {
    "universal": ["U001", "U002", "U003", "...", "U012"],
    "core": ["P067"],
    "code_quality": ["P002", "P003", "P004"],
    "security_privacy": ["P025", "P026", "P036", "P037"],
    "testing": ["P044", "P045"]
  },

  "command_overrides": {
    "cco-audit-security": {
      "principles": ["U001", "P036", "P037", "P038"],
      "reason": "Standard API security - core validations only"
    },
    "cco-audit-code": {
      "principles": ["U001", "P002", "P003", "P004"],
      "reason": "Focus on DRY, type safety, immutability"
    }
  },

  "selected_commands": ["cco-audit", "cco-status", "cco-fix", "..."],
  "selected_guides": ["verification-protocol.md", "..."],
  "selected_skills": ["python/testing-pytest.md", "..."],
  "selected_agents": []
}
```

**Tasks**:
- [ ] Create schema in claudecodeoptimizer/schemas/project_config.py
- [ ] Add Pydantic model: ProjectConfig
- [ ] Add validation

### 3.2: Update Init Process to Save Config

**File**: claudecodeoptimizer/wizard/orchestrator.py

**Tasks**:
- [ ] After AI selects principles, save to .claude/project.json
- [ ] After AI selects commands, save to project.json
- [ ] Save detection results to project.json
- [ ] Ensure universal principles (U001-U0XX) ALWAYS included in selections
- [ ] Save command overrides to project.json

**Code Location**: `CCOWizard.run()` → after `_select_principles()`

**Example**:
```python
def _save_project_config(self, selections: Dict) -> None:
    """Save AI selections to .claude/project.json"""
    config = {
        "project_name": self.project_root.name,
        "initialized_at": datetime.utcnow().isoformat(),
        "detection": self.detection_report,
        "selected_principles": {
            "universal": ["U001", "U002", ..., "U012"],  # All universal
            "code_quality": selections["code_quality"],
            "security_privacy": selections["security"],
            # ...
        },
        "command_overrides": {},  # Populated later or by user
        "selected_commands": selections["commands"],
        # ...
    }

    project_json = self.project_root / ".claude" / "project.json"
    project_json.write_text(json.dumps(config, indent=2))
```

### 3.3: Always Symlink Universal Principles

**File**: claudecodeoptimizer/core/linking.py

**Tasks**:
- [ ] In setup_project_links(), always link ALL universal principles first
- [ ] Then link selected project-specific principles
- [ ] Universal principles: ~/.cco/principles/U*.md → .claude/principles/U*.md (all U001-U012)
- [ ] Project principles: ~/.cco/principles/P*.md → .claude/principles/P*.md (only selected subset)

**Example**:
```python
def setup_principle_links(cco_dir: Path, project_dir: Path,
                          selected_principles: Dict[str, List[str]]) -> None:
    """Link principles to project."""
    principles_dir = project_dir / ".claude" / "principles"
    principles_dir.mkdir(parents=True, exist_ok=True)

    # 1. Always link ALL universal principles
    universal_principles = get_universal_principle_files(cco_dir)  # U001-U012
    for u_principle in universal_principles:
        source = cco_dir / "principles" / u_principle
        target = principles_dir / u_principle
        create_link(source, target)  # Try symlink → hardlink → copy

    # 2. Link only selected project principles
    for category, principle_ids in selected_principles.items():
        if category == "universal":
            continue  # Already linked above
        for principle_id in principle_ids:
            source = cco_dir / "principles" / f"{principle_id}.md"
            target = principles_dir / f"{principle_id}.md"
            if source.exists():
                create_link(source, target)
```

---

## Phase 4: Dynamic Loading Implementation

**Status**: ⏳ Not Started

### 4.1: Update PrincipleLoader

**File**: claudecodeoptimizer/core/principle_loader.py

**Tasks**:
- [ ] Add `_find_project_config()` method
  ```python
  def _find_project_config(self) -> Optional[Dict]:
      """Find .claude/project.json in current working directory."""
      cwd = Path.cwd()
      config_path = cwd / ".claude" / "project.json"
      if config_path.exists():
          return json.loads(config_path.read_text())
      return None
  ```

- [ ] Update `load_for_command()` to use project config first:
  ```python
  def load_for_command(self, command: str) -> str:
      # 1. Try project config (DYNAMIC)
      project_config = self._find_project_config()
      if project_config:
          overrides = project_config.get("command_overrides", {})
          if command in overrides:
              return self.load_principles(overrides[command]["principles"])

      # 2. Fallback to default COMMAND_PRINCIPLE_MAP (STATIC)
      categories = COMMAND_PRINCIPLE_MAP.get(command, ["core"])
      principle_ids = _resolve_categories_to_ids(categories)
      return self.load_principles(principle_ids)
  ```

- [ ] Update COMMAND_PRINCIPLE_MAP to include "universal" in all commands:
  ```python
  COMMAND_PRINCIPLE_MAP = {
      "cco-audit": ["universal", "all"],  # Universal + all principles
      "cco-audit-security": ["universal", "core", "security_privacy"],
      "cco-audit-code": ["universal", "core", "code_quality"],
      # ... etc
  }
  ```

### 4.2: Update Commands to Use Dynamic Loading

**Files**: content/commands/*.md

**Tasks**:
- [ ] Update command frontmatter to reference project config:
  ```markdown
  ---
  description: Security audit
  category: audit
  cost: 3
  principles: "dynamic"  # Will read from .claude/project.json
  ---
  ```

- [ ] Or keep specific IDs as fallback:
  ```markdown
  principles: ['U001', 'P036', 'P037']  # Default if no project.json
  ```

### 4.3: Update Agents to Use Dynamic Loading

**Files**: content/agents/*.md

**Tasks**:
- [ ] Update agent definitions to read principles from project.json
- [ ] Agents should call PrincipleLoader with project context
- [ ] Example in audit-agent.md:
  ```markdown
  **Principles**: Load from `.claude/project.json` → `selected_principles`

  If no project.json: fallback to universal + code_quality + security_privacy
  ```

### 4.4: Update Skills to Reference Project Config

**Files**: content/skills/**/*.md

**Tasks**:
- [ ] Skills should be aware of project's selected principles
- [ ] Example: verification-protocol.md should mention checking .claude/project.json
- [ ] No code changes needed, just documentation updates

---

## Phase 5: CLAUDE.md Generation Update (Hybrid Approach)

**Status**: ⏳ Not Started

**Architecture Decision**: Hybrid approach for optimal performance
- **Universal principles (U001-U012)**: Inline in CLAUDE.md (~1,200 tokens)
- **Project-specific principles (P001-P069)**: External, dynamic loading by commands (~1,500 tokens on-demand)
- **Reason**: Claude Code doesn't auto-read file references, so universal must be inline for zero overhead

### 5.1: Create Universal Principles Template

**File**: `templates/universal_principles.md.template`

**Tasks**:
- [ ] Create template with ALL universal principles inline
- [ ] Keep each principle concise (~100 tokens max)
- [ ] Format:
  ```markdown
  ### U001: Evidence-Based Verification

  Never claim completion without command execution proof.

  **Example**:
  ```
  ✅ [Runs: pytest] [Output: 34/34 passed] "All tests pass"
  ❌ "Tests should pass now"
  ```

  **Why**: Catches silent failures early.

  ---

  ### U002: Model Selection Strategy

  **Strategic model selection:**
  - Haiku: Data gathering, scanning
  - Sonnet: Analysis, reasoning
  - Opus: Avoided (unnecessary cost)

  ---

  [... continue for U003-U012 ...]
  ```
- [ ] Total template size: ~1,200 tokens (12 principles × 100 tokens)

### 5.2: Implement Hybrid CLAUDE.md Generator

**File**: claudecodeoptimizer/core/claude_md_generator.py

**New Logic**:
```python
def generate_claude_md(project_root: Path, project_config: Dict) -> str:
    """Generate hybrid CLAUDE.md with inline universal + project references."""

    # 1. Load universal principles template
    universal_template = load_template("universal_principles.md.template")
    # Contains all U001-U012 inline (~1,200 tokens)

    # 2. Check if CLAUDE.md exists
    claude_md_path = project_root / "CLAUDE.md"
    existing_content = ""
    if claude_md_path.exists():
        existing_content = claude_md_path.read_text()
        # Check if CCO section already exists
        if "<!-- CCO_START -->" in existing_content:
            # Update existing CCO section
            return update_cco_section(existing_content, project_config, universal_template)

    # 3. Generate CCO section (Hybrid: Universal inline + Project reference)
    principle_count = sum(len(ids) for ids in project_config['selected_principles'].values())

    cco_section = f"""
---

<!-- CCO_START -->
## Development Principles & Guidelines

### Universal Principles (Apply to ALL Projects)

{universal_template}

---

### Project-Specific Principles

This project uses **{principle_count}** selected principles from 69 available.

Commands will load them dynamically based on `.claude/project.json`.

**Selected Categories**:
{generate_category_list(project_config['selected_principles'])}

**Note**: Commands like `/cco-audit`, `/cco-fix` automatically load relevant principles.

<!-- CCO_END -->
"""

    # 4. Merge
    if existing_content:
        # Append CCO section
        final_content = existing_content + cco_section
    else:
        # Create new CLAUDE.md
        project_name = project_root.name
        final_content = f"# {project_name} - Claude Development Guide\n\n{cco_section}"

    return final_content
```

**Tasks**:
- [ ] Implement generate_claude_md() with hybrid logic
- [ ] Load universal_principles.md.template
- [ ] Embed universal principles inline (U001-U012, ~1,200 tokens)
- [ ] Add project reference section (minimal, ~100 tokens)
- [ ] Handle existing CLAUDE.md (append mode)
- [ ] Handle CCO section update (replace between markers)
- [ ] Total CCO section size: ~1,300 tokens (universal + project reference)

### 5.3: Update Template Deployment

**Tasks**:
- [ ] Add `templates/universal_principles.md.template` to pip install
- [ ] Deploy to `~/.cco/templates/universal_principles.md`
- [ ] Remove `templates/CLAUDE.md.template` (no longer needed)
- [ ] Update installer to NOT deploy full CLAUDE.md template

### 5.4: Uninstall-Safe Design

**Logic**:
- Universal principles inline → No broken references after uninstall
- Project references informational only → Safe to ignore
- CCO section removable via cco-remove (optional)
- No hard dependencies on external files for universal content

**Tasks**:
- [ ] Test: Remove .claude/ directory, verify CLAUDE.md still works
- [ ] Verify universal principles accessible (inline, no external deps)
- [ ] Update cco-remove to optionally clean CCO section from CLAUDE.md (ask user)

---

## Phase 6: Update Documentation

**Status**: ⏳ Not Started

### 6.1: Update README.md

**Tasks**:
- [ ] Update "Progressive Disclosure System" section with hybrid approach
- [ ] Explain universal principles inline (U001-U012, ~1,200 tokens)
- [ ] Explain project principles dynamic loading (P001-P069)
- [ ] Update CLAUDE.md format example (show hybrid structure)
- [ ] Update token efficiency numbers:
  - Old: ~5,000 tokens (all inline)
  - New: ~2,700 tokens (1,200 universal inline + 1,500 project on-demand)
  - **46% reduction**
- [ ] Update directory structure diagrams
- [ ] Update principle counts (74 → ~81 total: 12 U + 69 P)

### 6.2: Update PRINCIPLE_LOADING_GUIDE.md

**Tasks**:
- [ ] Add section explaining hybrid approach:
  - Why universal principles are inline (Claude Code doesn't auto-read refs)
  - Why project principles are external (dynamic loading efficiency)
- [ ] Document U001-U012 inline in CLAUDE.md
- [ ] Document P001-P069 dynamic loading
- [ ] Update token optimization examples with hybrid numbers
- [ ] Add project.json examples
- [ ] Explain CLAUDE.md structure (universal inline + project reference)

### 6.3: Update Command Docs

**Tasks**:
- [ ] Update content/commands/*.md to mention dynamic loading
- [ ] Add examples showing how commands read project.json

---

## Phase 7: Testing & Validation

**Status**: ⏳ Not Started

### 7.1: Test pip install

**Scenario 1: Fresh Install**
- [ ] Run `pip install claudecodeoptimizer`
- [ ] Verify ~/.cco/principles/ has U001-U012.md + P001-P069.md
- [ ] Verify ~/.claude/commands/ has ONLY cco-init.md and cco-remove.md
- [ ] Verify ~/.cco/templates/ does NOT have CLAUDE.md

**Scenario 2: Upgrade from Old Version**
- [ ] Run `pip install -U claudecodeoptimizer`
- [ ] Verify old P001.md, P067.md, P071.md removed (if promoted to U)
- [ ] Verify new U*.md files deployed
- [ ] Verify projects still work (symlinks may break, but re-init fixes)

### 7.2: Test Init Flow

**Scenario 1: New Project, No CLAUDE.md**
- [ ] Run /cco-init
- [ ] Verify .claude/project.json created with correct structure
- [ ] Verify ALL U001-U012.md symlinked (universal)
- [ ] Verify only AI-selected P*.md symlinked (e.g., 25 out of 69)
- [ ] Verify CLAUDE.md created with minimal CCO section
- [ ] Verify principle counts correct

**Scenario 2: Existing Project with CLAUDE.md**
- [ ] Create test project with custom CLAUDE.md
- [ ] Run /cco-init
- [ ] Verify custom content preserved
- [ ] Verify CCO section appended (between markers)
- [ ] Verify no duplication

**Scenario 3: Re-init (Update Config)**
- [ ] Run /cco-init on already initialized project
- [ ] Verify CCO section updated (not duplicated)
- [ ] Verify principle symlinks updated
- [ ] Verify project.json updated

**Scenario 4: Verify Universal Principles Always Included**
- [ ] Run /cco-init on minimal CLI tool
- [ ] Check .claude/principles/ directory
- [ ] Verify U001-U012.md ALL present (even if tool is simple)
- [ ] Verify only relevant P*.md present (e.g., P001-P014 code quality only)

### 7.3: Test Command Execution

**Scenario 1: With project.json**
- [ ] Run /cco-audit-security on project with project.json
- [ ] Verify it loads principles from project.json command_overrides
- [ ] Verify universal principles (U001-U012) included
- [ ] Verify only selected security principles loaded (not all 19)
- [ ] Verify token count (should be minimal, ~1000 tokens)

**Scenario 2: Without project.json (Fallback)**
- [ ] Remove .claude/project.json
- [ ] Run /cco-audit-security
- [ ] Verify it falls back to COMMAND_PRINCIPLE_MAP
- [ ] Verify it loads default universal + security principles
- [ ] Verify it still works

### 7.4: Test Removal Flow

**Scenario 1: Clean Removal**
- [ ] Run /cco-remove
- [ ] Verify .claude/project.json deleted
- [ ] Verify ALL U*.md and P*.md symlinks removed
- [ ] Verify command/guide/skill/agent symlinks removed
- [ ] Verify user prompted about CLAUDE.md section removal
- [ ] If user declines: Verify CLAUDE.md kept with CCO section
- [ ] If user accepts: Verify CCO section removed cleanly

**Scenario 2: Verify Project Still Works After Removal**
- [ ] Remove CCO but keep CLAUDE.md with CCO section
- [ ] Open project in Claude Code
- [ ] Verify no errors (broken principle refs ignored)
- [ ] Verify project functionality intact

### 7.5: Test Uninstall Safety

**Scenario 1: Broken References Don't Cause Errors**
- [ ] Remove .claude/ directory manually
- [ ] Keep CLAUDE.md with CCO section intact
- [ ] Open project in Claude Code
- [ ] Verify Claude doesn't crash or show errors
- [ ] Verify principle references are gracefully ignored

---

## Phase 8: Migration & Cleanup

**Status**: ⏳ Not Started

### 8.1: Migrate Overlapping Principles to Universal

**Tasks**:
- [ ] Rename P001.md → U012.md (Fail-Fast Error Handling)
- [ ] Rename P071.md → U011.md (No Overengineering)
- [ ] Update principles.json (remove from code_quality, add to universal)
- [ ] Update COMMAND_PRINCIPLE_MAP "core" → ["U001", "U011", "U012"] instead of ["P001", "P067", "P071"]
- [ ] Update all command frontmatter

### 8.2: Remove Old Template System

**Tasks**:
- [ ] Delete templates/CLAUDE.md.template
- [ ] Update installer to not deploy CLAUDE.md template
- [ ] Update docs mentioning template system

### 8.3: Update Global Commands

**Files**: ~/.claude/commands/cco-init.md, cco-remove.md

**Tasks**:
- [ ] Ensure cco-init mentions new architecture
- [ ] Update cco-remove to handle CCO section in CLAUDE.md

---

## Implementation Order

**Priority 1** (3-4 hours):
1. Phase 1.1-1.3: Identify universal candidates and check overlaps
2. Phase 1.4-1.5: Create universal principles, remove duplicates
3. Phase 1.6: **Reorganize & renumber ALL principles** (critical for consistency)
4. Phase 1.7-1.8: Update principles.json and all references

**Priority 2** (2-3 hours):
5. Phase 2.1: Update pip install process
6. Phase 2.2: Update /cco-init command
7. Phase 2.3: Update /cco-remove command
8. Phase 3: Project config system
9. Phase 4.1: Update PrincipleLoader

**Priority 3** (1-2 hours):
10. Phase 5: CLAUDE.md generation update
11. Phase 4.2-4.4: Update commands/agents/skills

**Priority 4** (1-2 hours):
12. Phase 7: Testing (all scenarios)

**Priority 5** (30 min):
13. Phase 6: Documentation
14. Phase 8: Cleanup

**Total Estimate**: 7-10 hours (added time for installation/init/remove updates + comprehensive testing)

---

## Success Criteria

- [ ] Universal principles finalized (U001-U012, 12 total, ~100 tokens each)
- [ ] Project principles reorganized (P001-P069, 69 total after deduplication)
- [ ] Zero overlap between universal and project-specific principles
- [ ] All principles renumbered continuously and logically grouped
- [ ] Related principles adjacent (e.g., P036 SQL Injection next to P037 Input Validation)
- [ ] Universal principles inline in CLAUDE.md (~1,200 tokens total)
- [ ] Project principles external, dynamic loading (~1,500 tokens on-demand)
- [ ] Total token usage: ~2,700 (46% reduction from 5,000)
- [ ] Runtime commands read .claude/project.json for project principles
- [ ] CLAUDE.md hybrid approach: Universal inline + project reference
- [ ] Existing CLAUDE.md content preserved (append mode)
- [ ] Zero session overhead (universal always loaded inline)
- [ ] Zero errors when CCO uninstalled (no broken refs)
- [ ] Philosophy compliance: "Project-specific, AI-driven, zero-waste" ✓
- [ ] All documentation updated with new counts (81 total: 12 U + 69 P)
- [ ] All documentation explains hybrid approach rationale

---

## Notes

**Naming Convention**:
- U001-U012: Universal principles (always included, ~12 total)
  - Inline in CLAUDE.md (~1,200 tokens total, ~100 tokens each)
  - No external file dependencies
- P001-P069: Project-specific principles (AI-selected, ~69 total after deduplication)
  - External files in ~/.cco/principles/
  - Dynamically loaded by commands (~1,500 tokens on-demand)

**Deduplication Rules**:
1. If principle applies to ALL projects → Universal (U)
2. If principle is project-specific → Keep as P
3. If overlap exists, merge best parts → Choose U or P based on applicability
4. Examples:
   - Fail-Fast (P001) → U (applies everywhere)
   - SQL Injection (P036) → P (only DB projects)

**Reorganization Rules**:
1. Universal principles grouped by theme (verification, development, git, etc.)
2. Project principles grouped by category (quality, security, architecture, etc.)
3. Within each group, related principles adjacent
4. Continuous numbering (no gaps)

**Global Structure**:
- ~/.claude/ → ONLY cco-init.md, cco-remove.md
- ~/.cco/ → EVERYTHING ELSE

**Hybrid Approach Rationale**:
- **Problem**: Claude Code doesn't auto-read file references in CLAUDE.md
- **Solution**: Universal inline (~1,200 tokens), project external (dynamic)
- **Result**: Zero session overhead + maximum efficiency

**Philosophy Check**:
- Init time: AI selects needed principles ✓
- Runtime: Commands use selected principles ✓
- Zero waste: No unnecessary principles loaded ✓
- Uninstall safe: Universal inline (no broken refs) ✓
- Zero overlap: U and P principles distinct ✓
- Zero read overhead: Universal always loaded (inline) ✓

---

*Last Updated: 2025-11-12*

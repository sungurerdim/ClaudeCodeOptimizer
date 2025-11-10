# ClaudeCodeOptimizer - TODO & Roadmap

**Last Updated**: 2025-11-10  
**Current Version**: 0.1.0-alpha  
**Target**: v0.2.0 Production Readiness (2 weeks)

**📌 Completed Tasks**: See DONE.md

---

## 🎯 CURRENT SPRINT: Init System Completion & File Generation

**Priority**: 🔴 CRITICAL  
**Estimated Effort**: 16 hours (Faz 1-2)  
**Goal**: Complete init system için eksik features ve file generation  

**Tamamlanma Oranı**: %75 → %95 (hedef)

---

## 🔥 FAZ 1: Kritik Düzeltmeler (P0 - 4 saat)

### Task 1.1: Template Dosyaları Oluştur
**Öncelik**: 🔴 CRITICAL  
**Süre**: 2 saat

**Sorun**: `.editorconfig` ve `.pre-commit-config.yaml` içerikleri kod içinde hardcoded.

**Yapılacaklar**:
- [ ] `templates/.editorconfig.template` oluştur
- [ ] `templates/.pre-commit-config.yaml.template` oluştur  
- [ ] `orchestrator.py`'deki hardcoded içerikleri kaldır, template'lerden oku

**Verification**:
```bash
ls templates/.editorconfig.template
ls templates/.pre-commit-config.yaml.template
cat .editorconfig  # After init
```

---

### Task 1.2: Quick Mode Optimization  
**Öncelik**: 🔴 CRITICAL  
**Süre**: 1 saat

**Sorun**: Quick mode HEPSİ guide/skill/agent'ı seçiyor, recommendation kullanmıyor.

**Yapılacaklar**:
- [ ] `orchestrator.py` line 609-611 düzelt:
  ```python
  # DOĞRU:
  if self.mode == "quick":
      self.selected_guides = self._recommend_guides_for_project()
      self.selected_agents = self._recommend_agents_for_project()  # NEW
      self.selected_skills = self._recommend_skills_for_project()
  ```

---

### Task 1.3: Agent Recommendation Logic  
**Öncelik**: 🔴 CRITICAL  
**Süre**: 1 saat

**Sorun**: Agent'lar için context-aware recommendation yok.

**Yapılacaklar**:
- [ ] `orchestrator.py` içinde `_recommend_agents_for_project()` ekle
- [ ] Interactive mode'da agent selection UI iyileştir (descriptions, numbers)

---

## 🟡 FAZ 2: Eksik File Generation (P1 - 12 saat)

### Task 2.1: PR Template + CODEOWNERS + VSCode Settings  
**Öncelik**: 🟡 HIGH  
**Süre**: 4 saat

**Yapılacaklar**:
- [ ] `templates/pull_request_template.md.template` oluştur
- [ ] `templates/CODEOWNERS.template` oluştur  
- [ ] `templates/.vscode-settings.json.template` oluştur
- [ ] `orchestrator.py` içinde generation methods ekle

---

### Task 2.2: GitLab CI Support  
**Öncelik**: 🟡 HIGH  
**Süre**: 4 saat

**Yapılacaklar**:
- [ ] `templates/.gitlab-ci.yml.template` oluştur
- [ ] `_generate_gitlab_ci()` method ekle (dil bazlı)
- [ ] `ci_provider == "gitlab_ci"` ise generate et

---

### Task 2.3: Progressive Disclosure - Principle Categories  
**Öncelik**: 🟡 HIGH  
**Süre**: 4 saat  
**Token Savings**: 10x (5000 → 500 token)

**Yapılacaklar**:
- [ ] `~/.cco/knowledge/principles/core.md` (P001, P067, P071-P074)
- [ ] `~/.cco/knowledge/principles/code-quality.md` (P002-P018)
- [ ] `~/.cco/knowledge/principles/security.md` (P019-P037)
- [ ] `~/.cco/knowledge/principles/testing.md` (P038-P043)
- [ ] `~/.cco/knowledge/principles/architecture.md` (P044-P053)
- [ ] `~/.cco/knowledge/principles/performance.md` (P054-P058)
- [ ] `~/.cco/knowledge/principles/operations.md` (P059-P066)
- [ ] `~/.cco/knowledge/principles/git-workflow.md` (P072-P074)
- [ ] CLAUDE.md güncelle: Sadece core + category links
- [ ] Commands'da kategori dosyalarını referans et

---

## 🟢 FAZ 3-4: Advanced Features (P2-P3 - 32 saat)

**Not**: Faz 1-2 tamamlandıktan sonra değerlendirilecek.

- Context Matrix (6h)
- UI Adapter - Claude Code Rich UI (6h)
- P074 - Automated Versioning Implementation (4h)
- Enhanced Decision Points (16h)

---

## 📋 KALAN TASKLAR (v0.2.0 Öncesi)

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

### v0.2.0 Release Checklist

**Before Release**:
- [ ] All P0 tasks complete (wshobson/agents integration)
- [ ] All critical tasks complete
- [ ] Test coverage ≥60%
- [ ] Zero try-except-pass
- [ ] Type annotations complete
- [ ] CI/CD green
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

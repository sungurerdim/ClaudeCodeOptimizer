# CCO Principles Index

**Complete reference for all CCO principles**

---

## Summary

**Total Principles**: 13

**Categories**:
- **Universal (cco-principle-u-*)**: 8 - Core development best practices (apply everywhere)
- **Claude-Specific (cco-principle-c-*)**: 5 - Optimizations for Claude Code

> **Note**: Project-specific principles (formerly P_*) have been integrated into domain-specific skills for better organization. See [Skills Catalog](../skills/) for security, testing, architecture, and other domain guidance.

---

## Table of Contents

- [Universal Principles (cco-principle-u-*)](#universal-principles-cco-principle-u-)
- [Claude-Specific Principles (cco-principle-c-*)](#claude-specific-principles-cco-principle-c-)
- [Integrated Domain Guidance](#integrated-domain-guidance)

---

## Universal Principles (cco-principle-u-*)

**Core development best practices - Apply everywhere**

These principles are fundamental to all development work, regardless of language, framework, or project type.

### 1. cco-principle-u-change-verification

**Verify all changes BEFORE claiming completion**

- Never claim "done" without evidence
- Run commands, check outputs, confirm results
- Prevents incomplete work and integration failures

**File**: `cco-principle-u-change-verification.md`

---

### 2. cco-principle-u-cross-platform-compatibility

**Use cross-platform compatible bash commands and paths**

- Always forward slashes (Windows accepts them)
- Git Bash commands (ls, grep, cat, find)
- Quote paths with spaces

**File**: `cco-principle-u-cross-platform-compatibility.md`

---

### 3. cco-principle-u-dry

**Every piece of knowledge must have a single, unambiguous representation**

- No duplicate functions or data
- Database = truth, cache = derived
- Configuration defined once, referenced everywhere

**File**: `cco-principle-u-dry.md`

---

### 4. cco-principle-u-evidence-based-analysis

**Never claim completion without command execution proof**

- Show command output, exit codes, timestamps
- Use 5 Whys for root cause analysis
- Fix at source, not symptom
- Complete accounting (all items have disposition)
- Accurate outcome categorization

**File**: `cco-principle-u-evidence-based-analysis.md`

---

### 5. cco-principle-u-follow-patterns

**Always follow existing code patterns and conventions**

- Examine existing code first
- Match naming conventions exactly
- Consistency > personal preference

**File**: `cco-principle-u-follow-patterns.md`

---

### 6. cco-principle-u-minimal-touch

**Edit only required files - No drive-by improvements**

- Touch ONLY files REQUIRED for task
- No scope creep, no "while I'm here" changes
- Surgical, focused edits only

**File**: `cco-principle-u-minimal-touch.md`

---

### 7. cco-principle-u-no-hardcoded-examples

**Never use hardcoded examples in templates**

- Use placeholders: {FILE_PATH}, {LINE_NUMBER}, {FUNCTION_NAME}
- AI models cannot distinguish example from real data
- Runtime outputs must use actual project data

**File**: `cco-principle-u-no-hardcoded-examples.md`

---

### 8. cco-principle-u-no-overengineering

**Choose simplest solution - Avoid premature abstraction**

- Solve current problem, not hypothetical ones
- Extract abstractions after 3rd duplication (Rule of Three)
- Simple > complex, always

**File**: `cco-principle-u-no-overengineering.md`

---

## Claude-Specific Principles (cco-principle-c-*)

**Optimizations for Claude Code - Claude AI best practices**

These principles optimize Claude Code's behavior for efficiency, cost, and quality.

### 1. cco-principle-c-context-window-mgmt

**Optimize context via targeted reads and strategic model selection**

- Grep → Preview → Precise Read (3-stage strategy)
- Use offset+limit for large files
- Parallel operations where independent

**File**: `cco-principle-c-context-window-mgmt.md`

---

### 2. cco-principle-c-efficient-file-operations

**Grep-first: discovery → preview → precise read**

- Stage 1: files_with_matches (find which files)
- Stage 2: content with context (verify relevance)
- Stage 3: targeted Read with offset+limit (exact section)

**File**: `cco-principle-c-efficient-file-operations.md`

---

### 3. cco-principle-c-native-tool-interactions

**All user interactions must use native Claude Code tools**

- Use AskUserQuestion (not text prompts)
- Every multiSelect must have "All" option first
- Consistent UI, validation, accessibility

**File**: `cco-principle-c-native-tool-interactions.md`

---

### 4. cco-principle-c-no-unsolicited-file-creation

**Never create files unless explicitly requested**

- Prefer editing existing files
- Always ask before creating documentation
- No unsolicited temp files

**File**: `cco-principle-c-no-unsolicited-file-creation.md`

---

### 5. cco-principle-c-project-context-discovery

**Use Haiku sub-agent to extract project context before analysis**

- Read README, CONTRIBUTING, ARCHITECTURE docs
- Extract goals, conventions, tech stack
- Align findings with project objectives

**File**: `cco-principle-c-project-context-discovery.md`

---

## Integrated Domain Guidance

**Project-specific best practices are now in skills**

Domain-specific guidance (formerly P_* principles) has been consolidated into specialized skills for better organization and contextual activation:

Skills are dynamically discovered from ~/.claude/skills/. Run /cco-status to see all.

Skills are auto-activated based on context and provide comprehensive guidance for each domain.

---

## Using Principles

### In CLAUDE.md

Principles are automatically injected via markers:

```markdown
<!-- CCO_PRINCIPLES_START -->
@principles/cco-principle-u-change-verification.md
@principles/cco-principle-u-cross-platform-compatibility.md
@principles/cco-principle-u-dry.md
@principles/cco-principle-u-evidence-based-analysis.md
@principles/cco-principle-u-follow-patterns.md
@principles/cco-principle-u-minimal-touch.md
@principles/cco-principle-u-no-hardcoded-examples.md
@principles/cco-principle-u-no-overengineering.md
@principles/cco-principle-c-context-window-mgmt.md
@principles/cco-principle-c-efficient-file-operations.md
@principles/cco-principle-c-native-tool-interactions.md
@principles/cco-principle-c-no-unsolicited-file-creation.md
@principles/cco-principle-c-project-context-discovery.md
<!-- CCO_PRINCIPLES_END -->
```

See [ADR-001: Marker-based CLAUDE.md System](../../docs/ADR/001-marker-based-claude-md.md)

### Principle Selection

- **Universal (cco-principle-u-*)**: Always loaded (dynamically discovered)
- **Claude (cco-principle-c-*)**: Always loaded (dynamically discovered)
- **Domain Skills**: Auto-activated based on project context

---

## Principle Compliance

All CCO components (commands, skills, agents) follow these principles:

- ✅ No hardcoded examples (cco-principle-u-no-hardcoded-examples)
- ✅ Native tool interactions (cco-principle-c-native-tool-interactions)
- ✅ Evidence-based with complete accounting (cco-principle-u-evidence-based-analysis)
- ✅ Follow existing patterns (cco-principle-u-follow-patterns)
- ✅ Cross-platform compatibility (cco-principle-u-cross-platform-compatibility)

See [PR Template](../../.github/PULL_REQUEST_TEMPLATE.md) for full compliance checklist.

---

**Total**: Dynamically discovered from ~/.claude/ directories

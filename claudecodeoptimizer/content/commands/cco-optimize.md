---
name: cco-optimize
description: Comprehensive optimization - context deduplication, code quality, performance, and cross-source duplication detection (CLAUDE.md + system prompt awareness)

parameters:
  context:
    keywords: [slim context, optimize rules, compress claude.md, system prompt, deduplication]
    category: context
  code-quality:
    keywords: [refactor, complexity, dead code, unused imports, code smell, lint]
    category: quality
  performance:
    keywords: [optimize performance, slow code, n+1, caching, profiling, bottleneck]
    category: performance
  markdown:
    keywords: [slim markdown, optimize docs, compress documentation, reduce tokens]
    category: documentation
  claude-tools:
    keywords: [slim skills, optimize agents, compress commands, reduce tool tokens]
    category: tooling
  all:
    keywords: [full optimization, comprehensive, everything]
    category: all
---

# CCO Optimize: Comprehensive Codebase Optimization

**Three pillars: Context Optimization | Code Quality | Performance**

**NEW: Cross-source duplication detection (CLAUDE.md + system prompt awareness)**
---


## Execution Guarantee

**This command WILL execute fully without requiring user presence during processing.**

**What Happens:**
1. **Step 0**: Introduction, mode selection, category selection (user input required)
2. **Step 0.5**: Project context discovery (optional, user choice)
3. **Discovery**: File categorization and token measurement (automated)
4. **Analysis**: Optimization opportunity identification (automated)
5. **Pre-Flight**: Summary and confirmation (user input required)
6. **Optimization**: Apply changes with verification (fully automated)
7. **Final Report**: Complete accounting and metrics (automated)

**User Interaction Points:**
- Mode selection (Conservative/Balanced/Aggressive)
- Category selection (what to optimize)
- Project context discovery (optional)
- Pre-flight confirmation
- Agent error handling (if failures occur)

**Automation:**
- All file discovery, analysis, optimization, verification runs without interruption
- Agents handle batch processing in parallel
- Complete accounting enforced (total = applied + skipped + rolled_back)
- Quality safeguards automated (syntax, semantic, effectiveness checks)

**Time Estimate:**
- Small projects (<100 files): 5-10 minutes
- Medium projects (100-500 files): 10-20 minutes
- Large projects (>500 files): 20-40 minutes

**Verification:**
- Every optimization verified before acceptance
- Rollback on quality degradation
- Accounting formula enforced: `total = applied + skipped + rolled_back`

---

## Design Principles


**Slim-Specific:**
1. **Context First** - CLAUDE.md duplication elimination (primary mission)
2. **Quality > Tokens** - Never sacrifice meaning, effectiveness, completeness
3. **Verification Heavy** - Every optimization verified before acceptance
4. **Conservative Default** - 100% safe optimizations only (unless user opts-in)

## Mission Statement

**COMPREHENSIVE OPTIMIZATION across three pillars:**

### Pillar 1: Context Optimization (--context)
- Eliminate CLAUDE.md duplication (skills/agents/commands loading same files)
- **NEW: Cross-source duplication detection** - Detect content in CLAUDE.md that duplicates system prompt
- Detect incomplete content (stubs, TODOs, missing implementations)
- Token reduction without quality loss

### Pillar 2: Code Quality Optimization (--code-quality)
- Dead code detection and removal (unused imports, unreachable code)
- Complexity reduction (functions >10 cyclomatic complexity)
- Code smell detection (long methods, god classes, feature envy)
- Lint/format violations

### Pillar 3: Performance Optimization (--performance)
- N+1 query detection
- Missing index suggestions
- Caching opportunities
- Slow algorithm detection
- Resource leak identification

### Cross-Source Duplication Detection (--context mode)

**System Prompt Awareness:**

Claude Code's system prompt already includes guidance for:
- Git commit/PR workflow
- Tool usage policies
- File operations best practices
- Security testing guidelines
- Task management

**CLAUDE.md content that duplicates these is REDUNDANT.**

Detection algorithm:
```python
SYSTEM_PROMPT_TOPICS = [
    "git commit", "pull request", "PR creation",
    "tool usage", "bash commands", "file operations",
    "security testing", "task management", "todo tracking",
    "code review", "professional objectivity"
]

def detect_system_prompt_duplication(claude_md_content: str) -> List[dict]:
    """Find CLAUDE.md content that duplicates system prompt."""
    duplications = []

    for topic in SYSTEM_PROMPT_TOPICS:
        if topic.lower() in claude_md_content.lower():
            duplications.append({
                "topic": topic,
                "recommendation": f"Content about '{topic}' may duplicate system prompt",
                "action": "Review and remove if redundant"
            })

    return duplications
```


---

## Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific:**
- **Primary Mission**: Eliminate CLAUDE.md duplication, detect incomplete content, optimize context
- **What You'll Be Asked**: Mode (Conservative/Balanced/Aggressive) → Categories → Scope → Context discovery (optional) → Confirmation
- **Time**: Setup 2-3min | Processing 5-40min (automated) | Total ~10-45min
- **Quality Guarantees**: Semantic preservation verified, backups created, rollback on degradation

---

## Execution Flow

```
/cco-optimize-context-usage
    │
    ├─► Step 0: Introduction & Confirmation
    │
    ├─► Mode Selection (Conservative/Balanced/Aggressive)
    │
    ├─► Category Selection (What to optimize)
    │
    ├─► Step 0.5: Project Context Discovery (Optional)
    │
    ├─► Discovery Phase (Categorize files, measure tokens)
    │
    ├─► Analysis Phase (Find optimization opportunities)
    │
    ├─► Pre-Flight Summary (Show what will change)
    │
    ├─► Optimization Phase (Apply changes with verification)
    │
    ├─► Verification Phase (Semantic + quality checks)
    │
    └─► Final Report (Token reduction, quality metrics, accounting)
```

---

## Component 1: Mode Selection

**Pattern:** Pattern 2 (Multi-Select with "All")

**Slim-Specific Modes:**
- **Conservative** (Recommended): 100% safe (whitespace, unused, formatting), zero risk, quality guaranteed
- **Balanced**: Safe + verified low-risk, quality checks + rollback on degradation
- **Aggressive**: All techniques, manual review required, highest risk

**Goal: Maximum optimization while preserving quality (no artificial caps).**

**Optional Context**: Add prompt after flags: `/cco-optimize-context-usage --balanced "Prioritize docs"`

---

## Component 2: Category Selection

**Pattern:** Pattern 2 (Multi-Select with "All")

**Optimization Categories:**

| Category | Flag | Description | Impact |
|----------|------|-------------|--------|
| **Context** | `--context` | CLAUDE.md deduplication, system prompt awareness, token reduction | HIGH |
| **Code Quality** | `--code-quality` | Dead code, complexity, code smells, lint violations | MEDIUM |
| **Performance** | `--performance` | N+1 queries, missing indexes, caching, slow algorithms | HIGH |
| **Markdown** | `--markdown` | Documentation token reduction, verbosity elimination | LOW |
| **Claude Tools** | `--claude-tools` | Skills, agents, commands optimization | MEDIUM |
| **All** | `--all` | Comprehensive optimization across all categories | FULL |

**System Prompt Duplication Warning:**
When `--context` selected, command will analyze CLAUDE.md against known system prompt topics and flag potential duplications.

---

## Component 2.5: Project Scope Detection


**Slim-Specific Scope:**
1. **Detect Project Root**: Git root or cwd
2. **File Discovery**: Apply exclusions (node_modules, dist, build, lock files), categorize remaining
3. **Detect Out-of-Project References**: Search for ~/.claude/*, absolute paths outside project
4. **Ask User**: Project only (recommended) | Project + external | External only | Cancel
5. **Final Scope**: Display total files, tokens, warnings if out-of-project included

---

## Component 3: Discovery Phase


**Slim-Specific Discovery:**
1. **File Exclusion**: Apply FIRST (build artifacts, dependencies, lock files)
2. **File Categorization**: Explore agent categorizes by patterns (markdown, code, tools, active context)
3. **Token Measurement**: Count lines/tokens, calculate redundancy/whitespace, aggregate by category
4. **Display Results**: Total files, tokens by category, top opportunities, estimated reduction

---

## Component 4: Analysis Phase


**Slim-Specific Analysis:**
- **Model Selection**: Conservative→Haiku | Balanced/Aggressive→Sonnet
- **Analysis Focus**: Whitespace, dead code, verbosity, examples, DRY, rewrites (based on mode)
- **Output**: Optimization opportunities list, estimated token savings

# Handle analysis errors
if analysis_result is None or (isinstance(analysis_result, dict) and "error" in analysis_result):
    error_msg = analysis_result.get('error', 'Unknown error') if isinstance(analysis_result, dict) else 'Agent returned None'

    response = AskUserQuestion({
        questions: [{
            question: f"Explore agent ({agent_model.capitalize()}) optimization analysis failed: {error_msg}. How to proceed?",
            header: f"Explore ({agent_model.capitalize()}) Error",
            multiSelect: false,
            options: [
                {label: "Retry", description: f"Run {mode} analysis again"},
                {label: "Retry", description: "Retry the operation"},
                {label: "Switch to Conservative", description: "Use Conservative mode instead (safer, fewer optimizations)"},
                {label: "Manual analysis", description: "Guide manual optimization identification"},
                {label: "Cancel", description: "Stop cco-optimize-context-usage"}
            ]
        }]
    })

    if response == "Retry":
        # Retry with same model
        analysis_result = Task({
            subagent_type: "Explore",
            model: agent_model,
            description: f"Find {mode} optimizations (retry)",
            prompt: # ... same prompt as above
        })
    elif response == "Retry":
        # Retry with more capable model
        # Let Claude Code decide the model
        analysis_result = Task({
            subagent_type: "Explore",
            model: new_model,
            description: f"Find {mode} optimizations (retry with {new_model})",
# Parse analysis result
if isinstance(analysis_result, str):
    try:
        optimizations = json.loads(analysis_result)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse analysis result as JSON. Raw result: {analysis_result[:200]}...")
        optimizations = []
elif isinstance(analysis_result, list):
    optimizations = analysis_result
else:
    print(f"Warning: Unexpected analysis result type: {type(analysis_result)}")
    optimizations = []

# Validate optimizations
total_token_savings = sum(opt.get("token_saving", 0) for opt in optimizations)
print(f"""
Analysis Complete:
- Mode: {mode}
- Model used: {agent_model}
- Optimizations found: {len(optimizations)}
- Estimated token savings: {total_token_savings:,} tokens
""")
```

### Optimization Categorization

```python
# Categorize by type for reporting
optimizations_by_type = {}
for opt in optimizations:
    opt_type = opt.get("type", "unknown")
    if opt_type not in optimizations_by_type:
        optimizations_by_type[opt_type] = []
    optimizations_by_type[opt_type].append(opt)

# Categorize by risk level
optimizations_by_risk = {
    "none": [opt for opt in optimizations if opt.get("risk") == "none"],
    "low": [opt for opt in optimizations if opt.get("risk") == "low"],
    "moderate": [opt for opt in optimizations if opt.get("risk") == "moderate"]
}

# Show breakdown
print(f"""
Optimization Breakdown:

By Type:
{chr(10).join(f"  - {type_name}: {len(opts)} optimizations (~{sum(o.get('token_saving', 0) for o in opts)} tokens)"
                for type_name, opts in optimizations_by_type.items())}

By Risk:
  - Zero risk: {len(optimizations_by_risk['none'])} optimizations
  - Low risk: {len(optimizations_by_risk['low'])} optimizations
  - Moderate risk: {len(optimizations_by_risk['moderate'])} optimizations
""")
```

---

## Component 4.5: Agent Optimization Strategy


**Slim-Specific Strategy:**
- **Parallel Processing**: Group files by category (markdown/code/tools), analyze all groups simultaneously
- **Model Selection**: Haiku for mechanical (whitespace, dead code, counting) | Sonnet for semantic (consolidation, restructuring)
- **Token Efficiency**: Concise prompts (35 tokens vs 200+), three-stage discovery (140 tokens vs 3000+)
- **Error Handling**: Model escalation (Haiku fails → ask user: retry/Sonnet/skip/abort)

---

## Component 5: Pre-Flight Summary


**Slim-Specific Display:**
- **What Changes**: Files count, optimizations count, token reduction (by category, by type with risk levels)
- **What Doesn't**: Excluded files (with reasons), skipped optimizations (risk/quality)
- **Quality Safeguards**: Backup, semantic/syntax verification, rollback on degradation
- **Confirmation**: "Start Optimization" (files + time) | "Modify Selection" | "Cancel"

---

## Component 6: Optimization Phase

**Pattern:** Pattern 4 (Complete Accounting)

**Slim-Specific Optimization Loop:**
1. **For each optimization**: Backup → Apply → Verify (4 checks) → Measure tokens → Record disposition
2. **Verification Checks**:
   - Structural (syntax by file type)
   - Semantic (concepts preserved)
   - Quality (instruction count, example coverage ≥90%, concept count)
   - Effectiveness (Claude tools only: no critical steps lost)
3. **Dispositions**: applied (success) | skipped (verification failed) | rolled_back (exception)
4. **Accounting Formula**: `applied + skipped + rolled_back = total_optimizations`

---

## Component 7: Final Report


**Slim-Specific Report:**
- **Results**: Files modified, token reduction (before/after/saved)
- **Accounting**: Total with formula verification (applied + skipped + rolled_back = total) ✓
- **Quality**: Semantic/syntax/effectiveness preserved ✅
- **Conditional Sections**: Rolled back items (if any), next steps (suggest higher mode if skipped > 0)

---

## Agent Integration


**Slim-Specific Agent Strategy:**
- **Threshold**: Always use agent (no threshold) for consistent behavior
- **Batching**: >20 optimizations → parallel batches (batch_size=20, Haiku model)
- **Single Batch**: ≤20 optimizations → single agent (Haiku model)
- **Error Handling**: Ask user (Retry | Retry with Sonnet | Skip batch | Manual mode | Cancel)
- **Aggregation**: Combine batch results, verify accounting formula, report totals

---

## CLI Usage

### Interactive (Default)
```bash
/cco-optimize
```

### Parametrized (Power Users)

**Mode selection:**
```bash
/cco-optimize --conservative  # Default - 100% safe
/cco-optimize --balanced      # Safe + verified low-risk
/cco-optimize --aggressive    # All techniques, manual review
```

**Category selection:**
```bash
/cco-optimize --context       # Context + system prompt awareness
/cco-optimize --code-quality  # Dead code, complexity, smells
/cco-optimize --performance   # N+1, indexes, caching
/cco-optimize --markdown      # Documentation optimization
/cco-optimize --claude-tools  # Skills, agents, commands
/cco-optimize --all           # Everything
```

**Combined examples:**
```bash
/cco-optimize --balanced --context --code-quality
/cco-optimize --conservative --all
/cco-optimize --aggressive --performance "Focus on database queries"
```

**Dry run (preview only):**
```bash
/cco-optimize --dry-run --all
```

**System prompt duplication check only:**
```bash
/cco-optimize --context --dry-run "Check CLAUDE.md for system prompt duplications"
```

---

## Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Slim-Specific Errors:**
- **Verification Failures**: Show file, optimization type, reason, metric details (before/after/threshold), rollback confirmation
- **Rollback Required**: Show count, files restored from backup, confirm no permanent modifications

---

## Success Criteria

- [ ] Step 0: Introduction and confirmation completed
- [ ] Mode selection presented
- [ ] Category selection completed
- [ ] Step 0.5: Project context discovery (optional)
- [ ] File discovery with exclusion protocol applied
- [ ] Discovery phase measured all files
- [ ] Analysis found optimization opportunities
- [ ] Pre-flight summary displayed
- [ ] User confirmed execution
- [ ] Optimizations applied with verification
- [ ] Quality metrics verified
- [ ] Complete accounting (applied + skipped + rolled back = total)
- [ ] Final report generated (concise format)
- [ ] Backup created and documented

---

## Next Steps: Calling Other Commands (C_COMMAND_CONTEXT_PASSING)

### If Missing Content Detected

When analysis reveals stub files, incomplete docs, or missing content:

**ALWAYS provide context before calling /cco-generate:**

```markdown
CONTEXT FOR /cco-generate:
Slim analysis found {COUNT} files with missing/stub content:
- Stub files: {FILE_LIST} (contain only TODO markers/placeholders)
- Pattern reference: {COMPLETE_FILE_EXAMPLE}
- Expected structure: {STRUCTURE_DESCRIPTION}

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-generate:
Slim analysis found 8-10 incomplete skill files containing only TODO markers without actual content. Affected files: skills/cco-skill-security.md, cco-skill-testing.md, cco-skill-database.md, +5 others in ~/.claude/skills/. These need comprehensive implementation following existing skill patterns (structure with examples, checklists).

SlashCommand({command: "/cco-generate skills"})
```

**Why This Matters:**
- `/cco-generate` receives specific file list and counts
- No need to re-scan all files
- Knows exactly which files to focus on
- Understands expected structure from reference

**DON'T:**
```markdown
# ❌ BAD: No context
Found some stub files.
SlashCommand({command: "/cco-generate"})
```


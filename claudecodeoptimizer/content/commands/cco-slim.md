---
name: cco-slim
description: Token-optimized content slimming with quality preservation and semantic verification
action_type: optimize
parameters:
  markdown:
    keywords: [slim markdown, optimize docs, compress documentation, reduce tokens]
    category: documentation
  code:
    keywords: [slim code, optimize source, reduce comments, dead code]
    category: code
  claude-tools:
    keywords: [slim skills, optimize agents, compress commands, reduce tool tokens]
    category: tooling
  active-context:
    keywords: [slim principles, optimize context, compress claude.md]
    category: context
---

# CCO Slim Command

**Token optimization with guaranteed quality preservation and semantic verification.**

---

## Design Principles

1. **Quality First** - Never sacrifice meaning, effectiveness, or completeness
2. **Verification Heavy** - Every optimization verified before acceptance
3. **Conservative Default** - Only 100% safe optimizations unless user opts-in
4. **Complete Accounting** - Every file categorized, every change tracked
5. **Semantic Preservation** - Meaning preserved at all costs
6. **Honest Reporting** - Exact truth about reductions and risks
7. **No Hardcoded Examples** - All examples use placeholders

---

## CRITICAL: Quality Preservation

**AI models must preserve quality above token reduction.**

### Optimization Hierarchy (Priority Order)

```
1. PRESERVE (Highest - NEVER compromise)
   ├─ Semantic meaning
   ├─ Instruction effectiveness
   ├─ Example didactic value
   ├─ Edge case coverage
   └─ Context completeness

2. VERIFY (Before any change)
   ├─ Meaning preserved?
   ├─ Effectiveness maintained?
   ├─ Quality not degraded?
   └─ Rollback if any doubt

3. OPTIMIZE (Only if preserve + verify passed)
   ├─ True redundancy only
   ├─ Safe transformations only
   ├─ Whitespace/formatting only
   └─ Cross-referencing only
```

---

## Execution Flow

```
/cco-slim
    │
    ├─► Mode Selection (Conservative/Balanced/Aggressive)
    │
    ├─► Category Selection (What to optimize)
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

**Always start here. Quality vs compression trade-off.**

```python
AskUserQuestion({
  questions: [{
    question: "Select optimization mode:",
    header: "Mode",
    multiSelect: false,
    options: [
      {
        label: "Conservative (Recommended)",
        description: "Only 100% safe optimizations - Quality guaranteed, 10-20% reduction"
      },
      {
        label: "Balanced",
        description: "Safe + verified low-risk - Quality checks enforced, 20-35% reduction"
      },
      {
        label: "Aggressive (Not Recommended)",
        description: "All optimizations - Higher risk, manual review required, 35-50% reduction"
      }
    ]
  }]
})
```

### Mode Details

**Conservative (Default):**
- Only whitespace, formatting, provably unused code
- No semantic risk
- Quality: 100% guaranteed
- Typical reduction: 10-20%
- Recommended for: Production content, critical documentation

**Balanced:**
- Conservative + example consolidation + instruction reordering
- Quality checks before acceptance
- Rollback on degradation
- Typical reduction: 20-35%
- Recommended for: Development content, iterative improvement

**Aggressive:**
- All techniques including example reduction, detail removal
- Manual review required
- Higher risk of quality loss
- Typical reduction: 35-50%
- Recommended for: Experimental optimization, draft content

---

## Component 2: Category Selection

**Choose what to optimize.**

```python
AskUserQuestion({
  questions: [{
    question: "What do you want to optimize?",
    header: "Categories",
    multiSelect: true,
    options: [
      {
        label: "All",
        description: "Optimize all categories (comprehensive)"
      },
      {
        label: "Markdown Docs",
        description: "README, ARCHITECTURE, principles, guides (*.md)"
      },
      {
        label: "Code Files",
        description: "Source code, tests, scripts (*.py, *.js, *.ts, etc.)"
      },
      {
        label: "Claude Tools",
        description: "Skills, agents, commands (cco-skill-*, cco-agent-*, cco-*.md)"
      },
      {
        label: "Active Context",
        description: "CLAUDE.md, principles, global instructions"
      },
      {
        label: "Custom Files/Folders",
        description: "Specify your own files/folders with wildcard patterns"
      }
    ]
  }]
})
```

### If "Custom Files/Folders" Selected

**Ask for wildcard patterns using native Claude conversation.**

```python
if "Custom Files/Folders" in selected_categories:
    # Prompt user for custom patterns via native conversation
    """
## Custom File/Folder Selection

**You can specify files or folders using wildcard patterns.**

**Examples:**
```
# Single file
docs/api.md

# All markdown in a folder
docs/**/*.md

# Multiple patterns (comma-separated)
src/components/**/*.tsx, tests/**/*.test.ts

# Specific files
README.md, CONTRIBUTING.md, docs/architecture.md

# Exclude pattern (use minus prefix)
src/**/*.py, -src/generated/**

# Combine patterns
claudecodeoptimizer/content/**/*.md, src/**/*.py, -**/*_test.py
```

**Enter your patterns (comma-separated):**
"""

    # Get user input via conversation
    custom_patterns = await_user_response()

    # Parse patterns
    include_patterns = []
    exclude_patterns = []

    for pattern in custom_patterns.split(','):
        pattern = pattern.strip()
        if pattern.startswith('-'):
            exclude_patterns.append(pattern[1:].strip())
        else:
            include_patterns.append(pattern)

    # Discover files
    custom_files = []
    for pattern in include_patterns:
        matched = Glob(pattern)
        custom_files.extend(matched)

    # Apply exclusions
    for pattern in exclude_patterns:
        excluded = Glob(pattern)
        custom_files = [f for f in custom_files if f not in excluded]

    # Add to discovery
    discovered["custom"] = custom_files

    # Report back to user
    print(f"""
## Custom Files Discovered

**Patterns Matched:** {len(include_patterns)} patterns
**Files Found:** {len(custom_files)} files
**Excluded:** {len([f for f in all_matched if f not in custom_files])} files

{if len(custom_files) > 0}
**Sample Files:**
{for file in custom_files[:10]}
- {file_path}
{endfor}
{if len(custom_files) > 10}
... and {len(custom_files) - 10} more files
{endif}
{else}
**No files found** matching your patterns. Please try different patterns.
{endif}
""")

    # Confirm or modify
    if len(custom_files) == 0:
        # Ask to re-enter patterns
        return "retry_custom_patterns"
```

---

## Component 3: Discovery Phase

**Categorize all files, measure current token usage.**

### Step 1: File Discovery

```python
# Discover all relevant files
discovered = {
    "markdown": [],
    "code": [],
    "claude_tools": {
        "skills": [],
        "agents": [],
        "commands": []
    },
    "active_context": []
}

# Markdown documentation
if "Markdown Docs" in selected_categories or "All" in selected_categories:
    discovered["markdown"] = Glob("**/*.md")
    # Exclude Claude tools (handled separately)
    discovered["markdown"] = [f for f in discovered["markdown"]
                              if not f.startswith("claudecodeoptimizer/content/")]

# Code files
if "Code Files" in selected_categories or "All" in selected_categories:
    discovered["code"].extend(Glob("**/*.py"))
    discovered["code"].extend(Glob("**/*.js"))
    discovered["code"].extend(Glob("**/*.ts"))
    discovered["code"].extend(Glob("**/*.tsx"))
    discovered["code"].extend(Glob("**/*.java"))
    discovered["code"].extend(Glob("**/*.go"))
    discovered["code"].extend(Glob("**/*.rs"))

# Claude tools
if "Claude Tools" in selected_categories or "All" in selected_categories:
    discovered["claude_tools"]["skills"] = Glob("**/cco-skill-*.md")
    discovered["claude_tools"]["agents"] = Glob("**/cco-agent-*.md")
    discovered["claude_tools"]["commands"] = Glob("**/cco-*.md",
                                                   path="claudecodeoptimizer/content/commands/")

# Active context
if "Active Context" in selected_categories or "All" in selected_categories:
    claude_md_path = "~/.claude/CLAUDE.md"
    if file_exists(claude_md_path):
        discovered["active_context"].append(claude_md_path)

    # Principles referenced in CLAUDE.md
    principles = extract_principle_references(claude_md_path)
    discovered["active_context"].extend(principles)
```

### Step 2: Token Measurement

```python
@dataclass
class FileMetrics:
    """Metrics for a single file."""
    path: str
    category: str
    size_bytes: int
    line_count: int
    token_estimate: int  # Rough estimate: words * 1.3
    redundancy_score: float  # 0.0-1.0 (higher = more redundancy)
    example_count: int
    whitespace_pct: float  # Percentage of whitespace lines

def measure_file(file_path: str, category: str) -> FileMetrics:
    """Measure file metrics."""
    content = Read(file_path)
    lines = content.split('\n')

    return FileMetrics(
        path=file_path,
        category=category,
        size_bytes=len(content.encode('utf-8')),
        line_count=len(lines),
        token_estimate=estimate_tokens(content),
        redundancy_score=calculate_redundancy(content),
        example_count=count_examples(content),
        whitespace_pct=calculate_whitespace_pct(lines)
    )

# Measure all discovered files
metrics = []
for category, files in discovered.items():
    if isinstance(files, dict):  # Claude tools
        for subcategory, subfiles in files.items():
            for file in subfiles:
                metrics.append(measure_file(file, f"{category}.{subcategory}"))
    else:
        for file in files:
            metrics.append(measure_file(file, category))

# Calculate totals
total_tokens_before = sum(m.token_estimate for m in metrics)
total_files = len(metrics)
```

### Step 3: Display Discovery Results

```markdown
## Discovery Complete

**Files Discovered:** {total_files}

### By Category

| Category | Files | Tokens | Avg Tokens/File |
|----------|-------|--------|-----------------|
| Markdown Docs | {count} | {tokens} | {avg} |
| Code Files | {count} | {tokens} | {avg} |
| Claude Tools | {count} | {tokens} | {avg} |
| ├─ Skills | {count} | {tokens} | {avg} |
| ├─ Agents | {count} | {tokens} | {avg} |
| └─ Commands | {count} | {tokens} | {avg} |
| Active Context | {count} | {tokens} | {avg} |

**Total Tokens (Before):** {total_tokens_before}

### Top Opportunities

Files with highest optimization potential:

| File | Tokens | Redundancy | Examples | Opportunity |
|------|--------|------------|----------|-------------|
| {file_path} | {tokens} | {redundancy_pct}% | {examples} | {opportunity_desc} |
| {file_path} | {tokens} | {redundancy_pct}% | {examples} | {opportunity_desc} |
| {file_path} | {tokens} | {redundancy_pct}% | {examples} | {opportunity_desc} |

**Estimated Reduction:** {min_pct}%-{max_pct}% ({min_tokens}-{max_tokens} tokens)
```

---

## Component 3.5: Context Duplication Analysis

**CRITICAL: Detect duplicated context loading and recommend CLAUDE.md improvements.**

### Why This Matters

- **Duplication**: If CLAUDE.md loads `@principles/U_DRY.md` AND a skill also loads it → waste
- **Missing References**: If many skills reference a file but CLAUDE.md doesn't → inefficiency

### Step 1: Analyze CLAUDE.md References

```python
@dataclass
class ContextReference:
    """Track what's loaded in CLAUDE.md."""
    file_path: str
    ref_type: str  # "principle", "skill", "direct"
    line: int

def extract_claude_md_references(claude_md_path: str) -> List[ContextReference]:
    """Extract all file references from CLAUDE.md."""
    content = Read(claude_md_path)
    references = []

    # Find @principles/... references
    principle_refs = re.findall(r'@principles/([\w_-]+\.md)', content)
    for ref in principle_refs:
        references.append(ContextReference(
            file_path=f"~/.claude/principles/{ref}",
            ref_type="principle",
            line=get_line_number(content, ref)
        ))

    # Find @skills/... references
    skill_refs = re.findall(r'@skills/([\w_-]+\.md)', content)
    for ref in skill_refs:
        references.append(ContextReference(
            file_path=f"~/.claude/skills/{ref}",
            ref_type="skill",
            line=get_line_number(content, ref)
        ))

    # Find other explicit file references
    # (Custom paths users might have added)

    return references

claude_md_refs = extract_claude_md_references(claude_md_path)
claude_md_loaded_files = {ref.file_path for ref in claude_md_refs}
```

### Step 2: Detect Duplications in Claude Tools

```python
@dataclass
class DuplicationIssue:
    """Context duplication - file loaded multiple times."""
    file_path: str
    loaded_in_claude_md: bool
    also_loaded_in: List[str]  # List of skills/agents/commands
    wasted_tokens: int
    recommendation: str

duplications = []

for tool_file in all_claude_tools:
    content = Read(tool_file)

    # Find file references in this tool
    # Look for Read(), Glob(), @principles/, @skills/ patterns
    references = extract_file_references(content)

    for ref_file in references:
        # Check if this file is already in CLAUDE.md
        if ref_file in claude_md_loaded_files:
            duplications.append(DuplicationIssue(
                file_path=ref_file,
                loaded_in_claude_md=True,
                also_loaded_in=[tool_file],
                wasted_tokens=estimate_tokens(Read(ref_file)),
                recommendation=f"Remove from {tool_file} - already in CLAUDE.md"
            ))

# Group duplications by file
duplication_groups = {}
for dup in duplications:
    if dup.file_path not in duplication_groups:
        duplication_groups[dup.file_path] = {
            "file": dup.file_path,
            "in_claude_md": True,
            "also_in": [],
            "tokens": dup.wasted_tokens
        }
    duplication_groups[dup.file_path]["also_in"].extend(dup.also_loaded_in)
```

### Step 3: Recommend CLAUDE.md Additions

```python
@dataclass
class CLAUDEmdRecommendation:
    """Recommend adding file to CLAUDE.md for efficiency."""
    file_path: str
    referenced_by: List[str]  # List of skills/agents/commands
    reference_count: int
    tokens: int
    benefit: str

recommendations = []

# Count file references across all Claude tools
file_reference_counts = {}
for tool_file in all_claude_tools:
    content = Read(tool_file)
    references = extract_file_references(content)

    for ref_file in references:
        if ref_file not in file_reference_counts:
            file_reference_counts[ref_file] = []
        file_reference_counts[ref_file].append(tool_file)

# Find frequently referenced files NOT in CLAUDE.md
for ref_file, referencing_tools in file_reference_counts.items():
    if len(referencing_tools) >= 3:  # Referenced by 3+ tools
        if ref_file not in claude_md_loaded_files:  # NOT in CLAUDE.md
            recommendations.append(CLAUDEmdRecommendation(
                file_path=ref_file,
                referenced_by=referencing_tools,
                reference_count=len(referencing_tools),
                tokens=estimate_tokens(Read(ref_file)),
                benefit=f"Load once in CLAUDE.md instead of {len(referencing_tools)} times"
            ))

# Sort by reference count (most referenced first)
recommendations.sort(key=lambda r: r.reference_count, reverse=True)
```

### Step 4: Display Context Analysis Results

```markdown
## Context Duplication Analysis

### ⚠️ Duplicated Context Loading

**Issues Found:** {len(duplication_groups)}

{if len(duplication_groups) > 0}
| File | Tokens | Loaded In | Also Loaded In | Recommendation |
|------|--------|-----------|----------------|----------------|
| {file_path} | {tokens} | CLAUDE.md | {tools} | Remove from tools |
| {file_path} | {tokens} | CLAUDE.md | {tools} | Remove from tools |

**Wasted Tokens:** {total_wasted_tokens}

**Action Required:** Remove these references from tools to eliminate duplication.
{else}
✅ **No duplications detected** - All files loaded only once.
{endif}

---

### 💡 CLAUDE.md Optimization Recommendations

**Opportunities Found:** {len(recommendations)}

{if len(recommendations) > 0}
| File | Referenced By | Count | Tokens | Benefit |
|------|---------------|-------|--------|---------|
| {file_path} | {tools} | {count}x | {tokens} | {benefit} |
| {file_path} | {tools} | {count}x | {tokens} | {benefit} |

**Potential Token Savings:** {total_potential_savings}

**Action:** Add these files to CLAUDE.md to load once instead of multiple times.
{else}
✅ **CLAUDE.md is optimal** - No additional files should be added.
{endif}

---

### User Confirmation

{if len(duplications) > 0 or len(recommendations) > 0}
```

```python
AskUserQuestion({
  questions: [{
    question: "Apply context optimizations?",
    header: "Context Optimization",
    multiSelect: true,
    options: [
      {
        label: "All",
        description: "Apply all context optimizations below"
      },
      {
        label: "Remove Duplications",
        description: f"Remove {len(duplication_groups)} duplicate references from tools"
      },
      {
        label: "Update CLAUDE.md",
        description: f"Add {len(recommendations)} frequently-used files to CLAUDE.md"
      },
      {
        label: "Skip",
        description: "Continue without context optimizations"
      }
    ]
  }]
})
```

### Step 5: Apply Context Optimizations

```python
if "Remove Duplications" in user_selection or "All" in user_selection:
    # Remove duplicate references from tools
    for file, data in duplication_groups.items():
        for tool in data["also_in"]:
            remove_file_reference(tool, file)
            print(f"✓ Removed {file} from {tool} (already in CLAUDE.md)")

if "Update CLAUDE.md" in user_selection or "All" in user_selection:
    # Add recommendations to CLAUDE.md
    claude_md_content = Read(claude_md_path)

    # Find appropriate section (e.g., <!-- CCO_PRINCIPLES_END -->)
    insertion_point = find_insertion_point(claude_md_content)

    # Add references
    new_references = []
    for rec in recommendations:
        # Determine reference type
        if "principles/" in rec.file_path:
            new_references.append(f"@principles/{basename(rec.file_path)}")
        elif "skills/" in rec.file_path:
            new_references.append(f"@skills/{basename(rec.file_path)}")
        else:
            new_references.append(f"@{rec.file_path}")

    # Insert into CLAUDE.md
    updated_content = insert_references(
        claude_md_content,
        insertion_point,
        new_references
    )

    Write(claude_md_path, updated_content)

    print(f"✓ Added {len(recommendations)} references to CLAUDE.md")

    # Remove from individual tools
    for rec in recommendations:
        for tool in rec.referenced_by:
            remove_file_reference(tool, rec.file_path)
            print(f"✓ Removed {rec.file_path} from {tool}")
```

**Benefits:**
- Eliminated duplication: {duplication_tokens_saved} tokens saved
- CLAUDE.md optimization: {recommendation_tokens_saved} tokens saved
- Total context savings: {total_context_savings} tokens

{endif}
```

---

## Component 4: Analysis Phase

**Find specific optimization opportunities per category.**

### Safe Optimizations (Conservative Mode)

```python
@dataclass
class SafeOptimization:
    """100% safe optimization - no semantic risk."""
    type: str
    file: str
    line: int
    description: str
    token_saving: int
    risk: str = "none"

safe_optimizations = []

# 1. Whitespace normalization
for file in all_files:
    content = Read(file)
    lines = content.split('\n')

    # Find excessive blank lines
    for i, (line1, line2, line3) in enumerate(zip(lines, lines[1:], lines[2:])):
        if not line1.strip() and not line2.strip() and not line3.strip():
            safe_optimizations.append(SafeOptimization(
                type="whitespace",
                file=file,
                line=i,
                description="Remove excessive blank lines (3+ consecutive)",
                token_saving=2  # Approximate
            ))

# 2. Dead code (provably unused)
for file in code_files:
    unused_imports = find_unused_imports(file)  # AST analysis
    for imp in unused_imports:
        safe_optimizations.append(SafeOptimization(
            type="dead_code",
            file=file,
            line=imp.line,
            description=f"Remove unused import: {imp.name}",
            token_saving=estimate_tokens(imp.text)
        ))

# 3. Spelling/grammar fixes
for file in markdown_files:
    typos = run_spell_check(file)
    for typo in typos:
        safe_optimizations.append(SafeOptimization(
            type="spelling",
            file=file,
            line=typo.line,
            description=f"Fix typo: {typo.wrong} → {typo.correct}",
            token_saving=0  # No token change, quality improvement
        ))

# 4. Format consistency
for file in markdown_files:
    inconsistencies = check_markdown_format(file)
    for inc in inconsistencies:
        safe_optimizations.append(SafeOptimization(
            type="format",
            file=file,
            line=inc.line,
            description=inc.description,
            token_saving=0  # No token change, consistency improvement
        ))
```

### Low-Risk Optimizations (Balanced Mode)

```python
@dataclass
class LowRiskOptimization:
    """Low-risk optimization - requires verification."""
    type: str
    file: str
    line: int
    description: str
    token_saving: int
    risk: str = "low"
    verification_required: bool = True

low_risk_optimizations = []

# 1. Example consolidation (if truly redundant)
for file in all_files:
    redundant_examples = find_redundant_examples(file)
    for example_group in redundant_examples:
        low_risk_optimizations.append(LowRiskOptimization(
            type="example_consolidation",
            file=file,
            line=example_group.start_line,
            description=f"Consolidate {len(example_group.examples)} redundant examples into 1",
            token_saving=estimate_tokens(example_group.redundant_text),
            verification_required=True
        ))

# 2. Table optimization
for file in markdown_files:
    tables = find_tables(file)
    for table in tables:
        if table.has_redundant_columns:
            low_risk_optimizations.append(LowRiskOptimization(
                type="table_optimization",
                file=file,
                line=table.line,
                description=f"Remove redundant column: {table.redundant_column}",
                token_saving=table.column_token_count,
                verification_required=True
            ))

# 3. Cross-referencing
for file in all_files:
    duplicates = find_duplicate_content(file, other_files)
    for dup in duplicates:
        low_risk_optimizations.append(LowRiskOptimization(
            type="cross_reference",
            file=file,
            line=dup.line,
            description=f"Replace duplicate with reference to {dup.source_file}",
            token_saving=estimate_tokens(dup.duplicate_text),
            verification_required=True
        ))
```

### High-Risk Optimizations (Aggressive Mode)

```python
@dataclass
class HighRiskOptimization:
    """High-risk optimization - strong verification required."""
    type: str
    file: str
    line: int
    description: str
    token_saving: int
    risk: str = "high"
    verification_required: bool = True
    manual_review_required: bool = True

high_risk_optimizations = []

# 1. Example reduction
for file in all_files:
    examples = find_all_examples(file)
    if len(examples) > 3:  # More than 3 examples
        high_risk_optimizations.append(HighRiskOptimization(
            type="example_reduction",
            file=file,
            line=examples[3].line,
            description=f"Reduce from {len(examples)} to 3 most effective examples",
            token_saving=sum(estimate_tokens(ex.text) for ex in examples[3:]),
            manual_review_required=True
        ))

# 2. Instruction condensing
for file in claude_tool_files:
    instructions = find_verbose_instructions(file)
    for inst in instructions:
        high_risk_optimizations.append(HighRiskOptimization(
            type="instruction_condensing",
            file=file,
            line=inst.line,
            description=f"Condense verbose instruction (may lose nuance)",
            token_saving=estimate_tokens(inst.verbose_part),
            manual_review_required=True
        ))
```

### Analysis Summary

```markdown
## Analysis Complete

**Optimization Opportunities Found:** {total_opportunities}

### By Type

#### ✅ Safe Optimizations ({count}) - {tokens} tokens
- Whitespace normalization: {count} instances
- Dead code removal: {count} instances
- Spelling/grammar: {count} instances
- Format consistency: {count} instances

#### ⚠️ Low-Risk Optimizations ({count}) - {tokens} tokens
- Example consolidation: {count} instances
- Table optimization: {count} instances
- Cross-referencing: {count} instances

#### ❌ High-Risk Optimizations ({count}) - {tokens} tokens
- Example reduction: {count} instances
- Instruction condensing: {count} instances
- Detail removal: {count} instances

### Mode Recommendations

**Conservative:** Apply {safe_count} safe optimizations → {safe_tokens} tokens saved
**Balanced:** Apply {safe_count + low_risk_count} optimizations → {balanced_tokens} tokens saved
**Aggressive:** Apply {all_count} optimizations → {aggressive_tokens} tokens saved (⚠️ Manual review required)
```

---

## Component 5: Pre-Flight Summary

**Show EXACTLY what will change before execution. No surprises.**

```markdown
## Pre-Flight Summary

**Mode:** {selected_mode}
**Categories:** {selected_categories}

### What Will Change

**Files to Optimize:** {file_count}
**Optimizations to Apply:** {optimization_count}
**Expected Token Reduction:** {min_pct}%-{max_pct}% ({tokens} tokens)

#### By Category

| Category | Files | Optimizations | Token Reduction |
|----------|-------|---------------|-----------------|
| {category} | {count} | {opt_count} | {tokens} ({pct}%) |
| {category} | {count} | {opt_count} | {tokens} ({pct}%) |

#### By Type

| Type | Count | Token Reduction | Risk |
|------|-------|-----------------|------|
| Whitespace | {count} | {tokens} | ✅ None |
| Dead code | {count} | {tokens} | ✅ None |
| Example consolidation | {count} | {tokens} | ⚠️ Low |
| Cross-reference | {count} | {tokens} | ⚠️ Low |

### What Will NOT Change

**Excluded Files:** {excluded_count}
- {reason}: {count} files
- {reason}: {count} files

**Skipped Optimizations:** {skipped_count}
- {type}: {count} instances (risk too high for mode)
- {type}: {count} instances (quality degradation detected)

### Quality Safeguards

✅ Backup created for all files
✅ Semantic verification enabled
✅ Syntax validation enabled
✅ Rollback on degradation
✅ Manual review for high-risk

### Estimated Impact

**Before:** {tokens_before} tokens
**After:** {tokens_after} tokens
**Reduction:** {delta_tokens} tokens ({pct}%)

**Quality:** Preserved (verified)
**Time:** ~{minutes} minutes
```

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start optimization?",
    header: "Confirm",
    multiSelect: false,
    options: [
      {
        label: "Start Optimization",
        description: f"Optimize {file_count} files (~{minutes} min)"
      },
      {
        label: "Modify Selection",
        description: "Change mode or categories"
      },
      {
        label: "Cancel",
        description: "Exit without optimizing"
      }
    ]
  }]
})
```

---

## Component 6: Optimization Phase

**Apply changes with verification at each step.**

### Optimization Loop

```python
@dataclass
class OptimizationState:
    """Track optimization progress and accounting."""

    total_optimizations: int = 0

    # Dispositions - MUST sum to total_optimizations
    applied: List[Optimization] = field(default_factory=list)
    skipped: List[Tuple[Optimization, str]] = field(default_factory=list)
    rolled_back: List[Tuple[Optimization, str]] = field(default_factory=list)

    # Metrics
    tokens_saved: int = 0
    files_modified: Set[str] = field(default_factory=set)

    def add_applied(self, opt: Optimization, tokens_saved: int):
        """Record successful optimization."""
        self.applied.append(opt)
        self.tokens_saved += tokens_saved
        self.files_modified.add(opt.file)

    def add_skipped(self, opt: Optimization, reason: str):
        """Record skipped optimization."""
        self.skipped.append((opt, reason))

    def add_rolled_back(self, opt: Optimization, reason: str):
        """Record rolled-back optimization."""
        self.rolled_back.append((opt, reason))

    def verify_accounting(self) -> bool:
        """Verify all optimizations accounted for."""
        accounted = len(self.applied) + len(self.skipped) + len(self.rolled_back)
        return accounted == self.total_optimizations

state = OptimizationState(total_optimizations=len(all_optimizations))

# Process each optimization
for opt in all_optimizations:
    # Create backup
    original_content = Read(opt.file)

    try:
        # Apply optimization
        new_content = apply_optimization(opt, original_content)

        # Verify
        if not verify_optimization(opt, original_content, new_content):
            state.add_skipped(opt, "Verification failed")
            continue

        # Write optimized content
        Write(opt.file, new_content)

        # Measure token reduction
        tokens_before = estimate_tokens(original_content)
        tokens_after = estimate_tokens(new_content)
        tokens_saved = tokens_before - tokens_after

        # Record success
        state.add_applied(opt, tokens_saved)

    except Exception as e:
        # Rollback on any error
        Write(opt.file, original_content)
        state.add_rolled_back(opt, str(e))

# Verify accounting
assert state.verify_accounting(), "Optimization accounting mismatch!"
```

### Verification Functions

```python
def verify_optimization(opt: Optimization, before: str, after: str) -> bool:
    """
    Verify optimization preserved quality.

    Returns True if optimization is safe to keep, False to reject.
    """

    # 1. Structural verification
    if not verify_syntax(after, get_file_type(opt.file)):
        return False

    # 2. Semantic verification
    if not verify_semantic_equivalence(before, after, opt.type):
        return False

    # 3. Quality verification
    if not verify_quality_preserved(before, after, opt.file):
        return False

    # 4. Effectiveness verification
    if opt.file.startswith("claudecodeoptimizer/content/"):
        # For Claude tools, verify instruction effectiveness
        if not verify_instruction_effectiveness(before, after):
            return False

    return True

def verify_syntax(content: str, file_type: str) -> bool:
    """Verify syntax is valid."""
    if file_type == "python":
        return python_syntax_check(content)
    elif file_type == "markdown":
        return markdown_syntax_check(content)
    # Add other file types
    return True

def verify_semantic_equivalence(before: str, after: str, opt_type: str) -> bool:
    """
    Verify semantic meaning preserved.

    For critical optimization types, use stricter checks.
    """
    if opt_type in ["whitespace", "spelling", "format"]:
        # These should never change semantics
        return True

    # For content changes, check key concepts preserved
    before_concepts = extract_key_concepts(before)
    after_concepts = extract_key_concepts(after)

    # All before concepts must be in after
    return before_concepts.issubset(after_concepts)

def verify_quality_preserved(before: str, after: str, file_path: str) -> bool:
    """Verify quality metrics not degraded."""

    metrics_before = calculate_quality_metrics(before, file_path)
    metrics_after = calculate_quality_metrics(after, file_path)

    # Check critical metrics
    checks = [
        metrics_after.instruction_count >= metrics_before.instruction_count,
        metrics_after.example_coverage >= metrics_before.example_coverage * 0.9,  # Allow 10% reduction
        metrics_after.concept_count >= metrics_before.concept_count,
    ]

    return all(checks)

def verify_instruction_effectiveness(before: str, after: str) -> bool:
    """
    Verify instruction effectiveness for Claude tools.

    Conservative: If in doubt, reject.
    """

    # Count instruction steps
    before_steps = count_instruction_steps(before)
    after_steps = count_instruction_steps(after)

    if after_steps < before_steps:
        # Steps reduced - verify no critical steps lost
        before_critical = extract_critical_steps(before)
        after_critical = extract_critical_steps(after)

        if not before_critical.issubset(after_critical):
            return False  # Critical step lost

    return True
```

---

## Component 7: Final Report

**Comprehensive accounting and metrics.**

```markdown
═══════════════════════════════════════════════════════════════
                    OPTIMIZATION REPORT
═══════════════════════════════════════════════════════════════

## Executive Summary

**Mode:** {mode}
**Status:** ✅ Complete

**Token Reduction:** {tokens_before} → {tokens_after} ({reduction_pct}% reduction)
**Tokens Saved:** {tokens_saved}
**Quality:** ✅ Preserved (verified)

**Files Modified:** {files_modified_count} / {files_analyzed_count}
**Optimizations Applied:** {applied_count} / {total_optimizations}

───────────────────────────────────────────────────────────────

## Optimization Summary

**Total Optimizations Planned:** {total_optimizations}

### ✅ Applied Successfully: {applied_count}

| Type | Count | Tokens Saved |
|------|-------|--------------|
| Whitespace | {count} | {tokens} |
| Dead code | {count} | {tokens} |
| Example consolidation | {count} | {tokens} |
| Cross-reference | {count} | {tokens} |
| Other | {count} | {tokens} |

### ⏭️ Skipped: {skipped_count}

| File | Type | Reason |
|------|------|--------|
| {file_path} | {type} | {reason} |
| {file_path} | {type} | {reason} |

### ↩️ Rolled Back: {rolled_back_count}

| File | Type | Reason |
|------|------|--------|
| {file_path} | {type} | {reason} |
| {file_path} | {type} | {reason} |

───────────────────────────────────────────────────────────────

**Verification:** {applied_count} + {skipped_count} + {rolled_back_count} = {total_optimizations} ✓

───────────────────────────────────────────────────────────────

## Detailed Results by Category

### Markdown Documentation

**Files:** {count}
**Before:** {tokens_before} tokens
**After:** {tokens_after} tokens
**Reduction:** {tokens_saved} tokens ({pct}%)

Top files:
| File | Before | After | Saved | Reduction % |
|------|--------|-------|-------|-------------|
| {file_path} | {before} | {after} | {saved} | {pct}% |
| {file_path} | {before} | {after} | {saved} | {pct}% |

### Code Files

**Files:** {count}
**Before:** {tokens_before} tokens
**After:** {tokens_after} tokens
**Reduction:** {tokens_saved} tokens ({pct}%)

Top files:
| File | Before | After | Saved | Reduction % |
|------|--------|-------|-------|-------------|
| {file_path} | {before} | {after} | {saved} | {pct}% |

### Claude Tools

**Files:** {count}
**Before:** {tokens_before} tokens
**After:** {tokens_after} tokens
**Reduction:** {tokens_saved} tokens ({pct}%)

By subcategory:
- Skills: {count} files, {tokens_saved} tokens saved
- Agents: {count} files, {tokens_saved} tokens saved
- Commands: {count} files, {tokens_saved} tokens saved

### Active Context

**Files:** {count}
**Before:** {tokens_before} tokens
**After:** {tokens_after} tokens
**Reduction:** {tokens_saved} tokens ({pct}%)

**Impact:** Context window usage reduced by {pct}%

───────────────────────────────────────────────────────────────

## Quality Verification

### Metrics Preserved

✅ **Semantic meaning:** 100% preserved
✅ **Instruction count:** {before_instructions} → {after_instructions} (preserved)
✅ **Example coverage:** {before_coverage}% → {after_coverage}% (preserved)
✅ **Concept completeness:** {before_concepts} → {after_concepts} (preserved)
✅ **Edge case handling:** Preserved

### Syntax Validation

✅ **Markdown:** {markdown_files} files validated
✅ **Python:** {python_files} files validated
✅ **JavaScript/TypeScript:** {js_files} files validated

All files pass syntax validation.

───────────────────────────────────────────────────────────────

## Recommendations

### Further Optimization Opportunities

{if skipped_count > 0}
**Skipped Optimizations ({skipped_count}):**
- Consider running in Balanced mode to apply low-risk optimizations
- Review skipped optimizations for manual application
- Estimated additional savings: {potential_tokens} tokens
{endif}

{if mode == "Conservative"}
**Next Steps:**
- Consider Balanced mode for {low_risk_count} additional optimizations
- Potential additional savings: {additional_tokens} tokens ({additional_pct}%)
{endif}

{if rolled_back_count > 0}
**Review Rolled-Back Items:**
- {rolled_back_count} optimizations failed verification
- Review reasons and consider manual fixes
{endif}

### Maintenance

**Regular Re-optimization:**
- Run `/cco-slim` monthly to catch new redundancy
- Review newly added files for optimization opportunities
- Monitor active context size (currently {context_tokens} tokens)

───────────────────────────────────────────────────────────────

## Files Modified

**Total:** {files_modified_count} files

{for file in files_modified}
✓ {file_path}
  Before: {tokens_before} tokens
  After: {tokens_after} tokens
  Saved: {tokens_saved} tokens ({pct}% reduction)
{endfor}

───────────────────────────────────────────────────────────────

## Backup Information

**Backup Location:** {backup_dir}
**Backup Created:** {timestamp}

To restore a file:
```bash
cp {backup_dir}/{file_path} {original_path}
```

To restore all files:
```bash
/cco-restore-backup {backup_dir}
```

═══════════════════════════════════════════════════════════════
```

---

## Agent Integration

**Use specialized agent for complex optimization.**

```python
# For large-scale optimization (50+ files), use parallel processing
if file_count > 50:
    # Launch optimization agent
    Task({
        subagent_type: "general-purpose",
        model: "sonnet",
        description: "Slim content optimization",
        prompt: f"""
        Optimize {file_count} files with {mode} mode.

        Categories: {selected_categories}

        For each file:
        1. Read file
        2. Apply {mode} optimizations
        3. Verify quality preserved
        4. Save if verification passes
        5. Report token reduction

        Return complete accounting:
        - Applied: {count} optimizations, {tokens} saved
        - Skipped: {count} optimizations, {reasons}
        - Rolled back: {count} optimizations, {reasons}

        Verification: applied + skipped + rolled_back = total
        """
    })
```

---

## CLI Usage

### Interactive (Default)
```bash
/cco-slim
```

### Parametrized (Power Users)

**Mode selection:**
```bash
/cco-slim --conservative  # Default
/cco-slim --balanced
/cco-slim --aggressive
```

**Category selection:**
```bash
/cco-slim --markdown
/cco-slim --code
/cco-slim --claude-tools
/cco-slim --active-context
/cco-slim --all
```

**Combined:**
```bash
/cco-slim --balanced --claude-tools
/cco-slim --conservative --all
```

**Dry run (preview only):**
```bash
/cco-slim --dry-run
```

---

## Error Handling

### Verification Failures

```markdown
## Verification Failed

**File:** {file_path}
**Optimization:** {optimization_type}

**Reason:** {failure_reason}

**Action:** Rolled back to original

**Details:**
- Metric: {metric_name}
- Before: {before_value}
- After: {after_value}
- Threshold: {threshold}
- Status: ❌ Degraded
```

### Rollback Confirmation

```markdown
## Rollback Required

**Optimizations with quality degradation:** {count}

**Action:** All changes rolled back

**Files restored:**
{for file in rolled_back_files}
✓ {file_path} (restored from backup)
{endfor}

**No files were permanently modified.**
```

---

## Success Criteria

- [ ] Mode selection presented
- [ ] Category selection completed
- [ ] Discovery phase measured all files
- [ ] Analysis found optimization opportunities
- [ ] Pre-flight summary displayed
- [ ] User confirmed execution
- [ ] Optimizations applied with verification
- [ ] Quality metrics verified
- [ ] Complete accounting (applied + skipped + rolled back = total)
- [ ] Final report generated
- [ ] Backup created and documented

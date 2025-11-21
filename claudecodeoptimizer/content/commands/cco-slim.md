---
name: cco-slim
description: Context optimization and duplication elimination (primary). Optional token reduction for other files.
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

# CCO Slim: Ultimate Context Optimization

**Primary: Context optimization (CLAUDE.md duplication elimination). Secondary: Token reduction for other content.**

---

## Design Principles

1. **Context First** - Primary focus on CLAUDE.md and context duplication (core mission)
2. **Quality First** - Never sacrifice meaning, effectiveness, or completeness
3. **Verification Heavy** - Every optimization verified before acceptance
4. **Conservative Default** - Only 100% safe optimizations unless user opts-in
4. **Complete Accounting** - Every file categorized, every change tracked
5. **Semantic Preservation** - Meaning preserved at all costs
6. **Honest Reporting** - Exact truth about reductions and risks
7. **No Hardcoded Examples** - All examples use placeholders

## Mission Statement

**PRIMARY GOAL: Minimize context usage while maximizing quality, efficiency, and AI performance.**

This means:
1. **Eliminate duplication**: CLAUDE.md + skills/agents/commands loading same files
2. **Detect incomplete content**: Stub files, TODO markers, missing implementations
3. **Optimize CLAUDE.md**: Add frequently-used files, remove redundant references
4. **Token reduction WITHOUT quality loss**: Preserve meaning, effectiveness, completeness
5. **Evaluate ALL context elements**: Principles, skills, agents, commands, README, ARCHITECTURE, CONTRIBUTING, all .md docs - EVERYTHING that can be context
6. **Optimize each file internally**: Every principle/skill/agent/command written with minimum tokens for maximum effectiveness

**Success = Minimum tokens for maximum quality.**

### Internal Content Optimization (Critical Component)

**Each context element must be internally optimized:**

**Goal**: Same effectiveness with minimum tokens.

**Target Elements**:
- **Principles**: Verbose explanations → Concise rules with examples
- **Skills**: Redundant instructions → Streamlined procedures
- **Agents**: Long prompts → Token-efficient directives
- **Commands**: Repeated patterns → DRY implementations
- **MD Docs**: Verbose text → Information-dense content

**Example Optimization**:
```markdown
❌ BEFORE (200 tokens, verbose):
"This principle is about ensuring that you always verify your changes before 
claiming that you have completed a task. You should never say that something 
is done without actually checking to make sure it's really done. This is very 
important because it prevents incomplete work and ensures reliability..."

✅ AFTER (50 tokens, optimized):
**Verify before claiming completion. Check, don't assume.**

**Why**: Prevents incomplete work, ensures reliability.

**How**: Run commands, check outputs, confirm results.
```

**Quality Preservation**:
- ✅ Meaning preserved (verify before claim)
- ✅ Effectiveness maintained (same outcome)
- ✅ Examples included (how to verify)
- ✅ 75% token reduction

**This applies to EVERY context file - no exceptions.**


---

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
        description: "Only 100% safe optimizations - Quality guaranteed, maximum reduction with zero risk"
      },
      {
        label: "Balanced",
        description: "Safe + verified low-risk - Quality checks enforced, maximum reduction with minimal risk"
      },
      {
        label: "Aggressive (Not Recommended)",
        description: "All optimizations - Higher risk, manual review required, maximum achievable reduction"
      }
    ]
  }]
})
```

### Mode Details
**Conservative (Default):**
- Only 100% safe optimizations (whitespace, provably unused, formatting)
- Zero semantic risk
- Quality: 100% guaranteed
- **Reduction: Maximum possible with zero risk** (not capped at %)
- Recommended for: Production content, critical documentation

**Balanced:**
- Safe + verified low-risk optimizations
- Quality checks before acceptance, rollback on degradation
- **Reduction: Maximum possible with minimal risk** (not capped at %)
- Recommended for: Development content, iterative improvement

**Aggressive:**
- All optimization techniques, manual review required
- Higher risk of quality loss (careful verification needed)
- **Reduction: Maximum achievable** (not capped at %)
- Recommended for: Experimental optimization, draft content

**Goal for ALL modes: Maximum optimization while preserving quality - no artificial caps.**
- Recommended for: Experimental optimization, draft content

---

## Optional Prompt Support (Advanced)

Add context after mode/category flags for optimization preferences:

**Examples:**
```bash
/cco-slim --balanced "Prioritize documentation optimization"
/cco-slim --conservative "Minimize changes to critical files"
/cco-slim --aggressive "Focus on removing duplicate patterns"
/cco-slim "Optimize commands and skills, preserve principles"
```

**The AI will:**
- Apply your preferences when analyzing optimization opportunities
- Prioritize areas you specify
- Adjust optimization aggressiveness based on your guidance
- Focus on specific file types or categories you mention

**Use cases:**
- Specify which files/categories to prioritize
- Provide context about which content is more critical
- Request focus on specific optimization types (whitespace, examples, duplicates)
- Indicate risk tolerance beyond mode selection

---

## Component 2: Category Selection


**Context-Aware Perspective**: ALL files are evaluated for context optimization because:
- README/docs may be read by skills during execution
- Code files may be analyzed by agents
- EVERYTHING is potential context - optimize accordingly

**Choose what to optimize.**

```python
AskUserQuestion({
  questions: [{
    question: "What do you want to optimize? (Space: select, Enter: confirm)",
    header: "Categories",
    multiSelect: true,
    options: [
      {
        label: "All (Ultimate Context Optimization)",
        description: "🎯 ULTIMATE: Optimize all project files - markdown, code, tools, documentation, everything"
      },
      {
        label: "Markdown Docs",
        description: "All markdown files (.md) anywhere in project - docs, guides, architecture"
      },
      {
        label: "Code Files",
        description: "All source code files (.py, .js, .ts, etc.) anywhere in project"
      },
      {
        label: "Tools & Architecture",
        description: "🔥 HIGH IMPACT: Tool configs, automation, patterns (skill, agent, command, principle related files)"
      },
      {
        label: "Active Context (Primary)",
        description: "🎯 PRIMARY: CLAUDE.md duplication elimination, principle optimization, context minimization"
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
# Launch discovery agent for efficient categorization
discovery_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    description: "Discover and categorize files",
    prompt: f"""
    Discover files for categories: {selected_categories}

    Rules:
    - "Markdown Docs": **/*.md
    - "Code Files": *.py, *.js, *.ts, *.tsx, *.java, *.go, *.rs
    - "Claude Tools": **/*{cco,skill,agent,command,principle}*.md (tools, architecture, configs anywhere in project)
    - "Active Context": ~/.claude/CLAUDE.md + referenced principles
    - "All": All categories

    Return JSON:
    {{
        "markdown": ["path1.md"],
        "code": ["path1.py"],
        "claude_tools": {{"skills": [], "agents": [], "commands": []}},
        "active_context": []
    }}
    """
})

# Handle discovery errors
if discovery_result is None or (isinstance(discovery_result, dict) and "error" in discovery_result):
    error_msg = discovery_result.get('error', 'Unknown error') if isinstance(discovery_result, dict) else 'Agent returned None'

    response = AskUserQuestion({
        questions: [{
            question: f"Explore agent (Haiku) file discovery failed: {error_msg}. How to proceed?",
            header: "Explore (Haiku) Error",
            multiSelect: false,
            options: [
                {label: "Retry", description: "Run discovery agent again"},
                {label: "Retry with Sonnet", description: "Use more capable model"},
                {label: "Manual discovery", description: "Use Glob() commands directly"},
                {label: "Cancel", description: "Stop cco-slim"}
            ]
        }]
    })

    if response == "Retry":
        discovery_result = Task({
            subagent_type: "Explore",
            model: "haiku",
            description: "Discover and categorize files (retry)",
            prompt: f"""
            Discover files for categories: {selected_categories}

            Rules:
            - "Markdown Docs": **/*.md
            - "Code Files": *.py, *.js, *.ts, *.tsx, *.java, *.go, *.rs
            - "Claude Tools": **/*{cco,skill,agent,command,principle}*.md (tools, architecture, configs anywhere in project)
            - "Active Context": ~/.claude/CLAUDE.md + referenced principles
            - "All": All categories

            Return JSON:
            {{
                "markdown": ["path1.md"],
                "code": ["path1.py"],
                "claude_tools": {{"skills": [], "agents": [], "commands": []}},
                "active_context": []
            }}
            """
        })
    elif response == "Retry with Sonnet":
        discovery_result = Task({
            subagent_type: "Explore",
            model: "sonnet",
            description: "Discover and categorize files (retry)",
            prompt: f"""
            Discover files for categories: {selected_categories}

            Rules:
            - "Markdown Docs": **/*.md
            - "Code Files": *.py, *.js, *.ts, *.tsx, *.java, *.go, *.rs
            - "Claude Tools": **/*{cco,skill,agent,command,principle}*.md (tools, architecture, configs anywhere in project)
            - "Active Context": ~/.claude/CLAUDE.md + referenced principles
            - "All": All categories

            Return JSON:
            {{
                "markdown": ["path1.md"],
                "code": ["path1.py"],
                "claude_tools": {{"skills": [], "agents": [], "commands": []}},
                "active_context": []
            }}
            """
        })
    elif response == "Manual discovery":
        # Fallback to manual Glob()
        discovered = {
            "markdown": [],
            "code": [],
            "claude_tools": {"skills": [], "agents": [], "commands": []},
            "active_context": []
        }

        if "Markdown Docs" in selected_categories or "All" in selected_categories:
            discovered["markdown"] = Glob("**/*.md")
            discovered["markdown"] = [f for f in discovered["markdown"]
                                      if not f.startswith("claudecodeoptimizer/content/")]

        if "Code Files" in selected_categories or "All" in selected_categories:
            for ext in ["*.py", "*.js", "*.ts", "*.tsx", "*.java", "*.go", "*.rs"]:
                discovered["code"].extend(Glob(f"**/{ext}"))

        if "Claude Tools" in selected_categories or "All" in selected_categories:
            discovered["claude_tools"]["skills"] = Glob("**/cco-skill-*.md")
            discovered["claude_tools"]["agents"] = Glob("**/cco-agent-*.md")
            discovered["claude_tools"]["commands"] = Glob("**/cco-*.md",
                                                           path="claudecodeoptimizer/content/commands/")

        if "Active Context" in selected_categories or "All" in selected_categories:
            claude_md_path = "~/.claude/CLAUDE.md"
            if file_exists(claude_md_path):
                discovered["active_context"].append(claude_md_path)
                principles = extract_principle_references(claude_md_path)
                discovered["active_context"].extend(principles)

        discovery_result = discovered
    else:  # Cancel
        return "cco-slim cancelled by user"

# Parse result
discovered = discovery_result if isinstance(discovery_result, dict) else json.loads(discovery_result)
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

# Use Explore agent for dependency analysis
duplication_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    description: "Analyze context duplication",
    prompt: """
    Analyze context duplication between CLAUDE.md and skills/commands/agents.

    1. Extract all @principles/, @skills/, file references from CLAUDE.md
    2. Find all file references in cco-skill-*.md, cco-agent-*.md, cco-*.md files
    3. Identify duplicates (same file loaded by both CLAUDE.md and other tools)
    4. Identify missing (frequently referenced but not in CLAUDE.md)

    Return JSON:
    {
        "claude_md_refs": ["principle1.md", "skill1.md"],
        "tool_refs": {"skill1.md": ["file1.md", "file2.md"]},
        "duplicates": [{"file": "file1.md", "loaded_by": ["CLAUDE.md", "skill1.md"]}],
        "missing": [{"file": "file2.md", "referenced_by": ["skill1", "skill2", "skill3"]}]
    }
    """
})

# Handle errors
if duplication_result is None or (isinstance(duplication_result, dict) and "error" in duplication_result):
    error_msg = duplication_result.get('error', 'Unknown error') if isinstance(duplication_result, dict) else 'Agent returned None'

    response = AskUserQuestion({
        questions: [{
            question: f"Explore agent (Haiku) duplication analysis failed: {error_msg}. How to proceed?",
            header: "Explore (Haiku) Error",
            multiSelect: false,
            options: [
                {label: "Retry", description: "Run analysis agent again"},
                {label: "Retry with Sonnet", description: "Use more capable model"},
                {label: "Skip duplication check", description: "Continue without this analysis"},
                {label: "Cancel", description: "Stop cco-slim"}
            ]
        }]
    })

    if response == "Retry":
        duplication_result = Task({
            subagent_type: "Explore",
            model: "haiku",
            description: "Analyze context duplication (retry)",
            prompt: """
            Analyze context duplication between CLAUDE.md and skills/commands/agents.

            1. Extract all @principles/, @skills/, file references from CLAUDE.md
            2. Find all file references in cco-skill-*.md, cco-agent-*.md, cco-*.md files
            3. Identify duplicates (same file loaded by both CLAUDE.md and other tools)
            4. Identify missing (frequently referenced but not in CLAUDE.md)

            Return JSON:
            {
                "claude_md_refs": ["principle1.md", "skill1.md"],
                "tool_refs": {"skill1.md": ["file1.md", "file2.md"]},
                "duplicates": [{"file": "file1.md", "loaded_by": ["CLAUDE.md", "skill1.md"]}],
                "missing": [{"file": "file2.md", "referenced_by": ["skill1", "skill2", "skill3"]}]
            }
            """
        })
    elif response == "Retry with Sonnet":
        duplication_result = Task({
            subagent_type: "Explore",
            model: "sonnet",
            description: "Analyze context duplication (retry)",
            prompt: """
            Analyze context duplication between CLAUDE.md and skills/commands/agents.

            1. Extract all @principles/, @skills/, file references from CLAUDE.md
            2. Find all file references in cco-skill-*.md, cco-agent-*.md, cco-*.md files
            3. Identify duplicates (same file loaded by both CLAUDE.md and other tools)
            4. Identify missing (frequently referenced but not in CLAUDE.md)

            Return JSON:
            {
                "claude_md_refs": ["principle1.md", "skill1.md"],
                "tool_refs": {"skill1.md": ["file1.md", "file2.md"]},
                "duplicates": [{"file": "file1.md", "loaded_by": ["CLAUDE.md", "skill1.md"]}],
                "missing": [{"file": "file2.md", "referenced_by": ["skill1", "skill2", "skill3"]}]
            }
            """
        })
    elif response == "Skip duplication check":
        duplication_result = {"duplicates": [], "missing": []}
    else:  # Cancel
        return "cco-slim cancelled by user"
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
    question: "Apply context optimizations? (Space: select, Enter: confirm)",
    header: "Context Optimization",
    multiSelect: true,
    options: [
      {
        label: "All (Ultimate Context Optimization)",
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

**Find specific optimization opportunities per category using Explore agent.**

### Agent-Based Optimization Discovery

**Use appropriate model based on mode complexity and risk level.**

```python
# Select agent model based on mode
if mode == "conservative":
    agent_model = "haiku"  # Fast, cheap for simple patterns
    optimization_prompt = """
    Find 100% safe optimizations (zero semantic risk):

    1. **Whitespace normalization**:
       - Excessive blank lines (3+ consecutive → 2)
       - Trailing whitespace at line ends
       - Inconsistent indentation

    2. **Dead code removal** (provably unused):
       - Unused imports (verify with AST analysis)
       - Commented-out code blocks
       - Unreachable code after return/break

    3. **Spelling/grammar fixes**:
       - Typos in documentation
       - Grammar improvements (no meaning change)

    4. **Format consistency**:
       - Markdown heading format (ATX vs Setext)
       - Code block language tags
       - List marker consistency (- vs *)

    For each optimization, return:
    {
        "type": "whitespace|dead_code|spelling|format",
        "file": "path/to/file.md",
        "line": 123,
        "description": "Specific change description",
        "token_saving": 5,
        "risk": "none"
    }

    Only include changes with ZERO semantic risk.
    """

elif mode == "balanced":
    agent_model = "sonnet"  # Balanced for judgment calls
    optimization_prompt = """
    Find balanced optimizations (low semantic risk, requires verification):

    1. **Verbosity reduction**:
       - "In order to" → "To"
       - "It is important to note that" → "Note:"
       - Remove filler phrases

    2. **Example consolidation**:
       - Multiple redundant examples → 1 clear example
       - Keep one representative of each pattern

    3. **Redundant explanation**:
       - Same concept explained multiple ways
       - Obvious statements ("JavaScript is a programming language")

    4. **DRY improvements**:
       - Repeated patterns → single reference
       - Duplicated sections across files

    For each optimization, return:
    {
        "type": "verbosity|example_consolidation|redundant|dry",
        "file": "path/to/file.md",
        "line": 123,
        "description": "Specific change description",
        "token_saving": 45,
        "risk": "low",
        "verification_required": true,
        "original_text": "text to be changed",
        "proposed_text": "new text"
    }

    Include LOW-RISK changes only. Preserve all semantics.
    """

else:  # aggressive
    agent_model = "sonnet"  # Complex analysis required
    optimization_prompt = """
    Find aggressive optimizations (moderate semantic risk, quality verification required):

    1. **Comprehensive rewrites**:
       - Multi-paragraph explanations → concise single paragraph
       - Verbose tutorials → essential reference

    2. **Format compression**:
       - Markdown → plain text (where formatting not needed)
       - JSON examples → YAML (shorter)
       - Code examples → pseudocode

    3. **Technical jargon**:
       - Long technical terms → abbreviations (first use full, then abbr)
       - "authentication and authorization" → "auth/z"

    4. **Content restructuring**:
       - Move detailed content to appendices
       - Replace detailed examples with links to external docs
       - Summarize reference sections

    For each optimization, return:
    {
        "type": "rewrite|compression|jargon|restructure",
        "file": "path/to/file.md",
        "line": 123,
        "description": "Specific change description",
        "token_saving": 150,
        "risk": "moderate",
        "quality_check_required": true,
        "original_text": "text to be changed",
        "proposed_text": "new text"
    }

    Moderate semantic risk acceptable IF quality preserved.
    """

# Launch analysis agent
analysis_result = Task({
    subagent_type: "Explore",
    model: agent_model,
    description: f"Find {mode} optimizations",
    prompt: f"""
    Analyze {len(all_files)} files for {mode} mode optimizations.

    Categories to analyze: {selected_categories}

    Skills:
    - cco-skill-content-optimization-automation
    - cco-skill-code-quality-refactoring-complexity

    Files to analyze:
    - Markdown: {len(markdown_files)} files
    - Code: {len(code_files)} files
    - Claude Tools: {len(claude_tool_files)} files
    - Active Context: {len(active_context_files)} files

    {optimization_prompt}

    Return JSON array of optimizations.
    Estimate token savings for each.
    Total optimizations must be verifiable.
    """
})

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
                {label: "Retry with Sonnet", description: "Use more capable model"} if agent_model == "haiku" else {label: "Retry with Opus", description: "Use most capable model"},
                {label: "Switch to Conservative", description: "Use Conservative mode instead (safer, fewer optimizations)"},
                {label: "Manual analysis", description: "Guide manual optimization identification"},
                {label: "Cancel", description: "Stop cco-slim"}
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
    elif response == "Retry with Sonnet" or response == "Retry with Opus":
        # Retry with more capable model
        new_model = "sonnet" if response == "Retry with Sonnet" else "opus"
        analysis_result = Task({
            subagent_type: "Explore",
            model: new_model,
            description: f"Find {mode} optimizations (retry with {new_model})",
            prompt: # ... same prompt as above
        })
    elif response == "Switch to Conservative":
        # Switch to conservative mode and retry
        mode = "conservative"
        agent_model = "haiku"
        optimization_prompt = # ... conservative prompt from above

        analysis_result = Task({
            subagent_type: "Explore",
            model: "haiku",
            description: "Find conservative optimizations",
            prompt: f"""
            Analyze {len(all_files)} files for conservative mode optimizations.

            {optimization_prompt}

            Return JSON array of 100% safe optimizations.
            """
        })
    elif response == "Manual analysis":
        # Guide user through manual identification
        print(f"""
        Manual Optimization Identification Guide:

        For {mode} mode, look for:
        {optimization_prompt}

        Use these tools:
        - Grep("pattern", output_mode="files_with_matches") - Find patterns
        - Read(file) - Read file contents
        - Document each optimization manually
        """)
        return "Manual mode - user identifying optimizations"
    else:  # Cancel
        return "cco-slim cancelled by user"

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

**Always use agents for consistent execution. Parallel batches for large workloads.**

```python
# Always use agent (no threshold) - ensures consistent behavior
# Use parallel batches for efficient processing of large workloads

optimization_count = len(optimizations)

if optimization_count > 20:
    # Split into batches for parallel processing
    batch_size = 20
    batches = [optimizations[i:i + batch_size]
               for i in range(0, len(optimizations), batch_size)]

    print(f"Processing {optimization_count} optimizations in {len(batches)} parallel batches...")

    results = []
    for batch_id, batch in enumerate(batches):
        print(f"Starting batch {batch_id + 1}/{len(batches)} ({len(batch)} optimizations)...")

        batch_result = Task({
            subagent_type: "general-purpose",
            model: "haiku",  # Fast, cheap model for simple edits
            description: f"Apply optimization batch {batch_id + 1}/{len(batches)}",
            prompt: f"""
            Apply {len(batch)} optimizations from batch {batch_id + 1}.

            Mode: {mode}

            For each optimization:
            1. Read file at specified path
            2. Apply the specified change
            3. Verify quality preserved (semantic check)
            4. Save file if verification passes
            5. Report token reduction
            6. If verification fails, rollback and report

            Optimizations to apply:
            {json.dumps(batch, indent=2)}

            Return accounting JSON:
            {{
                "applied": [
                    {{"file": "path.md", "line": 123, "tokens_saved": 45, "description": "..."}}
                ],
                "skipped": [
                    {{"file": "path.md", "line": 123, "reason": "..."}}
                ],
                "rolled_back": [
                    {{"file": "path.md", "line": 123, "reason": "verification failed"}}
                ]
            }}

            Verification: len(applied) + len(skipped) + len(rolled_back) = {len(batch)}
            """
        })

        # Handle batch errors
        if batch_result is None or (isinstance(batch_result, dict) and "error" in batch_result):
            error_msg = batch_result.get('error', 'Unknown error') if isinstance(batch_result, dict) else 'Agent returned None'

            response = AskUserQuestion({
                questions: [{
                    question: f"general-purpose agent (Haiku) batch {batch_id + 1}/{len(batches)} failed: {error_msg}. How to proceed?",
                    header: "general-purpose (Haiku) Error",
                    multiSelect: false,
                    options: [
                        {label: "Retry batch", description: f"Retry batch {batch_id + 1} with same model"},
                        {label: "Retry with Sonnet", description: "Use more capable model for this batch"},
                        {label: "Skip batch", description: f"Skip {len(batch)} optimizations in this batch"},
                        {label: "Manual mode", description: "Apply batch optimizations manually"},
                        {label: "Cancel all", description: "Stop optimization phase entirely"}
                    ]
                }]
            })

            if response == "Retry batch":
                # Retry with same model and prompt
                batch_result = Task({
                    subagent_type: "general-purpose",
                    model: "haiku",
                    description: f"Apply optimization batch {batch_id + 1} (retry)",
                    prompt: # ... same prompt as above
                })
            elif response == "Retry with Sonnet":
                # Retry with more capable model
                batch_result = Task({
                    subagent_type: "general-purpose",
                    model: "sonnet",
                    description: f"Apply optimization batch {batch_id + 1} (retry with Sonnet)",
                    prompt: # ... same prompt as above
                })
            elif response == "Skip batch":
                # Mark all optimizations in batch as skipped
                batch_result = {
                    "applied": [],
                    "skipped": [
                        {"file": opt["file"], "line": opt["line"], "reason": "Batch skipped by user"}
                        for opt in batch
                    ],
                    "rolled_back": []
                }
            elif response == "Manual mode":
                # Guide user through manual application for this batch
                print(f"""
                Manual Application - Batch {batch_id + 1}:

                {len(batch)} optimizations to apply:
                """)
                for i, opt in enumerate(batch, 1):
                    print(f"{i}. {opt['file']}:{opt['line']} - {opt['description']}")
                    print(f"   Token savings: {opt['token_saving']}")
                    print()

                return "Manual mode activated for batch {batch_id + 1}"
            else:  # Cancel all
                print(f"Optimization cancelled at batch {batch_id + 1}/{len(batches)}")
                print(f"Processed: {batch_id} batches")
                print(f"Remaining: {len(batches) - batch_id} batches")
                return "Optimization phase cancelled by user"

        results.append(batch_result)
        print(f"✓ Batch {batch_id + 1} complete")

else:
    # Single agent for small workloads
    print(f"Processing {optimization_count} optimizations (single batch)...")

    optimization_result = Task({
        subagent_type: "general-purpose",
        model: "haiku",  # Fast, cheap for simple edits
        description: "Apply all optimizations",
        prompt: f"""
        Apply {optimization_count} optimizations with {mode} mode.

        For each optimization:
        1. Read file at specified path
        2. Apply the specified change
        3. Verify quality preserved (semantic check)
        4. Save file if verification passes
        5. Report token reduction
        6. If verification fails, rollback and report

        Optimizations to apply:
        {json.dumps(optimizations, indent=2)}

        Return complete accounting JSON:
        {{
            "applied": [
                {{"file": "path.md", "line": 123, "tokens_saved": 45, "description": "..."}}
            ],
            "skipped": [
                {{"file": "path.md", "line": 123, "reason": "..."}}
            ],
            "rolled_back": [
                {{"file": "path.md", "line": 123, "reason": "verification failed"}}
            ]
        }}

        Verification: len(applied) + len(skipped) + len(rolled_back) = {optimization_count}
        """
    })

    # Handle errors
    if optimization_result is None or (isinstance(optimization_result, dict) and "error" in optimization_result):
        error_msg = optimization_result.get('error', 'Unknown error') if isinstance(optimization_result, dict) else 'Agent returned None'

        response = AskUserQuestion({
            questions: [{
                question: f"general-purpose agent (Haiku) optimization failed: {error_msg}. How to proceed?",
                header: "general-purpose (Haiku) Error",
                multiSelect: false,
                options: [
                    {label: "Retry", description: "Run optimization agent again"},
                    {label: "Retry with Sonnet", description: "Use more capable model"},
                    {label: "Manual optimization", description: "Apply optimizations manually"},
                    {label: "Cancel", description: "Stop cco-slim"}
                ]
            }]
        })

        if response == "Retry":
            # Retry with same model
            optimization_result = Task({
                subagent_type: "general-purpose",
                model: "haiku",
                description: "Apply all optimizations (retry)",
                prompt: # ... same prompt as above
            })
        elif response == "Retry with Sonnet":
            # Retry with more capable model
            optimization_result = Task({
                subagent_type: "general-purpose",
                model: "sonnet",
                description: "Apply all optimizations (retry with Sonnet)",
                prompt: # ... same prompt as above
            })
        elif response == "Manual optimization":
            # Guide user through manual application
            print(f"""
            Manual Application Mode:

            {optimization_count} optimizations to apply:
            """)
            for i, opt in enumerate(optimizations, 1):
                print(f"{i}. {opt['file']}:{opt['line']} - {opt['description']}")
                print(f"   Token savings: {opt['token_saving']}")
                if 'original_text' in opt and 'proposed_text' in opt:
                    print(f"   Change: {opt['original_text'][:50]}... → {opt['proposed_text'][:50]}...")
                print()

            return "Manual optimization mode - user will apply changes"
        else:  # Cancel
            return "cco-slim cancelled by user"

    results = [optimization_result]

# Aggregate results from all batches
total_applied = []
total_skipped = []
total_rolled_back = []

for result in results:
    if isinstance(result, dict):
        total_applied.extend(result.get("applied", []))
        total_skipped.extend(result.get("skipped", []))
        total_rolled_back.extend(result.get("rolled_back", []))

# Calculate totals
total_tokens_saved = sum(opt.get("tokens_saved", 0) for opt in total_applied)
files_modified = len(set(opt["file"] for opt in total_applied))

print(f"""
Optimization Complete:
- Applied: {len(total_applied)} optimizations
- Skipped: {len(total_skipped)} optimizations
- Rolled back: {len(total_rolled_back)} optimizations
- Files modified: {files_modified}
- Total tokens saved: {total_tokens_saved:,}

Accounting verification: {len(total_applied)} + {len(total_skipped)} + {len(total_rolled_back)} = {optimization_count}
""")

# Verify accounting
if len(total_applied) + len(total_skipped) + len(total_rolled_back) != optimization_count:
    print(f"⚠️ WARNING: Accounting mismatch!")
    print(f"Expected: {optimization_count}")
    print(f"Actual: {len(total_applied) + len(total_skipped) + len(total_rolled_back)}")
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
Slim analysis found 15-20 stub principle files containing only TODO markers without actual content. Affected files: principles/U_CHANGE_VERIFICATION.md, U_COMPLETE_REPORTING.md, C_HONEST_REPORTING.md, +12 others in ~/.claude/principles/. These need comprehensive implementation following C_AGENT_ORCHESTRATION_PATTERNS.md pattern (1847 tokens, complete structure with examples, rules, checklists).

SlashCommand({command: "/cco-generate principles"})
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


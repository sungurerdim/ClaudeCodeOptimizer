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

1. **Eliminate duplication** - CLAUDE.md + skills/agents/commands loading same files
2. **Detect incomplete content** - Stub files, TODO markers, missing implementations  
3. **Optimize CLAUDE.md** - Add frequently-used files, remove redundant references
4. **Token reduction without quality loss** - Preserve meaning, effectiveness, completeness
5. **Evaluate ALL context elements** - Principles, skills, agents, commands, docs, everything
6. **Optimize each file internally** - Every file with minimum tokens for maximum effectiveness

**Success = Minimum tokens for maximum quality.**


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

Use glob patterns (comma-separated):

**Examples:**
```
# Single file: docs/api.md
# Multiple patterns: src/components/**/*.tsx, tests/**/*.test.ts
# Exclude: src/**/*.py, -src/generated/**
```

---

## Component 2.5: Project Scope Detection (Default Behavior)

**DEFAULT: Optimize ONLY project files. Detect out-of-project files and ask user.**

### Why This Matters

- **Project files**: Safe to optimize, user has full control
- **Out-of-project files**: Could be shared across projects (e.g., global ~/.claude/)
- **User choice**: Let user decide whether to include external files

### Step 1: Detect Project Root

```python
import os
import subprocess

def get_project_root() -> str:
    """Get project root directory (git root or current working directory)."""

    # Try git root first
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        git_root = result.stdout.strip()
        if os.path.exists(git_root):
            return git_root
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to current working directory
    return os.getcwd()

project_root = get_project_root()
print(f"Project root detected: {project_root}")
```

### Step 2: Discover PROJECT-ONLY Files (Default Scope)

```python
# Launch discovery agent for PROJECT INTERNAL files ONLY
project_discovery_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    description: "Discover project-only files",
    prompt: f"""
    Discover files ONLY within project root directory.

    **STRICT PROJECT-ONLY SCOPE:**

    **Base directory:** {project_root}
    **Include:** All files and subdirectories WITHIN {project_root}
    **Exclude:** ANY paths outside {project_root}

    **Categories to find:**
    - Markdown: **/*.md files within project
    - Code: *.py, *.js, *.ts, *.tsx, *.java, *.go, *.rs within project
    - Tools: Any cco-*.md, skill, agent, principle files within project

    **CRITICAL:** Use Glob with base path {project_root} to ensure project-only scope.

    Return JSON:
    {{
        "project_root": "{project_root}",
        "markdown": ["path1.md"],
        "code": ["path1.py"],
        "tools": ["cco-*.md"],
        "total_files": 123,
        "total_tokens_estimate": 50000
    }}
    """
})

# Parse project files
project_files = project_discovery_result
```

### Step 3: Detect OUT-OF-PROJECT File References

```python
# Search for references to files OUTSIDE project root
out_of_project_refs = Task({
    subagent_type: "Explore",
    model: "haiku",
    description: "Detect out-of-project references",
    prompt: f"""
    Search for references to files OUTSIDE project root: {project_root}

    **Look for:**
    1. ~/.claude/* paths
    2. C:\\Users\\* paths (Windows)
    3. /Users/* paths (macOS)
    4. @principles/ @skills/ @agents/ references to global files
    5. Absolute paths outside {project_root}

    **Search in:**
    - README.md, CONTRIBUTING.md, ARCHITECTURE.md
    - All *.md files in project
    - CLAUDE.md if exists (may reference global principles)

    **Return JSON:**
    {{
        "out_of_project_files": [
            "~/.claude/CLAUDE.md",
            "~/.claude/principles/U_CHANGE_VERIFICATION.md",
            ...
        ],
        "reference_count": 50,
        "unique_files": 20
    }}

    If NO out-of-project references found, return empty list.
    """
})

# Parse out-of-project files
out_of_project_files = out_of_project_refs.get("out_of_project_files", [])
```

### Step 4: Ask User About Out-of-Project Files

```python
if len(out_of_project_files) > 0:
    # Display detected out-of-project files
    print(f"""
════════════════════════════════════════════════════════════════
         OUT-OF-PROJECT FILES DETECTED
════════════════════════════════════════════════════════════════

## Default Scope (Project Files ONLY)

**Project Root:** {project_root}
**Project Files:** {len(project_files['markdown']) + len(project_files['code']) + len(project_files['tools'])} files

✅ **Included by default:**
- All files within {project_root}

════════════════════════════════════════════════════════════════

## Out-of-Project Files Detected

**Location:** Outside {project_root}
**Total:** {len(out_of_project_files)} files detected

**Examples:**
{chr(10).join(f"  - {f}" for f in out_of_project_files[:10])}
{f"  ... and {len(out_of_project_files) - 10} more" if len(out_of_project_files) > 10 else ""}

════════════════════════════════════════════════════════════════
    """)

    # Ask user
    include_external = AskUserQuestion({
        questions: [{
            question: "Include out-of-project files in optimization?",
            header: "Scope Selection",
            multiSelect: false,
            options: [
                {
                    label: "No (Project Files ONLY - Recommended)",
                    description: f"Optimize ONLY files within {project_root} ({len(project_files['total_files'])} files)"
                },
                {
                    label: "Yes (Project + Out-of-Project)",
                    description: f"Include project ({len(project_files['total_files'])}) + out-of-project ({len(out_of_project_files)}) files"
                },
                {
                    label: "Only Out-of-Project Files",
                    description: f"Optimize ONLY the {len(out_of_project_files)} out-of-project files"
                },
                {
                    label: "Cancel",
                    description: "Exit cco-slim"
                }
            ]
        }]
    })

    # Handle user choice
    if include_external == "No (Project Files ONLY - Recommended)":
        final_files = project_files
        scope_description = f"Project files only ({project_root})"
    elif include_external == "Yes (Project + Out-of-Project)":
        # Merge project + out-of-project files
        final_files = merge_file_lists(project_files, out_of_project_files)
        scope_description = f"Project + out-of-project files"
    elif include_external == "Only Out-of-Project Files":
        # Use ONLY out-of-project files
        final_files = {"out_of_project": out_of_project_files}
        scope_description = "Out-of-project files only"
    else:  # Cancel
        return "cco-slim cancelled by user"
else:
    # No out-of-project files detected
    final_files = project_files
    scope_description = f"Project files only ({project_root})"
    print(f"✅ No out-of-project files detected. Optimizing project files only.")
```

### Step 5: Display Final Scope

```markdown
## Final Optimization Scope

**Scope:** {scope_description}
**Total Files:** {total_file_count}
**Estimated Tokens:** {total_token_estimate}

{if scope includes out-of-project}
⚠️ **Note:** Out-of-project files will be optimized. These may be shared across multiple projects.
{endif}
```

---

## Component 3: Discovery Phase

**Categorize all files in final scope, measure current token usage.**

### Step 1: File Discovery

**Discovery Flow:**

1. **Launch Explore Agent** (Haiku model for efficiency)
   - Input: `{selected_categories}` from Component 2
   - Task: Categorize files by patterns (markdown, code, tools, active context)
   - Output: JSON with categorized file lists

2. **Error Handling** (if agent fails):
   - Ask user via `AskUserQuestion`: Retry | Retry with Sonnet | Manual Glob | Cancel
   - **Retry**: Re-run with Haiku
   - **Retry with Sonnet**: Use more capable model
   - **Manual**: Fallback to `Glob("**/*.md")`, `Glob("**/*.py")`, etc. for each category
   - **Cancel**: Exit cco-slim

3. **Category Patterns:**
   - **Markdown**: `**/*.md` (exclude claudecodeoptimizer/content/)
   - **Code**: `*.{py,js,ts,tsx,java,go,rs}`
   - **Claude Tools**: `**/cco-*.md`, `**/skill-*.md`, `**/agent-*.md`
   - **Active Context**: `~/.claude/CLAUDE.md` + referenced principles

**Result:** `discovered` dict with file lists per category
```

### Step 2: Token Measurement

**For each discovered file:**
- Read content, count lines/tokens (estimate: words × 1.3)
- Calculate: redundancy score, example count, whitespace %
- Aggregate metrics by category

**Result:** `metrics[]` with per-file data + `total_tokens_before` sum

### Step 3: Display Discovery Results

**Show user:**
- Total files discovered: `{total_files}`
- Tokens by category (table: Category | Files | Tokens | Avg)
- Top optimization opportunities (files with high redundancy/examples)
- Estimated reduction range: `{min_pct}%-{max_pct}%`

---

## Component 3.5: Context Duplication Analysis
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
Slim analysis found 15-20 stub principle files containing only TODO markers without actual content. Affected files: principles/U_CHANGE_VERIFICATION.md, U_EVIDENCE_BASED_ANALYSIS.md, U_FOLLOW_PATTERNS.md, +12 others in ~/.claude/principles/. These need comprehensive implementation following C_AGENT_ORCHESTRATION_PATTERNS.md pattern (1847 tokens, complete structure with examples, rules, checklists).

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


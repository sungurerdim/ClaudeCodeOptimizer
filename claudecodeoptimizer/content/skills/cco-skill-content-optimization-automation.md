---
name: Content Optimization & Token Efficiency
description: Automatically detect, analyze, and optimize Claude Code content files to reduce token consumption while preserving 100% semantic meaning and functionality
keywords: [context window, token limit, optimize content, reduce tokens, large files, verbose content, context efficiency, token efficiency, content cleanup, optimization]
category: productivity
related_commands:
  action_types: [audit, optimize, status]
  categories: [quality]
pain_points: [5]
---

# Skill: Content Optimization & Token Efficiency

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


## Domain
Content optimization, token efficiency, context management

## Purpose
Proactively identify and optimize verbose Claude Code content (skills, commands, agents, principles, guides, CLAUDE.md) to maximize context window efficiency, achieving significant token reduction while preserving 100% functionality and professional quality.
---

---

## Core Techniques

### 1. Discovery & Analysis
**Systematically discover ALL Claude Code content**:
```python
# Step 1: Find CLAUDE.md to discover content structure
claude_md = Glob("**/CLAUDE.md")[0] if Glob("**/CLAUDE.md") else None

# Step 2: Extract @ references to find active content
active_content = []
if claude_md:
    content = Read(claude_md)
    # Find all @path/to/file.md references
    active_content = re.findall(r'@([^\s\n]+\.md)', content)

# Step 3: Find all .claude/ and content/ directories
all_claude_files = []
all_claude_files.extend(Glob("**/.claude/**/*.md"))
all_claude_files.extend(Glob("**/content/**/*.md"))

# Step 4: Auto-detect categories from directory structure
categories = {}
for file in all_claude_files:
    # Extract category from path (e.g., "content/skills/..." → "skills")
    path_parts = file.split('/')
    if 'content' in path_parts:
        idx = path_parts.index('content')
        category = path_parts[idx + 1] if len(path_parts) > idx + 1 else 'other'
    elif '.claude' in path_parts:
        idx = path_parts.index('.claude')
        category = path_parts[idx + 1] if len(path_parts) > idx + 1 else 'other'
    else:
        category = 'other'

    if category not in categories:
        categories[category] = []
    categories[category].append(file)

# Step 5: Analyze sizes and flag candidates
candidates = []
for file in all_claude_files:
    char_count = len(Read(file))
    token_estimate = char_count // 4

    if token_estimate > 1000:  # Flag large files
        candidates.append({
            'file': file,
            'chars': char_count,
            'tokens': token_estimate,
            'category': detect_category(file),
            'in_claude_md': file.replace('./', '') in active_content,
            'priority': 'high' if token_estimate > 5000 else 'medium'
        })
```

**Why**: Dynamic discovery catches all content types (known + future additions), prioritizes files actively loaded in CLAUDE.md

### 2. Verbosity Detection
**Pattern matching for optimization potential**:
```python
# Detect verbose patterns
verbosity_indicators = {
    'redundant_explanations': r'(Why|Purpose|Because|In order to).*\n.*\n.*\n',
    'tutorial_style': r'(Step \d+:|First,|Second,|Next,|Finally,)',
    'extensive_examples': r'```[\s\S]{500,}```',  # Code blocks >500 chars
    'duplicate_sections': r'(## .+\n[\s\S]+?){2,}(?=## )',  # Similar headers
    'verbose_comments': r'#.*{50,}',  # Long comments
    'excessive_whitespace': r'\n{3,}',  # 3+ newlines
}

score = sum([
    len(re.findall(pattern, content)) * weight
    for pattern, weight in verbosity_indicators.items()
])
```

**Why**: Quantifies optimization potential before user approval

### 3. Template-Based Optimization
**Category-specific templates for all Claude Code content types**:

**Commands**:
```markdown
# Command: [name]
**Purpose**: [1-2 sentences]
**Usage**: `[syntax]`

## Parameters
- **param**: [description]

## Workflow
1. [step]

## Example
```bash
[minimal]
```

**Output**: [format]
```

**Principles**:
```markdown
# [ID]: [Title]
**Severity**: [level]
[1-sentence summary]

## Why
[1 paragraph max]

## Rules/Patterns
- [concise bullets]

## Examples
### ❌ Bad
[minimal code]
**Why**: [1 line]

### ✅ Good
[minimal code]
**Why**: [1 line]
```

**Skills**:
```markdown
# Skill: [name]
**Domain**: [area]
**Purpose**: [1-2 sentences]

## Core Techniques
- **Technique**: [description]

## Patterns
### ✅ Good
```[lang]
[code]
```
**Why**: [1 line]

### ❌ Bad
```[lang]
[code]
```
**Why**: [1 line]

## Checklist
- [ ] [item]
```

**Agents**:
```markdown
# Agent: [name]
**Purpose**: [1-2 sentences]
**Capabilities**: [bullet list]

## Workflow
1. [step]

## Decision Logic
- **When**: [trigger]
- **Then**: [action]

## Example
[minimal]
```

**Guides**:
```markdown
# Guide: [name]
**Topic**: [area]
**Purpose**: [1 sentence]

## Steps
1. [action]

## Best Practices
- [item]

## Example
[minimal]
```

**CLAUDE.md**:
```markdown
<!-- Comments for metadata -->
@content/category/file.md

<!-- Concise section headers -->
## Section
Brief explanation (2-3 sentences max)
```

**Why**: Standardized templates ensure consistency and optimal compression across all content types

### 4. Parallel Agent Optimization
**Batch processing**:
```python
# Group files by similarity for parallel optimization
batches = group_by_category_and_size(candidates)

# Launch parallel agents (max 10 at once)
for batch in batches:
    tasks = []
    for file in batch[:10]:  # Max 10 parallel
        tasks.append(Task({
            'subagent_type': 'general-purpose',
            'model': 'sonnet',  # Balance quality/cost
            'prompt': f"""
Optimize {file} to reduce token count by 40-70%.

Template: {get_template(file_category)}

CRITICAL RULES:
1. Read file first
2. Preserve 100% functionality - ALL parameters, sections, examples
3. Remove ONLY: verbose explanations, redundant text, excessive whitespace
4. Use Edit tool (preserve git history)
5. Target 40-70% reduction (NOT more - quality over aggressive optimization)
6. Maintain professional quality and completeness

MUST PRESERVE:
- All metadata fields (id, name, description, category)
- All critical sections (Parameters, Workflow, Examples, etc.)
- All code examples (can condense, but keep at least 50%)
- All references and links
- All core techniques/capabilities
- Professional readability

Report back:
- Original chars
- New chars
- % reduction
- What was preserved (critical sections list)
- What was removed (verbose elements only)
"""
        }))

    # Wait for batch completion
    results = await_all(tasks)
```

**Why**: Significantly faster than sequential processing

### 5. User Approval Workflow
**Present findings with AskUserQuestion**:
```python
# Generate optimization proposal
report = f"""
OPTIMIZATION ANALYSIS
=====================

Files Analyzed: {total_files}
Optimization Candidates: {len(candidates)}
Estimated Token Savings: ~{total_savings:,} tokens

TOP 10 HIGH-IMPACT FILES:
{format_table(top_10_files)}

BREAKDOWN BY CATEGORY:
- Principles: {principles_count} files (~{principles_tokens:,} tokens)
- Commands: {commands_count} files (~{commands_tokens:,} tokens)
- Skills: {skills_count} files (~{skills_tokens:,} tokens)
- Agents: {agents_count} files (~{agents_tokens:,} tokens)

Optimization will:
✓ Preserve 100% functionality
✓ Reduce verbosity 60-80%
✓ Standardize format
✓ Free {total_savings:,} tokens for code analysis
"""

# Ask user for approval
AskUserQuestion({
    'questions': [{
        'question': f'{report}\n\nWhich files should I optimize?',
        'header': 'Optimization',
        'multiSelect': True,
        'options': [
            {'label': 'All candidates', 'description': f'Optimize all {len(candidates)} files'},
            {'label': 'Top 10 only', 'description': 'Just the largest files'},
            {'label': 'By category', 'description': 'Let me choose categories'},
            {'label': 'Manual selection', 'description': 'I\'ll pick specific files'}
        ]
    }]
})
```

**Why**: User maintains control, sees impact before execution

### 6. Quality Validation (CRITICAL - Zero Information Loss)
**Comprehensive post-optimization verification**:
```python
def verify_optimization(original_file, optimized_file):
    """
    STRICT validation to ensure professional quality maintained.
    ANY failure = rollback to original.
    """
    original = Read(original_file)
    optimized = Read(optimized_file)
    validation_errors = []

    # ==========================================
    # 1. METADATA PRESERVATION (100% Required)
    # ==========================================
    if original.startswith('---'):
        orig_yaml = extract_frontmatter(original)
        opt_yaml = extract_frontmatter(optimized)

        # Check ALL metadata fields preserved
        required_fields = ['id', 'name', 'description', 'category']
        for field in required_fields:
            if field in orig_yaml and field not in opt_yaml:
                validation_errors.append(f"Missing metadata field: {field}")
            elif orig_yaml.get(field) != opt_yaml.get(field):
                validation_errors.append(f"Metadata changed: {field}")

    # ==========================================
    # 2. CRITICAL SECTIONS PRESERVATION
    # ==========================================
    critical_sections = {
        'commands': {
            'required': ['## Parameters', '## Workflow', '## Example'],
            'patterns': [r'`/cco-[\w-]+`']  # Command syntax
        },
        'skills': {
            'required': ['## Core Techniques', '## Patterns', '## Checklist'],
            'patterns': [r'### ✅ Good', r'### ❌ Bad']  # Good/Bad examples
        },
        'agents': {
            'required': ['## Workflow', '## Decision Logic', '## Example'],
            'patterns': [r'## Capabilities']
        },
        'principles': {
            'required': ['## Why', '## Examples'],
            'patterns': [r'\*\*Severity\*\*:', r'### ✅', r'### ❌']
        },
        'guides': {
            'required': ['## Steps', '## Best Practices'],
            'patterns': []
        }
    }

    category = detect_category(original_file)
    if category in critical_sections:
        specs = critical_sections[category]

        # Check required sections
        for section in specs['required']:
            if section in original and section not in optimized:
                validation_errors.append(f"CRITICAL: Missing section '{section}'")

        # Check critical patterns
        for pattern in specs['patterns']:
            orig_matches = len(re.findall(pattern, original))
            opt_matches = len(re.findall(pattern, optimized))
            if orig_matches > opt_matches:
                validation_errors.append(
                    f"Pattern '{pattern}' reduced: {orig_matches} → {opt_matches}"
                )

    # ==========================================
    # 3. FUNCTIONAL CONTENT PRESERVATION
    # ==========================================

    # Commands: All parameters must be preserved
    if category == 'commands':
        orig_params = re.findall(r'- \*\*(\w+)\*\*:', original)
        opt_params = re.findall(r'- \*\*(\w+)\*\*:', optimized)
        missing_params = set(orig_params) - set(opt_params)
        if missing_params:
            validation_errors.append(f"Missing parameters: {missing_params}")

    # Skills: All core techniques must be preserved
    if category == 'skills':
        orig_techniques = re.findall(r'- \*\*([^*]+)\*\*:', original)
        opt_techniques = re.findall(r'- \*\*([^*]+)\*\*:', optimized)
        missing_techniques = set(orig_techniques) - set(opt_techniques)
        if missing_techniques:
            validation_errors.append(f"Missing techniques: {missing_techniques}")

    # Principles: Severity must be preserved
    if category == 'principles':
        orig_severity = re.search(r'\*\*Severity\*\*:\s*(\w+)', original)
        opt_severity = re.search(r'\*\*Severity\*\*:\s*(\w+)', optimized)
        if orig_severity and not opt_severity:
            validation_errors.append("Severity level missing")
        elif orig_severity and opt_severity:
            if orig_severity.group(1) != opt_severity.group(1):
                validation_errors.append("Severity level changed")

    # ==========================================
    # 4. CODE EXAMPLES PRESERVATION
    # ==========================================
    orig_code_blocks = len(re.findall(r'```[\s\S]*?```', original))
    opt_code_blocks = len(re.findall(r'```[\s\S]*?```', optimized))

    # Allow reduction but not complete removal
    if orig_code_blocks > 0 and opt_code_blocks == 0:
        validation_errors.append("All code examples removed!")
    elif opt_code_blocks < orig_code_blocks * 0.5:  # <50% of examples
        validation_errors.append(
            f"Too many examples removed: {orig_code_blocks} → {opt_code_blocks}"
        )

    # ==========================================
    # 5. REFERENCES & LINKS PRESERVATION
    # ==========================================
    # @ references (to other content)
    orig_refs = set(re.findall(r'@(content/[^\s\n]+)', original))
    opt_refs = set(re.findall(r'@(content/[^\s\n]+)', optimized))
    missing_refs = orig_refs - opt_refs
    if missing_refs:
        validation_errors.append(f"Missing references: {missing_refs}")

    # Related commands/skills
    orig_related = set(re.findall(r'/cco-[\w-]+', original))
    opt_related = set(re.findall(r'/cco-[\w-]+', optimized))
    missing_related = orig_related - opt_related
    if missing_related:
        validation_errors.append(f"Missing related items: {missing_related}")

    # ==========================================
    # 6. SEMANTIC KEYWORDS PRESERVATION
    # ==========================================
    # Critical domain keywords must not be removed
    category_keywords = {
        'skills': ['technique', 'pattern', 'checklist'],
        'commands': ['parameter', 'workflow', 'example', 'output'],
        'agents': ['workflow', 'decision', 'capability'],
        'principles': ['why', 'rule', 'example']
    }

    if category in category_keywords:
        for keyword in category_keywords[category]:
            orig_count = original.lower().count(keyword)
            opt_count = optimized.lower().count(keyword)
            if orig_count > 0 and opt_count == 0:
                validation_errors.append(
                    f"Critical keyword '{keyword}' completely removed"
                )

    # ==========================================
    # 7. REDUCTION QUALITY CHECK
    # ==========================================
    orig_tokens = len(original) // 4
    opt_tokens = len(optimized) // 4
    reduction = (orig_tokens - opt_tokens) / orig_tokens

    # Conservative target: 40-70% (NOT 60-90%)
    if reduction < 0.40:
        validation_errors.append(
            f"Insufficient optimization: {reduction:.1%} (target: 40-70%)"
        )
    elif reduction > 0.70:
        validation_errors.append(
            f"Over-optimization risk: {reduction:.1%} (target: 40-70%)"
        )

    # ==========================================
    # 8. READABILITY CHECK
    # ==========================================
    # Ensure file is still readable (not completely cryptic)
    if opt_tokens < 100:  # Less than 400 chars
        validation_errors.append(
            f"File too short: {opt_tokens} tokens (may be over-compressed)"
        )

    # ==========================================
    # FINAL VERDICT
    # ==========================================
    validation_passed = len(validation_errors) == 0

    return {
        'original_tokens': orig_tokens,
        'optimized_tokens': opt_tokens,
        'reduction': reduction,
        'validation_passed': validation_passed,
        'errors': validation_errors,
        'checks': {
            'metadata_preserved': 'Missing metadata field' not in str(validation_errors),
            'sections_intact': 'Missing section' not in str(validation_errors),
            'parameters_preserved': 'Missing parameters' not in str(validation_errors),
            'examples_adequate': 'examples removed' not in str(validation_errors),
            'references_intact': 'Missing references' not in str(validation_errors),
            'reduction_acceptable': 0.40 <= reduction <= 0.70
        }
    }

# ROLLBACK LOGIC
def apply_optimization_with_rollback(file, optimized_content, validation):
    if not validation['validation_passed']:
        print(f"⚠ VALIDATION FAILED for {file}:")
        for error in validation['errors']:
            print(f"  ❌ {error}")
        print(f"  → ROLLING BACK to original")

        # Restore from backup
        backup_file = get_backup_path(file)
        Bash(f"cp {backup_file} {file}")

        return {
            'status': 'rolled_back',
            'reason': validation['errors']
        }
    else:
        # Validation passed, optimization accepted
        return {
            'status': 'success',
            'reduction': validation['reduction']
        }
```

**Why**: **STRICT** validation ensures professional quality maintained, automatic rollback on ANY quality issue

### 7. Impact Reporting
**Generate comprehensive report**:
```python
# After optimization, create detailed report
report = f"""
# Content Optimization Report

**Date**: {datetime.now()}
**Status**: ✅ COMPLETED

## Summary
- Files Optimized: {optimized_count}
- Total Token Savings: ~{total_savings:,} tokens
- Average Reduction: {avg_reduction:.1%}
- Context Efficiency: {efficiency_gain:.1f}x improvement

## By Category
{generate_category_table(results)}

## Top 10 Optimizations
{generate_top_10_table(results)}

## Quality Metrics
- Metadata Preserved: {metadata_ok}/{total_files} ✓
- Sections Intact: {sections_ok}/{total_files} ✓
- Functionality Verified: {func_ok}/{total_files} ✓

## Context Window Impact
- Before: {before_usage:.1%} context used by docs
- After: {after_usage:.1%} context used by docs
- Available for Code: {code_context:.1%} → {new_code_context:.1%}
"""

# Display report in console (zero file pollution)
print(report)
```

**Why**: Provides transparency, tracks improvements over time

---

## Patterns

### ✅ Good: Proactive Detection
```python
# Triggered by context window warning
if "context window" in system_message or token_usage > 150000:
    # Scan for optimization opportunities
    candidates = scan_for_verbose_files()

    if candidates:
        # Automatic proposal
        present_optimization_proposal(candidates)
```
**Why**: Prevents context overflow before it becomes a problem

### ✅ Good: Incremental Optimization
```python
# After adding new content
@hook('post_file_create', pattern='**/.claude/**/*.md')
def check_new_content(file_path):
    size = os.path.getsize(file_path)
    if size > 5000:  # >5KB
        suggest_optimization(file_path)
```
**Why**: Keeps content lean from day one

### ✅ Good: Backup Before Optimization
```python
# Use git for backup (zero file pollution)
# Git already tracks all changes, no separate backup needed
Bash("git stash push -m 'Pre-optimization backup'")

# Or for specific files, rely on git history:
# git show HEAD:path/to/file

# Now safe to optimize
optimize_files(to_optimize)
```
**Why**: Allows rollback if optimization causes issues

### ❌ Bad: Optimize Without Analysis
```python
# DON'T blindly optimize
for file in all_md_files:
    optimize(file)  # May optimize already-lean files!
```
**Why**: Wastes time, may over-compress critical content

### ❌ Bad: No User Approval
```python
# DON'T auto-optimize without consent
if len(file) > 10000:
    optimize(file)  # User didn't approve!
```
**Why**: Violates user control, may surprise user with changes

### ❌ Bad: Sequential Processing
```python
# DON'T process files one-by-one
for file in large_files:
    result = optimize_file(file)  # Very slow!
```
**Why**: Parallel agents are significantly faster

---

## Checklist

### Before Optimization
- [ ] Scan all Claude content files (skills/commands/agents/principles)
- [ ] Calculate token usage and optimization potential
- [ ] Generate analysis report with top candidates
- [ ] Present findings to user with AskUserQuestion
- [ ] Get explicit approval for files to optimize

### During Optimization
- [ ] Create backup of all files to optimize
- [ ] Use parallel agents (max 10) for batch processing
- [ ] Apply category-specific templates
- [ ] Target 60-80% token reduction per file
- [ ] Preserve ALL metadata and critical sections

### After Optimization
- [ ] Verify metadata intact for each file
- [ ] Verify critical sections preserved
- [ ] Check token reduction within 60-90% range
- [ ] Run validation checks (grep for missing sections)
- [ ] Generate optimization report with metrics
- [ ] Update CLAUDE.md if structure changed
- [ ] Commit changes with detailed commit message

### Quality Assurance
- [ ] Test skill/command activation after optimization
- [ ] Verify principles still load correctly
- [ ] Check no broken @content/... references
- [ ] Confirm context window usage improved

---

## Success Metrics

**Target Results**:
- Token reduction: significant per file
- Zero information loss: 100% functionality preserved
- Batch efficiency: fast parallel processing
- Context gain: significantly more space for code analysis

**Indicators of Success**:
- Context warnings eliminated
- Faster Claude Code sessions
- More code fits in context window
- Consistent file formats across content

---

## Automatic Activation

This skill activates when:
- Context window >150K tokens (75% full)
- Large files detected in `.claude/` or `content/`
- Keywords: "optimize content", "reduce tokens", "context window"
- Post-addition: New skill/command/principle >5KB created
- Manual: `/cco-optimize` command

---

## Example Workflow

```
1. Detection:
   "⚠ Context window 160K/200K (80% full)"
   → Skill activates automatically

2. Analysis:
   Scanning content files...
   Found [N] optimization candidates
   Potential savings: significant tokens

3. Proposal:
   TOP HIGH-IMPACT FILES:
   [List of files with token counts]
   ...

   Optimize all [N] files? [Yes] [Top 10] [Custom]

4. Execution:
   ✓ Backing up [N] files...
   ✓ Launching 10 parallel agents...
   ✓ Batch 1/5 complete (10 files, 8 min)
   ✓ Batch 2/5 complete (10 files, 7 min)
   ...

5. Validation:
   ✓ [N]/[N] metadata preserved
   ✓ [N]/[N] sections intact
   ✓ Average reduction: [X]%
   ✓ Token savings: [N] tokens

6. Report:
   Context: significantly improved
   Recovery: git stash pop (if needed)
```

---

## Integration with Other Skills

**Works well with**:
- `cco-skill-git-branching-pr-review` - Commit optimized files properly
- `cco-skill-docs-api-openapi-adr-runbooks` - Optimize documentation
- `cco-skill-cicd-gates-deployment-automation` - Run in CI for content validation

**Triggers**:
- Large skill/command file created → Suggest optimization
- Context window warning → Auto-analyze and propose
- Manual optimization request → Execute workflow
- Periodic maintenance → Monthly optimization check

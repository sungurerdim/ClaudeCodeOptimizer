---
name: ai-code-quality-verification-debt
description: Detect and fix AI-generated code issues including hallucination, copy/paste patterns, code bloat, model inconsistency, and vibe coding anti-patterns through signature analysis and quality metrics
keywords: [AI code, hallucination, copy paste, code bloat, vibe coding, AI debt, model detection, ChatGPT, Copilot, Claude, generated code quality, AI verification]
category: quality
related_commands:
  action_types: [audit, fix]
  categories: [ai-quality, ai-debt, tech-debt, code-quality]
pain_points: [2, 3, 8, 9]
---

# AI Code Quality, Verification & Debt

Detect and fix AI-generated code issues: hallucination, copy/paste, bloat, model inconsistency, vibe coding.
---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Domain

Projects using AI code assistants (ChatGPT, Copilot, Claude, Cursor, etc.), codebases with 10%+ AI-generated code.

---

## Purpose

**2025 Crisis:** AI generates 35%+ of code, but:
- 66% developers frustrated: "almost right, not quite"
- 45% say debugging AI code takes MORE time
- Copy/paste code surpassed moved code in 2022, still rising
- "Vibe coding": prompt without reading → technical debt tsunami
- Only 3% "highly trust" AI output

This skill helps identify AI-generated code problems BEFORE they become production issues.

---

## Core Techniques

### 1. AI Tool Signature Detection

**Identify which AI generated code:**

```python
# ChatGPT Signatures
CHATGPT_PATTERNS = [
    r"Here's how you can",
    r"You can use",
    r"This will allow you to",
    r"# Step \d+:",
    r"very_descriptive_variable_name",  # Over-verbose names
]

# GitHub Copilot Signatures
COPILOT_PATTERNS = [
    r"\bres\b|\bdata\b|\bresult\b|\bresponse\b",  # Generic names
    r"# TODO: Error handling",  # Placeholder comments
    r"pass  # Implementation",
]

# Claude Signatures
CLAUDE_PATTERNS = [
    r"<!--.*?-->",  # XML-style comments
    r"# IMPORTANT:",
    r"Comprehensive error handling",
    r"Type hints.*fully specified",
]

def detect_ai_tool(code: str) -> Optional[str]:
    """Returns: 'chatgpt', 'copilot', 'claude', or None"""
    scores = {
        'chatgpt': sum(1 for p in CHATGPT_PATTERNS if re.search(p, code, re.I)),
        'copilot': sum(1 for p in COPILOT_PATTERNS if re.search(p, code, re.I)),
        'claude': sum(1 for p in CLAUDE_PATTERNS if re.search(p, code, re.I))
    }
    tool, score = max(scores.items(), key=lambda x: x[1])
    return tool if score > 2 else None
```

**Model Consistency Check:**
```python
def check_model_consistency(file_path: str) -> dict:
    """Detect if multiple AI tools used in same file (bad practice)"""
    with open(file_path) as f:
        functions = extract_functions(f.read())

    tools = [detect_ai_tool(fn) for fn in functions if detect_ai_tool(fn)]
    unique_tools = set(tools)

    return {
        'consistent': len(unique_tools) <= 1,
        'tools_used': list(unique_tools),
        'mixing_detected': len(unique_tools) > 1
    }
```

---

### 2. API Hallucination Detection

**Non-existent APIs, wrong signatures:**

```python
def detect_api_hallucination(code: str, project_files: List[str]) -> List[dict]:
    """Find calls to non-existent functions/methods"""
    issues = []

    # Extract all function calls
    calls = re.findall(r'(\w+)\(', code)

    # Check if defined in project or stdlib
    import_checker = ImportChecker(project_files)
    for call in calls:
        if not import_checker.exists(call):
            issues.append({
                'type': 'hallucinated_function',
                'function': call,
                'severity': 'HIGH',
                'message': f"Function '{call}' doesn't exist"
            })

    # Check method signatures
    method_calls = re.findall(r'(\w+)\.(\w+)\((.*?)\)', code)
    for obj, method, args in method_calls:
        expected_sig = import_checker.get_signature(obj, method)
        actual_args = len(args.split(',')) if args else 0
        if expected_sig and actual_args != expected_sig.param_count:
            issues.append({
                'type': 'wrong_signature',
                'method': f"{obj}.{method}",
                'expected': expected_sig.param_count,
                'actual': actual_args,
                'severity': 'HIGH'
            })

    return issues
```

---

### 3. Copy/Paste Pattern Detection

**AST-based similarity:**

```python
from ast import parse, dump

def detect_copy_paste(file_path: str) -> List[dict]:
    """Find duplicated code blocks (AI copy/paste signature)"""
    with open(file_path) as f:
        tree = parse(f.read())

    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    duplicates = []

    for i, fn1 in enumerate(functions):
        for fn2 in functions[i+1:]:
            similarity = compute_ast_similarity(fn1, fn2)
            if similarity > 0.80:  # 80%+ similar
                duplicates.append({
                    'function1': fn1.name,
                    'function2': fn2.name,
                    'similarity': similarity,
                    'lines1': (fn1.lineno, fn1.end_lineno),
                    'lines2': (fn2.lineno, fn2.end_lineno),
                    'severity': 'MEDIUM'
                })

    return duplicates

def compute_ast_similarity(node1, node2) -> float:
    """Structural similarity ignoring variable names"""
    ast1 = normalize_ast(dump(node1))
    ast2 = normalize_ast(dump(node2))
    return difflib.SequenceMatcher(None, ast1, ast2).ratio()
```

---

### 4. Code Bloat Detection

**AI code tends to be verbose:**

```python
def detect_code_bloat(code: str) -> dict:
    """Measure unnecessary verbosity"""
    lines = [l.strip() for l in code.split('\n') if l.strip()]
    code_lines = [l for l in lines if not l.startswith('#')]
    comment_lines = [l for l in lines if l.startswith('#')]
    docstring_lines = len(re.findall(r'""".*?"""', code, re.DOTALL))

    complexity = calculate_complexity(code)  # McCabe complexity

    return {
        'lines_of_code': len(code_lines),
        'comment_ratio': len(comment_lines) / len(lines) if lines else 0,
        'docstring_density': docstring_lines / len(code_lines) if code_lines else 0,
        'complexity': complexity,
        'bloat_score': calculate_bloat_score(len(code_lines), complexity),
        'is_bloated': len(code_lines) > 50 and complexity < 5  # Simple but verbose
    }

def calculate_bloat_score(loc: int, complexity: int) -> float:
    """Higher score = more bloat. Ideal ratio: ~10 LOC per complexity point"""
    if complexity == 0:
        return 100  # Trivial function with many lines = bloat
    ratio = loc / complexity
    return min(100, (ratio / 10) * 100)  # 10 LOC/complexity = 100% bloat
```

---

### 5. Vibe Coding Detection

**Code without understanding:**

```python
def detect_vibe_coding(file_path: str, git_log: str) -> dict:
    """Pattern: Complex code + No comments + Recent commit = Vibe coding"""
    with open(file_path) as f:
        code = f.read()

    # Check recent changes
    is_recent = file_path in git_log  # Modified in last commit

    # Calculate vibe coding score
    complexity = calculate_complexity(code)
    comment_density = len([l for l in code.split('\n') if l.strip().startswith('#')])
    lines = len([l for l in code.split('\n') if l.strip() and not l.strip().startswith('#')])

    vibe_score = complexity / (comment_density + 1)  # Higher = likely vibe coded

    return {
        'vibe_coding_score': vibe_score,
        'is_vibe_coded': vibe_score > 5 and is_recent,  # Complex, no comments, recent
        'complexity': complexity,
        'comments': comment_density,
        'lines': lines,
        'recommendation': 'Add detailed comments explaining logic' if vibe_score > 5 else None
    }
```

---

### 6. Logic Bug Detection

**Common AI mistakes:**

```python
def detect_common_ai_bugs(code: str) -> List[dict]:
    """Find typical AI-generated bugs"""
    issues = []

    # Off-by-one errors
    if re.search(r'for\s+\w+\s+in\s+range\([^)]+\):\s*\n\s*\w+\[\w+\s*\+\s*1\]', code):
        issues.append({
            'type': 'potential_off_by_one',
            'pattern': 'Loop index + 1 in array access',
            'severity': 'MEDIUM'
        })

    # Infinite loop risk
    while_loops = re.findall(r'while\s+(.+?):', code)
    for condition in while_loops:
        if 'True' in condition or '1' in condition:
            issues.append({
                'type': 'infinite_loop_risk',
                'condition': condition,
                'severity': 'HIGH'
            })

    # Missing error handling
    try_blocks = len(re.findall(r'\btry:', code))
    risky_ops = len(re.findall(r'open\(|requests\.|http|urllib', code))
    if risky_ops > 0 and try_blocks == 0:
        issues.append({
            'type': 'missing_error_handling',
            'risky_operations': risky_ops,
            'severity': 'MEDIUM'
        })

    # Type errors (no type hints on complex functions)
    complex_funcs = re.findall(r'def\s+(\w+)\([^)]*\):', code)
    typed_funcs = re.findall(r'def\s+\w+\([^)]*\)\s*->', code)
    if len(complex_funcs) > 5 and len(typed_funcs) == 0:
        issues.append({
            'type': 'missing_type_hints',
            'functions': len(complex_funcs),
            'severity': 'LOW'
        })

    return issues
```

---

## Patterns

### Complete AI Code Audit

```python
def audit_ai_code_quality(file_path: str, git_log: str) -> dict:
    """Comprehensive AI code quality check"""
    with open(file_path) as f:
        code = f.read()

    return {
        'ai_tool': detect_ai_tool(code),
        'model_consistency': check_model_consistency(file_path),
        'hallucinations': detect_api_hallucination(code, project_files),
        'copy_paste': detect_copy_paste(file_path),
        'bloat': detect_code_bloat(code),
        'vibe_coding': detect_vibe_coding(file_path, git_log),
        'logic_bugs': detect_common_ai_bugs(code)
    }
```

### Automated Fixes

```python
def fix_ai_debt(file_path: str, issues: dict) -> List[str]:
    """Apply safe automated fixes"""
    fixes_applied = []

    # Deduplicate copy/pasted code
    if issues['copy_paste']:
        extract_common_function(issues['copy_paste'])
        fixes_applied.append('Deduplicated copy/pasted code')

    # Add error handling
    if any(i['type'] == 'missing_error_handling' for i in issues['logic_bugs']):
        add_try_catch_blocks(file_path)
        fixes_applied.append('Added error handling')

    # Add type hints
    if any(i['type'] == 'missing_type_hints' for i in issues['logic_bugs']):
        infer_and_add_types(file_path)
        fixes_applied.append('Added type hints')

    # Reduce bloat (requires approval - risky)
    if issues['bloat']['is_bloated']:
        fixes_applied.append('NEEDS_APPROVAL: Refactor bloated code')

    return fixes_applied
```

---

## Checklist

### Detection
- [ ] AI tool signature identified
- [ ] Model consistency checked (no mixing)
- [ ] API hallucinations detected
- [ ] Copy/paste patterns found
- [ ] Code bloat measured
- [ ] Vibe coding score calculated
- [ ] Common logic bugs checked

### Quality Metrics
- [ ] Bloat score < 50 (acceptable verbosity)
- [ ] Vibe coding score < 5 (adequate comments)
- [ ] No hallucinated APIs
- [ ] Copy/paste similarity < 80%
- [ ] Error handling present for risky ops
- [ ] Type hints on complex functions

### Fixes
- [ ] Deduplicate copy/pasted code
- [ ] Add missing error handling
- [ ] Add type hints
- [ ] Document complex logic
- [ ] Refactor bloated code (with approval)

---

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for AI code quality domain
action_types: [audit, fix]
keywords: [AI code, hallucination, copy paste, code bloat, vibe coding, AI debt]
category: quality
pain_points: [2, 3, 8, 9]  # AI Quality Crisis, AI Tech Debt, Platform Incompatibility, AI Security
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*[pattern]` in frontmatter
2. Match `category: quality` or related categories
3. Present matching commands with their parameters

---

## References

- [GitClear: AI Copilot Code Quality Report 2024-2025](https://www.gitclear.com/)
- [DORA 2025: AI Amplification Effect](https://dora.dev/)
- [Stack Overflow Survey 2025: AI Trust Crisis](https://survey.stackoverflow.co/2025/)
- [Ox Security: AI Technical Debt Report](https://www.oxsecurity.com/)

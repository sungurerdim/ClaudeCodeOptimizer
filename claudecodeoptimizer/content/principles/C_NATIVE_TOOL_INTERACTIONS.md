---
name: native-tool-interactions
description: All user interactions must use native Claude Code tools with MultiSelect questions including "All" option
type: claude
severity: critical
keywords: [user interaction, UX, multiselect, native tools, cross-platform]
category: [ux, tooling]
---

# C_NATIVE_TOOL_INTERACTIONS: Native Claude Code Tools for All User Interactions

**Severity**: Critical

All user interactions must use native Claude Code tools (AskUserQuestion, etc.). MultiSelect questions must always include "All" option.

---

## Why

- Text-based prompts break UX flow and require manual parsing
- Native tools provide consistent UI, validation, and accessibility
- "All" option enables efficient bulk selection without clicking each item
- Ensures cross-platform compatibility

---

## Rules

### 1. Always Use Native Tools

```python
# ❌ BAD: Text-based prompt
print("Select option (1/2/3): ")
user_input = input()

# ❌ BAD: Markdown checkbox list
print("""
Select options:
- [ ] Security
- [ ] Testing
- [ ] Database
""")

# ✅ GOOD: Native AskUserQuestion
AskUserQuestion({
  questions: [{
    question: "Which checks do you want to run?",
    header: "Audit Selection",
    multiSelect: true,
    options: [
      {label: "All", description: "Select all options"},
      {label: "Security", description: "OWASP, secrets, vulnerabilities"},
      {label: "Testing", description: "Coverage, isolation, pyramid"},
      {label: "Database", description: "N+1, indexes, migrations"}
    ]
  }]
})
```

### 2. MultiSelect Must Have "All" Option

```python
# ❌ BAD: No All option
options: [
  {label: "Security", description: "..."},
  {label: "Testing", description: "..."},
  {label: "Database", description: "..."}
]

# ✅ GOOD: All option first
options: [
  {label: "All", description: "Select all options below"},
  {label: "Security", description: "..."},
  {label: "Testing", description: "..."},
  {label: "Database", description: "..."}
]
```

### 3. Handle "All" Selection

```python
def process_selection(selected_options):
    """When All is selected, treat as all options selected."""

    if "All" in selected_options:
        # All means everything except "All" itself
        return [opt for opt in ALL_OPTIONS if opt != "All"]

    return selected_options
```

### 4. Grouped MultiSelect with "All [Group]"

When questions have categories/tabs, each group needs its own "All":

```python
# Critical category question
options: [
  {label: "All Critical", description: "Select all critical checks"},
  {label: "Security", description: "OWASP Top 10"},
  {label: "AI Security", description: "Prompt injection"},
  {label: "Tech Debt", description: "Dead code, complexity"}
]

# High priority category question
options: [
  {label: "All High", description: "Select all high priority checks"},
  {label: "Testing", description: "Coverage gaps"},
  {label: "Integration", description: "Import errors"}
]
```

---

## Question Design Patterns

### Single Selection (No "All" needed)

```python
# Confirmation - Yes/No
{
  question: "Proceed with fixes?",
  header: "Confirm",
  multiSelect: false,
  options: [
    {label: "Yes", description: "Apply all safe fixes"},
    {label: "No", description: "Cancel operation"}
  ]
}
```

### Multiple Selection (Always "All")

```python
# Category selection
{
  question: "Which categories to audit?",
  header: "Categories",
  multiSelect: true,
  options: [
    {label: "All", description: "Run all category audits"},
    {label: "Security", description: "Vulnerabilities and secrets"},
    {label: "Quality", description: "Code quality and tech debt"},
    {label: "Testing", description: "Test coverage and isolation"}
  ]
}
```

### Tabbed/Grouped Selection

```python
# Multiple questions, each with its own "All"
questions: [
  {
    question: "Critical checks?",
    header: "Critical",
    multiSelect: true,
    options: [
      {label: "All Critical", description: "All critical checks"},
      {label: "SQL Injection", description: "..."},
      {label: "XSS", description: "..."}
    ]
  },
  {
    question: "High priority checks?",
    header: "High",
    multiSelect: true,
    options: [
      {label: "All High", description: "All high priority checks"},
      {label: "N+1 Queries", description: "..."},
      {label: "Missing Tests", description: "..."}
    ]
  }
]
```

---

## Self-Enforcement

This principle applies to:
1. **CCO component definitions** - All user prompts use AskUserQuestion
2. **Runtime execution** - Components use native tools when running
3. **Generated outputs** - Any new commands follow same pattern

### Verification

```python
# Check for non-native patterns
NON_NATIVE_PATTERNS = [
    r'print\(["\']Select',
    r'input\(',
    r'\[ \]',  # Markdown checkboxes
    r'Enter.*:',
    r'\(y/n\)',
    r'\(1/2/3\)',
]

# Check for missing All option
def verify_multiselect(question):
    if question.get("multiSelect") and question.get("options"):
        labels = [opt["label"] for opt in question["options"]]
        if not any("All" in label for label in labels):
            raise ValueError(f"MultiSelect missing 'All' option: {question['header']}")
```

---

## Checklist

- [ ] All user interactions use AskUserQuestion tool
- [ ] Every multiSelect has "All" as first option
- [ ] Grouped questions have "All [Group]" option each
- [ ] No text-based prompts (print/input patterns)
- [ ] No markdown checkbox lists for selection
- [ ] "All" selection handled correctly (expands to all other options)

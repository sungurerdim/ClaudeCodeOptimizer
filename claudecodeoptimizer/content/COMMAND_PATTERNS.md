# CCO Command Patterns - Reusable Templates

**Purpose:** DRY for common command patterns. Define once, reference everywhere.

**How to Use:** Commands reference this file instead of duplicating patterns.

---

## Pattern 1: Step 0 Introduction Template

**Usage:** Every command MUST start with Step 0 introduction + single confirmation.

```markdown
## Step 0: Introduction and Confirmation

**Welcome to cco-{command} - {Title}**

This command {what-it-does-in-1-2-sentences}.

### What This Command Does

**{Category} Types:**
- {Type 1 with brief description}
- {Type 2 with brief description}
- {Type 3 with brief description}

### What You'll Be Asked

1. **Confirmation** (Start {command})
2. **{Selection Type}** (Which {items} to {action})
3. **{Optional Step}** (If applicable)

### Time Commitment

- {Phase 1}: {time-range}
- {Phase 2}: {time-range}
- Total: {total-range}

### What You'll Get

**{Output Category}:**
- {Expected output 1}
- {Expected output 2}
- {Expected output 3}

\`\`\`python
AskUserQuestion({
  questions: [{
    question: "Ready to start {command}?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {
        label: "Start {Command}",
        description: "Begin {action description}"
      },
      {
        label: "Cancel",
        description: "Exit cco-{command}"
      }
    ]
  }]
})
\`\`\`

**If user selects "Cancel":**
Exit immediately with message: "cco-{command} cancelled. No changes made."

**If user selects "Start":**
Continue to {next-step}.
```

---

## Pattern 2: Category Selection (Multi-Select with "All")

**Usage:** When user selects which categories to process.

```python
AskUserQuestion({
  questions: [
    {
      question: "Select {category-group-1} to {action}:",
      header: "{Group-1-Label}",
      multiSelect: true,
      options: [
        {
          label: "All {Group-1}",
          description: "Select all {group-1} {items}"
        },
        {
          label: "{Item-1}",
          description: "{Description with metrics if available}"
        },
        {
          label: "{Item-2}",
          description: "{Description with metrics}"
        },
        {
          label: "{Item-3}",
          description: "{Description with metrics}"
        }
      ]
    },
    {
      question: "Select {category-group-2} to {action}:",
      header: "{Group-2-Label}",
      multiSelect: true,
      options: [
        {
          label: "All {Group-2}",
          description: "Select all {group-2} {items}"
        },
        {
          label: "{Item-1}",
          description: "{Description with metrics}"
        },
        {
          label: "{Item-2}",
          description: "{Description with metrics}"
        }
      ]
    },
    {
      question: "Or select all:",
      header: "✅ All",
      multiSelect: true,
      options: [
        {
          label: "All {Items}",
          description: "Run ALL {actions} with full {coverage}"
        }
      ]
    }
  ]
})
```

**Processing "All" selections:**

```python
def process_selections(user_selections: Dict[str, List[str]]) -> List[str]:
    """
    Process user selections, handling "All" options.

    Returns: List of individual items selected
    """
    selected_items = []

    # Check for global "All"
    if "All Items" in user_selections.get("✅ All", []):
        return ALL_POSSIBLE_ITEMS

    # Process per-group "All" options
    for group, selections in user_selections.items():
        if f"All {group}" in selections:
            # Add all items from this group
            selected_items.extend(get_all_items_in_group(group))
        else:
            # Add individual selections
            selected_items.extend(selections)

    return selected_items
```

---

## Pattern 3: Progress Reporting (Phase Transitions)

**Usage:** Explicit phase start/complete announcements.

```python
class PhaseTracker:
    """Track and report phase transitions."""

    def __init__(self, total_phases: int):
        self.total_phases = total_phases
        self.current_phase = 0
        self.phase_times = {}

    def start_phase(self, phase_number: int, phase_name: str):
        """Announce phase start."""
        self.current_phase = phase_number
        self.phase_times[phase_number] = {"start": time.time()}

        print(f"""
════════════════════════════════════════════════════════════════
Phase {phase_number}/{self.total_phases}: {phase_name} ▶ STARTED
════════════════════════════════════════════════════════════════
""")

    def complete_phase(self, phase_number: int, phase_name: str):
        """Announce phase completion with duration."""
        end_time = time.time()
        start_time = self.phase_times[phase_number]["start"]
        duration = end_time - start_time

        print(f"""
════════════════════════════════════════════════════════════════
Phase {phase_number}/{self.total_phases}: {phase_name} ✓ COMPLETE ({duration:.1f}s)
════════════════════════════════════════════════════════════════
""")

# Usage example:
tracker = PhaseTracker(total_phases=3)

tracker.start_phase(1, "Discovery")
# ... do work ...
tracker.complete_phase(1, "Discovery")

tracker.start_phase(2, "Analysis")
# ... do work ...
tracker.complete_phase(2, "Analysis")

tracker.start_phase(3, "Reporting")
# ... do work ...
tracker.complete_phase(3, "Reporting")
```

---

## Pattern 4: Complete Accounting Formula

**Usage:** Every operation that modifies state MUST track complete accounting.

```python
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class AccountingState:
    """
    Track complete accounting for all operations.

    Formula: total = completed + skipped + failed + cannot_do
    """
    total_items: int = 0
    completed: List[str] = field(default_factory=list)
    skipped: List[Tuple[str, str]] = field(default_factory=list)  # (item, reason)
    failed: List[Tuple[str, str]] = field(default_factory=list)   # (item, error)
    cannot_do: List[Tuple[str, str]] = field(default_factory=list)  # (item, reason)

    def add_completed(self, item: str):
        """Mark item as completed."""
        self.completed.append(item)

    def add_skipped(self, item: str, reason: str):
        """Mark item as skipped with reason."""
        self.skipped.append((item, reason))

    def add_failed(self, item: str, error: str):
        """Mark item as failed with error."""
        self.failed.append((item, error))

    def add_cannot_do(self, item: str, reason: str):
        """Mark item as cannot-do with reason."""
        self.cannot_do.append((item, reason))

    def verify_accounting(self) -> bool:
        """
        Verify accounting formula.

        Returns: True if accounting is correct, False otherwise
        """
        accounted = (
            len(self.completed) +
            len(self.skipped) +
            len(self.failed) +
            len(self.cannot_do)
        )
        return accounted == self.total_items

    def get_report(self) -> str:
        """Generate accounting report."""
        return f"""
════════════════════════════════════════════════════════════════
                    ACCOUNTING VERIFICATION
════════════════════════════════════════════════════════════════

Total Items: {self.total_items}

Completed: {len(self.completed)}
Skipped: {len(self.skipped)}
Failed: {len(self.failed)}
Cannot Do: {len(self.cannot_do)}

Verification: {self.total_items} = {len(self.completed)} + {len(self.skipped)} + {len(self.failed)} + {len(self.cannot_do)} {"✓" if self.verify_accounting() else "❌"}

════════════════════════════════════════════════════════════════
"""

# Usage example:
state = AccountingState(total_items=10)

# Process items
for item in items:
    try:
        result = process_item(item)
        if result.success:
            state.add_completed(item)
        elif result.should_skip:
            state.add_skipped(item, result.skip_reason)
    except CannotDoError as e:
        state.add_cannot_do(item, str(e))
    except Exception as e:
        state.add_failed(item, str(e))

# Verify accounting
assert state.verify_accounting(), "Accounting mismatch!"

# Report
print(state.get_report())
```

---

## Pattern 5: Error Handling with User Choice

**Usage:** When operation fails, ask user how to proceed.

```python
def handle_operation_error(
    operation_name: str,
    error_type: str,
    error_message: str,
    retry_available: bool = True,
    skip_available: bool = True
) -> str:
    """
    Handle operation error with user choice.

    Returns: User's choice ("retry", "skip", "cancel", etc.)
    """
    options = []

    if retry_available:
        options.append({
            "label": "Retry",
            "description": f"Try {operation_name} again"
        })

    if skip_available:
        options.append({
            "label": "Skip",
            "description": f"Skip this {operation_name} and continue"
        })

    options.extend([
        {
            "label": "Manual Fix",
            "description": "Show manual fix instructions"
        },
        {
            "label": "Cancel",
            "description": "Stop entire operation"
        }
    ])

    response = AskUserQuestion({
        "questions": [{
            "question": f"{operation_name} failed: {error_type} - {error_message}. How to proceed?",
            "header": f"{operation_name} Error",
            "multiSelect": False,
            "options": options
        }]
    })

    return response["answers"]["question"]

# Usage example:
try:
    execute_operation()
except OperationError as e:
    choice = handle_operation_error(
        operation_name="Database Migration",
        error_type=type(e).__name__,
        error_message=str(e),
        retry_available=True,
        skip_available=False
    )

    if choice == "Retry":
        execute_operation()  # Retry
    elif choice == "Manual Fix":
        show_manual_instructions()
    elif choice == "Cancel":
        exit_gracefully()
```

---

## Pattern 6: Agent Task Execution with Verification

**Usage:** Launch agent task and ALWAYS verify output.

```python
def execute_agent_task(
    agent_type: str,
    model: str,
    description: str,
    prompt: str,
    verify_fn: callable
) -> dict:
    """
    Execute agent task with mandatory verification.

    Args:
        agent_type: Agent type (e.g., "fix-agent", "audit-agent")
        model: Model to use ("haiku", "sonnet", "opus")
        description: Short description for tracking
        prompt: Full agent prompt
        verify_fn: Function to verify agent output

    Returns:
        Verified agent result

    Raises:
        VerificationError: If verification fails
    """
    # Execute agent task
    result = Task({
        "subagent_type": agent_type,
        "model": model,
        "description": description,
        "prompt": prompt
    })

    # ALWAYS verify agent output
    if not verify_fn(result):
        raise VerificationError(
            f"Agent output verification failed for: {description}\n"
            f"Result: {result}"
        )

    return result

# Usage example:
def verify_fix_applied(result: dict) -> bool:
    """Verify that fix was actually applied."""
    # Read file to confirm change
    file_content = Read(result["file_path"])
    return result["expected_change"] in file_content

result = execute_agent_task(
    agent_type="fix-agent",
    model="sonnet",
    description="Fix SQL injection in auth.py",
    prompt="Fix SQL injection vulnerability in auth.py:145",
    verify_fn=verify_fix_applied
)
```

---

## Pattern 7: File Discovery with Exclusion (Stage 0)

**Usage:** ALWAYS apply exclusions BEFORE processing files.

```python
def discover_files_with_exclusions(
    root_dir: str,
    pattern: str = "**/*"
) -> Tuple[List[str], List[str], Dict[str, int]]:
    """
    Discover files with exclusions applied FIRST (Stage 0).

    Returns:
        (included_files, excluded_files, stats)
    """
    # Get all files matching pattern
    all_files = Glob(pattern, path=root_dir)

    included = []
    excluded = []
    excluded_reasons = {}

    for file in all_files:
        exclusion_reason = check_exclusion(file)
        if exclusion_reason:
            excluded.append(file)
            excluded_reasons[exclusion_reason] = excluded_reasons.get(exclusion_reason, 0) + 1
        else:
            included.append(file)

    stats = {
        "total_found": len(all_files),
        "included": len(included),
        "excluded": len(excluded),
        "inclusion_rate": len(included) / len(all_files) if all_files else 0,
        "excluded_reasons": excluded_reasons
    }

    return included, excluded, stats

def check_exclusion(file_path: str) -> str:
    """
    Check if file should be excluded.

    Returns: Exclusion reason or empty string if not excluded
    """
    path_parts = Path(file_path).parts

    # Check directory exclusions
    for excluded_dir in EXCLUDED_DIRS:
        if excluded_dir in path_parts:
            return f"excluded_dir:{excluded_dir}"

    # Check file pattern exclusions
    filename = Path(file_path).name
    for pattern in EXCLUDED_FILES:
        if fnmatch.fnmatch(filename, pattern):
            return f"excluded_pattern:{pattern}"

    return ""

# Usage example:
included, excluded, stats = discover_files_with_exclusions(
    root_dir="D:/GitHub/MyProject",
    pattern="**/*.py"
)

print(f"""
Files discovered: {stats['total_found']}
Files included: {stats['included']} ({stats['inclusion_rate']:.0%})
Files excluded: {stats['excluded']}
""")
```

---

## Pattern 8: Dynamic Results Generation

**Usage:** Generate results from ACTUAL data, never use hardcoded examples.

```python
def generate_results_report(
    category: str,
    operations: List[Operation],
    state: AccountingState
) -> str:
    """
    Generate results report from actual operations.

    NEVER use hardcoded examples - always use real data.
    """
    # Calculate real metrics
    total_time = sum(op.duration for op in operations)
    avg_time = total_time / len(operations) if operations else 0

    # Generate report from actual data
    report = f"""
════════════════════════════════════════════════════════════════
                {category.upper()} RESULTS
════════════════════════════════════════════════════════════════

Operations Completed: {len(state.completed)}/{state.total_items}

"""

    # List completed operations with REAL data
    if state.completed:
        report += "Completed Operations:\n"
        for item in state.completed:
            op = find_operation(operations, item)
            report += f"  ✓ {op.name}\n"
            report += f"    File: {op.file_path}:{op.line_number}\n"
            report += f"    Duration: {op.duration:.2f}s\n"
            report += f"    Improvement: {op.improvement}\n"

    # List skipped with REAL reasons
    if state.skipped:
        report += "\nSkipped Operations:\n"
        for item, reason in state.skipped:
            report += f"  ⊘ {item}\n"
            report += f"    Reason: {reason}\n"

    # List failed with REAL errors
    if state.failed:
        report += "\nFailed Operations:\n"
        for item, error in state.failed:
            report += f"  ✗ {item}\n"
            report += f"    Error: {error}\n"

    # Metrics from REAL data
    report += f"""
════════════════════════════════════════════════════════════════

Metrics:
  Total Time: {total_time:.2f}s
  Average Time: {avg_time:.2f}s
  Success Rate: {len(state.completed)/state.total_items*100:.0%}

{state.get_report()}
"""

    return report
```

---

## Pattern 9: Context Passing Between Commands

**Usage:** Pass context from one command to another to avoid duplicate work.

```markdown
## CRITICAL: Check for Context from Calling Command

**BEFORE running {action}, check conversation for "CONTEXT FOR /cco-{command}:"**

✓ **If found**: Use provided {data}, skip {duplicate-work}, proceed with {main-task}
✗ **If not found**: Run {prerequisite} first, then proceed

**Why**: Eliminates duplicate {work-type} - previous command already {action}.

See **C_COMMAND_CONTEXT_PASSING** principle.

---

## Context Check Implementation

\`\`\`python
def check_for_calling_context(command_name: str) -> Optional[dict]:
    """
    Check if calling command provided context.

    Returns: Context dict if found, None otherwise
    """
    # Search conversation history for context marker
    marker = f"CONTEXT FOR /cco-{command_name}:"

    # If found, extract and parse context
    # If not found, return None

    return context_data if found else None

# Usage:
context = check_for_calling_context("fix")

if context:
    # Use provided issue list
    issues = context["issues"]
    print(f"Using {len(issues)} issues from calling command")
else:
    # No context - run audit first
    print("No context found - running audit to discover issues")
    issues = run_audit()
\`\`\`
```

---

## References

- **Quality Standards:** `COMMAND_QUALITY_STANDARDS.md`
- **Agent Standards:** `AGENT_STANDARDS.md`
- **Principle Files:** `~/.claude/principles/*.md`

---

**Last Updated:** 2025-01-23
**Version:** 1.0.0
**Status:** Active - All commands MUST use these patterns

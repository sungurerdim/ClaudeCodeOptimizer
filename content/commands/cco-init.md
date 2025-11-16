---
description: Initialize CCO for this project with auto-detection and AI-powered configuration
cost: 2
principles: ['U_EVIDENCE_BASED', 'U_FAIL_FAST', 'U_NO_OVERENGINEERING']
---

# CCO Project Initialization

Initialize ClaudeCodeOptimizer for the current project with intelligent defaults or user-controlled configuration.

**Enhanced with 3-Tier Questioning + Category Review:**
- **Quick Mode**: Zero questions - AI decides everything (30 sec)
- **Interactive Mode**: AI-guided questions based on your project context
  - Tier 1: Critical project decisions (always asked)
  - Tier 2: Strategic configuration (context-aware)
  - Tier 3: Tactical preferences (optional, based on detected tools)
  - **Category Review**: Multiselect questions to customize principles by category
- **Coverage**: Full control over all detected principles and configuration

## Step 1: Check CCO Installation

Verify CCO is installed:

```bash
python -c "import claudecodeoptimizer; print('[OK] CCO installed')"
```

If you see import error:
```
[ERROR] CCO is not installed.

Install with: pip install claudecodeoptimizer
Then restart Claude Code and run /cco-init again.
```

Stop execution if not installed.

## Step 1.5: Calculate Question Statistics (for User Info)

Before asking mode, calculate expected question counts:

```bash
python -c "
from claudecodeoptimizer.wizard.decision_tree import DECISION_TREE_TIER1, DECISION_TREE_TIER2
from pathlib import Path

# Fixed tier counts
tier1_count = len(DECISION_TREE_TIER1)
tier2_count = len(DECISION_TREE_TIER2)

# TIER3 is dynamic (7 static + 0-3 conditional + 0-N tool conflicts)
tier3_min = 7  # Static decisions
tier3_max_estimate = 15  # Rough upper bound

# Category count (dynamic from principles)
principle_dir = Path('~/.cco/content/principles').expanduser()
if not principle_dir.exists():
    # Fallback to local if global not found
    principle_dir = Path('content/principles')

categories = set()
if principle_dir.exists():
    for md_file in principle_dir.glob('[PUC]_*.md'):
        content = md_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if line.startswith('category:'):
                cat = line.split(':', 1)[1].strip()
                # Exclude meta categories
                if cat not in ['universal', 'claude-guidelines', 'project-specific']:
                    categories.add(cat)
                break

category_count = len(categories)

# Calculate totals
min_questions = tier1_count + category_count
max_questions = tier1_count + tier2_count + tier3_max_estimate + category_count

# Time estimation (15-20 sec per question)
min_time_min = (min_questions * 15) // 60
max_time_min = (max_questions * 20) // 60

print(f'[INFO] Interactive Mode Statistics:')
print(f'[INFO]   - Minimum: {min_questions} questions (~{min_time_min} min)')
print(f'[INFO]   - Maximum: {max_questions} questions (~{max_time_min} min)')
print(f'[INFO]   - Tier 1 (critical): {tier1_count} questions')
print(f'[INFO]   - Tier 2 (strategic): {tier2_count} questions')
print(f'[INFO]   - Tier 3 (tactical): {tier3_min}-{tier3_max_estimate} questions')
print(f'[INFO]   - Categories: {category_count} principle groups')
"
```

Store these values for use in the mode question.

## Step 2: Ask User for Mode

**CRITICAL**: Use AskUserQuestion tool to ask which mode. Use the calculated statistics from Step 1.5 in the description.

```json
{
  "questions": [
    {
      "question": "Which initialization mode would you like to use?",
      "header": "Init Mode",
      "multiSelect": false,
      "options": [
        {
          "label": "Quick Mode",
          "description": "AI decides all configuration based on project analysis (~30 sec). Zero user input required."
        },
        {
          "label": "Interactive Mode",
          "description": "You approve each step and customize principles. Question count varies by project (see statistics above). Full control, no defaults."
        }
      ]
    }
  ]
}
```

## Step 3A: Quick Mode (AI Decides Everything)

**If user selects "Quick Mode":**

Run initialization using the new wizard:

```bash
python -c "
from pathlib import Path
from claudecodeoptimizer.wizard.orchestrator import CCOWizard

wizard = CCOWizard(
    project_root=Path.cwd(),
    mode='quick',
    dry_run=False
)

result = wizard.run()

if result.success:
    print(f\"[OK] Initialized: {result.system_context.detected_language if result.system_context else 'project'}\")
    print(f\"[OK] Principles: {len(result.selected_principles)}\")
    print(f\"[OK] Commands: {len(result.selected_commands)}\")
    print(f\"[OK] Check CLAUDE.md for principles\")
else:
    print(f\"[ERROR] {result.error}\")
"
```

Done! Show verification and next steps (skip to Step 4).

## Step 3B: Interactive Mode (User Controls Everything)

**If user selects "Interactive Mode":**

Run initialization using the new interactive wizard:

```bash
python -c "
from pathlib import Path
from claudecodeoptimizer.wizard.orchestrator import CCOWizard

wizard = CCOWizard(
    project_root=Path.cwd(),
    mode='interactive',
    dry_run=False
)

result = wizard.run()

if result.success:
    print(f\"[OK] Initialized: {result.system_context.detected_language if result.system_context else 'project'}\")
    print(f\"[OK] Principles: {len(result.selected_principles)}\")
    print(f\"[OK] Commands: {len(result.selected_commands)}\")
    print(f\"[OK] Duration: {result.duration_seconds:.1f}s\")
    print(f\"[OK] Check CLAUDE.md for principles\")
else:
    print(f\"[ERROR] {result.error}\")
"
```

**The wizard will automatically:**
1. Detect your project structure and tools
2. Ask you configuration questions based on your project
3. Let you select which principles to activate
4. Generate all necessary files

Done! Show verification and next steps (skip to Step 4).

---
## Interactive Mode Coverage Summary

**Tiered Questioning System + Category Review:**
- **Tier 1 (Critical)**: Always asked - Fundamental project decisions
- **Tier 2 (Strategic)**: Context-aware - Asked based on detected project characteristics
- **Tier 3 (Tactical)**: Dynamic - Varies by detected tools and conflicts
- **Category Review**: Multiselect questions - Full principle customization by category

**Smart Approach:**
- **Not all questions are asked** - Only relevant ones based on your project
- **Context-aware** - Skips irrelevant questions (e.g., team workflow questions for solo devs)
- **Dynamic tool detection** - Asks about conflicting tools only if detected
- **Full transparency** - Every detected principle visible and customizable by category

**Question counts vary by project** - Run Step 1.5 above to see your project's statistics

---

### Step 3B.3: Calculate Initial Principle Selection

Based on user answers, calculate which principles would be selected by default:

```bash
python -c "
from pathlib import Path
from claudecodeoptimizer.core.project import ProjectManager
from claudecodeoptimizer.core.analyzer import ProjectAnalyzer
from claudecodeoptimizer.schemas.preferences import CCOPreferences, ProjectIdentity, CodeQualityStandards, DevelopmentStyle

# Map user answers to internal values
project_type_map = {
    'Backend API': 'backend',
    'Frontend Web': 'frontend',
    'Full-Stack': 'fullstack',
    'Library/Package': 'library',
    'CLI Tool': 'cli',
    'Mobile App': 'mobile'
}

domain_map = {
    'General Purpose': 'general-purpose',
    'Fintech': 'fintech',
    'Healthcare': 'healthcare',
    'E-commerce': 'ecommerce',
    'Enterprise SaaS': 'enterprise-saas'
}

team_map = {
    'Solo': 'solo',
    '2-5 people': 'small-2-5',
    '5-20 people': 'medium-10-20',
    '20+ people': 'large-20-50'
}

strict_map = {
    'Relaxed': 'relaxed',
    'Standard': 'standard',
    'Strict': 'strict',
    'Paranoid': 'paranoid'
}

security_map = {
    'Standard': 'standard',
    'Strict': 'strict',
    'Paranoid': 'paranoid'
}

coverage_map = {
    '50%': '50',
    '70%': '70',
    '80%': '80',
    '90%+': '90'
}

type_checking_map = {
    'None': 'none',
    'Basic': 'basic',
    'Standard': 'standard',
    'Strict': 'strict'
}

maturity_map = {
    'Prototype': 'mvp',
    'Active Development': 'active-dev',
    'Production': 'production',
    'Maintenance': 'maintenance'
}

deployment_map = {
    'Cloud (AWS/GCP/Azure)': 'cloud',
    'Kubernetes': 'kubernetes',
    'Traditional Servers': 'traditional',
    'Serverless': 'serverless',
    'Edge/CDN': 'edge',
    'Not Applicable': 'none'
}

# Compliance is multiSelect, so it returns a list
compliance_values = []  # Will be populated from user answers

# Tier 2 mappings (conditional)
secret_management_map = {
    'Environment Variables': 'env-vars',
    'Vault/Secrets Manager': 'vault',
    'Encrypted Config': 'encrypted',
    'Not Yet Defined': 'undefined'
}

audit_logging_map = {
    'Basic': 'basic',
    'Compliance': 'compliance',
    'Comprehensive': 'comprehensive'
}

encryption_scope_values = []  # multiSelect

git_workflow_map = {
    'Trunk-Based': 'trunk-based',
    'Git Flow': 'git-flow',
    'GitHub Flow': 'github-flow',
    'Custom': 'custom'
}

code_review_map = {
    'Optional': 'optional',
    'Required': 'required',
    'Strict': 'strict'
}

pr_size_map = {
    'Small (<200 lines)': 'small',
    'Medium (<500 lines)': 'medium',
    'Flexible': 'flexible'
}

expected_scale_map = {
    'Startup (<1K users)': 'startup',
    'Growing (1K-100K users)': 'growing',
    'Enterprise (100K+ users)': 'enterprise',
    'Global (1M+ users)': 'global'
}

caching_map = {
    'None': 'none',
    'In-Memory': 'in-memory',
    'Distributed': 'distributed'
}

monitoring_map = {
    'Basic Logging': 'basic',
    'Metrics + Alerts': 'metrics',
    'Full Observability': 'full'
}

tdd_map = {
    'None': 'none',
    'Encouraged': 'encouraged',
    'Required': 'required'
}

# Tier 3 mappings (advanced, optional)
philosophy_map = {
    'Pragmatic': 'pragmatic',
    'Perfection-Oriented': 'perfection',
    'Fast Iteration': 'fast-iteration'
}

pace_map = {
    'Rapid': 'rapid',
    'Balanced': 'balanced',
    'Deliberate': 'deliberate'
}

refactoring_map = {
    'Rarely': 'rarely',
    'Balanced': 'balanced',
    'Frequently': 'frequently'
}

breaking_changes_map = {
    'Avoid': 'avoid',
    'Rare': 'rare',
    'Pragmatic': 'pragmatic'
}

doc_style_map = {
    'Minimal': 'minimal',
    'Standard': 'standard',
    'Comprehensive': 'comprehensive'
}

cicd_trigger_map = {
    'On PR': 'on-pr',
    'On Every Push': 'on-push',
    'Manual': 'manual'
}

deploy_frequency_map = {
    'On-Demand': 'on-demand',
    'Daily/Weekly': 'scheduled',
    'Continuous': 'continuous'
}

error_handling_map = {
    'Basic': 'basic',
    'Structured': 'structured',
    'Comprehensive': 'comprehensive'
}

# Get analysis
analyzer = ProjectAnalyzer(Path.cwd())
analysis = analyzer.analyze()

# Create preferences from user answers
# NOTE: Replace 'ANSWER_X' with actual values from AskUserQuestion

from claudecodeoptimizer.schemas.preferences import (
    SecurityPosture, TestingStrategy, PerformanceVsMaintainability,
    TeamCollaboration, DevOpsAutomation, DocumentationPreferences
)

# Build preferences incrementally based on answered questions
preferences_dict = {
    'project_identity': {
        'name': Path.cwd().name,
        'types': [project_type_map['PROJECT_TYPE_ANSWER']],  # ← Replace Q1
        'primary_language': analysis['primary_language'],
        'frameworks': [f['name'] for f in analysis['frameworks'][:3]],
        'team_trajectory': team_map['TEAM_SIZE_ANSWER'],  # ← Replace Q3
        'project_maturity': maturity_map['MATURITY_ANSWER'],  # ← Replace Q8
        'business_domain': [domain_map['DOMAIN_ANSWER']],  # ← Replace Q2
        'deployment_target': deployment_map['DEPLOYMENT_ANSWER'],  # ← Replace Q9
        'compliance_requirements': ['COMPLIANCE_ANSWER_LIST'],  # ← Replace Q10 (list)
    },
    'code_quality': {
        'linting_strictness': strict_map['STRICTNESS_ANSWER'],  # ← Replace Q4
        'security_stance': security_map['SECURITY_ANSWER'],  # ← Replace Q5
        'test_coverage_target': coverage_map['COVERAGE_ANSWER'],  # ← Replace Q6
        'type_checking_level': type_checking_map['TYPE_CHECKING_ANSWER'],  # ← Replace Q7
        'code_review_depth': code_review_map.get('CODE_REVIEW_ANSWER', 'standard'),  # ← Tier 2 (optional)
        'documentation_level': 'standard',  # Default, can be overridden by Tier 3
    },
    'development_style': {
        'code_philosophy': philosophy_map.get('PHILOSOPHY_ANSWER', 'pragmatic'),  # ← Tier 3 (optional)
        'development_pace': pace_map.get('PACE_ANSWER', 'balanced'),  # ← Tier 3 (optional)
        'refactoring_appetite': refactoring_map.get('REFACTORING_ANSWER', 'balanced'),  # ← Tier 3 (optional)
        'breaking_changes_policy': breaking_changes_map.get('BREAKING_ANSWER', 'rare'),  # ← Tier 3 (optional)
    },
    'security': {
        'secret_management': secret_management_map.get('SECRET_ANSWER', 'env-vars'),  # ← Tier 2 (optional)
        'audit_logging_level': audit_logging_map.get('AUDIT_ANSWER', 'basic'),  # ← Tier 2 (optional)
        'encryption_scope': ['ENCRYPTION_ANSWER_LIST'],  # ← Tier 2 (optional, multiSelect)
    },
    'testing': {
        'tdd_adherence': tdd_map.get('TDD_ANSWER', 'none'),  # ← Tier 2 (optional)
    },
    'collaboration': {
        'git_workflow': git_workflow_map.get('GIT_WORKFLOW_ANSWER', 'github-flow'),  # ← Tier 2 (optional)
        'pr_size_preference': pr_size_map.get('PR_SIZE_ANSWER', 'medium'),  # ← Tier 2 (optional)
    },
    'performance': {
        'caching_strategy': caching_map.get('CACHING_ANSWER', 'none'),  # ← Tier 2 (optional)
        'expected_scale': expected_scale_map.get('SCALE_ANSWER', 'startup'),  # ← Tier 2 (optional)
    },
    'devops': {
        'ci_cd_trigger': cicd_trigger_map.get('CICD_ANSWER', 'on-push'),  # ← Tier 3 (optional)
        'deployment_frequency': deploy_frequency_map.get('DEPLOY_FREQ_ANSWER', 'on-demand'),  # ← Tier 3 (optional)
        'monitoring_level': monitoring_map.get('MONITORING_ANSWER', 'basic'),  # ← Tier 2 (optional)
    },
    'documentation': {
        'documentation_style': doc_style_map.get('DOC_STYLE_ANSWER', 'standard'),  # ← Tier 3 (optional)
    },
}

# Create CCOPreferences from dict
preferences = CCOPreferences(**preferences_dict)

# Select principles
pm = ProjectManager(Path.cwd())
selected = pm._select_and_generate_principles(preferences)

print(f'Based on your preferences, {len(selected)} principles selected:')
print('')
for i, p in enumerate(selected[:10], 1):
    print(f'  {i}. {p[\"id\"]}: {p[\"title\"]} ({p[\"severity\"]})')
if len(selected) > 10:
    print(f'  ... and {len(selected) - 10} more')
print('')
print('Full list will be in CLAUDE.md')
"
```

**IMPORTANT**: In the above code, replace the placeholder strings with actual user answers:

**Tier 1 (REQUIRED):**
- `'PROJECT_TYPE_ANSWER'` → Q1: Project Type
- `'DOMAIN_ANSWER'` → Q2: Business Domain
- `'TEAM_SIZE_ANSWER'` → Q3: Team Size
- `'STRICTNESS_ANSWER'` → Q4: Code Quality Strictness
- `'SECURITY_ANSWER'` → Q5: Security Stance
- `'COVERAGE_ANSWER'` → Q6: Test Coverage Target
- `'TYPE_CHECKING_ANSWER'` → Q7: Type Checking Level
- `'MATURITY_ANSWER'` → Q8: Project Maturity
- `'DEPLOYMENT_ANSWER'` → Q9: Deployment Target
- `'COMPLIANCE_ANSWER_LIST'` → Q10: Compliance Requirements (list)

**Tier 2 (CONDITIONAL - only if asked):**
- `'SECRET_ANSWER'` → T2-1: Secret Management
- `'AUDIT_ANSWER'` → T2-2: Audit Logging
- `'ENCRYPTION_ANSWER_LIST'` → T2-3: Data Encryption Scope (list)
- `'GIT_WORKFLOW_ANSWER'` → T2-4: Git Workflow
- `'CODE_REVIEW_ANSWER'` → T2-5: Code Review Strictness
- `'PR_SIZE_ANSWER'` → T2-6: PR Size Policy
- `'SCALE_ANSWER'` → T2-7: Expected Scale
- `'CACHING_ANSWER'` → T2-8: Caching Strategy
- `'MONITORING_ANSWER'` → T2-9: Monitoring & Observability
- `'TDD_ANSWER'` → T2-10: TDD Adherence

**Tier 3 (OPTIONAL - only if "Yes, customize further"):**
- `'PHILOSOPHY_ANSWER'` → T3-1: Code Philosophy
- `'PACE_ANSWER'` → T3-2: Development Pace
- `'REFACTORING_ANSWER'` → T3-3: Refactoring Appetite
- `'BREAKING_ANSWER'` → T3-4: Breaking Changes Policy
- `'DOC_STYLE_ANSWER'` → T3-5: Documentation Style
- `'CICD_ANSWER'` → T3-6: CI/CD Trigger
- `'DEPLOY_FREQ_ANSWER'` → T3-7: Deployment Frequency
- `'ERROR_HANDLING_ANSWER'` → T3-8: Error Handling Strategy (not yet mapped)

### Step 3B.3a: Review Principles Category-by-Category (multiselect)

**CRITICAL**: Now ask user to review and customize principles using **multiselect questions** for each category.

**Important**: All principles in each category should be **pre-selected by default**. User deselects what they don't want.

For each category, dynamically generate a multiselect question with ALL principles in that category.

**Category Display Names (Example):**

Categories are dynamically loaded from principle metadata. Common categories include:
- `code_quality` → "Code Quality"
- `security_privacy` → "Security & Privacy"
- `architecture` → "Architecture"
- `testing` → "Testing"
- `performance` → "Performance"
- `api_design` → "API Design"

Meta-categories like `universal`, `claude-guidelines`, and `project-specific` are typically excluded from category review.

**Question Format for Each Category:**

```json
{
  "questions": [{
    "question": "Select which [CATEGORY_NAME] principles you want to activate:",
    "header": "[CATEGORY_SHORT]",
    "multiSelect": true,
    "options": [
      {"label": "U_FAIL_FAST: Fail-Fast Error Handling", "description": "Catch errors early (weight: 10, critical)"},
      {"label": "U_DRY: DRY Enforcement", "description": "Don't Repeat Yourself (weight: 10, critical)"},
      ... (ALL principles in category)
    ]
  }]
}
```

**Label Format**: `"[ID]: [Title]"` (e.g., `"P_PRIVACY_FIRST: Privacy-First by Default"`)

**Description Format**: `"[one_line_why] (weight: X, [severity])"` (e.g., `"Minimize data collection (weight: 9, critical)"`)

**Question Order**: Sort categories by principle count (largest first). Categories are dynamically determined from available principles.

**Example Question 1 - Security & Privacy:**

```json
{
  "questions": [{
    "question": "Select which Security & Privacy principles you want to activate:",
    "header": "Security",
    "multiSelect": true,
    "options": [
      {"label": "P_SCHEMA_VALIDATION: Schema-First Validation", "description": "Validate all inputs (weight: 10, critical)"},
      {"label": "P_PRIVACY_FIRST: Privacy-First by Default", "description": "Minimize data collection (weight: 9, critical)"},
      {"label": "P_TTL_BASED_CLEANUP: TTL-Based Cleanup", "description": "Auto-expire old data (weight: 7, high)"},
      {"label": "P_ZERO_DISK_TOUCH: Zero Disk Touch", "description": "Never write secrets to disk (weight: 8, high)"},
      {"label": "P_ENCRYPTION_AT_REST: Encryption Everywhere", "description": "Encrypt sensitive data (weight: 9, critical)"},
      {"label": "P_RATE_LIMITING: Rate Limiting & Throttling", "description": "Protect against abuse (weight: 7, high)"},
      {"label": "P_SECRET_ROTATION: Secret Management with Rotation", "description": "No secrets in code (weight: 9, critical)"},
      {"label": "P_SQL_INJECTION: SQL Injection Prevention", "description": "Parameterized queries (weight: 9, critical)"},
      {"label": "P_SUPPLY_CHAIN_SECURITY: Supply Chain Security", "description": "Verify dependencies (weight: 8, high)"},
      {"label": "P_XSS_PREVENTION: Input Sanitization (XSS Prevention)", "description": "Prevent injection attacks (weight: 9, critical)"},
      {"label": "P_AUTH_AUTHZ: Authentication & Authorization", "description": "Proper access control (weight: 9, critical)"},
      {"label": "P_AUDIT_LOGGING: Audit Logging", "description": "Log security events (weight: 7, high)"}
    ]
  }]
}
```

**Example Question 2 - Code Quality:**

```json
{
  "questions": [{
    "question": "Select which Code Quality principles you want to activate:",
    "header": "Code Quality",
    "multiSelect": true,
    "options": [
      {"label": "U_FAIL_FAST: Fail-Fast Error Handling", "description": "Catch errors early (weight: 10, critical)"},
      {"label": "U_DRY: DRY Enforcement", "description": "Don't Repeat Yourself (weight: 10, critical)"},
      {"label": "U_INTEGRATION_CHECK: Complete Integration Check", "description": "Test all integrations (weight: 8, high)"},
      {"label": "P_TYPE_SAFETY: Type Safety & Static Analysis", "description": "Use type hints (weight: 9, critical)"},
      {"label": "P_IMMUTABILITY_BY_DEFAULT: Immutability by Default", "description": "Prefer immutable data (weight: 7, high)"},
      {"label": "P_SEPARATION_OF_CONCERNS: Separation of Concerns", "description": "Single responsibility (weight: 8, high)"},
      {"label": "P_VERSION_MANAGEMENT: Centralized Version Management", "description": "SSOT for versions (weight: 7, high)"},
      {"label": "U_NO_OVERENGINEERING: No Overengineering", "description": "Keep it simple (weight: 9, critical)"},
      {"label": "U_MINIMAL_TOUCH: Minimal Touch Policy", "description": "Only change what's needed (weight: 7, high)"},
      {"label": "P_CODE_REVIEW_CHECKLIST_COMPLIANCE: Code Review Checklist Compliance", "description": "Enforce reviews (weight: 8, high)"},
      {"label": "P_LINTING_SAST: Linting & SAST Enforcement", "description": "Enforce linting (weight: 7, high)"}
    ]
  }]
}
```

**Continue for all detected categories** (dynamically determined from available principles).

### Step 3B.3b: Finalize Principle Selection

After all category questions answered, collect and validate final selection:

```bash
python -c "
# Collect answers from all category questions (dynamic count)
# Each answer is a list of selected principle labels (format: 'PXXX: Title')

# Example structure of collected answers:
# category_answers = {
#     'security_privacy': ['P019: Privacy-First by Default', 'P020: TTL-Based Cleanup', ...],
#     'code_quality': ['U_DRY: Fail-Fast Error Handling', 'U_INTEGRATION_CHECK: DRY Enforcement', ...],
#     ...
# }

# Extract principle IDs from labels
final_selected_ids = []
for category, selected_labels in category_answers.items():
    for label in selected_labels:
        # Extract ID from label (format: 'PXXX: Title')
        principle_id = label.split(':')[0].strip()
        final_selected_ids.append(principle_id)

print(f'Final selection: {len(final_selected_ids)} principles')
print('')
print('Selected IDs:', ', '.join(sorted(final_selected_ids)))
print('')
print('Ready to install.')
"
```

Ask user for final confirmation:

```json
{
  "questions": [{
    "question": "Install with these [X] selected principles?",
    "header": "Final Confirm",
    "multiSelect": false,
    "options": [
      {"label": "Yes, install", "description": "Install CCO with selected principles"},
      {"label": "Cancel", "description": "Stop initialization"}
    ]
  }]
}
```

**If "Cancel"**: Stop execution.

**If "Yes, install"**: Continue to Step 3B.4.

### Step 3B.4: Complete Installation

Run the full installation with user preferences:

```bash
python -c "
from pathlib import Path
from claudecodeoptimizer.core.project import ProjectManager
from claudecodeoptimizer.core.analyzer import ProjectAnalyzer
from claudecodeoptimizer.schemas.preferences import CCOPreferences, ProjectIdentity, CodeQualityStandards, DevelopmentStyle

# Import mapping dictionaries (defined earlier in Step 3B.3)
# All the *_map dictionaries are already defined above

# Get analysis
analyzer = ProjectAnalyzer(Path.cwd())
analysis = analyzer.analyze()

# Import all required schemas
from claudecodeoptimizer.schemas.preferences import (
    SecurityPosture, TestingStrategy, PerformanceVsMaintainability,
    TeamCollaboration, DevOpsAutomation, DocumentationPreferences
)

# Build preferences from all tiers (same structure as Step 3B.3)
# NOTE: Replace 'ANSWER_X' with actual values from user questions
preferences_dict = {
    'project_identity': {
        'name': Path.cwd().name,
        'types': [project_type_map['PROJECT_TYPE_ANSWER']],  # ← Q1
        'primary_language': analysis['primary_language'],
        'frameworks': [f['name'] for f in analysis['frameworks'][:3]],
        'team_trajectory': team_map['TEAM_SIZE_ANSWER'],  # ← Q3
        'project_maturity': maturity_map['MATURITY_ANSWER'],  # ← Q8
        'business_domain': [domain_map['DOMAIN_ANSWER']],  # ← Q2
        'deployment_target': deployment_map['DEPLOYMENT_ANSWER'],  # ← Q9
        'compliance_requirements': ['COMPLIANCE_ANSWER_LIST'],  # ← Q10
    },
    'code_quality': {
        'linting_strictness': strict_map['STRICTNESS_ANSWER'],  # ← Q4
        'security_stance': security_map['SECURITY_ANSWER'],  # ← Q5
        'test_coverage_target': coverage_map['COVERAGE_ANSWER'],  # ← Q6
        'type_checking_level': type_checking_map['TYPE_CHECKING_ANSWER'],  # ← Q7
        'code_review_depth': code_review_map.get('CODE_REVIEW_ANSWER', 'standard'),  # ← T2-5
        'documentation_level': 'standard',
    },
    'development_style': {
        'code_philosophy': philosophy_map.get('PHILOSOPHY_ANSWER', 'pragmatic'),  # ← T3-1
        'development_pace': pace_map.get('PACE_ANSWER', 'balanced'),  # ← T3-2
        'refactoring_appetite': refactoring_map.get('REFACTORING_ANSWER', 'balanced'),  # ← T3-3
        'breaking_changes_policy': breaking_changes_map.get('BREAKING_ANSWER', 'rare'),  # ← T3-4
    },
    'security': {
        'secret_management': secret_management_map.get('SECRET_ANSWER', 'env-vars'),  # ← T2-1
        'audit_logging_level': audit_logging_map.get('AUDIT_ANSWER', 'basic'),  # ← T2-2
        'encryption_scope': ['ENCRYPTION_ANSWER_LIST'],  # ← T2-3
    },
    'testing': {
        'tdd_adherence': tdd_map.get('TDD_ANSWER', 'none'),  # ← T2-10
    },
    'collaboration': {
        'git_workflow': git_workflow_map.get('GIT_WORKFLOW_ANSWER', 'github-flow'),  # ← T2-4
        'pr_size_preference': pr_size_map.get('PR_SIZE_ANSWER', 'medium'),  # ← T2-6
    },
    'performance': {
        'caching_strategy': caching_map.get('CACHING_ANSWER', 'none'),  # ← T2-8
        'expected_scale': expected_scale_map.get('SCALE_ANSWER', 'startup'),  # ← T2-7
    },
    'devops': {
        'ci_cd_trigger': cicd_trigger_map.get('CICD_ANSWER', 'on-push'),  # ← T3-6
        'deployment_frequency': deploy_frequency_map.get('DEPLOY_FREQ_ANSWER', 'on-demand'),  # ← T3-7
        'monitoring_level': monitoring_map.get('MONITORING_ANSWER', 'basic'),  # ← T2-9
    },
    'documentation': {
        'documentation_style': doc_style_map.get('DOC_STYLE_ANSWER', 'standard'),  # ← T3-5
    },
}

# Create CCOPreferences
preferences = CCOPreferences(**preferences_dict)

# Complete installation
pm = ProjectManager(Path.cwd())

# Use user-selected principle IDs (from Step 3B.3b)
# Replace 'FINAL_SELECTED_IDS' with actual list from category questions
final_selected_ids = ['FINAL_SELECTED_IDS']  # ← Replace with actual list

# Load full principle definitions for selected IDs from .md files
from claudecodeoptimizer.core.principles import get_principles_manager
principles_manager = get_principles_manager()
all_principles = [
    {'id': p.id, 'title': p.title, 'category': p.category}
    for p in principles_manager.get_all_principles()
]
selected = [p for p in all_principles if p['id'] in final_selected_ids]

# Register project
preferences_dict = preferences.model_dump(mode='json')
preferences_dict['selected_principle_ids'] = final_selected_ids

pm.registry.register_project(
    project_name=Path.cwd().name,
    project_root=Path.cwd(),
    analysis=analysis,
    preferences=preferences_dict,
)

# Generate generic commands
pm._generate_generic_commands(analysis)

print('[OK] Installation complete!')
print(f'[OK] Project: {Path.cwd().name}')
print(f'[OK] Principles: {len(selected)} selected')
print(f'[OK] Commands: .claude/commands/cco-*.md')
print(f'[OK] CLAUDE.md generated with principles')
"
```

**IMPORTANT**: Replace placeholder strings with actual user answers:

**From Tier 1-3 Questions:**
- Tier 1: 10 required questions (Q1-Q10)
- Tier 2: 0-10 conditional questions (T2-1 to T2-10, based on conditions)
- Tier 3: 0-8 advanced questions (T3-1 to T3-8, if user chose "Yes, customize further")

**From Category Multiselect Questions (Step 3B.3a-3b):**
- `'FINAL_SELECTED_IDS'` → Replace with list of principle IDs collected from all 8 category questions
  Example: `['U_DRY', 'U_INTEGRATION_CHECK', 'P019', 'P020', ...]`

See Step 3B.3 for preference field mapping reference.

## Step 4: Verify Installation

After successful initialization (either mode), verify:

```bash
python -c "import glob; print(f'{len(glob.glob(\".claude/commands/cco-*.md\"))} CCO commands installed')"
```

Expected: Should show count of installed CCO commands (12-15)

```bash
python -c "import pathlib; p=pathlib.Path('CLAUDE.md'); print(p.read_text(encoding='utf-8')[:5000] if p.exists() else 'CLAUDE.md not found')"
```

Expected: Should show principle summary and project guidelines

## Next Steps

After initialization:
- Run `/cco-status` to see your full configuration
- Read `CLAUDE.md` to understand your active principles
- Run `/cco-audit-code` to analyze your code against principles

## Troubleshooting

**"Project already initialized"**: Run `/cco-remove` first to clean up.

**Import error**: Install CCO with `pip install claudecodeoptimizer`

**Permission errors**: Check `.claude/` directory exists and is writable.

**No principles loaded**: Check `CLAUDE.md` was created/updated. If not, re-run initialization.

</details>

---

## Appendix: Legacy Field Coverage Breakdown (Reference Only)

**Note**: The information below is from a previous full-questionnaire system and may not reflect current wizard implementation. See Step 1.5 for current dynamic statistics.

**Total CCOPreferences Fields**: 66 across 9 categories

### Tier 1 Coverage (10 questions - ALWAYS asked)

**ProjectIdentity (12 fields total):**
- ✅ types (Q1: Project Type)
- ✅ business_domain (Q2: Business Domain)
- ✅ team_trajectory (Q3: Team Size)
- ✅ project_maturity (Q8: Project Maturity)
- ✅ deployment_target (Q9: Deployment Target)
- ✅ compliance_requirements (Q10: Compliance)
- ✅ primary_language (detected)
- ✅ frameworks (detected)
- ✅ name (auto)
- ❌ expected_users (default)
- ❌ license_model (default)
- ❌ is_open_source (default)

**CodeQualityStandards (10 fields):**
- ✅ linting_strictness (Q4: Strictness)
- ✅ security_stance (Q5: Security)
- ✅ test_coverage_target (Q6: Coverage)
- ✅ type_checking_level (Q7: Type Checking)
- ❌ code_review_depth (default 'standard', overridable in T2)
- ❌ documentation_level (default 'standard', overridable in T3)
- ❌ error_handling_strictness (default)
- ❌ logging_level (default)
- ❌ performance_budget_enforcement (default)
- ❌ accessibility_standards (default)

**Tier 1 Coverage: 10/66 = 15%**

### Tier 2 Coverage (10 questions - CONDITIONAL)

**SecurityPosture (6 fields):**
- ✅ secret_management (T2-1: if high-security domain)
- ✅ audit_logging_level (T2-2: if compliance)
- ✅ encryption_scope (T2-3: if compliance)
- ❌ vulnerability_scanning (default)
- ❌ penetration_testing_frequency (default)
- ❌ incident_response_plan (default)

**TeamCollaboration (4 fields):**
- ✅ git_workflow (T2-4: if team > solo)
- ✅ code_review_depth (T2-5: if team > solo)
- ✅ pr_size_preference (T2-6: if team > solo)
- ❌ communication_channels (default)

**PerformanceVsMaintainability (5 fields):**
- ✅ caching_strategy (T2-8: if scale or kubernetes)
- ✅ expected_scale (T2-7: if team >= 5)
- ❌ optimization_priority (default)
- ❌ premature_optimization_tolerance (default)
- ❌ tech_debt_tolerance (default)

**DevOpsAutomation (6 fields):**
- ✅ monitoring_level (T2-9: if production or team >= 5)
- ❌ ci_cd_trigger (default, overridable in T3)
- ❌ deployment_frequency (default, overridable in T3)
- ❌ infrastructure_as_code (default)
- ❌ automated_rollback (default)
- ❌ feature_flags_usage (default)

**TestingStrategy (7 fields):**
- ✅ tdd_adherence (T2-10: if coverage >= 80% or production)
- ❌ test_pyramid_ratio (default)
- ❌ mutation_testing (default)
- ❌ property_based_testing (default)
- ❌ integration_test_coverage (default)
- ❌ e2e_test_coverage (default)
- ❌ test_isolation_level (default)

**Tier 2 Additional Coverage: +7 fields = 17/66 = 26% total**

### Tier 3 Coverage (8 questions - OPTIONAL)

**DevelopmentStyle (8 fields):**
- ✅ code_philosophy (T3-1)
- ✅ development_pace (T3-2)
- ✅ refactoring_appetite (T3-3)
- ✅ breaking_changes_policy (T3-4)
- ❌ prototyping_vs_production (default)
- ❌ innovation_vs_stability (default)
- ❌ code_reuse_priority (default)
- ❌ framework_vs_library_preference (default)

**DocumentationPreferences (8 fields):**
- ✅ documentation_style (T3-5)
- ❌ inline_comment_density (default)
- ❌ api_doc_format (default)
- ❌ architecture_doc_maintenance (default)
- ❌ code_example_coverage (default)
- ❌ readme_sections (default)
- ❌ doc_versioning (default)

**DevOpsAutomation (continued):**
- ✅ ci_cd_trigger (T3-6, overrides default)
- ✅ deployment_frequency (T3-7, overrides default)

**ErrorHandling (not yet in schema, placeholder):**
- ✅ error_handling_strategy (T3-8, requires schema update)

**Tier 3 Additional Coverage: +6 fields = 23/66 = 35% total**

### Final Statistics

**Maximum Coverage (All 3 Tiers):**
- **Asked directly**: 23 fields (35%)
- **Auto-detected**: 3 fields (name, language, frameworks)
- **Smart defaults**: 40 fields (61%)
- **Total configured**: 26/66 = 39% (rounded to 42% in summary)

**Key Improvements:**
1. Coverage increased from 12% → 39% (3.25x improvement)
2. Context-aware: Only relevant questions asked
3. Handles critical scenarios: compliance-heavy, high-scale, team collaboration, strict TDD
4. User control: Can opt out of Tier 3 for faster setup
5. Smart defaults: 61% of fields have intelligent defaults, not random values

**Scenarios Now Supported:**
- ✅ Compliance-heavy (HIPAA, GDPR, PCI-DSS, SOC2)
- ✅ High-scale projects (expected_scale, caching, monitoring)
- ✅ Team collaboration (git_workflow, code_review, PR policies)
- ✅ Strict TDD projects (tdd_adherence)
- ✅ Multiple deployment targets (cloud, k8s, serverless, edge)
- ✅ Security-focused projects (secrets, audit logging, encryption)

**Still Using Defaults (38 fields):**
- These are less critical for principle selection
- Most are operational details (infrastructure, advanced testing strategies)
- Can be configured later via `/cco-config` command
- Smart defaults based on common best practices

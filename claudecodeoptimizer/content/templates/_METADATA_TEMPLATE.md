# Universal CCO File Metadata Template

All CCO files (guides, skills, agents, commands) should use this standard frontmatter structure.

## Standard Frontmatter Structure

```yaml
---
# REQUIRED FIELDS
title: "Human-readable title"
category: "main-category"  # e.g., quality, testing, security, performance, infrastructure
description: "Short one-line description (max 100 chars)"

# RECOMMENDATION MATCHING
use_cases:
  # Match against AnswerContext keys - add any relevant criteria
  development_philosophy: [quality_first, balanced, move_fast]  # optional
  project_maturity: [prototype, mvp, active-dev, production, legacy]  # optional
  team_dynamics: [solo, small-2-5, medium-10-20, large-20-50]  # optional
  project_purpose: [backend, frontend, web-app, microservice, cli, library, data-pipeline, ml, analytics]  # optional
  testing_approach: [none, minimal, balanced, comprehensive]  # optional
  security_stance: [standard, production, high]  # optional
  git_workflow: [main_only, github_flow, git_flow, gitlab_flow]  # optional
  error_handling: [fail_fast, retry_logic, graceful_degradation]  # optional

# OPTIONAL METADATA (for skills/agents/commands)
metadata:
  name: "Display name"
  activation_keywords: ["keyword1", "keyword2"]
  category: "subcategory"
  priority: high  # high, medium, low

# TAGS (optional)
tags: [tag1, tag2, tag3]

# AUTHOR (optional)
author: "Author Name"
---
```

## Field Explanations

### Required Fields

**title**: Human-readable display name
- Example: `"Verification Protocol"`
- Used in UI, documentation

**category**: Primary categorization
- Values: `quality`, `testing`, `security`, `performance`, `infrastructure`, `analysis`, `planning`
- Used for filtering, grouping

**description**: Short description (max 100 chars)
- Displayed in selection UI
- Should clearly convey purpose

### Optional Metadata

**metadata.activation_keywords**: Keywords that trigger this file (for skills)
**metadata.priority**: Recommendation priority (high/medium/low)


**tags**: Free-form tags for search/filtering

## Examples by File Type

### Guide Example
```yaml
---
title: Git Workflow Guide
category: version-control
description: Git commit, branching, and PR guidelines for teams
use_cases:
  team_dynamics: [small-2-5, medium-10-20, large-20-50]
  git_workflow: [git_flow, github_flow, gitlab_flow]
tags: [git, team, collaboration, branching]
---
```

### Skill Example
```yaml
---
title: Verification Protocol Skill
category: quality
description: Evidence-based fix-verify-commit loop for violations
metadata:
  name: "Verification Protocol"
  activation_keywords: ["verify", "verification", "violations"]
  category: "enforcement"
use_cases:
  development_philosophy: [quality_first, balanced]
  project_maturity: [active-dev, production, legacy]
  testing_approach: [comprehensive, balanced]
---
```

### Agent Example
```yaml
---
title: Audit Agent
category: analysis
description: Comprehensive codebase audit and violation detection
metadata:
  name: "Audit Agent"
  priority: high
use_cases:
  project_maturity: [active-dev, production, legacy]
  development_philosophy: [quality_first, balanced]
---
```

### Command Example
```yaml
---
title: Project Status Check
category: bootstrap
description: Quick health check - git status, dependencies, tests, documentation
metadata:
  command_id: cco-status
  priority: high
  category: status
author: Claude Code
use_cases:
  project_maturity: [active-dev, production, legacy]
---
```

## Best Practices

1. **Keep descriptions concise** (max 100 chars)
2. **Use specific use_cases** - only include criteria that truly apply
3. **Avoid overmatching** - don't make every file match every context
4. **Update use_cases** when file purpose changes
5. **Use consistent category values** across files
6. **Follow AnswerContext key naming** exactly (e.g., `project_maturity` not `maturity`)


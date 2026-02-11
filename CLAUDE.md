<!-- cco-blueprint-start -->
## CCO Blueprint Profile

**Project:** ClaudeCodeOptimizer | **Type:** Developer Tool | **Stack:** Markdown + Go + Shell | **Target:** Production

### Config
- **Priorities:** Security, Code Quality, Architecture, Documentation
- **Constraints:** No restrictions
- **Data:** No sensitive data | **Regulations:** N/A
- **Audience:** Public users | **Deploy:** GitHub releases (install scripts)

### Project Map
```
Entry: install.sh / install.ps1 → GitHub raw download → ~/.claude/
Modules:
  rules/        → Core rules (1 file, auto-loaded)
  commands/     → Slash commands (8 files)
  agents/       → Subagents (3 files)
  extras/       → Optional add-ons (statusline: Go)
  docs/         → Documentation (5 files)
  .github/      → CI/CD (2 workflows)
External: GitHub API (tags), release-please, gitleaks
Toolchain: gofmt + go vet | GitHub Actions CI | No container
```

### Ideal Metrics
| Metric | Target |
|--------|--------|
| Coupling | <30% |
| Cohesion | >80% |
| Complexity | <8 |
| Coverage | 85%+ |

### Current Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| Security | 90 | OK |
| Code Quality | 86 | OK |
| Architecture | 76 | WARN |
| Stack Health | 86 | OK |
| DX | 78 | WARN |
| Documentation | 81 | WARN |
| Overall | 84 | WARN |

### Run History
- 2026-02-08: Applied 3 | Failed 0 | Overall 82→83
- 2026-02-09: Applied 3 | Failed 0 | Overall 83→84

### Decisions
<!-- cco-blueprint-end -->

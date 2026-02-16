<!-- cco-blueprint-start -->
## CCO Blueprint Profile

**Project:** ClaudeCodeOptimizer | **Type:** Developer Tool | **Stack:** Markdown + Go | **Target:** Production

### Config
- **Priorities:** Security, Code Quality, Architecture, Documentation
- **Constraints:** No restrictions
- **Data:** No sensitive data | **Regulations:** N/A
- **Audience:** Public users | **Deploy:** GitHub releases (Go binary installer)

### Project Map
```
Entry: extras/installer/ (Go binary) → GitHub release download → ~/.claude/
Modules:
  rules/        → Core rules (1 file, auto-loaded)
  skills/       → Slash skills (8 directories, each with SKILL.md)
  agents/       → Subagents (3 files)
  extras/       → Optional add-ons (statusline: Go, installer: Go)
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
| Security & Privacy | 90 | OK |
| Code Quality | 86 | OK |
| Architecture | 76 | WARN |
| Performance | 88 | OK |
| Resilience | 82 | OK |
| Testing | 70 | WARN |
| Stack Health | 86 | OK |
| DX | 78 | WARN |
| Documentation | 81 | WARN |
| Overall | 82 | WARN |
<!-- cco-blueprint-end -->

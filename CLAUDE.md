<!-- cco-blueprint-start -->
## CCO Blueprint Profile

**Project:** ClaudeCodeOptimizer | **Type:** Developer Tool | **Stack:** Markdown + Go | **Target:** Production

### Config
- **Priorities:** Security, Code Quality, Architecture, Documentation
- **Constraints:** No restrictions
- **Data:** No sensitive data | **Regulations:** N/A
- **Audience:** Public users | **Deploy:** GitHub releases (Go binary installer)
- **Repo:** Public | **Team:** Solo | **Distribution:** Open source

### Project Map
```
Entry: extras/installer/ (Go binary) → GitHub release download → ~/.claude/
Modules:
  rules/           → Core rules (1 file, auto-loaded)
  skills/          → Slash skills (8 directories, each with SKILL.md)
  agents/          → Subagents (3 files)
  extras/          → Optional add-ons (statusline: Go, installer: Go)
  docs/            → Documentation (5 files)
  .github/         → CI/CD (2 workflows) + Dependabot
  .claude/commands → Custom commands (1 file)
External: GitHub API (tags), release-please, gitleaks, Dependabot
Toolchain: gofmt + go vet + golangci-lint | GoReleaser | GitHub Actions CI | No container
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
| Security & Privacy | 92 | OK |
| Code Quality | 88 | OK |
| Architecture | 80 | WARN |
| Performance | 89 | OK |
| Resilience | 83 | OK |
| Testing | 80 | WARN |
| Stack Health | 85 | OK |
| DX | 79 | WARN |
| Documentation | 72 | ALERT |
| Overall | 84 | OK |
<!-- cco-blueprint-end -->

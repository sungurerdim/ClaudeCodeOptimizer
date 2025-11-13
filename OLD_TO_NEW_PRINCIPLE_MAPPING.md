# Old → New Principle ID Mapping

## Context
When universal principles (U001-U012) were added in commit f99df1d, all P-numbered principles were renumbered.

## Critical Mappings for Common References

### Universal Principles (extracted from old P-series)
- **OLD P001** (Fail-Fast Error Handling) → **NEW U002**
- **OLD P067** (Evidence-Based Verification) → **NEW U001**
- **OLD P071** (No Overengineering) → **NEW U011**
- **OLD P072** (Concise Commit Messages) → **NEW U010**
- **OLD P073** (Atomic Commits) → **NEW U009**
- **OLD P074** (Automated Semantic Versioning) → **NEW P052**

### Complete Old → New Mapping

```
OLD P001: Fail-Fast Error Handling → NEW U002
OLD P002: DRY Enforcement → NEW P001
OLD P003: Complete Integration Check → NEW P002
OLD P004: No Backward Compatibility Debt → NEW P003
OLD P005: Schema-First Validation → NEW P022
OLD P006: Precision in Calculations → NEW P004
OLD P007: Immutability by Default → NEW P005
OLD P008: Code Review Checklist Compliance → NEW P006
OLD P009: Linting & SAST Enforcement → NEW P007
OLD P010: Performance Profiling Before Optimization → NEW P008
OLD P011: Event-Driven Architecture → NEW P012
OLD P012: Singleton Pattern for Expensive Resources → NEW P013
OLD P013: Separation of Concerns → NEW P014
OLD P014: Microservices with Service Mesh → NEW P015
OLD P015: CQRS Pattern → NEW P016
OLD P016: Dependency Injection → NEW P017
OLD P017: Circuit Breaker Pattern → NEW P018
OLD P018: API Versioning Strategy → NEW P019
OLD P019: Privacy-First by Default → NEW P023
OLD P020: TTL-Based Cleanup → NEW P024
OLD P021: Encryption Everywhere → NEW P025
OLD P022: Zero Disk Touch → NEW P026
OLD P023: Type Safety & Static Analysis → NEW P009
OLD P024: Authentication & Authorization → NEW P027
OLD P025: SQL Injection Prevention → NEW P028
OLD P026: Secret Management with Rotation → NEW P029
OLD P027: Rate Limiting & Throttling → NEW P030
OLD P028: CORS Policy → NEW P031
OLD P029: Input Sanitization (XSS Prevention) → NEW P032
OLD P030: Audit Logging → NEW P033
OLD P031: Minimal Responsibility → NEW P058
OLD P032: Configuration as Code → NEW P059
OLD P033: Infrastructure as Code + GitOps → NEW P060
OLD P034: Observability with OpenTelemetry → NEW P061
OLD P035: Health Checks & Readiness Probes → NEW P062
OLD P036: Graceful Shutdown → NEW P063
OLD P037: Test Coverage Targets → NEW P041
OLD P038: Test Isolation → NEW P042
OLD P039: Integration Tests for Critical Paths → NEW P043
OLD P040: Test Pyramid → NEW P044
OLD P041: CI Gates → NEW P045
OLD P042: Property-Based Testing → NEW P046
OLD P043: Commit Message Conventions → NEW P047
OLD P044: Branching Strategy → NEW P048
OLD P045: PR Guidelines → NEW P049
OLD P046: Rebase vs Merge Strategy → NEW P050
OLD P047: Semantic Versioning → NEW P051
OLD P048: Caching Strategy → NEW P053
OLD P049: Database Query Optimization → NEW P054
OLD P050: Lazy Loading & Pagination → NEW P055
OLD P051: Async I/O → NEW P056
OLD P052: RESTful API Conventions → NEW P068
OLD P053: Centralized Version Management → NEW P010
OLD P054: Supply Chain Security → NEW P034
OLD P055: AI/ML Security → NEW P035
OLD P056: Container Security → NEW P036
OLD P057: Kubernetes Security → NEW P037
OLD P058: Zero Trust Architecture → NEW P038
OLD P059: GitOps Practices → NEW P064
OLD P060: Incident Response Readiness → NEW P065
OLD P061: Privacy Compliance → NEW P039
OLD P062: API Security Best Practices → NEW P069
OLD P063: Dependency Management → NEW P040
OLD P064: Continuous Profiling → NEW P057
OLD P065: Compliance as Code → NEW P066
OLD P066: Agent Orchestration Patterns → NEW P020
OLD P067: Evidence-Based Verification → NEW U001
OLD P068: Grep-First Search Strategy → NEW P011
OLD P069: Incremental Safety Patterns → NEW P067
OLD P070: Context Window Management → NEW P021
OLD P071: No Overengineering → NEW U011
OLD P072: Concise Commit Messages → NEW U010
OLD P073: Atomic Commits → NEW U009
OLD P074: Automated Semantic Versioning → NEW P052
```

## Files That Need Updating

All references to OLD principle IDs need to be updated based on CONTENT CONTEXT:
- Check what the OLD ID referred to conceptually
- Map to correct NEW ID based on content/title match
- Verify context makes sense

### Known Locations:
1. `claudecodeoptimizer/core/claude_md_generator.py`
2. `claudecodeoptimizer/core/principle_selector.py`
3. `claudecodeoptimizer/wizard/orchestrator.py`
4. `content/commands/*.md`
5. `content/agents/*.md`
6. `content/skills/*.md`
7. `content/guides/*.md`

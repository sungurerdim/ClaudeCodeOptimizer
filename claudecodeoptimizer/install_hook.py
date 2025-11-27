"""CCO Setup - Install commands, agents, and standards to ~/.claude/"""

import re
import shutil
import sys
from pathlib import Path

from .config import AGENTS_DIR, CLAUDE_DIR, COMMANDS_DIR


def get_content_dir() -> Path:
    """Get package content directory."""
    return Path(__file__).parent / "content"


def _setup_content(src_subdir: str, dest_dir: Path, verbose: bool = True) -> list[str]:
    """Copy cco-*.md files from source to destination directory."""
    src = get_content_dir() / src_subdir
    if not src.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    for old in dest_dir.glob("cco-*.md"):
        old.unlink()
    installed = []
    for f in sorted(src.glob("cco-*.md")):
        shutil.copy2(f, dest_dir / f.name)
        installed.append(f.name)
        if verbose:
            print(f"  + {f.name}")
    return installed


def setup_commands(verbose: bool = True) -> list[str]:
    """Copy cco-*.md commands to ~/.claude/commands/"""
    return _setup_content("commands", COMMANDS_DIR, verbose)


def setup_agents(verbose: bool = True) -> list[str]:
    """Copy cco-*.md agents to ~/.claude/agents/"""
    return _setup_content("agents", AGENTS_DIR, verbose)


def setup_claude_md(verbose: bool = True) -> None:
    """Add CCO Principles to ~/.claude/CLAUDE.md"""
    standards = """<!-- CCO_STANDARDS_START -->
## Core
- Paths: forward slash (/), relative, quote spaces
- Reference Integrity: find ALL refs → update in order → verify (grep old=0, new=expected)
- Verification: total = done + skip + fail + cannot_do, no "fixed" without Read proof
- MultiSelect: "All" as first option

## Code Quality
- Fail-Fast: immediate visible failure, no silent fallbacks
- DRY: single source of truth, zero duplicates
- No Orphans: every function called, every import used
- Type Safety: annotations + strict static analysis (mypy/pyright)
- Complexity: cyclomatic <10 per function
- Tech Debt: ratio <5%, track via SonarQube
- Maintainability: index >65
- Linting: ruff/eslint + SAST (Semgrep/CodeQL)
- Evidence-Based: command output + exit code proof
- No Overengineering: minimum for current task, no hypotheticals
- Clean Code: meaningful names, single responsibility
- Code Review: standardized checklist
- Immutability: prefer immutable, mutate only for performance
- Profile First: measure before optimize
- Version: single source, SemVer (MAJOR.MINOR.PATCH)

## Security
- Input Validation: Pydantic/Joi/Zod at all entry points
- Privacy-First: PII managed, cleaned from memory, GDPR/CCPA
- Encryption: AES-256-GCM for data at rest
- Zero Disk: sensitive data in RAM only
- Auth: OAuth2 + RBAC + mTLS, verify every request (Zero Trust)
- SQL: parameterized queries only
- Secrets: Vault/AWS, rotate 30-90 days, never hardcode
- Rate Limit: all endpoints, per-user/IP, return headers
- XSS: sanitize all user input
- Supply Chain: SBOM, Sigstore signing, lockfiles
- AI Security: validate prompts/outputs, prevent injection
- Container: distroless, non-root, CVE scan (Trivy)
- K8s: RBAC least privilege, NetworkPolicy, PodSecurity
- Policy-as-Code: OPA/Sentinel
- CORS: configure allowed origins/methods
- Audit Log: all security events, immutable
- OWASP: API Top 10 compliance
- Dependencies: Dependabot, scan in CI
- Incident Response: IR plan, SIEM, DR tested

## AI-Assisted (2025)
- Review AI Code: treat as junior output, verify
- Workflow: Plan → Act → Review → Repeat
- Test AI Output: unit tests before integration
- Decompose: break complex tasks for AI
- No Vibe Coding: avoid rare langs/new frameworks
- Context Files: CLAUDE.md, plan.md, arch docs
- Human-AI: humans architect, AI implements, humans review
- Challenge: "are you sure?" for perfect-looking solutions

## Architecture
- Event-Driven: async patterns, communicate via events
- Service Mesh: Istio/Linkerd for mTLS, observability
- Separation: one aspect per module/class
- DI: inject dependencies, enable testing
- Dependency Rule: inward only toward business logic
- Circuit Breaker: fail fast on unhealthy downstream
- Bounded Contexts: DDD, own models/rules per context
- API Versioning: explicit versions, backward compatible
- Idempotency: safe to retry without side effects
- Event Sourcing: state as event sequence

## Operations
- Zero Maintenance: auto-manage lifecycle
- Config as Code: versioned, validated, env-aware
- IaC + GitOps: Terraform/Pulumi + ArgoCD/Flux
- Observability: OpenTelemetry (metrics, traces, logs)
- Health: /health + /ready endpoints
- Graceful Shutdown: SIGTERM → drain → close
- Blue/Green: zero downtime, instant rollback
- Canary: progressive rollout, auto-rollback on errors
- Feature Flags: decouple deploy from release
- Incremental Safety: stash → change → test → rollback on fail

## Testing
- Coverage: 80% min, 100% critical paths
- Integration: e2e for critical workflows
- CI Gates: lint + test + coverage + security before merge
- Isolation: no dependencies between tests
- TDD: tests first, code satisfies
- Contract: verify API contracts between services

## Performance
- DB: indexing, N+1 prevention, explain plans
- Async I/O: no blocking in async context
- Caching: cache-aside/write-through, TTL, invalidation
- Cache Hit: >80% target
- Connection Pool: reuse, size based on load
- Lazy Load: defer until needed
- Compression: gzip/brotli responses

## Data
- Backup: automated, defined RPO/RTO, tested restore
- Migrations: versioned, backward compatible, rollback
- Retention: defined periods, auto-cleanup

## API
- REST: proper methods, status codes, resource naming
- Pagination: cursor-based for large datasets
- Docs: OpenAPI spec, examples, synced with code
- Errors: consistent format, no stack traces in prod
- GraphQL: complexity limits, depth limits, persisted queries

## Accessibility
- WCAG 2.2 AA: perceivable, operable, understandable, robust
- Semantic HTML: native elements (button, nav, form)
- ARIA: only when HTML insufficient
- Keyboard: all interactive elements accessible
- Screen Reader: alt text, heading hierarchy, labels
- Contrast: 4.5:1 normal, 3:1 large text
- Focus: logical order, trap in modals

## i18n
- Externalized: no hardcoded user text
- Unicode: UTF-8 everywhere
- RTL: support Arabic, Hebrew
- Locale: date/time/number formatting
- Pluralization: proper rules per language

## Reliability
- Chaos: inject failures in production
- Resilience: validate failure scenarios
- Timeouts: explicit for all external calls
- Retry: exponential backoff + jitter
- Bulkhead: isolate failures
- Fallback: graceful degradation

## Cost
- FinOps: monitor, right-size, spot instances
- Tagging: all cloud resources
- Auto-Scale: scale to zero when idle
- Green: energy-efficient, carbon-aware

## Docs
- README: description, setup, usage, contributing
- API Docs: complete, accurate, auto-generated
- ADR: decisions + context + consequences
- Comments: why not what
- Runbooks: ops procedures

## DX
- Local Parity: match production
- Fast Feedback: quick builds, fast tests
- Self-Service: provision without tickets
- Golden Paths: recommended approaches

## Compliance
- License: track deps, no GPL without review
- Frameworks: SOC2/HIPAA/PCI-DSS as applicable
- Classification: data by sensitivity
<!-- CCO_STANDARDS_END -->
"""
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    action = "created"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        content = re.sub(
            r"<!-- CCO_PRINCIPLES_START -->.*?<!-- CCO_PRINCIPLES_END -->\n?",
            "",
            content,
            flags=re.DOTALL,
        )
        if "<!-- CCO_STANDARDS_START -->" in content:
            content = re.sub(
                r"<!-- CCO_STANDARDS_START -->.*?<!-- CCO_STANDARDS_END -->\n?",
                standards,
                content,
                flags=re.DOTALL,
            )
            action = "updated"
        else:
            content = content.rstrip() + "\n\n" + standards
            action = "appended"
    else:
        content = standards

    content = re.sub(r"\n{3,}", "\n\n", content)
    claude_md.write_text(content, encoding="utf-8")

    if verbose:
        print(f"  CLAUDE.md: CCO Principles {action}")
        print("    17 categories, 118 principles")


def post_install() -> int:
    """CLI entry point for cco-setup."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: cco-setup")
        print("Install CCO commands, agents, and standards to ~/.claude/")
        return 0

    try:
        print("\n" + "=" * 50)
        print("CCO Setup")
        print("=" * 50)
        print(f"\nLocation: {CLAUDE_DIR}\n")

        # Commands
        print("Commands:")
        cmds = setup_commands()
        if not cmds:
            print("  (none)")
        print()

        # Agents
        print("Agents:")
        agents = setup_agents()
        if not agents:
            print("  (none)")
        print()

        # Rules
        print("Rules:")
        setup_claude_md()
        print()

        # Summary
        print("=" * 50)
        print("Summary")
        print("=" * 50)
        print(f"  Commands:  {len(cmds)}")
        print(f"  Agents:    {len(agents)}")
        print("  Principles: 17 categories in CLAUDE.md")
        print()
        print("CCO ready! Try: /cco-help")
        print()
        return 0

    except Exception as e:
        print(f"Setup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(post_install())

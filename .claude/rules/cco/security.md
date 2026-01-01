# Security Rules

- **Secrets**: Env vars or vault only, never in code
- **Input-Boundary**: Validate at system entry points
- **Least-Privilege**: Minimum necessary access
- **Deps-Audit**: Review before adding, keep updated
- **Defense-in-Depth**: Multiple layers, don't trust single control
- **Bandit**: Run bandit security linting
- **Safety**: Check for known vulnerabilities in dependencies
- **Gitleaks**: Scan for leaked secrets in git history
- **Path-Traversal**: Validate file paths to prevent traversal
- **Command-Injection**: Never shell=True with user input
- **SQL-Injection**: Use parameterized queries
- **XSS**: Escape user input in output
- **CSRF**: Use CSRF tokens for state-changing operations
- **Auth**: Implement proper authentication/authorization
- **Logging**: Don't log secrets or PII

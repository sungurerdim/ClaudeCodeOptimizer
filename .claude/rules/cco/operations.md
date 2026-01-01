# Operations Rules

## Deployment
- **PyPI-Release**: Push tags to trigger automated PyPI publishing via GitHub Actions
- **Version-SemVer**: MAJOR.MINOR.PATCH versioning
- **Changelog**: Update CHANGELOG.md before release with breaking changes marked
- **Git-Tags**: Create annotated git tags for releases
- **Release-Notes**: GitHub release notes with upgrade instructions

## Monitoring & Troubleshooting
- **Exit-Codes**: Use standard exit codes (0 success, 1 user error, 2 system error)
- **Logging-Basic**: Log to stderr for errors, stdout for normal output
- **Debug-Mode**: Support DEBUG=1 environment variable for verbose output
- **Error-Messages**: Clear, actionable error messages with context
- **Reproducibility**: Make bugs reproducible by logging inputs and state

## Maintenance
- **Dependency-Updates**: Check for updates monthly, test before upgrading
- **Security-Patches**: Apply immediately for security vulnerabilities
- **Issue-Triage**: Respond to issues within 48 hours
- **Documentation**: Keep README and usage docs in sync with code changes

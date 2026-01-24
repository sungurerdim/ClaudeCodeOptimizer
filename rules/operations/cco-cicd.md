# CI/CD
*Continuous integration and deployment rules*

## GitHub Actions (CI:GitHub)
**Trigger:** {github_workflow_dir}

- **Matrix-Test**: Matrix for multiple versions
- **Cache-Deps**: Cache dependencies
- **Secrets-Safe**: Use GitHub Secrets
- **Concurrency-Limit**: Cancel redundant runs

## GitLab CI (CI:GitLab)
**Trigger:** {gitlab_config}

- **Stage-Order**: Logical stage ordering
- **Cache-Key**: Proper cache key strategy
- **Artifacts-Expire**: Artifact expiration
- **Rules-Conditional**: Conditional job execution

## Jenkins (CI:Jenkins)
**Trigger:** {jenkins_config}

- **Pipeline-Declarative**: Declarative over scripted
- **Agent-Label**: Specific agent labels
- **Credentials-Bind**: Credentials binding
- **Parallel-Stages**: Parallel where independent

## CircleCI (CI:CircleCI)
**Trigger:** {circleci_config}

- **Orbs-Reuse**: Use orbs for common tasks
- **Workspace-Persist**: Persist between jobs
- **Resource-Class**: Appropriate resource class

## Azure DevOps (CI:Azure)
**Trigger:** {azure_config}

- **Templates-Share**: Shared YAML templates
- **Variable-Groups**: Variable groups for secrets
- **Environments-Deploy**: Environment approvals

## ArgoCD (CI:ArgoCD)
**Trigger:** {argocd_dir}, {argocd_config}

- **Sync-Policy**: Auto-sync vs manual
- **Health-Check-ArgoCD**: Custom health checks
- **Diff-Strategy**: Appropriate diff strategy

# Infrastructure Tools
*Infrastructure management tool rules*

**Trigger:** Infrastructure tool detected

## Ansible (Infra:Ansible)
**Trigger:** {ansible_config}, {ansible_patterns}

- **Inventory-Dynamic**: Use dynamic inventory for cloud resources
- **Role-Organization**: Organize playbooks into roles
- **Vault-Secrets**: Ansible Vault for sensitive data
- **Idempotency**: Ensure tasks are idempotent
- **Handler-Notify**: Use handlers for service restarts
- **Tags-Selective**: Tags for selective execution
- **Molecule-Testing**: Test roles with Molecule
- **Collections-Reuse**: Use Ansible Galaxy collections

## Consul (Infra:Consul)
**Trigger:** {consul_config}, {consul_patterns}

- **Service-Registration**: Auto-register services with health checks
- **KV-Store**: Use KV store for dynamic configuration
- **Service-Mesh**: Connect for service mesh
- **ACL-Policies**: ACL policies for security
- **Prepared-Queries**: Prepared queries for failover
- **Watch-Handlers**: Watches for configuration updates
- **Datacenter-Federation**: Multi-datacenter federation

## Vault (Infra:Vault)
**Trigger:** {vault_config}, {vault_patterns}

- **Secrets-Engines**: Use appropriate secrets engines
- **Authentication-Methods**: Configure auth methods per use case
- **Policies-Minimal**: Minimal policies (least privilege)
- **Dynamic-Secrets**: Dynamic secrets for databases
- **Token-TTL**: Short-lived tokens with renewal
- **Audit-Logging**: Enable audit logging
- **Seal-Unseal**: Secure seal/unseal procedures
- **Agent-Injection**: Vault Agent for Kubernetes injection

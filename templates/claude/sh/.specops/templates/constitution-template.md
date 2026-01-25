# Infrastructure Constitution

## Core Principles

### 1. Infrastructure as Code Philosophy
- **Declarative over Imperative**: All infrastructure should be defined declaratively
- **Version Control Everything**: Every infrastructure change must be tracked in Git
- **Immutable Infrastructure**: Prefer replacing resources over modifying them
- **Idempotency**: All operations should be safely repeatable
- **Self-Documenting**: Code should clearly express intent without extensive comments

### 2. Technology Stack Standards

#### VM Provisioning (Terraform)
- Use Terraform for all VM and cloud resource provisioning
- Follow the [Terraform Style Guide](https://www.terraform.io/docs/language/syntax/style.html)
- Organize code with modules for reusability
- Use remote state with appropriate locking mechanisms
- Tag all resources with:
  - `Environment` (dev/staging/prod)
  - `ManagedBy` (terraform)
  - `Project` (project name)
  - `Owner` (team/organization)

#### Kubernetes Setup (Ansible)
- Use Ansible for Kubernetes cluster installation and configuration
- Maintain separate playbooks for different cluster types (development, production)
- Use Ansible roles for modularity
- Store sensitive data in Ansible Vault
- Document all variables in `group_vars` with clear descriptions

#### Application Deployment (ArgoCD)
- All application deployments must use GitOps via ArgoCD
- Use Helm charts or Kustomize for application definitions
- Organize applications by namespace and environment
- Enable auto-sync only for non-production environments
- Require manual approval for production deployments

### 3. Multi-Tenancy & Network Isolation

#### Namespace Strategy
- Each organization gets dedicated namespace(s)
- Naming convention: `<org-name>-<environment>` (e.g., `acme-prod`, `acme-dev`)
- Never share namespaces between organizations
- Use ResourceQuotas and LimitRanges for each namespace

#### Network Policies (Cilium)
- Default deny-all network policy in each namespace
- Explicitly allow only required communication paths
- Use Cilium NetworkPolicies for L7 filtering when needed
- Document all network policy exceptions
- Regular review of network policies (quarterly minimum)

#### Security Boundaries
- Pod Security Standards: `restricted` for production, `baseline` for dev/staging
- No privileged containers in production
- No hostNetwork/hostPath in multi-tenant namespaces
- Enforce image scanning and signing
- Require security contexts for all workloads

### 4. Code Quality & Testing

#### Terraform Standards
- Run `terraform fmt` before every commit
- Run `terraform validate` in CI/CD
- Use `terraform plan` in pull requests (show output)
- Use `tflint` for additional validation
- Minimum test coverage: smoke tests for all modules

#### Ansible Standards
- Use `ansible-lint` for all playbooks
- Test playbooks with Molecule when possible
- Use check mode (`--check`) before actual runs
- Document prerequisites and dependencies clearly
- Keep playbooks focused and composable

#### Kubernetes Manifests
- Validate with `kubectl --dry-run=server`
- Use `kubeval` or `kubeconform` for schema validation
- Apply security best practices (kube-score, polaris)
- Test with ephemeral environments before production

### 5. Documentation Requirements

#### Repository Structure
```
infrastructure/
├── terraform/              # VM and cloud resources
│   ├── modules/           # Reusable Terraform modules
│   ├── environments/      # Environment-specific configs
│   └── README.md
├── ansible/               # Kubernetes cluster setup
│   ├── roles/            # Ansible roles
│   ├── playbooks/        # Playbooks
│   ├── inventory/        # Inventory files
│   └── README.md
├── kubernetes/            # Application deployments
│   ├── apps/             # Application manifests
│   ├── base/             # Base configurations
│   ├── overlays/         # Environment overlays
│   └── README.md
├── .specops/             # SpecOps artifacts
│   ├── memory/
│   │   └── constitution.md
│   ├── specs/
│   └── templates/
└── README.md
```

#### Required Documentation
- **README.md**: Overview, prerequisites, quick start
- **ARCHITECTURE.md**: High-level architecture diagrams and decisions
- **RUNBOOK.md**: Operational procedures and troubleshooting
- **SECURITY.md**: Security policies and compliance requirements
- Each module/role must have its own README with:
  - Purpose and scope
  - Input variables/parameters
  - Output values
  - Usage examples
  - Dependencies

### 6. Change Management

#### Development Workflow
1. Create feature branch from `main`
2. Implement changes following this constitution
3. Test in development environment
4. Create pull request with:
   - Clear description of changes
   - Infrastructure plan output (for Terraform)
   - Test results
   - Risk assessment
5. Require at least one approval
6. Merge to `main`
7. Apply to production with monitoring

#### Emergency Changes
- Document reason for emergency
- Follow expedited review process
- Create follow-up ticket for proper review
- Update documentation post-deployment

### 7. Monitoring & Observability

#### Required Metrics
- Infrastructure resource utilization
- Kubernetes cluster health
- Application deployment status
- Network policy violations
- Security scan results

#### Logging Standards
- Centralized logging for all components
- Structured logging format (JSON preferred)
- Retention: 30 days hot, 90 days cold, 1 year archive
- Log sensitive data filtering

#### Alerting Strategy
- Alert on anomalies, not absolutes
- Define clear escalation paths
- Document runbooks for each alert
- Regular review of alert effectiveness

### 8. Security & Compliance

#### Secrets Management
- Never commit secrets to Git
- Use Terraform Cloud/Enterprise for Terraform secrets
- Use Ansible Vault for Ansible secrets
- Use Kubernetes Secrets with encryption at rest
- Rotate secrets regularly (quarterly minimum)

#### Access Control
- Follow principle of least privilege
- Use RBAC for Kubernetes access
- Use IAM roles/policies for cloud resources
- Audit access logs regularly
- MFA required for production access

#### Vulnerability Management
- Scan all infrastructure code with security tools
- Scan container images before deployment
- Regular updates of base images and dependencies
- Documented process for patching critical vulnerabilities (24-hour SLA)

### 9. Disaster Recovery

#### Backup Strategy
- Automated daily backups of:
  - Terraform state files
  - Kubernetes etcd
  - Application data
  - Configuration repositories
- Test restore procedures quarterly
- Document RTO and RPO for each component

#### Business Continuity
- Multi-region capability for production
- Documented failover procedures
- Regular disaster recovery drills
- Communication plan for incidents

### 10. Performance Standards

#### Resource Efficiency
- Right-size resources based on actual usage
- Use auto-scaling where appropriate
- Regular cost optimization reviews
- Document baseline performance metrics

#### Deployment Speed
- Terraform apply: < 10 minutes
- Ansible playbook: < 15 minutes
- ArgoCD sync: < 5 minutes
- Zero-downtime deployments for stateless apps

---

## Governance

### Review & Updates
- This constitution should be reviewed quarterly
- Updates require team consensus
- Version control all changes
- Communicate updates to all stakeholders

### Enforcement
- All pull requests must comply with this constitution
- Non-compliance blocks merge
- Post-incident reviews should reference relevant principles
- Continuous improvement based on lessons learned

### Exceptions
- Exceptions must be documented and approved
- Include expiration date for temporary exceptions
- Track technical debt from exceptions
- Regular review of active exceptions

---

*This constitution guides all infrastructure decisions and implementations. When in doubt, refer to these principles.*
# [PROJECT_NAME] Infrastructure Constitution
<!-- Example: Multi-Tenant Platform Constitution, Production Cluster Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Infrastructure as Code (IaC) First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: 
All infrastructure must be defined as code with no manual changes
All IaC must be version controlled and peer-reviewed
State management must be centralized and secure (S3 + DynamoDB, etc.)
Manual changes trigger immediate drift detection and reconciliation
-->

### Zero-YAML Development
<!-- CRITICAL PRINCIPLE for SpecOps -->
**AI agent manages all Kubernetes manifests - users never write YAML manually**
- Agent generates all Kubernetes resources (Deployments, Services, Ingress, etc.)
- Agent selects appropriate deployment strategy (Helm vs Kustomize vs raw manifests)
- Agent discovers Helm charts from artifact registries before generating custom YAML
- Agent creates ArgoCD Application definitions automatically
- User describes intent in natural language; agent translates to infrastructure
- All generated manifests stored in Git for GitOps reconciliation
<!-- 
Decision Flow for Deployments:
1. Check if Helm chart exists (ArtifactHub, Bitnami, official repos)
2. If Helm exists → ArgoCD + Helm chart + values overlay
3. If no Helm → ArgoCD + Kustomize with base manifests
4. Custom apps → Kustomize with environment overlays
-->

### [PRINCIPLE_2_NAME]
<!-- Example: II. Validation Before Application -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example:
Every infrastructure change must pass validation gates before apply:
- terraform fmt → terraform validate → tflint (or equivalent)
- ansible-lint → syntax-check → dry-run (--check mode)
- kubectl dry-run → validation → policy checks
No direct applies to production without approval
-->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Multi-Tenancy Isolation (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example:
Namespace-based isolation mandatory for all organizations
Network policies: Default deny-all, explicit allows only
Resource quotas enforced per namespace/organization
RBAC: Least-privilege access, no cluster-admin for tenants
Cross-tenant communication prohibited unless explicitly documented
-->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Deployment Validation Checkpoints -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example:
Mandatory validation after each deployment phase:
- Infrastructure: terraform plan review + apply verification
- Kubernetes: All nodes Ready + networking functional
- Applications: Health checks pass + monitoring active
Validation failure stops deployment, requires rollback decision
-->

### [PRINCIPLE_5_NAME]
<!-- Example: V. GitOps & Declarative Configuration -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example:
All deployments via GitOps (ArgoCD, Flux, etc.)
Git as single source of truth for desired state
Auto-sync for non-production, manual approval for production
All changes auditable via Git history
Configuration drift triggers automatic alerts
-->

### [PRINCIPLE_6_NAME]
<!-- Example: VI. Observability & Monitoring -->
[PRINCIPLE_6_DESCRIPTION]
<!-- Example:
Metrics collection mandatory (Prometheus or equivalent)
Dashboards required: Cluster overview + per-organization
Alert rules for critical conditions (node down, quota exceeded)
Audit logging: All admin actions, API calls, policy changes
Log retention per compliance requirements (30d hot, 90d warm, 7y cold)
-->

### [PRINCIPLE_7_NAME]
<!-- Example: VII. Security Hardening -->
[PRINCIPLE_7_DESCRIPTION]
<!-- Example:
Network policies enforced cluster-wide
Secrets never in Git (use external secrets operator)
Encryption in-transit (TLS 1.2+ minimum) and at-rest
Regular vulnerability scanning (images, dependencies, cluster)
Security patches applied within SLA (critical: 7d, high: 14d, medium: 30d)
-->

### [PRINCIPLE_8_NAME]
<!-- Example: VIII. Disaster Recovery & Backup -->
[PRINCIPLE_8_DESCRIPTION]
<!-- Example:
RTO (Recovery Time Objective): [X hours]
RPO (Recovery Point Objective): [X minutes]
Backups: Automated, tested monthly, geographically distributed
Documented rollback procedures for each deployment phase
DR drills: Quarterly for production, annually for lower environments
-->

## Technology Standards

### [TECH_SECTION_1_NAME]
<!-- Example: Infrastructure Provisioning -->
[TECH_SECTION_1_CONTENT]
<!-- Example:
**Tool**: Terraform [VERSION] or equivalent
**Providers**: AWS [VERSION], Azure [VERSION], GCP [VERSION]
**State**: Remote backend (S3/Azure Storage/GCS) with locking
**Modules**: Reusable, versioned, documented
**Validation**: fmt + validate + tflint mandatory
**Testing**: terraform plan review required before apply
-->

### [TECH_SECTION_2_NAME]
<!-- Example: Configuration Management -->
[TECH_SECTION_2_CONTENT]
<!-- Example:
**Tool**: Ansible [VERSION] or equivalent
**Collections**: community.kubernetes [VERSION], ansible.posix [VERSION]
**Inventory**: Dynamic, generated from infrastructure state
**Validation**: ansible-lint + syntax-check + dry-run
**Idempotency**: All playbooks must be idempotent
**Secrets**: Never hardcoded, use vault or external secrets
-->

### [TECH_SECTION_3_NAME]
<!-- Example: Kubernetes Platform -->
[TECH_SECTION_3_CONTENT]
<!-- Example:
**Distribution**: [Vanilla K8s | EKS | AKS | GKE | RKE2] [VERSION]
**CNI**: Cilium [VERSION] or approved alternative
**Service Mesh**: [Istio | Linkerd | None] [VERSION if applicable]
**Ingress**: [NGINX | Traefik | ALB] [VERSION]
**Storage**: [EBS CSI | Azure Disk | GCP PD] [VERSION]
**High Availability**: Minimum 3 control plane nodes for production
-->

### [TECH_SECTION_4_NAME]
<!-- Example: GitOps Platform -->
[TECH_SECTION_4_CONTENT]
<!-- Example:
**Tool**: ArgoCD [VERSION] or Flux [VERSION]
**Repository**: Single source of truth for manifests
**Sync Policy**: 
  - Development: Auto-sync enabled
  - Staging: Auto-sync with self-heal
  - Production: Manual sync approval required
**Projects**: One per organization/tenant
**RBAC**: SSO integration, least-privilege access
-->

### Deployment Strategy Standards
<!-- CRITICAL: Agent-managed deployment decisions -->
**Helm Chart Discovery**:
- Primary sources: ArtifactHub, Bitnami, official vendor repos
- Agent MUST check for existing Helm charts before generating custom manifests
- Prefer community-maintained charts with >1000 downloads and active maintenance
- Pin chart versions explicitly (no `latest` or floating versions)

**ArgoCD Application Patterns**:
```yaml
# Helm-based deployment (when chart exists)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: [APP_NAME]
  namespace: argocd
spec:
  source:
    repoURL: [HELM_REPO_URL]
    chart: [CHART_NAME]
    targetRevision: [CHART_VERSION]
    helm:
      values: |
        # Environment-specific overrides
  destination:
    server: https://kubernetes.default.svc
    namespace: [TARGET_NAMESPACE]
```

```yaml
# Kustomize-based deployment (when no Helm chart)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: [APP_NAME]
  namespace: argocd
spec:
  source:
    repoURL: [GIT_REPO_URL]
    path: kubernetes/apps/[APP_NAME]/overlays/[ENV]
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: [TARGET_NAMESPACE]
```

**Kustomize Structure**:
```
kubernetes/apps/[app-name]/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml (if needed)
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

**Starter Infrastructure Components** (Agent provisions these automatically):
| Component | Helm Chart | Repository | Purpose |
|-----------|------------|------------|---------|
| nginx-ingress | ingress-nginx | https://kubernetes.github.io/ingress-nginx | Ingress controller |
| cert-manager | cert-manager | https://charts.jetstack.io | TLS certificates |
| external-secrets | external-secrets | https://charts.external-secrets.io | Secret management |
| prometheus-stack | kube-prometheus-stack | https://prometheus-community.github.io/helm-charts | Monitoring |
| argocd | argo-cd | https://argoproj.github.io/argo-helm | GitOps controller |
| sealed-secrets | sealed-secrets | https://bitnami-labs.github.io/sealed-secrets | Git-safe secrets |

### [TECH_SECTION_5_NAME]
<!-- Example: Monitoring & Observability -->
[TECH_SECTION_5_CONTENT]
<!-- Example:
**Metrics**: Prometheus [VERSION]
**Visualization**: Grafana [VERSION]
**Logging**: [Loki | ELK | CloudWatch] [VERSION]
**Tracing**: [Jaeger | Tempo] [VERSION] (if applicable)
**Alerting**: AlertManager with PagerDuty/Slack integration
**Dashboards**: Mandatory cluster + per-org views
**Retention**: Metrics 30d, Logs 90d, Audit logs per compliance
-->

## Multi-Tenancy Configuration

### [TENANCY_SECTION_1_NAME]
<!-- Example: Organization Structure -->
[TENANCY_SECTION_1_CONTENT]
<!-- Example:
**Namespace Naming**: [org-name]-[environment] (e.g., acme-prod, acme-dev)
**Default Organizations**: [Number] organizations
**Naming Convention**: Lowercase alphanumeric + hyphens only
**Metadata Labels**: 
  - organization: [org-name]
  - environment: [prod|staging|dev]
  - managed-by: terraform|argocd
-->

### [TENANCY_SECTION_2_NAME]
<!-- Example: Resource Quotas -->
[TENANCY_SECTION_2_CONTENT]
<!-- Example:
**Default Quotas per Organization**:
  - CPU requests: [X] cores
  - CPU limits: [Y] cores
  - Memory requests: [X] GiB
  - Memory limits: [Y] GiB
  - Pods: [N] maximum
  - Persistent volumes: [N] maximum, [X] GiB total
**Quota Adjustment**: Requires justification + approval
**Enforcement**: Hard limits, no burst above quota
-->

### [TENANCY_SECTION_3_NAME]
<!-- Example: Network Isolation -->
[TENANCY_SECTION_3_CONTENT]
<!-- Example:
**Default Policy**: Deny-all (zero-trust model)
**Allowed Traffic**:
  - DNS: Allow to kube-dns/CoreDNS
  - Ingress: Allow from ingress controller
  - Egress: Explicit allow-list per organization
**Cross-Tenant**: Prohibited unless explicitly documented
**Encryption**: WireGuard or TLS for sensitive workloads
**L7 Policies**: HTTP/gRPC filtering if required
-->

### [TENANCY_SECTION_4_NAME]
<!-- Example: Access Control (RBAC) -->
[TENANCY_SECTION_4_CONTENT]
<!-- Example:
**Organization Admin**: Full control within org namespaces
**Developer**: Deploy, view logs, exec into pods (non-prod only)
**Viewer**: Read-only access to resources and logs
**Platform Admin**: Cluster-level access (restricted team)
**No cluster-admin**: For tenant users under any circumstance
**MFA**: Required for production access
**Session Timeout**: [X] hours for interactive sessions
-->

## Compliance & Security

### [COMPLIANCE_SECTION_1_NAME]
<!-- Example: Compliance Standards -->
[COMPLIANCE_SECTION_1_CONTENT]
<!-- Example:
**Required Standards**: [SOC2 | PCI-DSS | HIPAA | ISO27001 | None]
**Audit Logging**: All kubectl commands, API calls, RBAC changes
**Log Retention**: [X] years minimum for audit logs
**Access Reviews**: Quarterly for production access
**Penetration Testing**: [Frequency] by [internal team | external vendor]
**Vulnerability Management**: Scan frequency, remediation SLAs
-->

### [COMPLIANCE_SECTION_2_NAME]
<!-- Example: Secrets Management -->
[COMPLIANCE_SECTION_2_CONTENT]
<!-- Example:
**Tool**: [AWS Secrets Manager | Azure Key Vault | HashiCorp Vault | External Secrets Operator]
**Rotation**: Automatic rotation every [X] days
**Access**: Kubernetes ServiceAccounts via IAM roles (IRSA/Workload Identity)
**Never in Git**: Secrets, credentials, API keys, certificates
**Encryption**: At-rest (cloud provider KMS) + in-transit (TLS)
-->

### [COMPLIANCE_SECTION_3_NAME]
<!-- Example: Image Security -->
[COMPLIANCE_SECTION_3_CONTENT]
<!-- Example:
**Registry**: Private container registry (ECR, ACR, GCR, Harbor)
**Scanning**: Trivy/Clair/Snyk scan on push
**Vulnerability Policy**: 
  - Critical: Block deployment
  - High: Warn + time-boxed remediation (7d)
  - Medium/Low: Track + remediate in backlog
**Base Images**: Approved list only (no :latest tag)
**Signature Verification**: Cosign or Notary v2 (if applicable)
-->

## Operational Standards

### [OPS_SECTION_1_NAME]
<!-- Example: Deployment Process -->
[OPS_SECTION_1_CONTENT]
<!-- Example:
**Phases**: Sequential execution (Prerequisites → Infrastructure → K8s → GitOps → Apps → Monitoring)
**Validation**: Mandatory checkpoint after each phase
**Approval**: 
  - Development: Auto-deploy on merge
  - Staging: Auto-deploy with notification
  - Production: Manual approval + change ticket
**Change Windows**: Production changes during [day/time] only
**Emergency Changes**: Requires incident commander + executive approval
-->

### [OPS_SECTION_2_NAME]
<!-- Example: Rollback Procedures -->
[OPS_SECTION_2_CONTENT]
<!-- Example:
**Documented per Phase**: 
  - Infrastructure: terraform destroy or previous state
  - Kubernetes: Re-apply previous manifests
  - Applications: ArgoCD rollback to previous revision
**RTO Target**: [X] minutes for application rollback
**Testing**: Rollback procedures tested [quarterly | annually]
**Decision Authority**: [Role] authorized to initiate rollback
-->

### [OPS_SECTION_3_NAME]
<!-- Example: Monitoring & Alerting -->
[OPS_SECTION_3_CONTENT]
<!-- Example:
**Critical Alerts** (Page immediately):
  - Node down
  - Control plane unhealthy
  - Quota exceeded causing pod failures
  - Certificate expiring < 7 days
**Warning Alerts** (Notify, no page):
  - High resource utilization (>80%)
  - Persistent volume near full (>85%)
  - Failed backup job
**Alert Routing**: PagerDuty primary, Slack secondary
**On-Call Rotation**: [Schedule] with escalation policy
-->

### [OPS_SECTION_4_NAME]
<!-- Example: Backup & Recovery -->
[OPS_SECTION_4_CONTENT]
<!-- Example:
**Backup Scope**: 
  - etcd snapshots (Kubernetes state)
  - Persistent volume data
  - Terraform state
  - Configuration files (Git already serves as backup)
**Frequency**: 
  - etcd: Hourly
  - PVs: Daily
  - Terraform state: On every apply
**Retention**: [X]d hot, [Y]d warm, [Z]y cold
**Recovery Testing**: Monthly for critical data
**Geographic Distribution**: Backups in ≥2 regions/zones
-->

## Development Workflow

### [WORKFLOW_SECTION_1_NAME]
<!-- Example: Code Review Requirements -->
[WORKFLOW_SECTION_1_CONTENT]
<!-- Example:
**Required Approvals**:
  - Infrastructure changes: [1-2] approvals from platform team
  - Kubernetes manifests: [1] approval from platform team
  - Application deployments: [1] approval from org owner
**Review Checklist**:
  - [ ] IaC passes validation (fmt, validate, lint)
  - [ ] No secrets in code
  - [ ] Documentation updated
  - [ ] Rollback plan documented (for production)
  - [ ] Constitution compliance verified
**Merge Requirements**: All CI checks pass + required approvals
-->

### [WORKFLOW_SECTION_2_NAME]
<!-- Example: Testing Gates -->
[WORKFLOW_SECTION_2_CONTENT]
<!-- Example:
**Pre-Merge**:
  - Terraform: fmt, validate, tflint, plan (no errors)
  - Ansible: ansible-lint, syntax-check (no errors)
  - Kubernetes: kubectl dry-run, validation (no errors)
**Post-Merge (CI/CD)**:
  - Deploy to development environment
  - Run smoke tests
  - Verify monitoring alerts configured
**Production Gates**:
  - Successful staging deployment
  - Manual approval
  - Change ticket approved
-->

### [WORKFLOW_SECTION_3_NAME]
<!-- Example: Documentation Requirements -->
[WORKFLOW_SECTION_3_CONTENT]
<!-- Example:
**Mandatory Documentation**:
  - README.md: Quickstart, prerequisites, usage
  - ARCHITECTURE.md: High-level design, component diagram
  - RUNBOOK.md: Common operations, troubleshooting
  - spec.md: Requirements and acceptance criteria
  - plan.md: Technical implementation design
**Update Trigger**: Any infrastructure or significant config change
**Format**: Markdown, diagrams in Mermaid or ASCII
**Location**: Co-located with infrastructure code
-->

## Performance Standards

### [PERF_SECTION_1_NAME]
<!-- Example: Infrastructure Performance -->
[PERF_SECTION_1_CONTENT]
<!-- Example:
**Provisioning Time**:
  - Infrastructure (Terraform): < [X] minutes
  - Kubernetes cluster ready: < [Y] minutes
  - Application deployment: < [Z] minutes
**Scalability**:
  - Horizontal pod autoscaling: Target [X]% CPU/memory
  - Cluster autoscaling: [Min]-[Max] nodes
  - Scale-up time: < [X] minutes
  - Scale-down grace period: [X] minutes
-->

### [PERF_SECTION_2_NAME]
<!-- Example: Service Level Objectives (SLOs) -->
[PERF_SECTION_2_CONTENT]
<!-- Example:
**Availability**: [99.9% | 99.95% | 99.99%] uptime
**Latency**: 
  - API calls: p95 < [X]ms, p99 < [Y]ms
  - Application requests: p95 < [X]ms, p99 < [Y]ms
**Error Rate**: < [X]% of requests
**RTO**: [X] hours for disaster recovery
**RPO**: [X] minutes maximum data loss
**Measurement**: [Monthly | Quarterly] SLO review
-->

## Cost Management

### [COST_SECTION_1_NAME]
<!-- Example: Budget & Optimization -->
[COST_SECTION_1_CONTENT]
<!-- Example:
**Target Budget**: $[X]/month for infrastructure
**Cost Allocation**: Per organization via resource tagging
**Optimization Strategies**:
  - Right-sizing: Monthly review of resource requests/limits
  - Spot instances: [Percentage]% of worker nodes (non-prod)
  - Auto-shutdown: Non-production environments after hours
  - Reserved instances: Production workloads with predictable usage
**Budget Alerts**: Notify at 80% and 95% of budget
**Cost Reviews**: [Monthly | Quarterly] with stakeholders
-->

## Governance

### [GOV_SECTION_1_NAME]
<!-- Example: Constitution Authority -->
[GOV_SECTION_1_CONTENT]
<!-- Example:
**Precedence**: This constitution supersedes all other policies
**Enforcement**: All PRs, reviews, deployments must verify compliance
**Non-Compliance**: Rejected immediately, no exceptions
**Justification Required**: Any deviation must be documented, approved, and time-boxed
-->

### [GOV_SECTION_2_NAME]
<!-- Example: Amendment Process -->
[GOV_SECTION_2_CONTENT]
<!-- Example:
**Proposal**: RFC document with rationale, impact analysis
**Review Period**: [X] days for team feedback
**Approval**: [Percentage]% consensus or [Role] approval
**Implementation**: Migration plan required for breaking changes
**Notification**: All stakeholders notified [X] days before effective
-->

### [GOV_SECTION_3_NAME]
<!-- Example: Compliance Verification -->
[GOV_SECTION_3_CONTENT]
<!-- Example:
**Automated Checks**: CI/CD pipeline enforces technical standards
**Manual Reviews**: Platform team verifies architectural compliance
**Audit Trail**: All changes logged with constitution compliance note
**Quarterly Review**: Constitution adherence audit by platform team
**Violation Handling**: Immediate remediation required, root cause analysis
-->

---

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 1.0.0 | Ratified: 2025-01-27 | Last Amended: 2025-01-27 -->

**Project**: [PROJECT_NAME]
**Maintainer**: [TEAM_NAME]
**Contact**: [EMAIL/SLACK_CHANNEL]

---

## Quick Start Guide (Beginner-Friendly)

<!--
  This section helps new users get started without deep Kubernetes knowledge.
  Agent provisions everything - user just describes what they want.
-->

### Minimum Viable Infrastructure

For a production-ready Kubernetes platform, agent provisions:

```
┌─────────────────────────────────────────────────────────────┐
│                    ArgoCD (GitOps Controller)               │
│                 Manages all deployments via Git             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ nginx-ingress│  │ cert-manager │  │ external-secrets │   │
│  │   (Ingress)  │  │    (TLS)     │  │    (Secrets)     │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Prometheus + Grafana                     │   │
│  │                  (Monitoring)                         │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                     Your Applications                        │
│     (Agent deploys via Helm charts or Kustomize)            │
└─────────────────────────────────────────────────────────────┘
```

### Getting Started Commands

**1. Create infrastructure specification:**
```
/specops.specify Deploy Kubernetes platform with monitoring for my web application
```

**2. Clarify requirements (optional):**
```
/specops.clarify
```

**3. Create implementation plan:**
```
/specops.plan
```

**4. Generate tasks:**
```
/specops.tasks
```

**5. Deploy infrastructure:**
```
/specops.implement
```

**6. Deploy your application:**
```
/specops.deploy my-app with image myrepo/app:v1.0 port 8080 to production
```

### Example: Deploy a Complete Platform

**User says:**
> "I want a Kubernetes cluster on AWS with ingress, TLS, monitoring, and I'll deploy 3 microservices"

**Agent provisions (automatically, zero YAML writing):**

| Component | Method | Source |
|-----------|--------|--------|
| EKS Cluster | Terraform | AWS provider |
| ArgoCD | Helm | argoproj.github.io |
| nginx-ingress | Helm | kubernetes.github.io |
| cert-manager | Helm | charts.jetstack.io |
| Prometheus Stack | Helm | prometheus-community |
| Microservice A | Kustomize | Generated base + overlays |
| Microservice B | Kustomize | Generated base + overlays |
| Microservice C | Kustomize | Generated base + overlays |

### Zero YAML Promise

Users never write:
- ❌ Kubernetes Deployment YAML
- ❌ Service YAML
- ❌ Ingress YAML
- ❌ ArgoCD Application YAML
- ❌ Helm values files
- ❌ Kustomization files

Users only describe:
- ✅ "Deploy my API with 3 replicas"
- ✅ "Add monitoring to my cluster"
- ✅ "Setup ingress for my-app.example.com"
- ✅ "I need a PostgreSQL database"

Agent handles:
- ✅ Helm chart discovery
- ✅ Manifest generation
- ✅ ArgoCD Application creation
- ✅ Environment overlays
- ✅ Git commits and sync
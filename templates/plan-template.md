# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/specops.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Cloud Provider**: [e.g., AWS, Azure, GCP, on-premise, hybrid or NEEDS CLARIFICATION]  
**IaC Tools**: [e.g., Terraform 1.6, Pulumi, CloudFormation, Ansible or NEEDS CLARIFICATION]  
**Kubernetes**: [if applicable, e.g., EKS 1.28, AKS, GKE, k3s or N/A]  
**GitOps**: [if applicable, e.g., ArgoCD, Flux, none or N/A]  
**Deployment Strategy**: [Helm-first with Kustomize fallback | Kustomize-only | Raw manifests]  
**State Backend**: [e.g., S3+DynamoDB, Azure Blob, GCS, Terraform Cloud or NEEDS CLARIFICATION]  
**Secrets Management**: [e.g., Vault, AWS Secrets Manager, Azure Key Vault or NEEDS CLARIFICATION]  
**Validation**: [e.g., terraform validate, ansible-lint, kubeval or NEEDS CLARIFICATION]  
**Target Environment**: [e.g., production, staging, development or NEEDS CLARIFICATION]
**Deployment Type**: [single-region/multi-region/multi-cloud - determines infrastructure structure]  
**Performance Goals**: [e.g., 99.9% uptime, RTO < 4h, RPO < 1h, 1000 pods or NEEDS CLARIFICATION]  
**Constraints**: [e.g., budget limits, compliance (SOC2, HIPAA), data residency or NEEDS CLARIFICATION]  
**Scale/Scope**: [e.g., 5 organizations, 50 namespaces, 100 nodes or NEEDS CLARIFICATION]

## Helm Chart Discovery

<!--
  CRITICAL: Agent MUST check for existing Helm charts before generating custom manifests.
  This section documents which components use Helm vs custom Kustomize.
-->

### Infrastructure Components

| Component | Helm Available? | Chart Source | Version | Notes |
|-----------|-----------------|--------------|---------|-------|
| Ingress Controller | ✅ Yes | kubernetes.github.io/ingress-nginx | 4.x | nginx-ingress recommended |
| Cert Manager | ✅ Yes | charts.jetstack.io | 1.x | TLS automation |
| ArgoCD | ✅ Yes | argoproj.github.io/argo-helm | 5.x | GitOps controller |
| Prometheus Stack | ✅ Yes | prometheus-community | 50.x | Full monitoring |
| External Secrets | ✅ Yes | charts.external-secrets.io | 0.9.x | Cloud secret sync |
| [Custom Component] | ❌ No | N/A | - | Use Kustomize |

### Helm Repository Configuration

```yaml
# ArgoCD Helm repositories (agent generates this)
apiVersion: v1
kind: Secret
metadata:
  name: helm-repo-[NAME]
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  name: [REPO_NAME]
  url: [REPO_URL]
  type: helm
```

### Custom Application Deployment

For applications without Helm charts, agent generates Kustomize structure:

```
kubernetes/
├── apps/
│   └── [app-name]/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── ingress.yaml
│       └── overlays/
│           ├── dev/
│           ├── staging/
│           └── prod/
└── argocd/
    └── applications/
        └── [app-name].yaml
```

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/specops.plan command output)
├── research.md          # Phase 0 output (/specops.plan command)
├── quickstart.md        # Phase 1 output (/specops.plan command) - validation scenarios
├── contracts/           # Phase 1 output (/specops.plan command) - service interfaces
└── tasks.md             # Phase 2 output (/specops.tasks command - NOT created by /specops.plan)
```

### Infrastructure Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this infrastructure. Delete unused options and expand the chosen structure with
  real paths (e.g., terraform/modules/vpc, k8s/namespaces/org-a). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single IaC tool (DEFAULT - e.g., Terraform only)
terraform/
├── modules/
│   ├── vpc/
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── scripts/

validation/
├── pre-deploy/
└── post-deploy/

# [REMOVE IF UNUSED] Option 2: Multi-tool (when Terraform + Kubernetes detected)
terraform/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
└── environments/

kubernetes/
├── base/
│   ├── namespaces/
│   ├── policies/
│   └── rbac/
├── overlays/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── apps/

argocd/
├── applications/
└── projects/

# [REMOVE IF UNUSED] Option 3: Multi-tenant (when organizations/tenants detected)
terraform/
├── shared/
│   ├── networking/
│   ├── security/
│   └── monitoring/
└── tenants/
    ├── org-a/
    ├── org-b/
    └── org-c/

kubernetes/
├── cluster-config/
└── tenants/
    ├── org-a/
    ├── org-b/
    └── org-c/
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Starter Infrastructure (Agent-Managed)

<!--
  These components are automatically provisioned by the agent.
  User specifies requirements; agent handles Helm discovery and ArgoCD setup.
-->

### Phase 0: Bootstrap Components

The agent provisions these foundational components automatically:

```
kubernetes/
├── bootstrap/                    # First-deployed components
│   ├── argocd/                  # GitOps controller (self-managed)
│   │   ├── install/             # ArgoCD installation
│   │   └── projects/            # ArgoCD projects per tenant
│   └── namespaces/              # Namespace definitions
│
├── infrastructure/              # Core platform services
│   ├── ingress-nginx/          # Ingress controller (Helm)
│   ├── cert-manager/           # TLS automation (Helm)
│   ├── external-secrets/       # Secret management (Helm)
│   └── monitoring/             # Prometheus + Grafana (Helm)
│
├── apps/                        # Application deployments
│   └── [app-name]/             # Per-app Kustomize structure
│       ├── base/
│       └── overlays/
│
└── argocd/
    └── applications/            # ArgoCD Application definitions
        ├── bootstrap.yaml       # App-of-apps for bootstrap
        ├── infrastructure.yaml  # App-of-apps for infra
        └── apps.yaml           # App-of-apps for user apps
```

### Deployment Decision Matrix

| Scenario | Strategy | Agent Action |
|----------|----------|--------------|
| Component has official Helm chart | Helm + ArgoCD | Discover chart, create ArgoCD Application with Helm source |
| Component has community Helm chart (>1k downloads) | Helm + ArgoCD | Validate chart quality, create ArgoCD Application |
| No Helm chart available | Kustomize + ArgoCD | Generate base manifests, create overlays, ArgoCD Application |
| Custom user application | Kustomize + ArgoCD | Create Kustomize structure, Dockerfile if needed |
| Existing Helm chart needs customization | Helm + values overlay | Use Helm with custom values.yaml overlay |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th IaC tool] | [current need] | [why 3 tools insufficient] |
| [e.g., Multi-region deployment] | [specific problem] | [why single-region insufficient] |
| [e.g., Custom CNI plugin] | [specific requirement] | [why standard CNI insufficient] |
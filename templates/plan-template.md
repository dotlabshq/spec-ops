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
**State Backend**: [e.g., S3+DynamoDB, Azure Blob, GCS, Terraform Cloud or NEEDS CLARIFICATION]  
**Secrets Management**: [e.g., Vault, AWS Secrets Manager, Azure Key Vault or NEEDS CLARIFICATION]  
**Validation**: [e.g., terraform validate, ansible-lint, kubeval or NEEDS CLARIFICATION]  
**Target Environment**: [e.g., production, staging, development or NEEDS CLARIFICATION]
**Deployment Type**: [single-region/multi-region/multi-cloud - determines infrastructure structure]  
**Performance Goals**: [e.g., 99.9% uptime, RTO < 4h, RPO < 1h, 1000 pods or NEEDS CLARIFICATION]  
**Constraints**: [e.g., budget limits, compliance (SOC2, HIPAA), data residency or NEEDS CLARIFICATION]  
**Scale/Scope**: [e.g., 5 organizations, 50 namespaces, 100 nodes or NEEDS CLARIFICATION]

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

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th IaC tool] | [current need] | [why 3 tools insufficient] |
| [e.g., Multi-region deployment] | [specific problem] | [why single-region insufficient] |
| [e.g., Custom CNI plugin] | [specific requirement] | [why standard CNI insufficient] |
# Implementation Plan: [Feature Name]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specops/templates/commands/plan.md` for the execution workflow.


## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technology Stack

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

### Infrastructure Provisioning
- **Tool**: Terraform
- **Version**: [e.g., 1.6.x]
- **State Backend**: [e.g., S3 + DynamoDB, Terraform Cloud]
- **Provider(s)**: [e.g., AWS, Azure, GCP]
- **Provider Version(s)**: [Specific versions]

### Configuration Management
- **Tool**: Ansible
- **Version**: [e.g., 2.15.x]
- **Python Version**: [e.g., 3.11]
- **Collections**: [List of Ansible collections needed]

### Kubernetes
- **Distribution**: [e.g., EKS, GKE, RKE2, vanilla]
- **Version**: [e.g., 1.28.x]
- **CNI**: [e.g., Cilium]
- **Cilium Version**: [e.g., 1.14.x]

### Ingress & Load Balancing
- **Ingress Controller**: NGINX Ingress Controller
- **Version**: [e.g., 1.9.x via Helm chart controller-v1.9.x]
- **Monitoring**: Prometheus metrics exposed on `/metrics`

### Application Deployment
- **Tool**: ArgoCD
- **Version**: [e.g., 2.9.x]
- **Manifest Format**: Helm | Kustomize | Plain YAML
- **Repository Structure**: [How GitOps repo is organized]


## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Architecture

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/specops.plan command output)
├── research.md          # Phase 0 output (/specops.plan command)
├── data-model.md        # Phase 1 output (/specops.plan command)
├── quickstart.md        # Phase 1 output (/specops.plan command)
├── contracts/           # Phase 1 output (/specops.plan command)
└── tasks.md             # Phase 2 output (/specops.tasks command - NOT created by /specops.plan)
```

### High-Level Architecture
```
[ASCII diagram or description of component relationships]

Example:
┌─────────────────┐
│   Terraform     │ ──> Provisions VMs/Cloud Resources
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    Ansible      │ ──> Installs K8s Cluster
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    ArgoCD       │ ──> Deploys Applications
└─────────────────┘
```

## File Structure
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
infrastructure/
├── terraform/
│   ├── modules/
│   │   ├── vpc/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── compute/
│   │   └── security/
│   ├── environments/
│   │   ├── dev/ 
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   └── prod/
│   └── README.md
│
├── ansible/
│   ├── inventory/
│   │   ├── dev/
│   │   └── prod/
│   ├── roles/
│   │   ├── k8s-control-plane/
│   │   ├── k8s-worker/
│   │   └── cilium/
│   ├── playbooks/
│   │   ├── k8s-setup.yml
│   │   └── cilium-install.yml
│   └── README.md
│
├── kubernetes/
│   ├── argocd/
│   │   ├── install/
│   │   └── projects/
│   ├── apps/
│   │   └── [feature-name]/
│   │       ├── base/
│   │       │   ├── deployment.yaml
│   │       │   ├── service.yaml
│   │       │   └── kustomization.yaml
│   │       └── overlays/
│   │           ├── dev/
│   │           └── prod/
│   └── README.md
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
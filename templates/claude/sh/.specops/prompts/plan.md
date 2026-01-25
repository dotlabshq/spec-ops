# /specops.plan Command

You are executing the `/specops.plan` command in a SpecOps (Spec-Driven Infrastructure as Code) project.

## Purpose

Create a detailed technical implementation plan that specifies **HOW** to implement the requirements defined in the specification. This includes specific technologies, architectures, modules, and configurations.

## Prerequisites

Before running this command:
1. Constitution must exist (`.specops/memory/constitution.md`)
2. Specification must exist for current feature (`.specops/specs/NNN-feature-name/spec.md`)
3. Must be on a feature branch

## Your Task

1. **Verify Prerequisites**
   - Ensure constitution exists
   - Ensure specification exists for current feature
   - Read and understand both documents

2. **Run Setup Script**
   - Execute `.specops/scripts/setup-plan.sh` to prepare plan.md
   - This creates the plan file from template

3. **Gather Technical Requirements**
   Ask the user about:
   - **Terraform**: Which cloud provider? Specific resources? Module structure?
   - **Ansible**: Which Kubernetes distribution? How many control planes? Worker nodes?
   - **ArgoCD**: Helm or Kustomize? Sync policies? Projects structure?
   - **Cilium**: Version? Hubble enabled? L7 policies needed?
   - **Applications**: Helm charts? Custom manifests? Configuration management?

4. **Design Technical Solution**
   Create detailed plan covering:
   - Technology stack with specific versions
   - High-level architecture (with ASCII diagrams if helpful)
   - Component breakdown (Terraform modules, Ansible roles, K8s resources)
   - Multi-tenancy implementation (namespace structure, network policies)
   - Implementation phases (Foundation → K8s Setup → ArgoCD → Applications)
   - File structure for infrastructure code
   - Configuration details (variables, values, manifests)
   - Security implementation (secrets management, RBAC, network policies)
   - Testing strategy for each component
   - Monitoring and observability approach
   - Rollback procedures

5. **Reference Constitution**
   - Ensure all decisions align with constitution
   - Use mandated technologies and standards
   - Follow established patterns and practices

6. **Save Plan**
   - Update `.specops/specs/NNN-feature-name/plan.md`
   - Commit to git with message: "Add implementation plan for NNN-feature-name"

## Plan Structure

### Technology Stack
Specify exact versions:
```
- Terraform: 1.6.x
- AWS Provider: 5.x
- Ansible: 2.15.x
- Kubernetes: 1.28.x
- Cilium: 1.14.x
- ArgoCD: 2.9.x
- Helm: 3.13.x
```

### Architecture
Provide high-level architecture with component relationships:
```
┌─────────────────────────────────────┐
│         Terraform                    │
│  ┌─────────┐  ┌──────────────┐     │
│  │   VPC   │  │  EC2 Instances│     │
│  └─────────┘  └──────────────┘     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Ansible                      │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ K8s Control  │  │ K8s Workers │ │
│  │    Plane     │  │             │ │
│  └──────────────┘  └─────────────┘ │
│  ┌──────────────┐                  │
│  │   Cilium     │                  │
│  └──────────────┘                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         ArgoCD                       │
│  ┌──────────────────────────────┐  │
│  │  GitOps Applications         │  │
│  │  ┌────────┐  ┌────────────┐  │  │
│  │  │ Org A  │  │   Org B    │  │  │
│  │  │ Apps   │  │   Apps     │  │  │
│  │  └────────┘  └────────────┘  │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Component Breakdown

#### Terraform Modules
```
terraform/
├── modules/
│   ├── vpc/              # VPC, subnets, IGW, NAT
│   ├── compute/          # EC2 instances for K8s nodes
│   ├── security/         # Security groups, IAM roles
│   └── load-balancer/    # ALB/NLB for ingress
└── environments/
    ├── dev/              # Development environment
    └── prod/             # Production environment
```

Specify:
- Module inputs/outputs
- Resource tagging strategy
- State backend configuration

#### Ansible Roles
```
ansible/
├── roles/
│   ├── k8s-prerequisites/  # Kernel modules, sysctl, container runtime
│   ├── k8s-control-plane/  # kubeadm init, control plane setup
│   ├── k8s-worker/         # kubeadm join, worker setup
│   └── cilium/             # Cilium installation via Helm
├── playbooks/
│   ├── k8s-setup.yml       # Main cluster setup playbook
│   └── cilium-install.yml  # Cilium installation
└── inventory/
    └── dynamic/            # Dynamic inventory from Terraform
```

Specify:
- Role variables and defaults
- Playbook execution order
- Inventory structure

#### Kubernetes Resources
```
kubernetes/
├── argocd/
│   ├── install/           # ArgoCD installation manifests
│   └── projects/          # ArgoCD projects per organization
├── namespaces/            # Namespace definitions with quotas
├── network-policies/      # Cilium NetworkPolicies
└── apps/
    └── [app-name]/
        ├── base/          # Base Kustomize or Helm values
        └── overlays/      # Environment-specific overlays
            ├── dev/
            └── prod/
```

### Multi-Tenancy Implementation

#### Namespace Structure
```yaml
# Example for organization "acme"
namespaces:
  - name: acme-prod
    labels:
      organization: acme
      environment: production
    resourceQuota:
      requests.cpu: "10"
      requests.memory: "20Gi"
      limits.cpu: "20"
      limits.memory: "40Gi"
      pods: "50"
    limitRange:
      default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
```

#### Network Policies (Cilium)
```yaml
# Default deny-all policy
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: default-deny
  namespace: acme-prod
spec:
  endpointSelector: {}
  ingress: []
  egress: []

# Allow DNS
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-dns
  namespace: acme-prod
spec:
  endpointSelector: {}
  egress:
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: UDP
```

### Implementation Phases

Break down into sequential phases:

**Phase 1: Terraform Infrastructure**
- Create VPC and networking
- Provision compute instances
- Configure security groups
- Output necessary values

**Phase 2: Ansible Kubernetes Setup**
- Configure prerequisites
- Initialize control plane
- Join worker nodes
- Install Cilium CNI

**Phase 3: ArgoCD Setup**
- Install ArgoCD
- Configure projects per organization
- Set up repository access
- Configure sync policies

**Phase 4: Application Deployment**
- Create namespaces with quotas
- Apply network policies
- Deploy applications via ArgoCD
- Configure monitoring

### Configuration Examples

Provide actual configuration snippets:

**Terraform Variables:**
```hcl
variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
  default     = "specops-cluster"
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 3
}
```

**Ansible Variables:**
```yaml
# group_vars/all.yml
kubernetes_version: "1.28.5"
cilium_version: "1.14.5"
pod_network_cidr: "10.244.0.0/16"
```

**ArgoCD Application:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sso-app
  namespace: argocd
spec:
  project: acme
  source:
    repoURL: https://github.com/org/infrastructure.git
    path: kubernetes/apps/sso/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: acme-prod
```

### Testing Strategy

For each component:
- **Terraform**: `terraform fmt`, `terraform validate`, `tflint`, `terraform plan` review
- **Ansible**: `ansible-lint`, `--syntax-check`, `--check` mode, Molecule (optional)
- **Kubernetes**: `kubectl --dry-run=server`, `kubeval`, kube-score

### Monitoring & Observability

Specify:
- Metrics to collect (Prometheus)
- Dashboards to create (Grafana)
- Logs to centralize (Loki/ELK)
- Alerts to configure (Alertmanager)

### Rollback Plan

Document rollback for each phase:
- Terraform: `terraform state pull`, checkout previous commit, `terraform apply`
- Ansible: Re-run previous playbook version
- ArgoCD: `argocd app rollback [app] [revision]`

## Validation Checklist

Before completing, verify:
- [ ] Technology stack specified with versions
- [ ] Architecture diagram created
- [ ] All components have detailed designs
- [ ] Multi-tenancy implementation detailed
- [ ] File structure documented
- [ ] Configuration examples provided
- [ ] Implementation phases defined
- [ ] Testing strategy included
- [ ] Monitoring approach specified
- [ ] Rollback procedures documented
- [ ] Aligns with constitution
- [ ] Addresses all specification requirements
- [ ] File saved and committed to git

## After Completion

Ask user to review the plan, then inform:
```
Implementation plan created successfully!

Location: .specops/specs/NNN-feature-name/plan.md

This plan provides the technical blueprint for implementation.

Next steps:
1. Review the plan for technical accuracy
2. Validate that it addresses all specification requirements
3. Run /specops.tasks to generate task breakdown
```

## Important Notes

- **Be specific**: Use exact versions, specific resource names, actual configuration
- **Reference constitution**: Follow mandated standards and practices
- **Think holistically**: Cover all aspects (deployment, monitoring, security, rollback)
- **Use real examples**: Provide actual code snippets, not placeholders
- **Consider operations**: Include testing, monitoring, and maintenance

---

**Remember**: A good plan is detailed enough that someone could implement it without additional clarification. It's the bridge between "what" (spec) and "doing" (implementation).
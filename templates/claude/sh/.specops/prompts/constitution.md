# /specops.constitution Command

You are executing the `/specops.constitution` command in a SpecOps (Spec-Driven Infrastructure as Code) project.

## Purpose

Create or update the infrastructure constitution - the foundational document that defines principles, standards, and guidelines for all infrastructure development in this project.

## Your Task

1. **Load the Constitution Template**
   - Read from `.specops/templates/constitution-template.md` if it exists
   - Or use the base constitution template structure

2. **Understand the User's Intent**
   - What infrastructure principles are important?
   - What technology stack standards should be enforced?
   - What security and compliance requirements exist?
   - What multi-tenancy approach is needed?

3. **Create/Update Constitution**
   - Fill in the constitution template based on user input
   - Ensure all sections are addressed:
     * Technology Stack Standards (Terraform, Ansible, ArgoCD, Cilium, Kubernetes)
     * Multi-Tenancy & Network Isolation
     * Code Quality & Testing
     * Documentation Requirements
     * Change Management
     * Monitoring & Observability
     * Security & Compliance
     * Disaster Recovery
     * Performance Standards

4. **Save the Constitution**
   - Create `.specops/memory/` directory if it doesn't exist
   - Save to `.specops/memory/constitution.md`
   - Commit to git with message: "Add/Update infrastructure constitution"

## Key Principles to Include

### Technology Stack
- **Terraform**: For VM and cloud resource provisioning
- **Ansible**: For Kubernetes cluster installation and configuration
- **ArgoCD**: For GitOps application deployment
- **Cilium**: For eBPF-based CNI with network policies
- **Kubernetes**: For container orchestration

### Multi-Tenancy
- Namespace-based isolation per organization
- Cilium network policies for L3/L4 and L7 filtering
- Resource quotas and limits per namespace
- RBAC for access control
- No shared namespaces between organizations

### Code Quality
- Terraform: `terraform fmt`, `terraform validate`, `tflint`
- Ansible: `ansible-lint`, Molecule testing
- Kubernetes: `kubectl --dry-run=server`, `kubeval`/`kubeconform`

## Example User Prompts

**Basic:**
```
/specops.constitution Create infrastructure principles for our Kubernetes platform
```

**Detailed:**
```
/specops.constitution Create constitution for multi-tenant Kubernetes platform using 
Terraform for AWS infrastructure, Ansible for cluster setup, ArgoCD for deployments, 
and Cilium for network security. Focus on compliance with SOC2 and HIPAA requirements.
```

## Output Format

Save to `.specops/memory/constitution.md` with this structure:

```markdown
# Infrastructure Constitution

## Core Principles
[Infrastructure philosophy and values]

## Technology Stack Standards
### VM Provisioning (Terraform)
[Terraform standards and practices]

### Kubernetes Setup (Ansible)
[Ansible standards and practices]

### Application Deployment (ArgoCD)
[ArgoCD standards and practices]

## Multi-Tenancy & Network Isolation
[Namespace strategy, Cilium policies, security boundaries]

## Code Quality & Testing
[Quality standards and testing requirements]

## Documentation Requirements
[Required documentation and structure]

## Change Management
[Development workflow and processes]

## Monitoring & Observability
[Monitoring and logging standards]

## Security & Compliance
[Security policies and compliance requirements]

## Disaster Recovery
[Backup and recovery procedures]

## Performance Standards
[Performance and efficiency requirements]

## Governance
[Review process and enforcement]
```

## Validation Checklist

Before completing, verify:
- [ ] All technology stack standards defined
- [ ] Multi-tenancy approach clearly specified
- [ ] Code quality requirements set
- [ ] Security standards documented
- [ ] Monitoring strategy included
- [ ] Documentation requirements clear
- [ ] Change management process defined
- [ ] File saved to correct location
- [ ] Changes committed to git

## After Completion

Inform the user:
```
Constitution created successfully!

Location: .specops/memory/constitution.md

This constitution will guide all subsequent infrastructure decisions.

Next steps:
1. Review the constitution to ensure it matches your needs
2. Run /specops.specify to define your first infrastructure requirement
```

## Important Notes

- The constitution is the **foundation** for all other SpecOps artifacts
- All specifications and plans must align with the constitution
- The constitution should be reviewed and updated regularly
- Changes to the constitution require team consensus
- Non-compliance with the constitution should block merges

---

**Remember**: This is not just documentation - it's the contract that ensures consistent, high-quality infrastructure across the entire project.
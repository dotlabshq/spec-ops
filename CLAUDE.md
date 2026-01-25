# SpecOps Commands for Claude Code

You are working in a **SpecOps** (Spec-Driven Infrastructure as Code) project. This project follows a structured methodology for building production-ready infrastructure using Terraform, Ansible, ArgoCD, and Kubernetes with Cilium.

## Available Commands

You have access to the following slash commands:

- `/specops.constitution` - Establish infrastructure principles and standards
- `/specops.specify` - Define infrastructure requirements (what and why)
- `/specops.plan` - Create technical implementation plan (how)
- `/specops.tasks` - Generate actionable task breakdown
- `/specops.implement` - Execute implementation with infrastructure automation

## Workflow

The SpecOps workflow follows this sequence:

1. **Constitution** → Define principles and standards
2. **Specification** → Define requirements (infrastructure scenarios, multi-tenancy, etc.)
3. **Planning** → Design technical solution (Terraform modules, Ansible playbooks, ArgoCD apps)
4. **Tasks** → Break down into executable tasks
5. **Implementation** → Execute infrastructure automation

## File Structure

```
.specops/
├── memory/
│   └── constitution.md          # Project principles and standards
├── specs/
│   └── NNN-feature-name/
│       ├── spec.md              # Infrastructure specification
│       ├── plan.md              # Technical implementation plan
│       └── tasks.md             # Task breakdown
├── scripts/
│   ├── common.sh                # Common utilities
│   ├── create-new-feature.sh   # Create new feature branch
│   └── setup-plan.sh            # Set up planning artifacts
└── prompts/
    ├── constitution.md          # Constitution command prompt
    ├── specify.md               # Specify command prompt
    ├── plan.md                  # Plan command prompt
    ├── tasks.md                 # Tasks command prompt
    └── implement.md             # Implement command prompt
```

## Technology Stack

This project uses:
- **Terraform** - Infrastructure provisioning (VMs, cloud resources)
- **Ansible** - Configuration management (Kubernetes cluster setup)
- **ArgoCD** - GitOps application deployment
- **Cilium** - eBPF-based CNI with network policies for multi-tenancy
- **Kubernetes** - Container orchestration platform

## Multi-Tenancy Approach

- Each organization gets dedicated namespace(s)
- Cilium network policies provide isolation
- Resource quotas and limits per namespace
- RBAC for access control
- No shared namespaces between organizations

## Best Practices

### When Executing Commands

1. **Always read the template first** - Load the template from `.specops/prompts/` before executing
2. **Follow the constitution** - Reference `.specops/memory/constitution.md` for all decisions
3. **Use scripts** - Run helper scripts in `.specops/scripts/` for Git operations
4. **Validate continuously** - Check Terraform plans, Ansible syntax, Kubernetes manifests
5. **Document decisions** - Keep specifications and plans up to date

### Infrastructure Code Quality

- **Terraform**: Run `terraform fmt`, `terraform validate`, use modules
- **Ansible**: Use `ansible-lint`, test with `--check` mode
- **Kubernetes**: Validate with `kubectl --dry-run=server`
- **Security**: Never commit secrets, use proper secret management

### Git Workflow

- Create feature branch for each infrastructure change
- Use descriptive branch names: `001-sso-deployment`, `002-monitoring-stack`
- Keep commits atomic and well-described
- Review Terraform plans before applying

## Important Notes

- **State Management**: Terraform state must use remote backend
- **Idempotency**: All operations should be safely repeatable
- **Rollback**: Always document rollback procedures
- **Monitoring**: Include observability in all deployments
- **Documentation**: Update README, runbooks, and architecture docs

## Command Details

### /specops.constitution
Creates or updates the infrastructure constitution. This is the foundation for all infrastructure decisions.

**What it does:**
- Loads constitution template
- Defines technology stack standards
- Establishes security and compliance requirements
- Sets code quality and testing standards
- Documents multi-tenancy approach

**Output:** `.specops/memory/constitution.md`

### /specops.specify
Defines infrastructure requirements without technical details.

**What it does:**
- Creates feature specification
- Documents business context and goals
- Defines functional and non-functional requirements
- Describes infrastructure scenarios
- Specifies multi-tenancy requirements

**Output:** `.specops/specs/NNN-feature-name/spec.md`

### /specops.plan
Creates technical implementation plan with specific technologies.

**What it does:**
- Designs technical architecture
- Specifies Terraform modules and resources
- Defines Ansible roles and playbooks
- Plans ArgoCD applications and sync policies
- Details Cilium network policies
- Creates implementation phases

**Output:** `.specops/specs/NNN-feature-name/plan.md`

### /specops.tasks
Generates actionable task breakdown from the plan.

**What it does:**
- Breaks plan into specific tasks
- Orders tasks with dependencies
- Marks parallel execution opportunities
- Specifies files to create/modify
- Defines validation criteria

**Output:** `.specops/specs/NNN-feature-name/tasks.md`

### /specops.implement
Executes the implementation by running infrastructure automation.

**What it does:**
- Executes Terraform to provision infrastructure
- Runs Ansible playbooks to configure Kubernetes
- Sets up ArgoCD and deploys applications
- Applies network policies and resource quotas
- Validates each phase before proceeding
- Documents any deviations or issues

**Output:** Working infrastructure + Git commits

## Example Usage

```bash
# 1. Establish principles
/specops.constitution Create constitution for multi-tenant Kubernetes platform
using Terraform, Ansible, ArgoCD, and Cilium

# 2. Define requirements
/specops.specify Deploy SSO solution using Zitadel for multiple organizations.
Need namespace isolation, PostgreSQL backend, and LDAP integration.

# 3. Create technical plan
/specops.plan Use Helm for Zitadel deployment. PostgreSQL in same namespace.
Cilium network policies for isolation. Ingress with cert-manager for TLS.

# 4. Generate tasks
/specops.tasks

# 5. Execute implementation
/specops.implement
```

## Validation Checklist

Before marking any phase complete, verify:

### Constitution
- [ ] Technology stack clearly defined
- [ ] Security standards documented
- [ ] Multi-tenancy approach specified
- [ ] Code quality requirements set

### Specification
- [ ] Business goals clear
- [ ] Requirements have acceptance criteria
- [ ] Multi-tenancy needs documented
- [ ] Dependencies identified

### Plan
- [ ] Architecture documented
- [ ] All components specified
- [ ] File structure defined
- [ ] Testing strategy included

### Tasks
- [ ] All tasks have clear actions
- [ ] Dependencies mapped
- [ ] Validation criteria defined
- [ ] Files to create listed

### Implementation
- [ ] All tasks executed
- [ ] Infrastructure deployed successfully
- [ ] Validation passed
- [ ] Documentation updated

---

**Remember**: SpecOps is about systematic, spec-driven infrastructure automation. Take time to plan properly before implementing.
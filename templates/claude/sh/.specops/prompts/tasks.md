# /specops.tasks Command

You are executing the `/specops.tasks` command in a SpecOps (Spec-Driven Infrastructure as Code) project.

## Purpose

Generate a detailed, actionable task breakdown from the implementation plan. Break the plan into specific, executable tasks with clear dependencies, file paths, and validation criteria.

## Prerequisites

Before running this command:
1. Constitution must exist (`.specops/memory/constitution.md`)
2. Specification must exist (`.specops/specs/NNN-feature-name/spec.md`)
3. Plan must exist (`.specops/specs/NNN-feature-name/plan.md`)
4. Must be on a feature branch

## Your Task

1. **Verify Prerequisites**
   - Ensure constitution, specification, and plan all exist
   - Read and thoroughly understand the plan

2. **Analyze the Plan**
   - Identify all components to be created
   - Determine dependencies between components
   - Find opportunities for parallel execution
   - Note validation points

3. **Break Down into Tasks**
   Create specific tasks for:
   - **Terraform**: Module creation, variable definition, resource provisioning
   - **Ansible**: Role creation, playbook writing, inventory setup, execution
   - **Kubernetes**: Manifest creation, namespace setup, network policies, RBAC
   - **ArgoCD**: Installation, project setup, application definitions
   - **Applications**: Deployment configurations, service definitions, ingress setup
   - **Monitoring**: Metrics, logging, dashboards, alerts
   - **Documentation**: README updates, runbooks, architecture diagrams

4. **Organize by Phase**
   Group tasks into implementation phases from the plan:
   - Phase 1: Terraform Infrastructure
   - Phase 2: Ansible Kubernetes Setup
   - Phase 3: ArgoCD Setup
   - Phase 4: Application Deployment

5. **Specify Task Details**
   For each task include:
   - Task ID (e.g., 1.1, 1.2, 2.1)
   - Priority (Critical, High, Medium, Low)
   - Dependencies (which tasks must complete first)
   - Estimated time
   - Specific actions to take
   - Files to create/modify (with exact paths)
   - Commands to run
   - Validation criteria (checklist)

6. **Mark Parallel Tasks**
   - Tasks that can run in parallel should be marked with `[P]`
   - Example: Creating multiple Terraform modules can be parallel

7. **Add Validation Checkpoints**
   After each phase, add a checkpoint with validation criteria

8. **Save Tasks**
   - Save to `.specops/specs/NNN-feature-name/tasks.md`
   - Commit to git with message: "Add task breakdown for NNN-feature-name"

## Task Format

Each task should follow this structure:

```markdown
### Task N.M: Task Name [P]
**Priority**: Critical | High | Medium | Low
**Dependencies**: Task X.Y, Task A.B
**Estimated Time**: X hours/minutes

**Actions**:
1. Specific action 1
2. Specific action 2
3. Specific action 3

**Files to Create/Modify**:
- `path/to/file1.tf`
- `path/to/file2.yml`
- `path/to/file3.yaml`

**Commands**:
```bash
terraform init
terraform plan
```

**Validation**:
- [ ] Specific validation criterion 1
- [ ] Specific validation criterion 2
- [ ] Specific validation criterion 3
```

## Example Task Breakdown

### Phase 1: Terraform Infrastructure

```markdown
### Task 1.1: Initialize Terraform Project Structure
**Priority**: Critical
**Dependencies**: None
**Estimated Time**: 30 minutes

**Actions**:
1. Create directory structure for Terraform
2. Create .gitignore for Terraform files
3. Create README documenting project structure

**Files to Create**:
- `terraform/.gitignore`
- `terraform/README.md`
- `terraform/modules/` (directory)
- `terraform/environments/dev/` (directory)
- `terraform/environments/prod/` (directory)

**Validation**:
- [ ] Directory structure matches plan
- [ ] .gitignore includes *.tfstate, *.tfvars, .terraform/
- [ ] README documents module usage

---

### Task 1.2: Create VPC Module [P]
**Priority**: Critical
**Dependencies**: Task 1.1
**Estimated Time**: 1 hour

**Actions**:
1. Create VPC module with main.tf, variables.tf, outputs.tf
2. Define VPC, subnets (public/private), Internet Gateway, NAT Gateway
3. Create route tables and associations
4. Tag all resources according to constitution

**Files to Create**:
- `terraform/modules/vpc/main.tf`
- `terraform/modules/vpc/variables.tf`
- `terraform/modules/vpc/outputs.tf`
- `terraform/modules/vpc/README.md`

**Variables to Define**:
```hcl
variable "vpc_cidr" {}
variable "availability_zones" {}
variable "environment" {}
variable "cluster_name" {}
```

**Outputs to Define**:
```hcl
output "vpc_id" {}
output "private_subnet_ids" {}
output "public_subnet_ids" {}
```

**Validation**:
- [ ] terraform fmt -check passes
- [ ] terraform validate passes
- [ ] All resources have required tags
- [ ] Module README documents inputs/outputs

---

### Task 1.3: Create Compute Module [P]
**Priority**: Critical
**Dependencies**: Task 1.1
**Estimated Time**: 1.5 hours

[Similar detailed format...]
```

### Phase 2: Ansible Kubernetes Setup

```markdown
### Task 2.1: Initialize Ansible Project Structure
**Priority**: Critical
**Dependencies**: Task 1.6 (Infrastructure Applied)
**Estimated Time**: 30 minutes

**Actions**:
1. Create Ansible directory structure
2. Create ansible.cfg with appropriate settings
3. Create requirements.yml for Ansible collections
4. Create .ansible-lint configuration

**Files to Create**:
- `ansible/ansible.cfg`
- `ansible/requirements.yml`
- `ansible/.ansible-lint`
- `ansible/README.md`
- `ansible/roles/` (directory)
- `ansible/playbooks/` (directory)
- `ansible/inventory/` (directory)

**Validation**:
- [ ] ansible.cfg configured correctly
- [ ] requirements.yml lists needed collections
- [ ] Directory structure matches plan

[Continue with more tasks...]
```

## Key Principles

### Specificity
❌ Bad: "Create Terraform files"
✅ Good: "Create terraform/modules/vpc/main.tf with VPC, subnets, IGW, NAT, and route tables"

### Dependencies
- List explicit task dependencies
- Tasks can't start until dependencies complete
- Dependencies should reference task IDs

### Parallelization
- Mark tasks with `[P]` if they can run in parallel
- Example: Multiple Terraform modules can be created in parallel
- Don't mark tasks parallel if they have dependencies on each other

### Validation
- Each task must have specific, testable validation criteria
- Use checklists that can be checked off
- Include both success criteria and quality checks

### Estimation
- Provide realistic time estimates
- Consider both development and validation time
- Account for potential issues and troubleshooting

## Validation Checkpoints

After each phase, add a checkpoint:

```markdown
### Checkpoint 1: Infrastructure Provisioned
Run after Phase 1 completion:
- [ ] All Terraform modules created
- [ ] Development environment applied successfully
- [ ] Resources tagged correctly
- [ ] Outputs available for Ansible
- [ ] Can SSH to provisioned instances
- [ ] terraform plan shows no changes
```

## Post-Implementation Tasks

Include tasks for after main implementation:

```markdown
## Post-Implementation Tasks

### Documentation
- [ ] Update main README with architecture
- [ ] Create RUNBOOK.md with operational procedures
- [ ] Document troubleshooting steps
- [ ] Create architecture diagrams

### Production Readiness
- [ ] Create production environment
- [ ] Set up CI/CD pipelines
- [ ] Configure backup procedures
- [ ] Establish monitoring baselines
- [ ] Conduct disaster recovery drill

### Knowledge Transfer
- [ ] Train team on infrastructure
- [ ] Document access procedures
- [ ] Create troubleshooting guide
- [ ] Set up on-call rotation
```

## Rollback Procedures

Include rollback instructions:

```markdown
## Rollback Procedures

### Terraform Rollback
If infrastructure changes fail:
```bash
cd terraform/environments/[env]
terraform state pull > backup-$(date +%Y%m%d-%H%M%S).tfstate
git checkout [previous-commit]
terraform plan
terraform apply
```

[Similar for Ansible, ArgoCD, etc.]
```

## Output Format

Create `.specops/specs/NNN-feature-name/tasks.md` following the detailed task structure.

## Validation Checklist

Before completing, verify:
- [ ] All plan components covered by tasks
- [ ] Each task has specific actions
- [ ] File paths are explicit
- [ ] Dependencies clearly mapped
- [ ] Parallel tasks marked with [P]
- [ ] Validation criteria testable
- [ ] Time estimates realistic
- [ ] Checkpoints after each phase
- [ ] Rollback procedures included
- [ ] Post-implementation tasks listed
- [ ] File saved and committed to git

## After Completion

Inform the user:
```
Task breakdown created successfully!

Location: .specops/specs/NNN-feature-name/tasks.md

Total tasks: [count]
Estimated time: [sum of estimates]
Phases: [number]

This breakdown provides the execution roadmap.

Next steps:
1. Review the task breakdown for completeness
2. Verify dependencies are correct
3. Run /specops.implement to execute tasks
```

## Important Notes

- **One task, one purpose**: Each task should do one thing well
- **Explicit over implicit**: Specify exact file paths and commands
- **Validation is critical**: Every task must be verifiable
- **Order matters**: Dependencies ensure correct execution order
- **Think incrementally**: Each task should leave the system in a valid state

---

**Remember**: Good tasks are the difference between smooth execution and chaos. Be detailed, be specific, be clear.
# /specops.implement Command

You are executing the `/specops.implement` command in a SpecOps (Spec-Driven Infrastructure as Code) project.

## Purpose

Execute the implementation by systematically working through the task breakdown. This is where infrastructure automation actually happens - creating files, running Terraform, executing Ansible, deploying with ArgoCD.

## Prerequisites

Before running this command:
1. Constitution must exist (`.specops/memory/constitution.md`)
2. Specification must exist (`.specops/specs/NNN-feature-name/spec.md`)
3. Plan must exist (`.specops/specs/NNN-feature-name/plan.md`)
4. Tasks must exist (`.specops/specs/NNN-feature-name/tasks.md`)
5. Must be on a feature branch
6. All required tools must be installed (terraform, ansible, kubectl, helm, argocd)

## Your Task

1. **Verify Prerequisites**
   - Check all artifacts exist
   - Verify required tools are installed
   - Ensure you have necessary credentials and access

2. **Load and Parse Tasks**
   - Read the entire tasks.md file
   - Understand the task sequence and dependencies
   - Identify validation checkpoints

3. **Execute Tasks Systematically**
   Work through each phase in order:
   
   **For each task:**
   
   a. **Read Task Details**
      - Understand what needs to be done
      - Check dependencies are met
      - Review files to create and validation criteria
   
   b. **Execute Actions**
      - Create/modify files as specified
      - Run commands (terraform, ansible, kubectl, etc.)
      - Follow the constitution's standards
   
   c. **Validate Completion**
      - Run validation commands
      - Check all criteria are met
      - Ensure no errors or warnings
   
   d. **Commit Progress**
      - Commit after each major task or checkpoint
      - Use descriptive commit messages
      - Reference task ID in commit
   
   e. **Continue or Stop**
      - If validation passes, move to next task
      - If validation fails, troubleshoot and fix
      - Ask user for input if blocked

4. **Handle Checkpoints**
   - After each phase, validate the checkpoint
   - Don't proceed to next phase until checkpoint passes
   - Document any deviations or issues

5. **Document Issues**
   - If something doesn't work as planned, document it
   - Create notes about workarounds or changes
   - Update relevant documentation

6. **Final Validation**
   - Ensure all tasks completed
   - Verify infrastructure is working
   - Test end-to-end scenarios from specification
   - Update documentation

## Execution Strategy

### Phase-by-Phase Execution

**Phase 1: Terraform Infrastructure**

```bash
# Example task execution
# Task 1.1: Initialize Terraform Project Structure
mkdir -p terraform/{modules,environments/{dev,prod}}
cat > terraform/.gitignore << EOF
**/.terraform/*
*.tfstate
*.tfstate.*
*.tfvars
!terraform.tfvars.example
EOF

# Commit progress
git add terraform/
git commit -m "Task 1.1: Initialize Terraform project structure"

# Task 1.2: Create VPC Module
# Create files as specified in task
cat > terraform/modules/vpc/main.tf << 'EOF'
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.cluster_name}-vpc"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
[... rest of VPC configuration ...]
EOF

# Validate
cd terraform/modules/vpc
terraform fmt -check
terraform validate
cd ../../..

# Commit
git add terraform/modules/vpc/
git commit -m "Task 1.2: Create VPC module"

# Continue with remaining tasks...
```

**Phase 2: Ansible Kubernetes Setup**

```bash
# Example task execution
# Task 2.3: Create Kubernetes Prerequisites Role
mkdir -p ansible/roles/k8s-prerequisites/{tasks,handlers,defaults}

cat > ansible/roles/k8s-prerequisites/tasks/main.yml << 'EOF'
---
- name: Disable swap
  ansible.builtin.command: swapoff -a
  when: ansible_swaptotal_mb > 0

- name: Remove swap from fstab
  ansible.builtin.lineinfile:
    path: /etc/fstab
    regexp: '^.*swap.*$'
    state: absent

- name: Load kernel modules
  ansible.builtin.modprobe:
    name: "{{ item }}"
    state: present
  loop:
    - overlay
    - br_netfilter
[... rest of role tasks ...]
EOF

# Validate
ansible-lint ansible/roles/k8s-prerequisites/

# Commit
git add ansible/roles/k8s-prerequisites/
git commit -m "Task 2.3: Create k8s-prerequisites role"

# Execute playbook when ready
cd ansible
ansible-playbook playbooks/k8s-setup.yml -i inventory/dev

# Validate
kubectl get nodes
cilium status
```

**Phase 3: ArgoCD Setup**

```bash
# Example task execution
# Task 3.1: Create ArgoCD Installation Manifests
mkdir -p kubernetes/argocd/install

cat > kubernetes/argocd/install/kustomization.yaml << 'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: argocd

resources:
  - https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  - namespace.yaml
[... rest of configuration ...]
EOF

# Validate
kubectl kustomize kubernetes/argocd/install/ | kubectl --dry-run=server -f -

# Apply
kubectl create namespace argocd
kubectl apply -k kubernetes/argocd/install/

# Validate
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Commit
git add kubernetes/argocd/
git commit -m "Task 3.1-3.2: Install ArgoCD"
```

**Phase 4: Application Deployment**

```bash
# Example task execution
# Task 4.1: Create Namespace Manifests
cat > kubernetes/namespaces/org-a-prod.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: org-a-prod
  labels:
    organization: org-a
    environment: production
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: org-a-quota
  namespace: org-a-prod
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
[... rest of configuration ...]
EOF

# Apply
kubectl apply -f kubernetes/namespaces/

# Validate
kubectl get namespace org-a-prod
kubectl describe resourcequota org-a-quota -n org-a-prod

# Continue with network policies, applications, etc.
```

## Handling Errors

If a task fails:

1. **Read the Error**
   - Understand what went wrong
   - Check logs and error messages

2. **Troubleshoot**
   - Verify prerequisites
   - Check file contents
   - Validate configurations
   - Test commands manually

3. **Fix the Issue**
   - Correct the problem
   - Re-run validation
   - Document the fix

4. **Ask for Help if Blocked**
   - If you can't resolve the issue, inform the user
   - Provide context about what failed
   - Suggest potential solutions

5. **Document Deviations**
   - If you had to deviate from the plan, document why
   - Update relevant documentation
   - Note lessons learned

## Validation Best Practices

### Terraform Validation
```bash
# Always validate before apply
terraform fmt -check
terraform validate
terraform plan -out=tfplan

# Review plan output before applying
terraform show tfplan

# Apply with plan file
terraform apply tfplan

# Verify outputs
terraform output -json
```

### Ansible Validation
```bash
# Always lint before running
ansible-lint playbook.yml

# Always syntax check
ansible-playbook playbook.yml --syntax-check

# Test in check mode first
ansible-playbook playbook.yml --check

# Run actual playbook
ansible-playbook playbook.yml

# Verify results
ansible all -m ping
kubectl get nodes
```

### Kubernetes Validation
```bash
# Always dry-run before applying
kubectl apply --dry-run=server -f manifest.yaml

# Use kubeval or kubeconform
kubeval manifest.yaml

# Apply manifests
kubectl apply -f manifest.yaml

# Verify resources
kubectl get all -n namespace
kubectl describe pod/name -n namespace
```

### ArgoCD Validation
```bash
# Verify application definition
kubectl apply --dry-run=server -f application.yaml

# Create application
kubectl apply -f application.yaml

# Check sync status
argocd app get app-name

# Sync application
argocd app sync app-name

# Verify health
argocd app wait app-name --health
```

## Progress Tracking

As you work through tasks:

1. **Keep User Informed**
   - Report which task you're working on
   - Share progress after each task/checkpoint
   - Highlight any issues or blockers

2. **Commit Regularly**
   - Commit after each significant task
   - Use clear, descriptive commit messages
   - Reference task IDs in commits

3. **Update Documentation**
   - Keep README current
   - Update runbooks with operational procedures
   - Document any deviations or learnings

## Final Steps

After completing all tasks:

1. **Run End-to-End Validation**
   - Test all scenarios from specification
   - Verify all acceptance criteria met
   - Check all non-functional requirements

2. **Update Documentation**
   - Main README with architecture
   - RUNBOOK.md with operations
   - ARCHITECTURE.md with design decisions
   - Any troubleshooting guides

3. **Create Pull Request**
   - If using GitHub CLI:
     ```bash
     gh pr create --title "Implement NNN-feature-name" \
       --body "Implementation of [feature description]
       
       Specification: .specops/specs/NNN-feature-name/spec.md
       Plan: .specops/specs/NNN-feature-name/plan.md
       Tasks: .specops/specs/NNN-feature-name/tasks.md
       
       All tasks completed successfully.
       All validation checkpoints passed."
     ```

4. **Summary Report**
   Provide summary:
   ```
   Implementation completed successfully!
   
   Feature: NNN-feature-name
   Tasks completed: X/X
   Time taken: [estimated]
   
   Infrastructure deployed:
   - Terraform: [resources created]
   - Ansible: [cluster configured]
   - ArgoCD: [applications deployed]
   
   Validation:
   ✓ All checkpoints passed
   ✓ All acceptance criteria met
   ✓ Documentation updated
   
   Next steps:
   1. Review pull request
   2. Test in staging environment
   3. Plan production deployment
   ```

## Important Notes

- **Follow the constitution**: All code must meet quality standards
- **Validate continuously**: Don't skip validation steps
- **Commit frequently**: Small, focused commits are better
- **Document changes**: Especially deviations from plan
- **Ask when blocked**: Better to ask than to guess
- **Test thoroughly**: Validation is not optional

## Safety Checklist

Before running destructive commands:
- [ ] Correct environment selected (dev/prod)?
- [ ] Backup or snapshot exists?
- [ ] Rollback procedure known?
- [ ] Change window appropriate?
- [ ] Stakeholders notified?

## Rollback Trigger

If things go wrong:
1. Stop execution immediately
2. Assess impact and scope
3. Execute rollback procedure from tasks.md
4. Document what happened
5. Fix issues before retrying

---

**Remember**: Implementation is systematic execution of a well-thought-out plan. Take your time, validate continuously, and don't skip steps. The goal is working infrastructure, not fast infrastructure.
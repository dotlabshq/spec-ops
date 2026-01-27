---
description: Execute infrastructure deployment by processing and executing all tasks with validation checkpoints
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").


2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```   

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. Setup Verification

  Detect and create/verify ignore files:
  - `.gitignore` (if git repo)
  - `.terraformignore` (if *.tf files)
  - `.dockerignore` (if Dockerfile)
  - `.helmignore` (if Helm charts)

  **Infrastructure patterns**:
  ```
  .terraform/
  *.tfstate*
  *.tfvars
  .kube/
  *.secret.yaml
  secrets/
  *.key
  *.pem
  .env*
  ```

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

7. Implementation execution rules:
   - **Prerequisites first**: Verify credentials, tools, state backend configuration
   - **Validation before deployment**: Define success criteria and validation commands for each phase
   - **Infrastructure provisioning**: Deploy cloud resources (network, compute, storage)
   - **Platform configuration**: Install and configure container orchestration platform
   - **Application platform**: Setup deployment pipeline (GitOps, CI/CD)
   - **Validation and monitoring**: Verify deployment health, configure observability stack

   **Deployment Strategy**: Follow `/memory/constitution.md` for:
   - Helm chart discovery sources and decision matrix
   - ArgoCD Application patterns (Helm-based and Kustomize-based)
   - Kustomize structure for custom applications
   - Standard infrastructure components and their Helm sources

8. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the task

9. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

  **Rollback Procedures**

  Phase-specific rollback:
  - Phase 2: `terraform destroy`
  - Phase 3: Re-provision instances
  - Phase 4: `kubectl delete -k kubernetes/argocd/install/`
  - Phase 5: `kubectl delete -f kubernetes/namespaces/`
  - Phase 6: `argocd app delete [app]`

  Complete rollback: Reverse order 7→6→5→4→3→2→1

  **Validation Checkpoints**

  | Phase | Validation |
  |-------|-----------|
  | 1 | Tools available, credentials work |
  | 2 | terraform plan passes |
  | 2.5 | ArgoCD installed, Helm repos configured |
  | 3 | All nodes Ready, network(Cilium) healthy |
  | 4 | Infrastructure apps synced (ingress, cert-manager) |
  | 5 | Network isolation verified |
  | 6 | Apps running, accessible via ingress |
  | 7 | Metrics flowing, dashboards configured |

  STOP if any validation fails. Suggest rollback or fix.

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.

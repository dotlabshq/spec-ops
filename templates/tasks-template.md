---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Validation**: The examples below include validation tasks. Validation tasks are OPTIONAL - only include them if explicitly requested in the infrastructure specification.

**Organization**: Tasks are grouped by infrastructure scenario to enable independent deployment and validation of each scenario.

## Format: `[ID] [P?] [Scenario] Description`

- **[P]**: Can run in parallel (different resources, no dependencies)
- **[Scenario]**: Which infrastructure scenario this task belongs to (e.g., IS1, IS2, IS3)
- Include exact file paths in descriptions (IaC modules, manifests, configs)

## Path Conventions

- **Single IaC tool**: `terraform/`, `validation/` at repository root
- **Multi-tool**: `terraform/`, `k8s/`, `argocd/`
- **Multi-tenant**: `terraform/shared/`, `terraform/tenants/`, `k8s/tenants/`
- Paths shown below assume single IaC tool - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /specops.tasks command MUST replace these with actual tasks based on:
  - Infrastructure scenarios from spec.md (with their priorities P1, P2, P3...)
  - Infrastructure requirements from plan.md
  - Resource definitions from data-model.md
  - Service interfaces from contracts/
  
  Tasks MUST be organized by infrastructure scenario so each scenario can be:
  - Deployed independently
  - Validated independently
  - Rolled back as an independent increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Prerequisites & Provider Configuration)

**Purpose**: Provider configuration, state backend, and credentials setup

- [ ] T001 Configure cloud provider credentials and authentication
- [ ] T002 Initialize state backend (S3+DynamoDB, Azure Blob, GCS, etc.)
- [ ] T003 [P] Setup IaC project structure per implementation plan

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY infrastructure scenario can be deployed

**⚠️ CRITICAL**: No scenario work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create VPC/networking module in terraform/modules/vpc/
- [ ] T005 [P] Configure IAM roles and policies in terraform/modules/iam/
- [ ] T006 [P] Setup security groups and network ACLs
- [ ] T007 Create base resource modules that all scenarios depend on
- [ ] T008 Configure logging and monitoring infrastructure
- [ ] T009 Setup secrets management integration (Vault, Secrets Manager, etc.)

**Checkpoint**: Foundation ready - infrastructure scenario deployment can now begin in parallel

---

## Phase 3: Infrastructure Scenario 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Scenario 1 (OPTIONAL - only if validation requested) ⚠️

> **NOTE: Write these validation tests FIRST, ensure infrastructure doesn't pass before deployment**

- [ ] T010 [P] [IS1] Pre-deploy validation script in validation/pre-deploy/[name].sh
- [ ] T011 [P] [IS1] Post-deploy validation script in validation/post-deploy/[name].sh

### Provisioning for Scenario 1

- [ ] T012 [P] [IS1] Create [Resource1] module in terraform/modules/[resource1]/
- [ ] T013 [P] [IS1] Create [Resource2] module in terraform/modules/[resource2]/
- [ ] T014 [IS1] Configure [Resource] dependencies in terraform/environments/[env]/main.tf
- [ ] T015 [IS1] Apply [resource/configuration] in terraform/environments/[env]/
- [ ] T016 [IS1] Configure outputs and variables for scenario 1
- [ ] T017 [IS1] Document rollback procedure for scenario 1

**Checkpoint**: At this point, Infrastructure Scenario 1 should be fully deployed and validated independently

---

## Phase 4: Infrastructure Scenario 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Scenario 2 (OPTIONAL - only if validation requested) ⚠️

- [ ] T018 [P] [IS2] Pre-deploy validation script in validation/pre-deploy/[name].sh
- [ ] T019 [P] [IS2] Post-deploy validation script in validation/post-deploy/[name].sh

### Provisioning for Scenario 2

- [ ] T020 [P] [IS2] Create [Resource] module in terraform/modules/[resource]/
- [ ] T021 [IS2] Configure [Resource] in terraform/environments/[env]/
- [ ] T022 [IS2] Apply [resource/configuration] for scenario 2
- [ ] T023 [IS2] Integrate with Scenario 1 infrastructure (if needed)

**Checkpoint**: At this point, Scenarios 1 AND 2 should both work independently

---

## Phase 5: Infrastructure Scenario 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Scenario 3 (OPTIONAL - only if validation requested) ⚠️

- [ ] T024 [P] [IS3] Pre-deploy validation script in validation/pre-deploy/[name].sh
- [ ] T025 [P] [IS3] Post-deploy validation script in validation/post-deploy/[name].sh

### Provisioning for Scenario 3

- [ ] T026 [P] [IS3] Create [Resource] module in terraform/modules/[resource]/
- [ ] T027 [IS3] Configure [Resource] in terraform/environments/[env]/
- [ ] T028 [IS3] Apply [resource/configuration] for scenario 3

**Checkpoint**: All infrastructure scenarios should now be independently deployable and validated

---

[Add more infrastructure scenario phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple infrastructure scenarios

- [ ] TXXX [P] Documentation updates in docs/ (runbooks, architecture diagrams)
- [ ] TXXX Infrastructure code cleanup and refactoring
- [ ] TXXX Performance optimization across all scenarios
- [ ] TXXX [P] Additional validation tests (if requested) in validation/
- [ ] TXXX Security hardening and compliance checks
- [ ] TXXX Configure alerting and monitoring dashboards
- [ ] TXXX Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all infrastructure scenarios
- **Infrastructure Scenarios (Phase 3+)**: All depend on Foundational phase completion
  - Scenarios can then proceed in parallel (if resources allow)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired scenarios being complete

### Infrastructure Scenario Dependencies

- **Scenario 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other scenarios
- **Scenario 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with IS1 but should be independently deployable
- **Scenario 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with IS1/IS2 but should be independently deployable

### Within Each Infrastructure Scenario

- Validation scripts (if included) MUST be written before deployment
- Modules before environment configurations
- Dependencies before dependent resources
- Core provisioning before integration
- Scenario complete and validated before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all scenarios can start in parallel (if team capacity allows)
- All validation tasks for a scenario marked [P] can run in parallel
- Modules within a scenario marked [P] can run in parallel
- Different scenarios can be worked on in parallel by different team members

---

## Parallel Example: Infrastructure Scenario 1

```bash
# Launch all validation scripts for Scenario 1 together (if validation requested):
Task: "Pre-deploy validation script in validation/pre-deploy/[name].sh"
Task: "Post-deploy validation script in validation/post-deploy/[name].sh"

# Launch all modules for Scenario 1 together:
Task: "Create [Resource1] module in terraform/modules/[resource1]/"
Task: "Create [Resource2] module in terraform/modules/[resource2]/"
```

---

## Implementation Strategy

### MVP First (Infrastructure Scenario 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all scenarios)
3. Complete Phase 3: Infrastructure Scenario 1
4. **STOP and VALIDATE**: Validate Scenario 1 independently
5. Deploy to staging/production if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add Scenario 1 → Validate independently → Deploy (MVP!)
3. Add Scenario 2 → Validate independently → Deploy
4. Add Scenario 3 → Validate independently → Deploy
5. Each scenario adds value without breaking previous deployments

### Parallel Team Strategy

With multiple engineers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Engineer A: Infrastructure Scenario 1
   - Engineer B: Infrastructure Scenario 2
   - Engineer C: Infrastructure Scenario 3
3. Scenarios complete and integrate independently

---

## Notes

- [P] tasks = different resources, no dependencies
- [Scenario] label maps task to specific infrastructure scenario for traceability
- Each infrastructure scenario should be independently deployable and validated
- Verify validation scripts are ready before deploying
- Commit after each task or logical group
- Stop at any checkpoint to validate scenario independently
- Document rollback procedures for each scenario
- Avoid: vague tasks, same resource conflicts, cross-scenario dependencies that break independence
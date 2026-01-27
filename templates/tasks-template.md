---
description: "Infrastructure deployment task list template"
---

# Infrastructure Tasks: [INFRASTRUCTURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for infrastructure scenarios), research.md, architecture.md

**Validation**: All infrastructure tasks include mandatory validation checkpoints. Each phase must pass validation before proceeding.

**Organization**: Tasks are grouped by infrastructure deployment phases to enable sequential deployment with validation gates.

## Format: `[ID] [P?] [Scenario] Description`

- **[P]**: Can run in parallel (different resources, no dependencies)
- **[Scenario]**: Which infrastructure scenario this task belongs to (e.g., IS1, IS2, IS3 from spec.md)
- Include exact file paths or commands in descriptions

## Path Conventions

Technology-agnostic - adjust based on your chosen tools from plan.md:
- **Infrastructure Code**: May use Terraform, Pulumi, CloudFormation, Bicep, CDK
- **Configuration**: May use Ansible, Chef, Puppet, SaltStack, scripts
- **Platform**: May use Kubernetes, OpenShift, Nomad, ECS, Docker Swarm
- **Deployment**: May use ArgoCD, Flux, Helm, Jenkins, GitLab CI
- Paths shown below are examples - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /specops.tasks command MUST replace these with actual tasks based on:
  - Infrastructure scenarios from spec.md (with their priorities P1, P2, P3...)
  - Technology stack from plan.md
  - Components from architecture.md
  - Requirements from spec.md
  
  Tasks MUST be organized by infrastructure scenario so each scenario can be:
  - Deployed independently
  - Validated independently
  - Rolled back if needed
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Prerequisites & Setup (Shared Infrastructure)

**Purpose**: Environment preparation and tool verification

- [ ] T001 Verify access credentials (cloud provider or on-premise)
- [ ] T002 Create remote state storage for infrastructure code
- [ ] T003 [P] Initialize version control repository structure
- [ ] T004 [P] Verify required tools installed (check versions)
- [ ] T005 [P] Configure authentication mechanisms (SSH keys, tokens, certificates)

**Checkpoint**: ✓ Environment ready for infrastructure deployment

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY scenario can be implemented

**⚠️ CRITICAL**: No infrastructure scenario work can begin until this phase is complete

Examples of foundational tasks (adjust based on your infrastructure):

- [ ] T006 Create network infrastructure (virtual network, subnets, routing)
- [ ] T007 [P] Configure security perimeter (firewalls, security groups, network ACLs)
- [ ] T008 [P] Provision compute resources (virtual machines, instances, nodes)
- [ ] T009 Configure DNS and service discovery
- [ ] T010 Setup shared storage or persistent volumes
- [ ] T011 Configure logging and audit infrastructure

**Checkpoint**: Foundation ready - infrastructure scenarios can now be deployed

---

## Phase 3: Infrastructure Scenario 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Infrastructure Scenario 1 ⚠️

> **NOTE: Define validation criteria BEFORE deployment**

- [ ] T012 [P] [IS1] Define success criteria for [infrastructure component]
- [ ] T013 [P] [IS1] Create validation tests for [infrastructure capability]

### Implementation for Infrastructure Scenario 1

- [ ] T014 [P] [IS1] Create [component A] configuration in [path/to/config-a]
- [ ] T015 [P] [IS1] Create [component B] configuration in [path/to/config-b]
- [ ] T016 [IS1] Deploy [component A] (depends on T014)
- [ ] T017 [IS1] Deploy [component B] (depends on T015)
- [ ] T018 [IS1] Configure [integration/networking] between components
- [ ] T019 [IS1] Apply [security policies/access controls]
- [ ] T020 [IS1] Validate deployment meets acceptance criteria

**Checkpoint**: At this point, Infrastructure Scenario 1 should be fully functional and independently testable

---

## Phase 4: Infrastructure Scenario 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Infrastructure Scenario 2 ⚠️

- [ ] T021 [P] [IS2] Define success criteria for [infrastructure component]
- [ ] T022 [P] [IS2] Create validation tests for [infrastructure capability]

### Implementation for Infrastructure Scenario 2

- [ ] T023 [P] [IS2] Create [component] configuration in [path/to/config]
- [ ] T024 [IS2] Deploy [component]
- [ ] T025 [IS2] Configure [integration] with Scenario 1 (if needed)
- [ ] T026 [IS2] Apply [policies/controls]
- [ ] T027 [IS2] Validate deployment meets acceptance criteria

**Checkpoint**: At this point, Infrastructure Scenarios 1 AND 2 should both work independently

---

## Phase 5: Infrastructure Scenario 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this scenario delivers]

**Independent Validation**: [How to verify this scenario works on its own]

### Validation for Infrastructure Scenario 3 ⚠️

- [ ] T028 [P] [IS3] Define success criteria for [infrastructure component]
- [ ] T029 [P] [IS3] Create validation tests for [infrastructure capability]

### Implementation for Infrastructure Scenario 3

- [ ] T030 [P] [IS3] Create [component] configuration in [path/to/config]
- [ ] T031 [IS3] Deploy [component]
- [ ] T032 [IS3] Configure [integration]
- [ ] T033 [IS3] Apply [policies/controls]
- [ ] T034 [IS3] Validate deployment meets acceptance criteria

**Checkpoint**: All infrastructure scenarios should now be independently functional

---

[Add more infrastructure scenario phases as needed, following the same pattern]

---

## Phase N: Monitoring & Cross-Cutting Concerns

**Purpose**: Observability and improvements that affect multiple scenarios

- [ ] TXXX [P] Deploy monitoring and alerting infrastructure
- [ ] TXXX [P] Configure dashboards for infrastructure visibility
- [ ] TXXX Update operational documentation in docs/
- [ ] TXXX Infrastructure optimization and cost review
- [ ] TXXX Security hardening and compliance verification
- [ ] TXXX Backup and disaster recovery testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Prerequisites (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Prerequisites completion - BLOCKS all scenarios
- **Infrastructure Scenarios (Phase 3+)**: All depend on Foundational phase completion
  - Scenarios can then proceed in parallel (if resources allow)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Monitoring (Final Phase)**: Depends on all desired scenarios being deployed

### Infrastructure Scenario Dependencies

- **Scenario 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other scenarios
- **Scenario 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with IS1 but should be independently testable
- **Scenario 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with IS1/IS2 but should be independently testable

### Within Each Scenario

- Validation criteria defined BEFORE deployment
- Configuration before deployment
- Core deployment before integration
- Security/policies before validation
- Scenario complete and validated before moving to next priority

### Parallel Opportunities

- All Prerequisites tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all scenarios can start in parallel (if resources allow)
- All validation tests for a scenario marked [P] can run in parallel
- Configuration files within a scenario marked [P] can be created in parallel
- Different scenarios can be worked on in parallel by different team members

---

## Parallel Example: Infrastructure Scenario 1

```bash
# Define all validation criteria together:
Task: "Define success criteria for network configuration"
Task: "Create validation tests for compute resources"

# Create all configurations together:
Task: "Create network config in infrastructure/network/main.tf"
Task: "Create compute config in infrastructure/compute/main.tf"
```

---

## Implementation Strategy

### MVP First (Infrastructure Scenario 1 Only)

1. Complete Phase 1: Prerequisites
2. Complete Phase 2: Foundational (CRITICAL - blocks all scenarios)
3. Complete Phase 3: Infrastructure Scenario 1
4. **STOP and VALIDATE**: Test Scenario 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Prerequisites + Foundational → Foundation ready
2. Add Infrastructure Scenario 1 → Validate independently → Deploy (MVP!)
3. Add Infrastructure Scenario 2 → Validate independently → Deploy
4. Add Infrastructure Scenario 3 → Validate independently → Deploy
5. Each scenario adds capability without breaking previous scenarios

### Parallel Team Strategy

With multiple team members:

1. Team completes Prerequisites + Foundational together
2. Once Foundational is done:
   - Team Member A: Infrastructure Scenario 1
   - Team Member B: Infrastructure Scenario 2
   - Team Member C: Infrastructure Scenario 3
3. Scenarios deployed and validated independently

---

## Rollback Procedures

Document rollback steps per scenario to enable safe recovery:

### Infrastructure Scenario 1 Rollback
```
[Tool-specific rollback commands]
Example: terraform destroy -target=module.scenario1
```

### Infrastructure Scenario 2 Rollback
```
[Tool-specific rollback commands]
```

### Complete Infrastructure Rollback
```
[Commands to tear down entire infrastructure in reverse order]
Phase N → Phase 5 → Phase 4 → Phase 3 → Phase 2
```

---

## Notes

- [P] tasks = different resources/files, no dependencies, safe to parallelize
- [Scenario] label (IS1, IS2, IS3) maps task to specific infrastructure scenario for traceability
- Each scenario should be independently deployable and testable
- Validation criteria must be defined before deployment
- Commit after each task or logical group
- Stop at any checkpoint to validate scenario independently
- Document all validation commands in plan.md
- Avoid: vague tasks, resource conflicts, cross-scenario dependencies that break independence
---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
handoffs: 
  - label: Analyze For Consistency
    agent: specops.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: specops.implement
    prompt: Start the implementation in phases
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (IaC tools, cloud provider, structure), spec.md (infrastructure scenarios with priorities)
   - **Optional**: data-model.md (resource definitions), contracts/ (API/service endpoints), research.md (architectural decisions), quickstart.md (validation scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract IaC tools, cloud provider, project structure
   - Load spec.md and extract infrastructure scenarios with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract resource definitions and map to infrastructure scenarios
   - If contracts/ exists: Map service endpoints to infrastructure scenarios
   - If research.md exists: Extract architectural decisions for setup tasks
   - Generate tasks organized by infrastructure scenario (see Task Generation Rules below)
   - Generate dependency graph showing scenario completion order
   - Create parallel execution examples per infrastructure scenario
   - Validate task completeness (each scenario has all needed tasks, independently deployable and testable)

4. **Generate tasks.md**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct infrastructure feature name from plan.md
   - Phase 1: Setup tasks (prerequisites, credentials, provider configuration)
   - Phase 2: Foundational tasks (blocking prerequisites for all infrastructure scenarios)
   - Phase 3+: One phase per infrastructure scenario (in priority order from spec.md)
   - Each phase includes: scenario goal, independent validation criteria, verification tasks, provisioning/configuration tasks
   - Final Phase: Polish & cross-cutting concerns (monitoring, alerting, documentation)
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task (IaC modules, manifests, configurations)
   - Dependencies section showing scenario completion order
   - Parallel execution examples per scenario
   - Implementation strategy section (MVP infrastructure first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per infrastructure scenario
   - Parallel opportunities identified
   - Independent validation criteria for each scenario
   - Suggested MVP scope (typically just Infrastructure Scenario 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: {ARGS}

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by infrastructure scenario to enable independent deployment and validation.

**Validation tasks are OPTIONAL**: Only generate validation/verification tasks if explicitly requested in the infrastructure specification or if user requests validation-driven approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Scenario?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different resources, no dependencies on incomplete tasks)
4. **[Scenario] label**: REQUIRED for infrastructure scenario phase tasks only
   - Format: [IS1], [IS2], [IS3], etc. (maps to infrastructure scenarios from spec.md)
   - Setup phase: NO scenario label
   - Foundational phase: NO scenario label  
   - Infrastructure Scenario phases: MUST have scenario label
   - Polish phase: NO scenario label
5. **Description**: Clear action with exact file path (IaC module, manifest, config file)

**Examples**:

- ✅ CORRECT: `- [ ] T001 Configure cloud provider credentials in terraform/providers.tf`
- ✅ CORRECT: `- [ ] T005 [P] Create VPC module in terraform/modules/vpc/main.tf`
- ✅ CORRECT: `- [ ] T012 [P] [IS1] Define namespace manifests in k8s/namespaces/tenant-a.yaml`
- ✅ CORRECT: `- [ ] T014 [IS1] Configure network policies in k8s/policies/tenant-isolation.yaml`
- ❌ WRONG: `- [ ] Create VPC module` (missing ID and Scenario label)
- ❌ WRONG: `T001 [IS1] Create namespace` (missing checkbox)
- ❌ WRONG: `- [ ] [IS1] Create namespace manifest` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [IS1] Create namespace` (missing file path)

### Task Organization

1. **From Infrastructure Scenarios (spec.md)** - PRIMARY ORGANIZATION:
   - Each infrastructure scenario (P1, P2, P3...) gets its own phase
   - Map all related components to their scenario:
     - IaC modules needed for that scenario
     - Configurations needed for that scenario
     - Deployments/resources needed for that scenario
     - If validation requested: Validation tasks specific to that scenario
   - Mark scenario dependencies (most scenarios should be independent)

2. **From Contracts/Service Definitions**:
   - Map each service endpoint → to the infrastructure scenario it serves
   - If validation requested: Each contract → validation task [P] before provisioning in that scenario's phase

3. **From Resource Definitions**:
   - Map each resource to the infrastructure scenario(s) that need it
   - If resource serves multiple scenarios: Put in earliest scenario or Setup phase
   - Dependencies → configuration tasks in appropriate scenario phase

4. **From Setup/Prerequisites**:
   - Shared infrastructure (provider config, state backend) → Setup phase (Phase 1)
   - Foundational/blocking tasks (VPC, networking) → Foundational phase (Phase 2)
   - Scenario-specific setup → within that scenario's phase

### Phase Structure

- **Phase 1**: Setup (provider configuration, state backend, credentials)
- **Phase 2**: Foundational (blocking prerequisites - VPC, networking, IAM - MUST complete before infrastructure scenarios)
- **Phase 3+**: Infrastructure Scenarios in priority order (P1, P2, P3...)
  - Within each scenario: Validation (if requested) → Modules → Resources → Configurations → Integration
  - Each phase should be a complete, independently deployable and rollback-ready increment
- **Final Phase**: Polish & Cross-Cutting Concerns (monitoring, alerting, documentation, runbooks)
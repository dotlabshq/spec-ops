---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: specops.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: specops.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Architecture

**Prerequisites:** `research.md` complete (if exists)

1. **Extract infrastructure components from spec** → `architecture.md`:
   - Component names (VPC, cluster, storage, etc.)
   - Resource specifications (CPU, memory, disk)
   - Dependencies and relationships
   - Network topology and connectivity
   - State management (Terraform state, etcd, etc.)

2. **Generate infrastructure manifests** from functional requirements:
   - For each infrastructure scenario → configuration files
   - Use IaC tool patterns (Terraform modules, Helm charts, etc.)
   - Output structure to `/infrastructure/` or `/kubernetes/`
   - Define validation criteria per component

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - Scripts detect which AI agent is in use
   - Update agent-specific context file
   - Add technology stack from current plan
   - Preserve manual additions between markers

**Output**: architecture.md, /infrastructure/* or /kubernetes/*, runbook.md, agent-specific file

## Key Rules

- Use absolute paths from repo root
- ERROR on constitution violations (unless JUSTIFIED)
- Resolve all [NEEDS CLARIFICATION] markers
- Provide real config examples, not placeholders
- Focus on infrastructure (resources, namespaces, policies)
- Include rollback procedures for each component
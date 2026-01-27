---
description: Create or update the infrastructure specification from a natural language feature description.
handoffs: 
  - label: Build Technical Plan
    agent: specops.plan
    prompt: Create technical implementation plan for the spec. I am deploying with...
  - label: Clarify Infrastructure Requirements
    agent: specops.clarify
    prompt: Clarify infrastructure requirements and multi-tenancy details
    send: true
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/specops.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., `deploy-[component]`, `setup-[service]`, `configure-[feature]`)
   - Preserve technical terms and acronyms (SSO, monitoring, ArgoCD, Cilium, K8s, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - Examples:
      - "Deploy single sign-on solution" → "sso-deployment"
      - "Set up monitoring with Prometheus and Grafana" → "monitoring-stack"
      - "Configure multi-tenant namespaces with Cilium" → "multi-tenant-networking"
      - "Add backup solution for PostgreSQL" → "postgres-backup"

2. **Check for existing branches before creating new one**:

   a. First, fetch all remote branches to ensure we have the latest information:

      ```bash
      git fetch --all --prune
      ```

   b. Find the highest feature number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`

   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number

   d. Run the script `{SCRIPT}` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `{SCRIPT} --json --number 5 --short-name "user-auth" "Add user authentication"`
      - PowerShell example: `{SCRIPT} -Json -Number 5 -ShortName "user-auth" "Add user authentication"`

   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, specs directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per feature
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `templates/spec-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: infrastructure components, deployment targets, organizations/tenants, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts infrastructure scope or multi-tenancy model
         - Multiple reasonable interpretations exist with different cost/security implications
         - No reasonable default exists (e.g., cloud provider, compliance requirements)
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: multi-tenancy scope > compliance > performance targets > technical preferences
    4. Fill Infrastructure Scenarios & Validation section
       Each scenario must be independently deployable and testable
       If no clear deployment flow: ERROR "Cannot determine infrastructure scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable and technology-agnostic where possible
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (RTO, RPO, uptime, provisioning time) and operational measures (cluster health, resource utilization)
       Each criterion must be verifiable without implementation details
    7. Identify Key Infrastructure Components (if resources involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]
      
      **Purpose**: Validate infrastructure specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]
      
      ## Content Quality
      
      - [ ] No premature tool/vendor lock-in (tool-agnostic where possible)
      - [ ] Focused on infrastructure outcomes and operational needs
      - [ ] Written for platform/DevOps teams and stakeholders
      - [ ] All mandatory sections completed
      
      ## Requirement Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable (RTO, RPO, uptime, provisioning time)
      - [ ] Success criteria are technology-agnostic (no specific tool versions)
      - [ ] All infrastructure scenarios are defined with acceptance criteria
      - [ ] Edge cases and failure modes are identified
      - [ ] Scope is clearly bounded (what's in/out of this deployment)
      - [ ] Dependencies and assumptions identified (existing infra, credentials, access)
      
      ## Feature Readiness
      
      - [ ] All functional requirements have clear acceptance criteria
      - [ ] Infrastructure scenarios cover primary deployment flows
      - [ ] Multi-tenancy requirements clearly defined (if applicable)
      - [ ] Rollback procedures considered for each scenario
      - [ ] No implementation details leak into specification
      
      ## Notes
      
      - Items marked incomplete require spec updates before `/specops.clarify` or `/specops.plan`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant spec section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |
           
           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/specops.clarify` or `/specops.plan`).

**NOTE:** The script creates and checks out the new branch and initializes the spec file before writing.

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** infrastructure should exist and **WHY** (business/operational needs).
- Avoid HOW to implement (no specific IaC tool syntax, vendor-specific configurations).
- Written for platform teams and DevOps stakeholders, not just developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact infrastructure scope or multi-tenancy model
   - Have multiple reasonable interpretations with different cost/security implications
   - Lack any reasonable default (e.g., cloud provider, compliance requirements)
4. **Prioritize clarifications**: multi-tenancy scope > compliance > performance targets > technical preferences
5. **Think like an SRE**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Infrastructure scope and boundaries (include/exclude specific components)
   - Organization/tenant list and access requirements (if multiple conflicting interpretations possible)
   - Compliance requirements (when legally/financially significant - HIPAA, SOC2, PCI-DSS)

**Examples of reasonable defaults** (don't ask about these):

- Namespace naming: `{org-name}-{environment}` pattern
- Network policies: Default deny-all with explicit allows
- Resource quotas: Based on organization size (small/medium/large tiers)
- Backup retention: 30 days hot, 90 days cold, 1 year archive
- RTO/RPO: Standard for application tier (critical/standard/low-priority)
- Monitoring: Prometheus/Grafana stack unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (RTO, RPO, uptime percentage, provisioning time)
2. **Technology-agnostic**: No mention of specific IaC tools, vendor versions, or proprietary configurations
3. **Operations-focused**: Describe outcomes from platform/DevOps perspective, not implementation internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Infrastructure provisioning completes in under 15 minutes"
- "Cluster handles 1000 pods without performance degradation"
- "All nodes reach Ready state within 5 minutes of provisioning"
- "RTO under 4 hours, RPO under 1 hour for critical workloads"
- "99.9% uptime SLA maintained across all tenant namespaces"
- "Tenant isolation prevents cross-namespace network traffic"

**Bad examples** (implementation-focused):

- "Terraform apply completes in under 10 minutes" (tool-specific, use "Infrastructure provisioning completes...")
- "ArgoCD sync interval is 3 minutes" (tool-specific, use "Configuration changes reflect within...")
- "Cilium network policies are applied" (tool-specific, use "Network isolation is enforced")
- "Prometheus scrape interval is 15 seconds" (tool-specific, use "Metrics are available within...")
---
description: Create or update the infrastructure constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: specops.specify
    prompt: Implement the infrastructure specification based on the updated constitution. I want to deploy...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[CLOUD_PROVIDER]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. **Load the existing constitution template** at `/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template structure. You will update the doc accordingly.

2. **Collect/derive values for placeholders**:
   
   **Infrastructure-specific placeholders:**
   - `[PROJECT_NAME]` - The infrastructure project name
   - `[CLOUD_PROVIDER]` - Primary cloud provider (AWS, Azure, GCP, On-Premise, Multi-Cloud)
   - `[TERRAFORM_VERSION]` - Target Terraform version (e.g., 1.6.x)
   - `[ANSIBLE_VERSION]` - Target Ansible version (e.g., 2.15.x)
   - `[KUBERNETES_VERSION]` - Target Kubernetes version (e.g., 1.28.x)
   - `[CILIUM_VERSION]` - Target Cilium CNI version (e.g., 1.14.x)
   - `[ARGOCD_VERSION]` - Target ArgoCD version (e.g., 2.9.x)
   - `[MULTI_TENANCY_STRATEGY]` - Namespace-based, Cluster-based, or Hybrid
   - `[NETWORK_POLICY_APPROACH]` - Cilium L3/L4, Cilium L7, or Kubernetes NetworkPolicy
   
   **Governance placeholders:**
   - `[RATIFICATION_DATE]` - Original adoption date (ISO format YYYY-MM-DD). If unknown, ask user or mark `TODO(RATIFICATION_DATE)`.
   - `[LAST_AMENDED_DATE]` - Today's date if changes are made (ISO format YYYY-MM-DD), otherwise keep previous.
   - `[CONSTITUTION_VERSION]` - Must increment according to semantic versioning:
     * MAJOR: Backward incompatible changes (e.g., switching from Terraform to Pulumi)
     * MINOR: New principle/section added or materially expanded guidance
     * PATCH: Clarifications, wording, typo fixes, non-semantic refinements
   - If version bump type ambiguous, propose reasoning before finalizing.
   
   **Organization-specific placeholders:**
   - `[ORGANIZATION_1]`, `[ORGANIZATION_2]`, etc. - Names of organizations using this infrastructure
   - `[SECURITY_COMPLIANCE]` - Required compliance standards (SOC2, HIPAA, PCI-DSS, etc.)
   - `[BACKUP_RETENTION]` - Backup retention policy (e.g., "30 days hot, 90 days cold, 1 year archive")
   - `[RTO]` - Recovery Time Objective
   - `[RPO]` - Recovery Point Objective

3. **Draft the updated constitution content**:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy exactly as in template.
   - Ensure each Principle section contains:
     * Succinct name line
     * Paragraph (or bullet list) capturing non-negotiable rules
     * Explicit rationale if not obvious
     * Examples where helpful
   - Ensure Technology Stack section specifies exact versions and standards.
   - Ensure Multi-Tenancy section details namespace strategy and network isolation.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. **Produce a Sync Impact Report** (prepend as an HTML comment at top of constitution file):
   
   ```markdown
   <!--
   SYNC IMPACT REPORT
   
   Constitution Version: [OLD_VERSION] → [NEW_VERSION]
   Amendment Date: [YYYY-MM-DD]
   Bump Type: [MAJOR|MINOR|PATCH]
   
   ## Changes Made:
   
   ### Modified Principles:
   - [Old Principle Title] → [New Principle Title]
   - [Another Change]
   
   ### Added Sections:
   - [New Section Name]: [Brief description]
   
   ### Removed Sections:
   - [Removed Section Name]: [Reason for removal]
   
   ### Technology Stack Updates:
   - Terraform: [OLD] → [NEW]
   - Kubernetes: [OLD] → [NEW]
   - Cilium: [OLD] → [NEW]
   
   ## Follow-up TODOs:
   - [ ] Update CI/CD pipelines to use new Terraform version
   - [ ] Schedule team training on new [PRINCIPLE_NAME] requirements
   - [ ] Review existing infrastructure for compliance with updated standards
   
   ## Deferred Items:
   - TODO(BACKUP_RETENTION): Specific retention periods pending storage cost analysis
   -->
   ```

6. **Validation before final output**:
   
   **Completeness checks:**
   - [ ] No remaining unexplained bracket tokens
   - [ ] All `[PLACEHOLDER]` tokens replaced with concrete values OR marked as `TODO(FIELD_NAME)`
   - [ ] Version line matches Sync Impact Report
   - [ ] Dates in ISO format YYYY-MM-DD
   
   **Quality checks:**
   - [ ] Principles are declarative and testable
   - [ ] No vague language - "should" replaced with MUST/SHOULD with clear rationale
   - [ ] Technology versions are specific (not "latest" or "any")
   - [ ] Multi-tenancy strategy clearly defined
   - [ ] Security and compliance requirements explicit
   - [ ] Disaster recovery metrics (RTO, RPO) specified
   
   **Infrastructure-specific checks:**
   - [ ] Terraform standards include: fmt, validate, tflint, modules, state backend
   - [ ] Ansible standards include: ansible-lint, syntax-check, idempotency
   - [ ] Kubernetes standards include: dry-run, kubeval/kubeconform, network policies
   - [ ] Cilium configuration specified: version, network policies, Hubble
   - [ ] ArgoCD configuration specified: sync policies, projects, RBAC
   
   **Consistency checks:**
   - [ ] All templates reference constitution principles
   - [ ] All prompts align with constitution workflow
   - [ ] Documentation reflects constitution tech stack

7. **Write the completed constitution** back to `/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

## Formatting & Style Requirements

**Markdown formatting:**
- Use heading levels exactly as in template (do not demote/promote)
- Single blank line between sections
- No trailing whitespace
- Code blocks use triple backticks with language identifiers

**Line wrapping:**
- Wrap long rationale lines to keep readability (<100 chars ideally)
- Do not create awkward breaks in the middle of technical terms
- Keep command examples and YAML/HCL on single lines when possible

**Infrastructure code style:**
- Terraform examples: HCL syntax, proper indentation
- Ansible examples: YAML syntax, proper indentation  
- Kubernetes examples: YAML syntax, apiVersion specified

**Tone:**
- Technical and precise
- Authoritative but not bureaucratic
- Action-oriented (use imperatives: "Use", "Ensure", "Configure")
- Examples over abstract descriptions

## Special Cases

**Partial updates:**
If the user supplies partial updates (e.g., only one principle revision):
- Still perform full validation and version decision steps
- Mark unchanged sections as validated in Sync Impact Report
- Only update templates/prompts affected by the change

**Missing critical information:**
If critical info missing (e.g., Kubernetes version unknown):
- Insert `TODO(<FIELD_NAME>): <explanation>` in constitution
- Add to "Deferred Items" in Sync Impact Report
- Suggest how to obtain this information (e.g., "Run: kubectl version")

**Multi-cloud scenarios:**
If project uses multiple cloud providers:
- Set `[CLOUD_PROVIDER]` to "Multi-Cloud"
- Add section "Cloud Provider Standards" with per-provider guidelines
- Ensure Terraform modules account for provider differences

**Existing infrastructure:**
If constitution updates for existing infrastructure:
- Add "Migration Plan" section in Sync Impact Report
- Flag breaking changes prominently
- Suggest gradual rollout strategy

## Important Notes

- **Do not create a new template** - Always operate on existing `/memory/constitution.md`
- **Preserve git history** - Include version history in Sync Impact Report
- **Infrastructure-first** - Focus on Terraform, Ansible, Kubernetes, ArgoCD
- **Multi-tenancy is critical** - Always address namespace isolation and network policies
- **Security is non-negotiable** - Compliance requirements must be explicit
- **Validation at every level** - Constitution, templates, prompts must all align

## Error Handling

If constitution file is malformed or missing placeholders:
1. Alert user to specific issues
2. Suggest fixes
3. Ask permission before making structural changes
4. Create backup before overwriting

If template updates would break existing specifications:
1. Flag breaking changes in Sync Impact Report
2. Suggest migration path
3. Create update guide for existing specs
4. Don't auto-update existing specs without explicit permission

---

**Remember**: The constitution is the foundation for all infrastructure decisions. Every template, prompt, and specification derives authority from this document. Take time to ensure it's correct, complete, and consistent.
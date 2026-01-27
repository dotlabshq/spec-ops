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



### 1. Generate Infrastructure Feature Name

**Create a concise short name** (2-4 words) for the branch:
- Analyze the infrastructure description and extract key components
- Use action-noun format for infrastructure: `deploy-[component]`, `setup-[service]`, `configure-[feature]`
- Preserve technical terms: SSO, monitoring, ArgoCD, Cilium, K8s, etc.
- Examples:
  - "Deploy single sign-on solution" → "sso-deployment"
  - "Set up monitoring with Prometheus and Grafana" → "monitoring-stack"
  - "Configure multi-tenant namespaces with Cilium" → "multi-tenant-networking"
  - "Add backup solution for PostgreSQL" → "postgres-backup"

### 2. Check for Existing Infrastructure Features

**Before creating new feature:**

a. **Fetch latest state**:
```bash
git fetch --all --prune
```

b. **Find highest feature number** for this short-name across:
- Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
- Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
- Specs directories: Check `.specops/specs/[0-9]+-<short-name>`

c. **Determine next number**:
- Extract all numbers from all sources
- Find highest number N
- Use N+1 for new branch

d. **Run feature creation script**:
```bash
.specops/scripts/create-new-feature.sh [short-name]
```

**IMPORTANT**:
- Only run script once per feature
- Script creates branch and initializes directory
- Use script output to get BRANCH_NAME and SPEC_FILE paths

### 3. Load Infrastructure Specification Template

Read `.specops/templates/spec-template.md` to understand required sections for infrastructure specifications.

### 4. Parse Infrastructure Requirements

**Extract key infrastructure components:**

1. **Infrastructure Type**:
   - VM provisioning (Terraform)
   - Kubernetes setup (Ansible)
   - Application deployment (ArgoCD)
   - Network configuration (Cilium)
   - Monitoring/observability
   - Backup/disaster recovery

2. **Multi-Tenancy Requirements**:
   - Which organizations need access?
   - Namespace isolation strategy
   - Resource quotas per organization
   - Network policies required

3. **Technical Constraints**:
   - Cloud provider
   - Compliance requirements (SOC2, HIPAA, etc.)
   - Performance targets (RTO, RPO, uptime)
   - Budget constraints

4. **Dependencies**:
   - Existing infrastructure
   - External services
   - Required credentials/access

### 5. Make Informed Infrastructure Decisions

**For unclear aspects, use industry-standard defaults:**

✅ **Make reasonable assumptions** (document in Assumptions section):
- Namespace naming: `{org-name}-{environment}` pattern
- Network policies: Default deny-all with explicit allows
- Resource quotas: Based on organization size (small/medium/large)
- Backup retention: 30 days hot, 90 days cold, 1 year archive
- RTO/RPO: Standard for application tier (critical/standard/low-priority)

❌ **Only ask for clarification** (max 3 total) if:
- Multiple cloud providers possible and significantly different costs
- Compliance requirements unclear (HIPAA vs SOC2 vs both)
- Organization list unknown (can't proceed without it)
- Critical security boundaries undefined

**Prioritize clarifications**: 
Multi-tenancy scope > Compliance > Performance targets > Technical preferences

### 6. Create Infrastructure Specification

**Fill specification following template structure:**

#### Overview Section
- Feature name and ID
- Business context (why this infrastructure is needed)
- Infrastructure goals (what it enables)

#### Requirements Section

**Functional Requirements (Infrastructure-specific)**:
```
FR-1: Deploy [Component]
Priority: Critical
Description: [What infrastructure resources needed]
Acceptance Criteria:
- [ ] [Resource 1] provisioned and accessible
- [ ] [Resource 2] configured correctly
- [ ] [Resource 3] integrated with existing infrastructure
```

**Non-Functional Requirements**:
- **Performance**: Uptime SLA, latency targets, throughput
- **Scalability**: Resource limits, growth capacity
- **Security**: Compliance standards, network isolation, access control
- **Reliability**: Backup strategy, disaster recovery, failover

#### Infrastructure Scenarios

**Template for scenarios**:
```
Scenario N: [Scenario Name]
Actor: [Platform Admin / Developer / End User]
Preconditions:
  - [Existing infrastructure state]
  - [Required access/credentials]

Flow:
1. [Terraform provisions resources]
2. [Ansible configures services]
3. [ArgoCD deploys applications]
4. [Verification steps]

Postconditions:
  - [Infrastructure state after deployment]
  - [Accessibility/connectivity established]

Validation:
- [ ] [How to verify this scenario works]
```

#### Multi-Tenancy Requirements

**Specify clearly**:
- Organization list with namespaces
- Resource quotas per organization
- Network isolation approach
- RBAC requirements
- Separate or shared resources

**Example**:
```yaml
Organizations:
  - name: acme
    namespaces:
      - acme-prod
      - acme-dev
    quota:
      cpu: "10"
      memory: "20Gi"
      pods: "50"
  
  - name: contoso
    namespaces:
      - contoso-prod
    quota:
      cpu: "5"
      memory: "10Gi"
      pods: "30"
```

#### Dependencies Section

**Infrastructure Dependencies**:
- Existing VMs/cloud accounts
- Network configuration (VPC, subnets)
- DNS setup
- Load balancers
- Storage systems

**External Dependencies**:
- Third-party services
- External APIs
- Cloud provider features

### 7. Specification Quality Validation

**Create validation checklist** at `.specops/specs/[FEATURE_ID]/checklists/requirements.md`:

```markdown
# Infrastructure Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate infrastructure specification completeness
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Infrastructure Completeness

- [ ] Infrastructure type clearly defined (VM/K8s/App/Network)
- [ ] All required resources identified
- [ ] Multi-tenancy requirements specified
- [ ] Organization list and quotas defined
- [ ] Network isolation approach documented

## Requirement Quality

- [ ] No implementation details (specific Terraform modules, Ansible roles)
- [ ] No [NEEDS CLARIFICATION] markers remain (max 3 allowed)
- [ ] All acceptance criteria are verifiable
- [ ] Success criteria are measurable and infrastructure-focused
- [ ] Dependencies identified (cloud account, existing infra, credentials)

## Multi-Tenancy Validation

- [ ] Each organization has namespace strategy
- [ ] Resource quotas specified per organization
- [ ] Network policy requirements defined
- [ ] RBAC/access control requirements clear

## Security & Compliance

- [ ] Compliance requirements identified (if applicable)
- [ ] Security boundaries defined
- [ ] Secret management approach outlined
- [ ] Backup/DR requirements specified

## Infrastructure Scenarios

- [ ] Deployment scenarios cover main flows
- [ ] Validation steps included for each scenario
- [ ] Rollback procedures considered
- [ ] Edge cases identified

## Notes

- Items marked incomplete require spec updates before `/specops.plan`
- Maximum 3 [NEEDS CLARIFICATION] markers allowed
```

**Run Validation**:

1. Review spec against checklist
2. **If all items pass**: Mark complete, proceed to step 8
3. **If items fail** (excluding [NEEDS CLARIFICATION]):
   - List failing items with specific issues
   - Update spec to address issues
   - Re-run validation (max 3 iterations)
   - Document remaining issues in checklist notes

4. **If [NEEDS CLARIFICATION] markers remain**:
   - Extract all markers from spec
   - **LIMIT**: Max 3 markers (prioritize by impact)
   - Present questions with table format:

```markdown
## Question [N]: [Infrastructure Topic]

**Context**: [Quote from spec]

**What we need to know**: [Specific question]

**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A | [Option A] | [Infrastructure impact] |
| B | [Option B] | [Infrastructure impact] |
| C | [Option C] | [Infrastructure impact] |
| Custom | [Your answer] | [Explain custom input] |

**Your choice**: _[Wait for response]_
```

   - **CRITICAL**: Proper markdown table formatting with aligned pipes
   - Wait for user response: "Q1: A, Q2: B, Q3: Custom - [details]"
   - Update spec with chosen answers
   - Re-run validation

5. **Update checklist** after each iteration

### 8. Success Criteria Guidelines

**Infrastructure-focused success criteria must be:**

1. **Measurable**: Include specific metrics
2. **Infrastructure-agnostic**: No mention of specific tools (use generic terms)
3. **Operationally-focused**: Describe deployment/operational outcomes
4. **Verifiable**: Can be tested without implementation knowledge

**Good Infrastructure Examples**:
- "Infrastructure provisioning completes in under 15 minutes"
- "System supports 10,000 concurrent users with 99.9% uptime"
- "Deployment rollback completes in under 5 minutes"
- "Each organization isolated with dedicated resources"
- "Backup recovery tested successfully (RPO: 1 hour, RTO: 4 hours)"
- "Network policies prevent unauthorized cross-namespace communication"

**Bad Examples** (too implementation-specific):
- "Terraform apply runs in under 10 minutes" → Use "Infrastructure provisioning..."
- "Ansible playbook completes successfully" → Use "Cluster configuration..."
- "ArgoCD syncs in under 2 minutes" → Use "Application deployment..."
- "Cilium policies are active" → Use "Network isolation enforced..."

### 9. Constitution Alignment Check

**Before finalizing, verify alignment with constitution**:

```bash
# Load constitution
constitution_file=".specops/memory/constitution.md"

# Check alignment:
# - Technology stack matches constitution standards
# - Multi-tenancy approach follows constitution strategy
# - Security requirements meet constitution compliance
# - Code quality standards referenced
```

**Add to spec if constitution exists**:
```markdown
## Constitution Alignment

This specification aligns with the following constitution principles:
- [PRINCIPLE_NAME]: [How spec aligns]
- [TECHNOLOGY_STANDARD]: [Version/approach used]
- [MULTI_TENANCY_STRATEGY]: [How implemented]
```

### 10. Write Specification

Write complete specification to `SPEC_FILE` with:
- All sections filled with concrete details
- No implementation specifics (Terraform modules, Ansible playbooks, etc.)
- Infrastructure-focused language (resources, namespaces, policies, quotas)
- Clear multi-tenancy requirements
- Measurable success criteria

### 11. Report Completion

Inform user with:

```
Infrastructure specification created successfully!

Feature: [FEATURE_ID] - [FEATURE_NAME]
Branch: [BRANCH_NAME]
Location: .specops/specs/[FEATURE_ID]/spec.md
Checklist: .specops/specs/[FEATURE_ID]/checklists/requirements.md

Infrastructure Type: [VM/K8s/App/Network/Multi]
Organizations: [COUNT] ([LIST])
Compliance: [REQUIREMENTS]

Validation Results:
✓ All quality checks passed
✓ No clarifications needed (OR: [N] clarifications resolved)
✓ Multi-tenancy requirements complete
✓ Constitution alignment verified

Next Steps:
1. Review specification for accuracy
2. Get stakeholder approval if needed
3. Run /specops.plan to create technical implementation plan

Suggested commit message:
feat(spec): add [FEATURE_ID] infrastructure specification
```

## General Guidelines

### Quick Guidelines

- Focus on **WHAT** infrastructure is needed and **WHY**
- Avoid **HOW** to implement (no Terraform modules, Ansible roles, ArgoCD apps)
- Written for infrastructure stakeholders, not implementation details
- Infrastructure-first language: resources, namespaces, quotas, policies
- Multi-tenancy is always a consideration
- Security and compliance upfront

### Section Requirements

**Mandatory for Infrastructure**:
- Overview with business context
- Functional requirements (infrastructure resources)
- Non-functional requirements (performance, security, reliability)
- Infrastructure scenarios (deployment flows)
- Multi-tenancy requirements (if applicable)
- Dependencies (cloud, network, existing infrastructure)

**Optional**:
- Key entities (if data/state management involved)
- Integration requirements (if connecting to external systems)

### Infrastructure-Specific Considerations

1. **Always think multi-tenant**: Even if starting with single org, design for future growth
2. **Network isolation first**: Define network boundaries before other details
3. **Resource quotas early**: Prevent resource contention between organizations
4. **Compliance as requirement**: Security standards are functional requirements
5. **Operational metrics**: Focus on deployment, availability, recovery metrics

### Common Infrastructure Patterns

**VM Provisioning Specs**:
- Cloud provider and region
- Instance types/sizes
- Network configuration
- Security groups/firewalls
- Storage requirements

**Kubernetes Deployment Specs**:
- Namespace strategy
- Resource quotas
- Network policies
- RBAC requirements
- Ingress/routing

**Application Deployment Specs**:
- Container registry
- Deployment strategy (rolling, blue-green)
- Health checks
- Resource limits
- Persistence requirements

**Monitoring/Observability Specs**:
- Metrics to collect
- Log aggregation
- Alerting rules
- Dashboard requirements
- Retention policies

### Reasonable Infrastructure Defaults

**Don't ask about these - use industry standards**:

- **Namespace naming**: `{org-name}-{environment}` pattern
- **Network policies**: Default deny-all with explicit allows
- **Resource quotas**: Small org (2 CPU, 4Gi), Medium (5 CPU, 10Gi), Large (10 CPU, 20Gi)
- **Backup retention**: 30 days hot, 90 days cold, 1 year archive
- **Uptime SLA**: 99.9% for production, 99% for staging
- **RTO/RPO**: Critical (1h/15m), Standard (4h/1h), Low (24h/4h)
- **Image scanning**: Before deployment
- **Secret rotation**: Quarterly minimum
- **Audit logging**: Enabled for all production

### When to Ask for Clarification (Max 3)

**Priority 1 - Scope/Multi-tenancy**:
- Number of organizations unknown and can't infer
- Conflicting organization requirements
- Shared vs isolated resources decision critical

**Priority 2 - Compliance/Security**:
- Multiple compliance standards possible (HIPAA vs SOC2)
- Data residency requirements unclear
- Security boundaries significantly impact architecture

**Priority 3 - Performance/Scale**:
- User load unclear and no reasonable default
- Geographic distribution requirements unknown
- Critical latency requirements unspecified

**Never ask about**:
- Specific tool choices (that's for /specops.plan)
- Implementation details
- Standard practices with clear defaults

---

**Remember**: This is an infrastructure specification, not a technical plan. Stay focused on WHAT infrastructure is needed and WHY, not HOW to build it. The constitution provides the standards, this spec defines the requirements.
# /specops.specify Command

You are executing the `/specops.specify` command in a SpecOps (Spec-Driven Infrastructure as Code) project.

## Purpose

Define infrastructure requirements WITHOUT technical implementation details. Focus on the **WHAT** and **WHY**, not the **HOW**.

## Prerequisites

Before running this command:
1. Constitution must exist (`.specops/memory/constitution.md`)
2. If starting a new feature, run the create-new-feature script

## Your Task

1. **Verify Prerequisites**
   - Check that constitution exists
   - If no constitution, inform user to run `/specops.constitution` first

2. **Create or Identify Feature**
   - Check if currently on a feature branch (pattern: `NNN-feature-name`)
   - If not, run `.specops/scripts/create-new-feature.sh <feature-name>` to create one
   - Extract feature name from user's request (e.g., "sso-deployment", "monitoring-stack")

3. **Understand Requirements**
   Ask clarifying questions about:
   - **Business Context**: What problem does this solve?
   - **Goals**: What are we trying to achieve?
   - **Scope**: What's included and excluded?
   - **Multi-Tenancy**: Which organizations need access? How should they be isolated?
   - **Dependencies**: What existing infrastructure is needed?
   - **Constraints**: Any budget, compliance, or technical constraints?

4. **Create Specification**
   - Load the specification template from `.specops/templates/spec-template.md`
   - Fill in ALL sections based on user input and clarifications
   - Use infrastructure-focused language (namespaces, resources, policies, quotas)
   - Define clear acceptance criteria

5. **Save Specification**
   - Save to `.specops/specs/NNN-feature-name/spec.md`
   - Commit to git with message: "Add specification for NNN-feature-name"

## Key Sections to Fill

### Overview
- High-level description
- Feature ID and metadata
- Status (Draft → In Review → Approved → Implemented)

### Business Context
- Problem statement (why this infrastructure is needed)
- Goals and objectives (measurable)
- Success criteria (how we'll know it works)
- Non-goals (what's out of scope)

### Requirements

#### Functional Requirements (FR)
Examples:
- FR-1: Deploy SSO solution supporting SAML and OIDC
- FR-2: Provide namespace isolation for each organization
- FR-3: Enable PostgreSQL persistence with automatic backups

#### Non-Functional Requirements (NFR)
Examples:
- NFR-1: 99.9% uptime SLA
- NFR-2: Support 10,000 concurrent users
- NFR-3: Deployment completes in under 15 minutes
- NFR-4: Comply with SOC2 requirements

### Infrastructure Scenarios

Example:
```
Scenario 1: Deploy Application for New Organization
Actor: Platform Administrator
Preconditions:
  - Kubernetes cluster is running
  - ArgoCD is configured
  - Git repository contains application manifests

Flow:
  1. Create namespace for organization
  2. Apply resource quotas and limits
  3. Create Cilium network policy for isolation
  4. Create ArgoCD Application pointing to manifests
  5. Sync application via ArgoCD
  6. Verify pods are running and healthy

Postconditions:
  - Application deployed and accessible
  - Namespace isolated from other organizations
  - Metrics and logs flowing to monitoring systems

Validation:
  - kubectl get pods -n org-name shows all pods Running
  - Network policy blocks unauthorized traffic
  - Application responds to health checks
```

### Multi-Tenancy Requirements

Specify:
- Which organizations need access
- Namespace naming convention
- Resource quota per organization
- Network isolation requirements
- RBAC requirements

### Dependencies & Constraints

List:
- Required infrastructure (existing VMs, cloud accounts, etc.)
- External services (DNS, load balancers, etc.)
- Technical constraints (specific cloud provider, regions, etc.)
- Budget constraints
- Compliance requirements

## What NOT to Include

❌ Don't specify:
- Specific Terraform modules to use
- Ansible playbook structure
- Helm chart values
- Kubernetes manifest details
- Network CIDR ranges
- Instance sizes or types

✅ Instead describe:
- What resources are needed (e.g., "PostgreSQL database")
- Why they're needed (e.g., "for persistent SSO session storage")
- How they should behave (e.g., "automatic failover for high availability")

## Example User Prompts

**Basic:**
```
/specops.specify Deploy monitoring stack with Prometheus and Grafana
```

**Detailed:**
```
/specops.specify Deploy Zitadel SSO solution for three organizations (Acme, Contoso, Fabrikam).
Each organization needs isolated authentication with their own LDAP integration. 
Require PostgreSQL for persistence, automated backups, and 99.9% uptime. 
Must support 5000 concurrent users per organization.
```

## Clarification Process

If requirements are unclear, ask questions like:

- "Which organizations will use this infrastructure?"
- "What are the performance requirements (users, requests/sec, latency)?"
- "What are the uptime/availability requirements?"
- "Are there specific compliance requirements (HIPAA, SOC2, etc.)?"
- "What's the disaster recovery requirement (RTO, RPO)?"
- "What resources quotas are needed per organization?"
- "How should monitoring and alerting work?"

## Output Format

Create `.specops/specs/NNN-feature-name/spec.md` following the template structure.

## Validation Checklist

Before completing, verify:
- [ ] Constitution referenced for alignment
- [ ] Feature branch created and checked out
- [ ] Business context clearly defined
- [ ] All functional requirements have acceptance criteria
- [ ] Non-functional requirements are measurable
- [ ] Infrastructure scenarios cover main use cases
- [ ] Multi-tenancy requirements specified
- [ ] Dependencies identified
- [ ] Constraints documented
- [ ] File saved to correct location
- [ ] Changes committed to git

## After Completion

Run the review checklist in the specification:
```
Review & Acceptance Checklist:
- [ ] Business context is clearly defined
- [ ] All functional requirements have acceptance criteria
- [ ] Non-functional requirements are measurable
- [ ] Infrastructure scenarios cover main use cases
- [ ] Multi-tenancy requirements are complete
- [ ] Dependencies are identified and validated
- [ ] Constraints and assumptions are documented
- [ ] Aligns with infrastructure constitution
```

Then inform the user:
```
Specification created successfully!

Location: .specops/specs/NNN-feature-name/spec.md
Branch: NNN-feature-name

Next steps:
1. Review the specification for completeness
2. Get stakeholder approval if needed
3. Run /specops.plan to create technical implementation plan
```

## Important Notes

- **Focus on WHAT, not HOW**: Describe the desired outcome, not the implementation
- **Be specific**: "Support 1000 users" not "support many users"
- **Use infrastructure terminology**: namespaces, quotas, policies, not just "resources"
- **Think multi-tenant**: Always consider organization isolation
- **Reference constitution**: Ensure alignment with established principles

---

**Remember**: A good specification is clear, measurable, and implementation-agnostic. It defines success criteria without prescribing the solution.
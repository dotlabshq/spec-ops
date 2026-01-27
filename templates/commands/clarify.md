---
description: Identify underspecified areas in infrastructure specification by asking up to 5 targeted clarification questions and encoding answers back into the spec.
handoffs: 
  - label: Build Technical Plan
    agent: specops.plan
    prompt: Create implementation plan for the infrastructure. I am deploying with...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

**Goal**: Detect and reduce ambiguity or missing decision points in the active infrastructure specification and record clarifications directly in the spec file.

**Note**: This clarification workflow should run BEFORE invoking `/specops.plan`. If user explicitly skips clarification (e.g., exploratory spike), warn that downstream rework risk increases.

### Execution Steps

#### 1. Prerequisites Check

**Run script** from repository root:
```bash
.specops/scripts/bash/check-prerequisites.sh --json --paths-only
```

**Parse JSON fields**:
- `FEATURE_DIR` - Feature directory path
- `FEATURE_SPEC` - Specification file path
- `IMPL_PLAN` - Plan file path (optional)
- `TASKS` - Tasks file path (optional)

**If JSON parsing fails**: Abort and instruct user to re-run `/specops.specify` or verify feature branch.

**Note**: For single quotes in args like "I'm deploying", use: `'I'\''m deploying'` or `"I'm deploying"`

---

#### 2. Infrastructure Ambiguity Scan

Load current spec and perform structured coverage scan. For each category, mark: **Clear** / **Partial** / **Missing**

**Infrastructure Scope & Purpose**:
- [ ] Infrastructure type clearly defined (VM/K8s/App/Network/Monitoring)
- [ ] Business context and goals explicit
- [ ] Explicit out-of-scope infrastructure
- [ ] Success criteria measurable and infrastructure-focused

**Multi-Tenancy Requirements**:
- [ ] Organization list complete
- [ ] Namespace strategy defined
- [ ] Resource quotas per organization
- [ ] Network isolation approach
- [ ] RBAC requirements clear

**Infrastructure Resources**:
- [ ] Cloud provider specified
- [ ] Region(s) and availability zones
- [ ] Compute resources (instance types, counts)
- [ ] Network topology (VPC, subnets, CIDR)
- [ ] Storage requirements (volumes, backups)
- [ ] Load balancers and ingress

**Technology Stack**:
- [ ] Terraform version and provider versions
- [ ] Ansible version and collections
- [ ] Kubernetes version and distribution
- [ ] Cilium version and configuration
- [ ] ArgoCD version and sync strategy

**Deployment Architecture**:
- [ ] High-level architecture clear
- [ ] Component relationships defined
- [ ] Data flow understood
- [ ] Integration points identified

**Non-Functional Requirements**:
- [ ] Performance targets (provisioning time, latency)
- [ ] Availability requirements (uptime SLA, RTO, RPO)
- [ ] Scalability limits (node counts, resource limits)
- [ ] Security requirements (compliance, encryption, network policies)
- [ ] Monitoring requirements (metrics, logs, alerts)

**Network & Security**:
- [ ] Network policy approach (default deny, L7 filtering)
- [ ] Ingress/egress rules
- [ ] Cross-namespace communication policy
- [ ] TLS/encryption requirements
- [ ] Firewall/security group rules

**Dependencies & Constraints**:
- [ ] Existing infrastructure dependencies
- [ ] External service integrations
- [ ] Credential requirements
- [ ] Cloud provider limits
- [ ] Budget constraints
- [ ] Compliance requirements

**Configuration Management**:
- [ ] Terraform state backend
- [ ] Ansible inventory approach
- [ ] Secret management strategy
- [ ] Configuration file locations

**Edge Cases & Failure Handling**:
- [ ] Deployment failure scenarios
- [ ] Resource quota exceeded
- [ ] Network partition handling
- [ ] Backup failure procedures
- [ ] Disaster recovery approach

**Operational Readiness**:
- [ ] Backup strategy and retention
- [ ] Rollback procedures
- [ ] Monitoring and alerting
- [ ] Runbook requirements
- [ ] Access control and audit logging

**Infrastructure Scenarios**:
- [ ] Deployment flow clear
- [ ] Validation steps defined
- [ ] Pre/post conditions explicit
- [ ] Rollback tested

**Terminology & Standards**:
- [ ] Infrastructure terms consistent
- [ ] Naming conventions defined
- [ ] Tagging strategy specified

**Constitution Alignment**:
- [ ] Technology versions match constitution
- [ ] Multi-tenancy strategy aligns
- [ ] Code quality standards referenced
- [ ] Security standards met

**Placeholders & TODOs**:
- [ ] No [NEEDS CLARIFICATION] markers
- [ ] No TODO items remaining
- [ ] No vague adjectives ("scalable", "robust")

---

#### 3. Generate Prioritized Questions

**Constraints**:
- Maximum 5 questions per session
- Maximum 10 questions total across all sessions
- Each question must be answerable with:
  - Multiple choice (2-5 options), OR
  - Short answer (≤5 words)

**Prioritization Heuristic**: Impact × Uncertainty

**High Impact Categories** (prioritize):
1. Multi-tenancy (affects isolation, security, resource allocation)
2. Cloud provider & region (affects cost, compliance, latency)
3. Compliance requirements (blocks deployment if wrong)
4. Network isolation strategy (affects security posture)
5. Backup & DR (affects data safety)

**Medium Impact Categories**:
6. Specific technology versions
7. Resource sizing
8. Monitoring approach
9. Deployment method

**Low Impact Categories** (defer to plan):
10. Specific module names
11. File organization
12. Stylistic preferences

**Exclusion Rules**:
- Already answered questions
- Plan-level execution details
- Trivial preferences
- Questions that don't impact architecture/security/compliance

---

#### 4. Sequential Question Loop (Interactive)

**Present ONE question at a time**

**For Multiple Choice Questions**:

1. **Analyze options** and determine most suitable based on:
   - Infrastructure best practices
   - Security and compliance
   - Cost optimization
   - Operational simplicity
   - Constitution alignment

2. **Present recommendation prominently**:
   ```
   **Recommended:** Option [X] - <1-2 sentence reasoning>
   ```

3. **Render options table**:
   ```markdown
   | Option | Description |
   |--------|-------------|
   | A | <Infrastructure option A> |
   | B | <Infrastructure option B> |
   | C | <Infrastructure option C> |
   | Short | Provide different answer (≤5 words) |
   ```

4. **Instructions**:
   ```
   Reply with: option letter ("A"), "yes"/"recommended" to accept suggestion, or custom answer (≤5 words)
   ```

**For Short Answer Questions**:

1. **Provide suggested answer**:
   ```
   **Suggested:** <answer> - <brief reasoning>
   ```

2. **Format constraint**:
   ```
   Format: Short answer (≤5 words)
   Reply: "yes"/"suggested" to accept, or provide your answer
   ```

**After User Answers**:
- If "yes"/"recommended"/"suggested" → Use AI's suggestion
- Otherwise validate: maps to option OR ≤5 words
- If ambiguous → Ask disambiguation (doesn't count as new question)
- Record answer in memory, proceed to next

**Stop Conditions**:
- All critical ambiguities resolved
- User signals "done"/"stop"/"no more"
- 5 questions asked
- No more high-impact unclear items

---

#### 5. Integration After Each Answer

**Maintain in-memory spec representation**

**First Answer Integration**:
- Ensure `## Clarifications` section exists (create after Overview)
- Create `### Session YYYY-MM-DD` subheading
- Append: `- Q: <question> → A: <answer>`

**Apply Clarification to Appropriate Section**:

**Infrastructure Scope** → Update Business Context or Overview
```markdown
## Business Context
- Cloud Provider: [ANSWER]
- Primary Region: [ANSWER]
```

**Multi-Tenancy** → Update Multi-Tenancy Requirements
```markdown
## Multi-Tenancy Requirements
Organizations: [LIST]
- [ORG_1]: [namespaces], quota: [ANSWER]
```

**Resources** → Update Requirements
```markdown
## Requirements
FR-1: Compute Resources
- Instance types: [ANSWER]
- Control plane: [COUNT] × [ANSWER]
```

**Network** → Update Multi-Tenancy or Security sections
```markdown
### Network Isolation
Strategy: [ANSWER]
Default policy: deny-all
L7 filtering: [ANSWER]
```

**Performance** → Update Non-Functional Requirements
```markdown
#### NFR-1: Performance
- Infrastructure provisioning: < [ANSWER] minutes
- RTO: [ANSWER]
- RPO: [ANSWER]
```

**Security** → Update Security sections
```markdown
#### NFR-4: Security
- Compliance: [ANSWER]
- Network encryption: [ANSWER]
- Secret management: [ANSWER]
```

**Dependencies** → Update Dependencies section
```markdown
## Dependencies
### Cloud Provider
- Provider: [ANSWER]
- Required access: [ANSWER]
```

**Edge Cases** → Add to Infrastructure Scenarios
```markdown
### Scenario N: Failure Handling
Trigger: [ANSWER]
Recovery: [ANSWER]
```

**Replace contradictory statements** (don't duplicate)

**Save spec file after each integration** (atomic write)

**Preserve formatting**:
- Keep heading hierarchy
- Don't reorder unrelated sections
- Minimal, testable additions

---

#### 6. Validation After Each Write

**Check**:
- [ ] One bullet per accepted answer in Clarifications
- [ ] Total questions ≤ 5
- [ ] No lingering placeholders question was meant to resolve
- [ ] No contradictory statements remain
- [ ] Markdown structure valid
- [ ] Only allowed new headings: `## Clarifications`, `### Session YYYY-MM-DD`
- [ ] Terminology consistent across updated sections

---

#### 7. Write Updated Spec

Save to `FEATURE_SPEC` file

---

#### 8. Report Completion

**After questioning loop ends**:

```markdown
Infrastructure Specification Clarification Complete

Questions Asked: [N]/5
Spec Updated: [PATH]

Sections Updated:
- Business Context
- Multi-Tenancy Requirements  
- Non-Functional Requirements (Performance)
- Dependencies (Cloud Provider)

Coverage Summary:

| Category | Status | Notes |
|----------|--------|-------|
| Infrastructure Scope | ✓ Resolved | Cloud provider and region defined |
| Multi-Tenancy | ✓ Resolved | Organization list and quotas clear |
| Resources | ✓ Resolved | Compute sizing defined |
| Network & Security | ⏭ Deferred | Details for plan phase |
| Performance | ✓ Resolved | RTO/RPO specified |
| Dependencies | ✓ Resolved | External services identified |
| Monitoring | ⚠ Outstanding | Low impact, can proceed |

Legend:
✓ Resolved - Was unclear, now addressed
⏭ Deferred - Better suited for planning phase
✓ Clear - Already sufficient
⚠ Outstanding - Still unclear but low impact

Recommendation: [READY FOR PLANNING | RUN CLARIFY AGAIN]

Next Steps:
1. Review updated specification
2. Validate multi-tenancy requirements
3. Run /specops.plan to create implementation design

Suggested command: /specops.plan
```

---

## Behavior Rules

### No Critical Ambiguities
If all categories Clear:
```
No critical infrastructure ambiguities detected.

Coverage Summary: All categories sufficient for planning.

Recommendation: Proceed to /specops.plan

Next command: /specops.plan Use Terraform for AWS, Ansible for K8s 1.28
```

### Missing Spec File
If `FEATURE_SPEC` not found:
```
Error: Specification file not found

Please run /specops.specify first to create infrastructure specification.

Command: /specops.specify Deploy monitoring for 3 organizations
```

### Question Quota Rules
- Maximum 5 questions per session
- Maximum 10 questions across all clarification sessions
- Disambiguation retries don't count as new questions
- If 5 reached with high-impact Outstanding → Flag in report

### Early Termination
User signals: "stop", "done", "proceed", "good"
→ Stop questioning, integrate answers so far, report

### Speculative Questions
Avoid unless absence blocks functional clarity:
- ❌ "Which Terraform version?" (if constitution defines it)
- ❌ "Module naming preference?" (stylistic)
- ✅ "Which cloud provider?" (affects everything)
- ✅ "Compliance requirements?" (blocks deployment)

### Context Priority
Use `$ARGUMENTS` for prioritization hints:
- User mentions "security" → Prioritize security questions
- User mentions "multi-cloud" → Prioritize cloud provider questions
- User mentions "compliance" → Prioritize compliance questions

---

## Infrastructure-Specific Question Examples

### High-Impact Questions

**Multi-Tenancy**:
```
Q: How many organizations require isolated infrastructure?

**Recommended:** Option B - Standard 3-org setup balances complexity and value

| Option | Description |
|--------|-------------|
| A | Single organization (pilot/MVP) |
| B | 3-5 organizations (standard multi-tenant) |
| C | 10+ organizations (enterprise scale) |
| Short | Specify exact count (≤5 words) |
```

**Cloud Provider**:
```
Q: Which cloud provider for infrastructure deployment?

**Recommended:** Option A - AWS most mature for Kubernetes + Cilium

| Option | Description |
|--------|-------------|
| A | AWS (EKS, mature ecosystem) |
| B | Azure (AKS, enterprise integration) |
| C | GCP (GKE, cost-effective) |
| D | On-premise (full control, higher ops) |
```

**Compliance**:
```
Q: What compliance standards must infrastructure meet?

**Recommended:** Option B - SOC2 standard for SaaS

| Option | Description |
|--------|-------------|
| A | None (internal use only) |
| B | SOC2 (standard SaaS compliance) |
| C | HIPAA (healthcare data) |
| D | PCI-DSS (payment processing) |
| Short | Specify other standard (≤5 words) |
```

**Network Isolation**:
```
Q: Default network policy for multi-tenant namespaces?

**Recommended:** Option B - Deny-all most secure

| Option | Description |
|--------|-------------|
| A | Allow all (no isolation) |
| B | Deny all with explicit allows (zero-trust) |
| C | Allow internal, deny external |
```

**Backup Strategy**:
```
Q: Backup retention policy for infrastructure state?

**Recommended:** Option B - Industry standard retention

| Option | Description |
|--------|-------------|
| A | 7 days only (minimal) |
| B | 30 days hot, 90 days cold (standard) |
| C | 365 days (compliance-driven) |
| Short | Specify custom policy (≤5 words) |
```

### Medium-Impact Questions

**Resource Sizing**:
```
Q: Expected peak concurrent users per organization?

**Suggested:** 1000 users - Typical small/medium org load

Format: Short answer (≤5 words)
Example: "500 users", "5000 concurrent"
```

**Kubernetes Distribution**:
```
Q: Kubernetes distribution preference?

**Recommended:** Option A - Managed service reduces ops burden

| Option | Description |
|--------|-------------|
| A | Managed (EKS/AKS/GKE - simpler ops) |
| B | Self-hosted (RKE2/K3s - more control) |
```

**Deployment Method**:
```
Q: Application deployment approach via ArgoCD?

**Recommended:** Option B - Helm most flexible

| Option | Description |
|--------|-------------|
| A | Plain YAML (simple, verbose) |
| B | Helm (templating, reusable) |
| C | Kustomize (overlay-based) |
```

---

## Example Full Session

**User**: `/specops.clarify`

**AI**: 
```
Loading infrastructure specification...
Analyzing coverage across 14 categories...

Found 3 high-impact ambiguities requiring clarification.

---

Question 1 of 5:

Which cloud provider for infrastructure deployment?

**Recommended:** Option A - AWS has most mature Kubernetes ecosystem with EKS, 
robust Cilium support, and extensive Terraform provider coverage.

| Option | Description |
|--------|-------------|
| A | AWS (EKS, mature ecosystem, wide adoption) |
| B | Azure (AKS, enterprise integration, AD) |
| C | GCP (GKE, cost-effective, simple) |
| D | On-premise (full control, higher ops burden) |
| Short | Specify other provider (≤5 words) |

Reply with: option letter ("A"), "yes"/"recommended", or custom answer
```

**User**: `A`

**AI**:
```
✓ Answer recorded: AWS

Updating specification...
- Updated: Dependencies > Cloud Provider
- Updated: Constraints > Cloud provider: AWS

---

Question 2 of 5:

How many organizations require isolated namespaces?

**Recommended:** Option B - 3-5 organizations is standard multi-tenant setup, 
balances operational complexity with business value.

| Option | Description |
|--------|-------------|
| A | 1 organization (pilot/MVP, simplest) |
| B | 3-5 organizations (standard multi-tenant) |
| C | 10+ organizations (enterprise scale) |
| Short | Specify exact count (≤5 words) |
```

**User**: `B`

**AI**:
```
✓ Answer recorded: 3-5 organizations

Updating specification...
- Updated: Multi-Tenancy Requirements > Organizations
- Added: Resource quotas per organization (Medium sizing)

---

Question 3 of 5:

What compliance standards must infrastructure meet?

**Recommended:** Option B - SOC2 Type II is standard for SaaS platforms,
covers security, availability, and confidentiality controls.

| Option | Description |
|--------|-------------|
| A | None (internal use, no compliance) |
| B | SOC2 Type II (standard SaaS) |
| C | HIPAA (healthcare PHI) |
| D | PCI-DSS (payment card data) |
| Short | Specify other (≤5 words) |
```

**User**: `SOC2`

**AI**:
```
✓ Answer recorded: SOC2 Type II

Updating specification...
- Updated: Non-Functional Requirements > Security > Compliance
- Added: Audit logging requirements
- Added: Encryption requirements (at rest + in transit)

All high-impact ambiguities resolved!

---

Infrastructure Specification Clarification Complete

Questions Asked: 3/5
Spec Updated: .specops/specs/001-monitoring/spec.md

Sections Updated:
- Dependencies (Cloud Provider: AWS)
- Multi-Tenancy Requirements (3-5 organizations)
- Non-Functional Requirements (Security: SOC2)
- Constraints (Cloud provider specified)

Coverage Summary:

| Category | Status | Notes |
|----------|--------|-------|
| Infrastructure Scope | ✓ Clear | Already well-defined |
| Multi-Tenancy | ✓ Resolved | Organization count and isolation strategy |
| Resources | ⏭ Deferred | Sizing details for plan phase |
| Technology Stack | ✓ Clear | Versions from constitution |
| Network & Security | ✓ Resolved | Compliance requirements added |
| Dependencies | ✓ Resolved | Cloud provider specified |
| Performance | ⏭ Deferred | RTO/RPO targets for plan |
| Monitoring | ⏭ Deferred | Implementation details for plan |

All critical ambiguities resolved. Ready for technical planning.

Next Steps:
1. Review updated specification
2. Validate multi-tenancy and compliance requirements
3. Run /specops.plan to create implementation design

Suggested command: 
/specops.plan Use Terraform 1.6 for AWS, Ansible 2.15 for K8s 1.28, ArgoCD 2.9 with Helm
```

---

**This clarification workflow ensures infrastructure specifications are complete, unambiguous, and ready for detailed technical planning!** 🎯
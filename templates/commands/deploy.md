````markdown
---
description: Deploy an application to Kubernetes using ArgoCD with automatic Helm/Kustomize detection. Zero YAML writing required.
handoffs: 
  - label: View Deployment Status
    agent: specops.implement
    prompt: Check the status of the deployed application
  - label: Add Another Application
    agent: specops.deploy
    prompt: Deploy another application
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Deploy applications to Kubernetes **without writing any YAML**. The agent handles everything:
- Helm chart discovery and ArgoCD Application generation
- Kustomize fallback for custom applications
- Environment-specific configurations

## Prerequisites

**MANDATORY**: Read `memory/constitution.md` for:
- Deployment Strategy Standards (Helm sources, decision criteria)
- Standard Helm Repositories table
- Starter Infrastructure Components

## Outline

1. **Parse deployment request** from `$ARGUMENTS`:
   - Application name (required)
   - Target namespace (default: app name)
   - Environment (default: dev)
   - Image/source if custom application
   - Replicas, ports, resources if specified

   **Example inputs**:
   - "nginx-ingress to infrastructure namespace"
   - "my-api with image myrepo/api:v1.0 to production"
   - "prometheus stack for monitoring"

2. **Helm Chart Discovery**:
   
   Follow the decision flow from `memory/constitution.md`:
   - Search ArtifactHub for official/community charts
   - Check standard repositories from constitution
   - Apply selection criteria (stars, maintenance, official status)
   
3. **Generate deployment artifacts**:

   ### Option A: Helm-based (chart found)
   
   1. Add Helm repository Secret to ArgoCD (if not exists)
   2. Create `values-[env].yaml` with environment-specific overrides
   3. Create ArgoCD Application pointing to Helm chart
   
   Files: `kubernetes/argocd/repositories/`, `kubernetes/infrastructure/[app]/`

   ### Option B: Kustomize-based (no chart / custom app)
   
   1. Create Kustomize base (deployment, service, ingress)
   2. Create environment overlays (dev, staging, prod)
   3. Create ArgoCD Application pointing to overlay path
   
   Files: `kubernetes/apps/[app]/base/`, `kubernetes/apps/[app]/overlays/`

4. **Commit and sync**:
   ```bash
   git add kubernetes/
   git commit -m "feat(deploy): add [APP_NAME] via [Helm/Kustomize]"
   git push
   ```

5. **Verify deployment**:
   ```bash
   argocd app get [APP_NAME] --refresh
   kubectl get pods -n [NAMESPACE] -l app=[APP_NAME]
   ```

6. **Report completion**:
   ```markdown
   ## Deployment Complete ✅
   
   **Application**: [APP_NAME]
   **Strategy**: [Helm / Kustomize]
   **Namespace**: [NAMESPACE]
   **Environment**: [ENV]
   
   ### Next Steps
   1. Monitor: `argocd app get [APP_NAME]`
   2. Logs: `kubectl logs -n [NAMESPACE] -l app=[APP_NAME]`
   ```

## Quick Deploy Examples

```bash
# Infrastructure (Helm)
/specops.deploy nginx-ingress to ingress-nginx namespace
/specops.deploy cert-manager to cert-manager namespace
/specops.deploy prometheus-stack to monitoring namespace

# Custom Apps (Kustomize)
/specops.deploy my-api with image myorg/api:v1.0 port 3000 to production
```

## Error Handling

| Error | Resolution |
|-------|------------|
| No Helm chart found | Generate Kustomize structure |
| ArgoCD not installed | Run bootstrap phase first |

## Notes

- Agent NEVER asks user to write YAML
- All manifests generated and committed to Git
- ArgoCD handles deployment via GitOps
- Refer to `memory/constitution.md` for Helm sources and standards
````
`````

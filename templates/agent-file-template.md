# [PROJECT NAME] Infrastructure Guidelines

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies

[EXTRACTED FROM ALL PLAN.MD FILES]

## Deployment Strategy

**Default**: Helm-first with Kustomize fallback (agent-managed)

| Component Type | Strategy | Source |
|----------------|----------|--------|
| Infrastructure (ingress, cert-manager) | Helm | Official repos |
| Monitoring (Prometheus, Grafana) | Helm | prometheus-community |
| GitOps (ArgoCD) | Helm | argoproj.github.io |
| Custom Applications | Kustomize | Generated manifests |
| Third-party apps with Helm chart | Helm | Discovered from ArtifactHub |
| Third-party apps without Helm | Kustomize | Generated manifests |

## Zero YAML Development

**CRITICAL**: Agent generates ALL Kubernetes manifests. Users describe intent in natural language.

**Agent workflow for deployments**:
1. Search ArtifactHub/Helm repos for existing chart
2. If chart exists → Create ArgoCD Application with Helm source
3. If no chart → Generate Kustomize base + overlays + ArgoCD Application
4. Commit to Git → ArgoCD syncs automatically

**User commands**:
```
/specops.deploy [app-name] with image [image] to [namespace]
/specops.deploy [component] to [namespace]  # Auto-discovers Helm chart
```

## Project Structure

```text
[ACTUAL STRUCTURE FROM PLANS]
```

## Standard Infrastructure Components

| Component | Helm Chart | Purpose |
|-----------|------------|---------|
| nginx-ingress | ingress-nginx | External traffic routing |
| cert-manager | cert-manager | TLS certificate automation |
| external-secrets | external-secrets | Cloud secret synchronization |
| prometheus-stack | kube-prometheus-stack | Monitoring and alerting |
| argocd | argo-cd | GitOps continuous delivery |

## Commands

[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES]

## Code Style

[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE]

## Recent Changes

[LAST 3 FEATURES AND WHAT THEY ADDED]

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
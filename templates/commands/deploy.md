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

Deploy applications to Kubernetes **without writing any YAML**. The agent:
1. Discovers if a Helm chart exists for the component
2. Generates appropriate ArgoCD Application definition
3. Creates Kustomize structure if no Helm chart available
4. Handles environment-specific configurations automatically

## Outline

1. **Parse deployment request** from `$ARGUMENTS`:
   - Extract application name (required)
   - Extract target namespace (default: app name)
   - Extract environment (default: dev)
   - Extract image/source if custom application
   - Extract replicas, ports, resources if specified

   **Example inputs**:
   - "deploy nginx-ingress to infrastructure namespace"
   - "deploy my-api with image myrepo/api:v1.0 to production"
   - "deploy prometheus stack for monitoring"
   - "deploy my-frontend from ./src with 3 replicas"

2. **Helm Chart Discovery** (MANDATORY before any manifest generation):

   a. **Search ArtifactHub** for official/community charts:
   ```bash
   curl -s "https://artifacthub.io/api/v1/packages/search?ts_query_web=[APP_NAME]&kind=0&limit=5" | jq '.packages[] | {name, repository, version, stars}'
   ```

   b. **Check common Helm repositories**:
   | Repository | URL | Common Charts |
   |------------|-----|---------------|
   | Bitnami | https://charts.bitnami.com/bitnami | nginx, postgresql, redis, mongodb |
   | Ingress-NGINX | https://kubernetes.github.io/ingress-nginx | ingress-nginx |
   | Jetstack | https://charts.jetstack.io | cert-manager |
   | Prometheus Community | https://prometheus-community.github.io/helm-charts | kube-prometheus-stack |
   | ArgoCD | https://argoproj.github.io/argo-helm | argo-cd, argo-workflows |
   | External Secrets | https://charts.external-secrets.io | external-secrets |

   c. **Decision criteria**:
   - ✅ Use Helm if: Official chart exists OR community chart has >500 stars/downloads
   - ✅ Use Helm if: Chart is actively maintained (updated within 6 months)
   - ❌ Use Kustomize if: No chart exists OR chart is abandoned
   - ❌ Use Kustomize if: Custom application code

3. **Generate deployment artifacts**:

   ### Option A: Helm-based Deployment (chart found)

   **Step 1**: Add Helm repository to ArgoCD (if not exists)
   ```yaml
   # kubernetes/argocd/repositories/[repo-name].yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: [repo-name]-repo
     namespace: argocd
     labels:
       argocd.argoproj.io/secret-type: repository
   stringData:
     name: [REPO_NAME]
     url: [REPO_URL]
     type: helm
   ```

   **Step 2**: Create values overlay
   ```yaml
   # kubernetes/infrastructure/[app-name]/values-[env].yaml
   # OR kubernetes/apps/[app-name]/values-[env].yaml
   
   # Environment-specific overrides
   replicaCount: [REPLICAS]
   image:
     tag: [VERSION]
   resources:
     requests:
       cpu: [CPU_REQUEST]
       memory: [MEM_REQUEST]
     limits:
       cpu: [CPU_LIMIT]
       memory: [MEM_LIMIT]
   ingress:
     enabled: [true/false]
     hosts:
       - host: [HOSTNAME]
   ```

   **Step 3**: Create ArgoCD Application
   ```yaml
   # kubernetes/argocd/applications/[app-name].yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: [APP_NAME]
     namespace: argocd
     finalizers:
       - resources-finalizer.argocd.argoproj.io
   spec:
     project: default
     source:
       repoURL: [HELM_REPO_URL]
       chart: [CHART_NAME]
       targetRevision: [CHART_VERSION]
       helm:
         valueFiles:
           - values-[ENV].yaml
     destination:
       server: https://kubernetes.default.svc
       namespace: [TARGET_NAMESPACE]
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
       syncOptions:
         - CreateNamespace=true
   ```

   ### Option B: Kustomize-based Deployment (no chart / custom app)

   **Step 1**: Create Kustomize base
   ```yaml
   # kubernetes/apps/[app-name]/base/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   
   resources:
     - deployment.yaml
     - service.yaml
     - ingress.yaml  # if needed
   
   commonLabels:
     app: [APP_NAME]
     managed-by: specops
   ```

   ```yaml
   # kubernetes/apps/[app-name]/base/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: [APP_NAME]
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: [APP_NAME]
     template:
       metadata:
         labels:
           app: [APP_NAME]
       spec:
         containers:
           - name: [APP_NAME]
             image: [IMAGE]
             ports:
               - containerPort: [PORT]
             resources:
               requests:
                 cpu: "100m"
                 memory: "128Mi"
               limits:
                 cpu: "500m"
                 memory: "512Mi"
             livenessProbe:
               httpGet:
                 path: /health
                 port: [PORT]
               initialDelaySeconds: 30
               periodSeconds: 10
             readinessProbe:
               httpGet:
                 path: /ready
                 port: [PORT]
               initialDelaySeconds: 5
               periodSeconds: 5
   ```

   ```yaml
   # kubernetes/apps/[app-name]/base/service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: [APP_NAME]
   spec:
     selector:
       app: [APP_NAME]
     ports:
       - port: 80
         targetPort: [PORT]
     type: ClusterIP
   ```

   **Step 2**: Create environment overlays
   ```yaml
   # kubernetes/apps/[app-name]/overlays/dev/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   
   namespace: [APP_NAME]-dev
   
   resources:
     - ../../base
   
   patches:
     - patch: |-
         - op: replace
           path: /spec/replicas
           value: 1
       target:
         kind: Deployment
         name: [APP_NAME]
   
   images:
     - name: [IMAGE]
       newTag: dev
   ```

   ```yaml
   # kubernetes/apps/[app-name]/overlays/prod/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   
   namespace: [APP_NAME]-prod
   
   resources:
     - ../../base
   
   patches:
     - patch: |-
         - op: replace
           path: /spec/replicas
           value: 3
       target:
         kind: Deployment
         name: [APP_NAME]
   
   images:
     - name: [IMAGE]
       newTag: v1.0.0
   ```

   **Step 3**: Create ArgoCD Application
   ```yaml
   # kubernetes/argocd/applications/[app-name].yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: [APP_NAME]-[ENV]
     namespace: argocd
     finalizers:
       - resources-finalizer.argocd.argoproj.io
   spec:
     project: default
     source:
       repoURL: [GIT_REPO_URL]
       path: kubernetes/apps/[APP_NAME]/overlays/[ENV]
       targetRevision: HEAD
     destination:
       server: https://kubernetes.default.svc
       namespace: [APP_NAME]-[ENV]
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
       syncOptions:
         - CreateNamespace=true
   ```

4. **Commit and sync**:
   
   a. Stage generated files:
   ```bash
   git add kubernetes/
   ```
   
   b. Commit with descriptive message:
   ```bash
   git commit -m "feat(deploy): add [APP_NAME] deployment via [Helm/Kustomize]
   
   - Deployment strategy: [Helm chart from X / Kustomize base]
   - Target namespace: [NAMESPACE]
   - Environment: [ENV]
   - ArgoCD Application: [APP_NAME]"
   ```
   
   c. Push to trigger ArgoCD sync:
   ```bash
   git push
   ```

5. **Verify deployment**:
   
   a. Check ArgoCD application status:
   ```bash
   argocd app get [APP_NAME] --refresh
   ```
   
   b. Verify pods are running:
   ```bash
   kubectl get pods -n [NAMESPACE] -l app=[APP_NAME]
   ```
   
   c. Check service endpoints:
   ```bash
   kubectl get svc -n [NAMESPACE] [APP_NAME]
   kubectl get ingress -n [NAMESPACE] [APP_NAME]
   ```

6. **Report completion**:
   
   ```markdown
   ## Deployment Complete ✅
   
   **Application**: [APP_NAME]
   **Strategy**: [Helm / Kustomize]
   **Namespace**: [NAMESPACE]
   **Environment**: [ENV]
   
   ### Files Generated
   
   | File | Purpose |
   |------|---------|
   | kubernetes/argocd/applications/[app].yaml | ArgoCD Application |
   | kubernetes/[location]/[app]/... | Deployment manifests |
   
   ### Deployment Status
   
   - ArgoCD Sync: [Synced / OutOfSync]
   - Pods: [X/Y Ready]
   - Service: [ClusterIP / LoadBalancer]
   - Ingress: [HOSTNAME or N/A]
   
   ### Next Steps
   
   1. Monitor with: `argocd app get [APP_NAME]`
   2. View logs: `kubectl logs -n [NAMESPACE] -l app=[APP_NAME]`
   3. Access app: [URL or port-forward command]
   ```

## Quick Deploy Examples

### Infrastructure Components

```bash
# Ingress controller (Helm)
/specops.deploy nginx-ingress to ingress-nginx namespace

# Certificate manager (Helm)
/specops.deploy cert-manager to cert-manager namespace

# Monitoring stack (Helm)
/specops.deploy prometheus-stack to monitoring namespace
```

### Custom Applications

```bash
# Node.js API (Kustomize)
/specops.deploy my-api with image myorg/api:v1.0 port 3000 to production

# Frontend app (Kustomize)
/specops.deploy frontend with image myorg/web:latest port 80 replicas 3 to staging

# Database (Helm - Bitnami)
/specops.deploy postgresql to database namespace with persistence enabled
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No Helm chart found | Component doesn't have public chart | Agent generates Kustomize structure |
| Chart version not found | Specified version doesn't exist | Use latest stable version |
| Namespace conflict | Namespace already has resources | Add unique suffix or use different namespace |
| ArgoCD not installed | GitOps platform not bootstrapped | Run bootstrap phase first |

## Notes

- Agent NEVER asks user to write YAML
- All manifests are generated and committed to Git
- ArgoCD handles actual deployment via GitOps
- Environment-specific configs via Helm values or Kustomize overlays
- Rollback available via ArgoCD or git revert
````

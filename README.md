# 🚀 SpecOps

**Spec-Driven Infrastructure as Code**

Build production-ready infrastructure with systematic deployment automation using Terraform, Ansible, and ArgoCD.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🤔 What is SpecOps?

SpecOps brings the **Spec-Driven Development** methodology to Infrastructure as Code. Instead of "vibe coding" your infrastructure, you:

1. **Define** infrastructure requirements clearly
2. **Plan** technical implementation systematically  
3. **Execute** with AI-assisted automation
4. **Deploy** confidently with GitOps

SpecOps is inspired by [GitHub's Spec Kit](https://github.com/github/spec-kit) and adapted specifically for infrastructure engineering.

---

## ⚡ Quick Start

### Prerequisites

- **Linux/macOS/Windows**
- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) package manager
- [Git](https://git-scm.com/downloads)
- **Infrastructure Tools**:
  - [Terraform](https://www.terraform.io/downloads) >= 1.6
  - [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/) >= 2.15
  - [kubectl](https://kubernetes.io/docs/tasks/tools/) >= 1.28
  - [Helm](https://helm.sh/docs/intro/install/) (optional)
  - [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/) (optional)

### Installation

```bash
# Install SpecOps CLI
uv tool install specops-cli --from git+https://github.com/dotlabshq/specops.git

# Verify installation
specops check
```

### Create Your First Infrastructure Project

```bash
# Initialize new project
specops init my-infrastructure --ai claude

# Navigate to project
cd my-infrastructure

# Launch your AI agent (e.g., Claude Code)
claude

# Follow the workflow:
# 1. /specops.constitution - Establish principles
# 2. /specops.specify - Define infrastructure requirements
# 3. /specops.plan - Create technical implementation plan
# 4. /specops.tasks - Generate task breakdown
# 5. /specops.implement - Execute deployment
```

---

## 🏗️ Technology Stack

SpecOps is built around a proven infrastructure stack:

| Component | Tool | Purpose |
|-----------|------|---------|
| **VM Provisioning** | Terraform | Infrastructure as Code for cloud resources |
| **K8s Setup** | Ansible | Configuration management and cluster installation |
| **App Deployment** | ArgoCD | GitOps continuous delivery |
| **Network** | Cilium | eBPF-based CNI with network policies |
| **Multi-tenancy** | Kubernetes | Namespace isolation with RBAC |

---

## 📚 Core Concepts

### Spec-Driven Infrastructure

Traditional approach:
```
💭 Idea → 🔨 Code → 📝 Documentation (maybe)
```

SpecOps approach:
```
💭 Idea → 📋 Specification → 📐 Plan → ✅ Tasks → 🚀 Implementation
```

### The Five Commands

#### 1. `/specops.constitution`
Establish your infrastructure principles and standards.

```
/specops.constitution Create principles for multi-tenant Kubernetes using Terraform, 
Ansible, ArgoCD, and Cilium. Focus on security, scalability, and operational excellence.
```

**Output**: `.specops/memory/constitution.md`

#### 2. `/specops.specify`
Define **what** you want to build and **why**.

```
/specops.specify Deploy a single sign-on (SSO) solution for our organization. 
Need to support multiple authentication providers and integrate with existing LDAP.
Must be isolated per organization using namespace boundaries.
```

**Output**: `.specops/specs/001-sso-deployment/spec.md`

#### 3. `/specops.plan`
Specify **how** to implement it technically.

```
/specops.plan Use Zitadel for SSO deployed via Helm. PostgreSQL backend in same namespace.
Configure Cilium network policies for isolation. Expose via ingress with TLS.
```

**Output**: `.specops/specs/001-sso-deployment/plan.md`

#### 4. `/specops.tasks`
Generate actionable task breakdown.

```
/specops.tasks
```

**Output**: `.specops/specs/001-sso-deployment/tasks.md`

#### 5. `/specops.implement`
Execute the implementation with AI assistance.

```
/specops.implement
```

**Result**: Working infrastructure deployed and version controlled!

---

## 🎯 Use Cases

### Multi-Organization Kubernetes Platform
Deploy a shared Kubernetes cluster with:
- Namespace-based isolation per organization
- Cilium network policies for security
- Resource quotas and limits
- GitOps deployment with ArgoCD

### Complete Application Stack
Provision end-to-end:
- VMs/cloud resources (Terraform)
- Kubernetes cluster (Ansible)
- Applications (ArgoCD)
- Monitoring (Prometheus + Grafana)
- Logging (ELK/Loki)

### Compliance-Ready Infrastructure
Build infrastructure that meets:
- Security best practices
- Audit requirements
- Disaster recovery standards
- Documentation requirements

---

## 📖 Documentation

### Getting Started
- [Installation Guide](docs/installation.md)
- [Quick Start Tutorial](docs/quickstart.md)
- [CLI Reference](docs/cli-reference.md)

### Concepts
- [Constitution Guide](docs/constitution.md)
- [Specification Writing](docs/specifications.md)
- [Multi-Tenancy Setup](docs/multi-tenancy.md)

### Examples
- [SSO Deployment](examples/sso-deployment/)
- [Monitoring Stack](examples/monitoring/)
- [CI/CD Pipeline](examples/cicd/)

---

## 🤖 Supported AI Agents

SpecOps works with popular AI coding assistants:

| Agent | Status | Notes |
|-------|--------|-------|
| [Claude Code](https://www.anthropic.com/claude-code) | ✅ Full Support | Recommended |
| [GitHub Copilot](https://code.visualstudio.com/) | ✅ Full Support | Via VS Code |
| [Cursor](https://cursor.sh/) | ✅ Full Support | |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ Full Support | |
| [Windsurf](https://windsurf.com/) | ✅ Full Support | |

---

## 🏛️ Project Structure

```
my-infrastructure/
├── terraform/              # Infrastructure provisioning
│   ├── modules/           # Reusable Terraform modules
│   └── environments/      # Environment configs (dev, prod)
├── ansible/               # Kubernetes cluster setup
│   ├── roles/            # Ansible roles
│   ├── playbooks/        # Playbooks for cluster management
│   └── inventory/        # Dynamic inventory
├── kubernetes/            # Application deployments
│   ├── argocd/           # ArgoCD setup and apps
│   ├── apps/             # Application manifests
│   ├── namespaces/       # Namespace definitions
│   └── network-policies/ # Cilium network policies
└── .specops/             # SpecOps artifacts
    ├── memory/
    │   └── constitution.md
    ├── specs/
    │   └── 001-feature/
    │       ├── spec.md
    │       ├── plan.md
    │       └── tasks.md
    └── templates/
```

---

## 🔧 CLI Reference

### Commands

```bash
# Initialize new project
specops init <project-name> [OPTIONS]

# Check installed tools
specops check

# Version information
specops --version
```

### Options

```bash
--ai <agent>              # AI agent: claude, copilot, cursor, gemini, windsurf
--script <type>           # Script type: sh (bash) or ps (PowerShell)
--here                    # Initialize in current directory
--force                   # Force overwrite in non-empty directory
--no-git                  # Skip git initialization
--ignore-agent-tools      # Skip AI agent checks
--debug                   # Enable debug output
```

### Examples

```bash
# Basic initialization
specops init my-infra --ai claude

# Initialize in current directory
specops init . --ai copilot
specops init --here --ai cursor

# Force overwrite
specops init . --force --ai claude

# Skip git initialization
specops init my-infra --ai gemini --no-git

# Debug mode
specops init my-infra --ai claude --debug
```

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dotlabshq/specops.git
cd specops

# Install dependencies
uv sync

# Install in editable mode
uv pip install -e .

# Run CLI
specops --help
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=specops_cli

# Run specific test
pytest tests/test_cli.py
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas We Need Help

- Additional AI agent integrations
- Cloud provider templates (AWS, Azure, GCP)
- Example infrastructure patterns
- Documentation improvements
- Bug fixes and testing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit)
- Built on top of industry-standard tools: Terraform, Ansible, Kubernetes, ArgoCD, Cilium

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dotlabshq/specops/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dotlabshq/specops/discussions)
- **Documentation**: [docs/](docs/)

---

**Built with ❤️ for infrastructure engineers who believe in systematic, spec-driven automation.**
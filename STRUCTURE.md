# SpecOps Project Structure

## Overview
Complete Spec-Driven Infrastructure as Code toolkit

## Directory Structure

```
specops/
├── src/specops_cli/              # CLI Source Code
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Direct execution support
│   ├── cli.py                   # Main CLI commands
│   ├── init.py                  # Project initialization
│   ├── check.py                 # Tool verification
│   └── utils.py                 # Utility functions
│
├── base/                         # Base Templates
│   ├── memory/
│   │   └── constitution-template.md
│   └── templates/
│       ├── spec-template.md
│       ├── plan-template.md
│       └── tasks-template.md
│
├── templates/                    # AI Agent Templates
│   └── claude/                  # Claude Code templates
│       └── sh/                  # Bash script variant
│           ├── CLAUDE.md        # Claude instructions
│           └── .specops/
│               ├── prompts/     # Slash command prompts
│               │   ├── constitution.md
│               │   ├── specify.md
│               │   ├── plan.md
│               │   ├── tasks.md
│               │   └── implement.md
│               ├── scripts/     # Helper scripts
│               │   ├── common.sh
│               │   ├── create-new-feature.sh
│               │   └── setup-plan.sh
│               └── templates/   # Document templates
│                   ├── constitution-template.md
│                   ├── spec-template.md
│                   ├── plan-template.md
│                   └── tasks-template.md
│
├── pyproject.toml               # Python package config
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
└── STRUCTURE.md                 # This file
```

## File Count

- **Python Files**: 6
- **Template Files**: 8
- **Prompt Files**: 5
- **Script Files**: 3
- **Documentation**: 4
- **Total**: 26+ files

## Installation

```bash
uv tool install specops-cli --from git+https://github.com/dotlabshq/specops.git
```

## Usage

```bash
# Initialize project
specops init my-infra --ai claude

# Check tools
specops check

# Work with AI agent
cd my-infra
claude  # or your AI agent

# Use commands
/specops.constitution
/specops.specify
/specops.plan
/specops.tasks
/specops.implement
```

## Key Features

✅ Spec Kit compatible workflow
✅ Infrastructure-focused templates  
✅ Multi-tenancy support (Cilium)
✅ Terraform + Ansible + ArgoCD
✅ Comprehensive documentation
✅ Helper scripts for automation
✅ Validation at every step

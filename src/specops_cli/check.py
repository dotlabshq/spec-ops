"""
Check command for SpecOps CLI - verifies installed infrastructure tools
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from specops_cli.utils import check_tool_installed

console = Console()


# Infrastructure tools to check
INFRASTRUCTURE_TOOLS = {
    "git": {
        "name": "Git",
        "description": "Version control system",
        "required": True,
    },
    "terraform": {
        "name": "Terraform",
        "description": "Infrastructure provisioning",
        "required": True,
    },
    "ansible": {
        "name": "Ansible",
        "description": "Configuration management",
        "required": True,
    },
    "kubectl": {
        "name": "kubectl",
        "description": "Kubernetes CLI",
        "required": True,
    },
    "helm": {
        "name": "Helm",
        "description": "Kubernetes package manager",
        "required": False,
    },
    "argocd": {
        "name": "ArgoCD CLI",
        "description": "GitOps continuous delivery",
        "required": False,
    },
}

# AI agents to check
AI_AGENTS = {
    "claude": {
        "name": "Claude Code",
        "description": "Anthropic's AI assistant",
    },
    "cursor": {
        "name": "Cursor",
        "description": "AI-powered code editor",
    },
    "code": {
        "name": "VS Code",
        "description": "Visual Studio Code (for Copilot)",
    },
}


def check_command() -> None:
    """
    Check for installed infrastructure tools and AI agents.
    """
    console.print()
    console.print(
        Panel(
            "[bold cyan]SpecOps Tool Checker[/bold cyan]\n"
            "Verifying installed infrastructure tools and AI agents",
            border_style="cyan",
        )
    )
    console.print()

    # Check infrastructure tools
    infra_table = Table(title="Infrastructure Tools", show_header=True, header_style="bold magenta")
    infra_table.add_column("Tool", style="cyan", width=15)
    infra_table.add_column("Status", width=10)
    infra_table.add_column("Description", style="dim")
    infra_table.add_column("Required", width=10)

    missing_required = []
    
    for tool_cmd, tool_info in INFRASTRUCTURE_TOOLS.items():
        installed = check_tool_installed(tool_cmd)
        status = "[green]✓ Installed[/green]" if installed else "[red]✗ Missing[/red]"
        required = "[yellow]Required[/yellow]" if tool_info["required"] else "[dim]Optional[/dim]"
        
        if not installed and tool_info["required"]:
            missing_required.append(tool_info["name"])
        
        infra_table.add_row(
            tool_info["name"],
            status,
            tool_info["description"],
            required,
        )

    console.print(infra_table)
    console.print()

    # Check AI agents
    ai_table = Table(title="AI Agents", show_header=True, header_style="bold magenta")
    ai_table.add_column("Agent", style="cyan", width=15)
    ai_table.add_column("Status", width=10)
    ai_table.add_column("Description", style="dim")

    for agent_cmd, agent_info in AI_AGENTS.items():
        installed = check_tool_installed(agent_cmd)
        status = "[green]✓ Installed[/green]" if installed else "[dim]✗ Not found[/dim]"
        
        ai_table.add_row(
            agent_info["name"],
            status,
            agent_info["description"],
        )

    console.print(ai_table)
    console.print()

    # Summary
    if missing_required:
        console.print(
            Panel(
                f"[yellow]⚠ Missing required tools:[/yellow]\n"
                + "\n".join(f"  • {tool}" for tool in missing_required)
                + "\n\n[dim]Please install missing tools before proceeding.[/dim]",
                border_style="yellow",
                title="Warning",
            )
        )
    else:
        console.print(
            Panel(
                "[green]✓ All required infrastructure tools are installed![/green]\n"
                "[dim]You're ready to start using SpecOps.[/dim]",
                border_style="green",
                title="Success",
            )
        )
    
    console.print()
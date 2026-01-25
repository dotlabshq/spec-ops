"""
SpecOps CLI - Spec-Driven Infrastructure as Code toolkit
"""
import click
from rich.console import Console
from rich.panel import Panel

from specops_cli.init import init_command
from specops_cli.check import check_command

console = Console()

__version__ = "0.0.1"


@click.group()
@click.version_option(version=__version__, prog_name="specops")
def main() -> None:
    """
    SpecOps - Spec-Driven Infrastructure as Code
    
    Build production-ready infrastructure with systematic deployment automation.
    """
    pass


@main.command(name="init")
@click.argument("project_name", required=False, default=".")
@click.option(
    "--ai",
    type=click.Choice(
        ["claude", "copilot", "cursor", "gemini", "windsurf"],
        case_sensitive=False
    ),
    help="AI assistant to use for infrastructure development",
)
@click.option(
    "--script",
    type=click.Choice(["sh", "ps"], case_sensitive=False),
    default="sh",
    help="Script variant: sh (bash/zsh) or ps (PowerShell)",
)
@click.option(
    "--ignore-agent-tools",
    is_flag=True,
    help="Skip checks for AI agent tools",
)
@click.option(
    "--no-git",
    is_flag=True,
    help="Skip git repository initialization",
)
@click.option(
    "--here",
    is_flag=True,
    help="Initialize project in current directory",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force overwrite when initializing in non-empty directory",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable detailed debug output",
)
def init(
    project_name: str,
    ai: str | None,
    script: str,
    ignore_agent_tools: bool,
    no_git: bool,
    here: bool,
    force: bool,
    debug: bool,
) -> None:
    """
    Initialize a new SpecOps project from the latest template.
    
    Examples:
    
        \b
        # Basic project initialization
        specops init my-infrastructure
        
        \b
        # Initialize with specific AI assistant
        specops init my-infra --ai claude
        
        \b
        # Initialize in current directory
        specops init . --ai claude
        # or
        specops init --here --ai claude
        
        \b
        # Force overwrite in non-empty directory
        specops init . --force --ai claude
    """
    init_command(
        project_name=project_name,
        ai=ai,
        script=script,
        ignore_agent_tools=ignore_agent_tools,
        no_git=no_git,
        here=here,
        force=force,
        debug=debug,
    )


@main.command(name="check")
def check() -> None:
    """
    Check for installed infrastructure tools.
    
    Verifies the presence of:
    - git
    - terraform
    - ansible
    - kubectl
    - helm
    - argocd
    - AI agents (claude, etc.)
    """
    check_command()


if __name__ == "__main__":
    main()
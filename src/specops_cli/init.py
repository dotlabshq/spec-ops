"""
Init command for SpecOps CLI - initializes new infrastructure projects
"""
import os
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich import print as rprint

from specops_cli.utils import (
    check_tool_installed,
    ensure_directory,
    copy_template_files,
    run_command,
    is_git_repository,
)

console = Console()


# Supported AI agents
SUPPORTED_AGENTS = {
    "claude": "Claude Code",
    "copilot": "GitHub Copilot",
    "cursor": "Cursor",
    "gemini": "Gemini CLI",
    "windsurf": "Windsurf",
}


def prompt_for_ai_agent() -> str:
    """
    Interactively prompt user to select an AI agent.
    
    Returns:
        Selected AI agent key
    """
    console.print()
    console.print("[bold cyan]Select AI Agent[/bold cyan]")
    console.print()
    
    for i, (key, name) in enumerate(SUPPORTED_AGENTS.items(), 1):
        console.print(f"  {i}. {name}")
    
    console.print()
    
    while True:
        choice = Prompt.ask(
            "Which AI agent would you like to use?",
            choices=[str(i) for i in range(1, len(SUPPORTED_AGENTS) + 1)],
        )
        
        agent_key = list(SUPPORTED_AGENTS.keys())[int(choice) - 1]
        return agent_key


def get_template_path(ai_agent: str, script_type: str) -> Path:
    """
    Get the template directory path for the specified AI agent and script type.
    
    Args:
        ai_agent: AI agent identifier
        script_type: Script type (sh or ps)
        
    Returns:
        Path to template directory
    """
    # In production, this would be in the installed package
    # For now, we'll use a relative path from the CLI module
    cli_dir = Path(__file__).parent
    package_root = cli_dir.parent.parent
    template_dir = package_root / "templates" / ai_agent / script_type
    
    if not template_dir.exists():
        console.print(f"[red]Error: Template directory not found: {template_dir}[/red]")
        sys.exit(1)
    
    return template_dir


def initialize_git_repository(project_dir: Path, debug: bool = False) -> None:
    """
    Initialize a git repository in the project directory.
    
    Args:
        project_dir: Project directory path
        debug: Whether to print debug information
    """
    if is_git_repository(project_dir):
        if debug:
            console.print("[dim]Git repository already exists[/dim]")
        return
    
    console.print("[cyan]Initializing git repository...[/cyan]")
    run_command(["git", "init"], cwd=project_dir, debug=debug)
    run_command(
        ["git", "config", "user.name", "SpecOps"],
        cwd=project_dir,
        check=False,
        debug=debug,
    )
    run_command(
        ["git", "config", "user.email", "specops@local"],
        cwd=project_dir,
        check=False,
        debug=debug,
    )
    
    # Create initial commit
    run_command(["git", "add", "."], cwd=project_dir, debug=debug)
    run_command(
        ["git", "commit", "-m", "Initial SpecOps project setup"],
        cwd=project_dir,
        check=False,
        debug=debug,
    )
    
    console.print("[green]✓[/green] Git repository initialized")


def check_required_tools(ignore_agent_tools: bool = False, debug: bool = False) -> bool:
    """
    Check if required tools are installed.
    
    Args:
        ignore_agent_tools: Skip AI agent tool checks
        debug: Whether to print debug information
        
    Returns:
        True if all required tools are present, False otherwise
    """
    required_tools = ["git", "terraform", "ansible", "kubectl"]
    missing_tools = []
    
    for tool in required_tools:
        if not check_tool_installed(tool, debug=debug):
            missing_tools.append(tool)
    
    if missing_tools:
        console.print()
        console.print(
            Panel(
                "[red]✗ Missing required tools:[/red]\n"
                + "\n".join(f"  • {tool}" for tool in missing_tools)
                + "\n\n[dim]Run 'specops check' for more details.[/dim]",
                border_style="red",
                title="Error",
            )
        )
        return False
    
    return True


def init_command(
    project_name: str,
    ai: Optional[str],
    script: str,
    ignore_agent_tools: bool,
    no_git: bool,
    here: bool,
    force: bool,
    debug: bool,
) -> None:
    """
    Initialize a new SpecOps project.
    
    Args:
        project_name: Name of the project or "." for current directory
        ai: AI agent to use
        script: Script type (sh or ps)
        ignore_agent_tools: Skip AI agent tool checks
        no_git: Skip git initialization
        here: Initialize in current directory
        force: Force overwrite in non-empty directory
        debug: Enable debug output
    """
    console.print()
    console.print(
        Panel(
            "[bold cyan]SpecOps Initialization[/bold cyan]\n"
            "Setting up your Infrastructure as Code project",
            border_style="cyan",
        )
    )
    console.print()
    
    # Check required tools
    if not check_required_tools(ignore_agent_tools, debug):
        sys.exit(1)
    
    # Determine project directory
    if here or project_name == ".":
        project_dir = Path.cwd()
        console.print(f"[cyan]Initializing in current directory:[/cyan] {project_dir}")
    else:
        project_dir = Path.cwd() / project_name
        console.print(f"[cyan]Creating project:[/cyan] {project_name}")
    
    # Check if directory exists and is not empty
    if project_dir.exists() and any(project_dir.iterdir()):
        if not force:
            console.print()
            console.print(f"[yellow]Directory is not empty:[/yellow] {project_dir}")
            if not Confirm.ask("Do you want to merge/overwrite?"):
                console.print("[red]Aborted.[/red]")
                sys.exit(1)
    
    # Ensure project directory exists
    ensure_directory(project_dir, debug=debug)
    
    # Prompt for AI agent if not specified
    if not ai:
        ai = prompt_for_ai_agent()
    
    if ai not in SUPPORTED_AGENTS:
        console.print(f"[red]Error: Unsupported AI agent: {ai}[/red]")
        console.print(f"[dim]Supported agents: {', '.join(SUPPORTED_AGENTS.keys())}[/dim]")
        sys.exit(1)
    
    console.print(f"[cyan]AI Agent:[/cyan] {SUPPORTED_AGENTS[ai]}")
    console.print(f"[cyan]Script Type:[/cyan] {script}")
    console.print()
    
    # Get template path
    template_dir = get_template_path(ai, script)
    
    # Copy template files
    console.print("[cyan]Copying template files...[/cyan]")
    copy_template_files(template_dir, project_dir, debug=debug)
    console.print("[green]✓[/green] Template files copied")
    
    # Initialize git repository
    if not no_git:
        initialize_git_repository(project_dir, debug=debug)
    
    # Success message
    console.print()
    console.print(
        Panel(
            "[bold green]✓ SpecOps project initialized successfully![/bold green]\n\n"
            "[cyan]Next steps:[/cyan]\n"
            f"  1. cd {project_name if project_name != '.' else project_dir.name}\n"
            f"  2. Launch your AI agent ({SUPPORTED_AGENTS[ai]})\n"
            "  3. Run [bold]/specops.constitution[/bold] to establish principles\n"
            "  4. Run [bold]/specops.specify[/bold] to define infrastructure requirements\n\n"
            "[dim]For detailed documentation, visit:[/dim]\n"
            "[link]https://github.com/dotlabshq/specops[/link]",
            border_style="green",
            title="Success",
        )
    )
    console.print()
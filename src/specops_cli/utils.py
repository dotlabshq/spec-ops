"""
Utility functions for SpecOps CLI
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def run_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    capture_output: bool = False,
    check: bool = True,
    debug: bool = False,
) -> subprocess.CompletedProcess:
    """
    Run a shell command with optional output capture.
    
    Args:
        cmd: Command and arguments as list
        cwd: Working directory
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        debug: Whether to print debug information
        
    Returns:
        CompletedProcess instance
    """
    if debug:
        console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")
    
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=check,
    )


def check_tool_installed(tool: str, debug: bool = False) -> bool:
    """
    Check if a tool is installed and available in PATH.
    
    Args:
        tool: Tool name to check
        debug: Whether to print debug information
        
    Returns:
        True if tool is installed, False otherwise
    """
    result = shutil.which(tool)
    if debug:
        status = "✓" if result else "✗"
        console.print(f"[dim]{status} {tool}: {result or 'not found'}[/dim]")
    return result is not None


def ensure_directory(path: Path, debug: bool = False) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        debug: Whether to print debug information
    """
    if not path.exists():
        if debug:
            console.print(f"[dim]Creating directory: {path}[/dim]")
        path.mkdir(parents=True, exist_ok=True)
    elif debug:
        console.print(f"[dim]Directory exists: {path}[/dim]")


def copy_template_files(
    source_dir: Path,
    dest_dir: Path,
    debug: bool = False,
) -> None:
    """
    Copy template files from source to destination.
    
    Args:
        source_dir: Source template directory
        dest_dir: Destination project directory
        debug: Whether to print debug information
    """
    if debug:
        console.print(f"[dim]Copying from {source_dir} to {dest_dir}[/dim]")
    
    for item in source_dir.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(source_dir)
            dest_path = dest_dir / relative_path
            
            ensure_directory(dest_path.parent, debug=debug)
            
            if debug:
                console.print(f"[dim]  Copying: {relative_path}[/dim]")
            
            shutil.copy2(item, dest_path)


def get_git_branch() -> Optional[str]:
    """
    Get current git branch name.
    
    Returns:
        Branch name or None if not in a git repository
    """
    try:
        result = run_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def is_git_repository(path: Optional[Path] = None) -> bool:
    """
    Check if the given path is inside a git repository.
    
    Args:
        path: Path to check (defaults to current directory)
        
    Returns:
        True if inside a git repository, False otherwise
    """
    try:
        result = run_command(
            ["git", "rev-parse", "--git-dir"],
            cwd=path,
            capture_output=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False
#!/usr/bin/env python3
"""
Modern Git Repository Manager
Version: 3.0 - 2025 Python Edition
Purpose: Manage multiple git repositories with style and reliability
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.status import Status
from rich.table import Table
from rich.text import Text

# Initialize Rich console
console = Console()

# Configuration
CONFIG_FILE = Path.home() / ".git_manager_config.yaml"
DEFAULT_CONFIG = {
    "git_server": "zimagitea",
    "preferred_repos": ["hrb", "shp", "gaming", "work"],
    "log_level": "INFO",
    "auto_create_config": True
}


class GitRepository:
    """Represents a git repository with its status and operations."""
    
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self._branch = None
        self._status = None
        self._ahead = None
        self._behind = None
        self._is_dirty = None
        
    def __str__(self):
        return f"GitRepository({self.name})"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def is_git_repo(self) -> bool:
        """Check if this is a valid git repository."""
        return (self.path / ".git").exists()
    
    @property
    def branch(self) -> str:
        """Get current branch name."""
        if self._branch is None:
            try:
                result = subprocess.run(
                    ["git", "-C", str(self.path), "branch", "--show-current"],
                    capture_output=True, text=True, timeout=10
                )
                self._branch = result.stdout.strip() or "unknown"
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                self._branch = "unknown"
        return self._branch
    
    @property
    def status_info(self) -> Dict[str, int]:
        """Get repository status information."""
        if self._status is None:
            try:
                # Get uncommitted changes count
                result = subprocess.run(
                    ["git", "-C", str(self.path), "status", "--porcelain"],
                    capture_output=True, text=True, timeout=10
                )
                uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                
                # Get ahead/behind info
                try:
                    ahead_result = subprocess.run(
                        ["git", "-C", str(self.path), "rev-list", "--count", "@{u}..HEAD"],
                        capture_output=True, text=True, timeout=10
                    )
                    ahead = int(ahead_result.stdout.strip()) if ahead_result.returncode == 0 else 0
                except:
                    ahead = 0
                
                try:
                    behind_result = subprocess.run(
                        ["git", "-C", str(self.path), "rev-list", "--count", "HEAD..@{u}"],
                        capture_output=True, text=True, timeout=10
                    )
                    behind = int(behind_result.stdout.strip()) if behind_result.returncode == 0 else 0
                except:
                    behind = 0
                
                self._status = {
                    "uncommitted": uncommitted,
                    "ahead": ahead,
                    "behind": behind
                }
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                self._status = {"uncommitted": 0, "ahead": 0, "behind": 0}
        
        return self._status
    
    @property
    def is_clean(self) -> bool:
        """Check if working directory is clean."""
        return self.status_info["uncommitted"] == 0
    
    def execute_git_command(self, command: str, timeout: int = 30) -> Tuple[bool, str, str]:
        """Execute a git command and return success, stdout, stderr."""
        try:
            result = subprocess.run(
                f"git -C {self.path} {command}".split(),
                capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, "", str(e)


class GitManager:
    """Main git repository manager class."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_FILE
        self.config = self._load_config()
        self.repos: List[GitRepository] = []
        self.operation_results = {"success": [], "failed": []}
        
        # Setup logging
        self._setup_logging()
        
        # Discover repositories
        self._discover_repositories()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
                # Merge with defaults
                merged_config = {**DEFAULT_CONFIG, **config}
                return merged_config
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load config file: {e}[/yellow]")
                return DEFAULT_CONFIG
        else:
            # Create default config file
            self._create_default_config()
            return DEFAULT_CONFIG
    
    def _create_default_config(self):
        """Create a default configuration file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, indent=2)
            console.print(f"[green]Created default config file at {self.config_path}[/green]")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not create config file: {e}[/yellow]")
    
    def _setup_logging(self):
        """Setup logging with timestamped files, keeping only 5 most recent."""
        log_level = getattr(logging, self.config.get("log_level", "INFO").upper())
        
        # Clean up old logs first (keep 5 most recent)
        self._cleanup_old_logs(keep_count=5)
        
        # Create new timestamped log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = Path.home() / f"git_operations_{timestamp}.log"
        
        # Simple file handler - no rotation needed
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        console_handler = RichHandler(console=console, show_time=False, show_path=False)
        
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler]
        )
        
        self.logger = logging.getLogger(__name__)
        self.log_file = log_file
        self.logger.info(f"Git Manager started - Log file: {log_file}")

    def _cleanup_old_logs(self, keep_count: int = 5):
        """Keep only the most recent N timestamped log files."""
        log_files = sorted(
            Path.home().glob("git_operations_*.log"),
            key=lambda p: p.stat().st_mtime,
            reverse=True  # Newest first
        )
        
        # Delete older files beyond our limit
        for old_log in log_files[keep_count:]:
            try:
                old_log.unlink()
            except OSError:
                pass
    
    def _discover_repositories(self):
        """Discover git repositories in current directory."""
        current_dir = Path.cwd()
        self.logger.info(f"Discovering repositories in {current_dir}")
        
        # Get preferred repos first
        preferred_repos = self.config.get("preferred_repos", [])
        found_repos = []
        
        # Check for preferred repos
        for repo_name in preferred_repos:
            repo_path = current_dir / repo_name
            if repo_path.exists() and (repo_path / ".git").exists():
                found_repos.append(GitRepository(repo_path))
                self.logger.info(f"Found preferred repository: {repo_name}")
        
        # Discover other git repos in current directory
        for item in current_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                # Skip if already in preferred repos
                if not any(repo.name == item.name for repo in found_repos):
                    found_repos.append(GitRepository(item))
                    self.logger.info(f"Discovered repository: {item.name}")
        
        self.repos = found_repos
        
        if not self.repos:
            console.print("[red]No git repositories found in current directory![/red]")
            sys.exit(1)
        
        console.print(f"[green]Found {len(self.repos)} repositories: {', '.join(repo.name for repo in self.repos)}[/green]")
    
    def check_git_server(self) -> bool:
        """Check SSH connectivity to git server."""
        git_server = self.config.get("git_server", "zimagitea")
        
        with Status(f"[cyan]Checking connectivity to {git_server}...", console=console):
            try:
                result = subprocess.run(
                    ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes", git_server],
                    capture_output=True, text=True, timeout=10
                )
                
                # For Gitea, we expect specific messages
                output = result.stderr + result.stdout
                if "successfully authenticated" in output or "does not provide shell access" in output:
                    self.logger.info(f"SSH connection to {git_server} successful")
                    return True
                else:
                    self.logger.warning(f"Cannot connect to {git_server} via SSH")
                    return False
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                self.logger.error(f"Git server check failed: {e}")
                return False
    
    def show_header(self, online: bool = True):
        """Display fancy header."""
        if online:
            header_text = Text("🚀 GIT REPOSITORY MANAGER", style="bold green")
            status_text = Text("✅ Git server (zimagitea) is online and ready!", style="green")
        else:
            header_text = Text("⚠️  GIT REPOSITORY MANAGER", style="bold yellow")
            status_text = Text("❌ Git server (zimagitea) is not accessible!", style="red")
        
        panel_content = Text()
        panel_content.append(header_text)
        panel_content.append("\n")
        panel_content.append(status_text)
        panel_content.append(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="cyan")
        
        console.print(Panel(panel_content, title="Modern Git Manager v3.0", border_style="cyan", padding=(0, 1), width=50))
    
    def show_repository_summary(self):
        """Display repository summary table."""
        table = Table(title="Repository Summary", show_header=True, header_style="bold magenta")
        table.add_column("Repository", style="cyan", no_wrap=True)
        table.add_column("Branch", style="green")
        table.add_column("Status", justify="center")
        table.add_column("Changes", justify="center")
        table.add_column("Sync Status", justify="center")
        
        for repo in self.repos:
            # Get repository information
            branch = repo.branch
            status_info = repo.status_info
            
            # Status indicators
            if repo.is_clean:
                status = Text("✅ Clean", style="green")
            else:
                status = Text(f"⚠️  {status_info['uncommitted']} changes", style="yellow")
            
            # Changes
            changes = str(status_info['uncommitted']) if status_info['uncommitted'] > 0 else "-"
            
            # Sync status
            sync_parts = []
            if status_info['ahead'] > 0:
                sync_parts.append(f"↑{status_info['ahead']}")
            if status_info['behind'] > 0:
                sync_parts.append(f"↓{status_info['behind']}")
            
            sync_status = " ".join(sync_parts) if sync_parts else "✅"
            
            table.add_row(repo.name, branch, status, changes, sync_status)
        
        console.print(table)
    
    def show_menu(self) -> str:
        """Show interactive menu and get user choice."""
        menu_options = {
            "s": "Show status",
            "a": "Add all changes (git add .)",
            "c": "Commit changes",
            "p": "Pull from remote",
            "P": "Push to remote",
            "l": "Show recent log",
            "d": "Show diff",
            "b": "Show branches",
            "r": "Refresh repository summary",
            "f": "Fetch from remote",
            "t": "Show tags",
            "q": "Quit"
        }
        
        console.print("\n[bold cyan]🚀 Git Operation Menu[/bold cyan]")
        
        for key, description in menu_options.items():
            style = "red" if key == "q" else "green"
            console.print(f"[{style}]{key}[/{style}] - {description}")
        
        return Prompt.ask("\n[cyan]Choose an operation", choices=list(menu_options.keys()))
    
    def handle_commit(self, message: Optional[str] = None) -> Optional[str]:
        """Handle commit operation with message input."""
        if not message:
            message = Prompt.ask("[cyan]📝 Enter your commit message")
        
        if not message or len(message.strip()) < 3:
            console.print("[red]❌ Commit message must be at least 3 characters long[/red]")
            return None
        
        self.logger.info(f"Preparing commit with message: '{message}'")
        return f'commit -m "{message.strip()}"'
    
    def execute_operation(self, operation: str, repos: Optional[List[GitRepository]] = None):
        """Execute git operation on repositories with live progress."""
        if repos is None:
            repos = self.repos
        
        # Handle special operations
        if operation == "REPO_SUMMARY":
            self.show_repository_summary()
            return
        
        # Reset operation results
        self.operation_results = {"success": [], "failed": []}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            main_task = progress.add_task(f"[cyan]Executing: git {operation}", total=len(repos))
            
            for repo in repos:
                repo_task = progress.add_task(f"[yellow]Processing {repo.name}...", total=1)
                
                # Execute the git command
                success, stdout, stderr = repo.execute_git_command(operation)
                
                if success:
                    self.operation_results["success"].append(f"{repo.name}: {operation}")
                    self.logger.info(f"✅ {repo.name}: git {operation} completed")
                    
                    # Show output if not empty
                    if stdout.strip():
                        console.print(f"\n[green]📁 {repo.name}:[/green]")
                        console.print(stdout.strip())
                else:
                    self.operation_results["failed"].append(f"{repo.name}: {operation}")
                    self.logger.error(f"❌ {repo.name}: git {operation} failed")
                    
                    if stderr.strip():
                        console.print(f"\n[red]📁 {repo.name} - Error:[/red]")
                        console.print(f"[red]{stderr.strip()}[/red]")
                
                progress.update(repo_task, completed=1)
                progress.update(main_task, advance=1)
                
                # Small delay for visual effect
                time.sleep(0.1)
    
    def print_operation_summary(self):
        """Print summary of operations."""
        if not self.operation_results["success"] and not self.operation_results["failed"]:
            return
        
        table = Table(title="Operation Summary", show_header=True)
        table.add_column("Status", justify="center", style="bold")
        table.add_column("Repository & Operation", style="cyan")
        
        # Add successful operations
        for op in self.operation_results["success"]:
            table.add_row("✅", op)
        
        # Add failed operations
        for op in self.operation_results["failed"]:
            table.add_row("❌", op)
        
        console.print(table)
        
        # Calculate success rate
        total = len(self.operation_results["success"]) + len(self.operation_results["failed"])
        if total > 0:
            success_rate = len(self.operation_results["success"]) * 100 // total
            console.print(f"\n[cyan]📊 Success Rate: {success_rate}% ({total} total operations)[/cyan]")
        
        console.print(f"[blue]📄 Detailed log saved to: {self.log_file}[/blue]")
    
    def run_interactive(self):
        """Run in interactive mode."""
        # Show initial summary
        self.show_repository_summary()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == "q":
                    console.print("[cyan]👋 Goodbye![/cyan]")
                    break
                elif choice == "r":
                    # Refresh repository data
                    for repo in self.repos:
                        repo._branch = None
                        repo._status = None
                    self.show_repository_summary()
                    continue
                elif choice == "c":
                    # Handle commit with message input
                    operation = self.handle_commit()
                    if not operation:
                        continue
                else:
                    # Map choices to git commands
                    command_map = {
                        "s": "status --short --branch",
                        "a": "add .",
                        "p": "pull",
                        "P": "push",
                        "l": "log --oneline -10",
                        "d": "diff --stat",
                        "b": "branch -v",
                        "f": "fetch",
                        "t": "tag -l"
                    }
                    operation = command_map.get(choice)
                
                if operation:
                    console.print()
                    self.execute_operation(operation)
                    
                    # Ask to continue
                    console.print()
                    if not Confirm.ask("Continue with another operation?", default=True):
                        break
                        
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Operation cancelled by user[/yellow]")
                break
        
        # Show final summary
        self.print_operation_summary()
    
    def run_command(self, command: str, commit_message: Optional[str] = None):
        """Run a single command."""
        # Normalize command (support both shortcuts and full names)
        command_aliases = {
            "s": "status",
            "a": "add", 
            "c": "commit",
            "p": "pull",
            "P": "push",
            "l": "log",
            "d": "diff",
            "b": "branches",
            "f": "fetch",
            "t": "tags",
            "r": "summary"
        }
        
        # Convert shortcut to full command if needed
        normalized_command = command_aliases.get(command, command)
        
        if normalized_command == "commit":
            operation = self.handle_commit(commit_message)
            if not operation:
                return
        else:
            # Map command to git operation
            command_map = {
                "status": "status --short --branch",
                "add": "add .",
                "pull": "pull",
                "push": "push",
                "log": "log --oneline -10",
                "diff": "diff --stat",
                "branches": "branch -v",
                "fetch": "fetch",
                "tags": "tag -l"
            }
            operation = command_map.get(normalized_command, normalized_command)
        
        if normalized_command == "summary":
            self.show_repository_summary()
        else:
            self.execute_operation(operation)
            self.print_operation_summary()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Modern Git Repository Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Interactive mode
  %(prog)s status                   # Show status of all repos
  %(prog)s s                        # Same as above (shortcut)
  %(prog)s commit -m "Fix bug"      # Commit with message
  %(prog)s c -m "Fix bug"           # Same as above (shortcut)
  %(prog)s pull                     # Pull all repos
  %(prog)s p                        # Same as above (shortcut)
  %(prog)s push                     # Push all repos
  %(prog)s P                        # Same as above (shortcut)
  %(prog)s summary                  # Show repository summary
  %(prog)s r                        # Same as above (shortcut)
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["status", "s", "add", "a", "commit", "c", "pull", "p", "push", "P", "log", "l", "diff", "d", "branches", "b", "fetch", "f", "tags", "t", "summary", "r"],
        help="Git command to execute on all repositories (accepts both full names and single-letter shortcuts)"
    )
    
    parser.add_argument(
        "-m", "--message",
        help="Commit message (only used with commit command)"
    )
    
    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Git Manager 3.0 - Python Edition"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize git manager
        manager = GitManager(args.config)
        
        # Check git server connectivity
        server_online = manager.check_git_server()
        manager.show_header(server_online)
        
        if not server_online:
            console.print("\n[yellow]⚠️  Some operations may fail without server connectivity[/yellow]")
            if not Confirm.ask("Continue anyway?", default=False):
                sys.exit(1)
        
        # Run in appropriate mode
        if args.command:
            manager.run_command(args.command, args.message)
        else:
            manager.run_interactive()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")
        logging.exception("Fatal error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()

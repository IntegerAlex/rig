#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""
Beautiful system setup tool with rich UI and comprehensive error handling.
Migrated from new1.sh with enhanced features.
"""

import sys
import time
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback
from rich.spinner import Spinner
from contextlib import contextmanager

from utils import SetupLogger, CommandRunner, InstallerResult, InstallOption, BaseInstaller
from utils.shell_config import update_shell_config
from utils.errors import RigError
from installers import (
    BootstrapInstaller,
    GitHubCLIInstaller,
    UVInstaller,
    NodeJSInstaller,
    PNPMInstaller,
    NeovimInstaller,
    BTopInstaller,
    NginxInstaller,
    CertbotInstaller,
    UFWInstaller,
    Fail2banInstaller,
    ImageViewerInstaller,
    CurlpadInstaller,
    DevToolsInstaller,
    SSHKeyInstaller,
    FastfetchInstaller,
    PodmanInstaller,
    ZshInstaller,
    GitInstaller,
    RkhunterInstaller,
    ChkrootkitInstaller,
    VRMSInstaller,
)

# Install rich traceback for better error display
install_rich_traceback(show_locals=True)

# Initialize console
console = Console()


@contextmanager
def spinner_context(message: str):
    """Context manager for showing a spinner during operations."""
    spinner = Spinner("dots", text=message)
    with console.status(spinner) as status:
        try:
            yield
        finally:
            status.stop()


class SetupManager:
    """Main setup manager with beautiful UI."""
    
    def __init__(self):
        self.logger = SetupLogger()
        self.runner = CommandRunner(self.logger)
        self.console = console
        self.install_options = self._create_install_options()
        self.results: List[tuple[str, InstallerResult]] = []
    
    def _create_install_options(self) -> List[InstallOption]:
        """Create list of installation options."""
        return [
            InstallOption(
                "Bootstrap",
                BootstrapInstaller(self.runner, self.logger),
                "Initialize system with essential packages"
            ),
            InstallOption(
                "GitHub CLI",
                GitHubCLIInstaller(self.runner, self.logger),
                "Install GitHub CLI (gh)"
            ),
            InstallOption(
                "uv",
                UVInstaller(self.runner, self.logger),
                "Install uv (Astral Python manager)"
            ),
            InstallOption(
                "Node.js",
                NodeJSInstaller(self.runner, self.logger),
                "Install Node.js via nvm"
            ),
            InstallOption(
                "pnpm",
                PNPMInstaller(self.runner, self.logger),
                "Enable pnpm via corepack"
            ),
            InstallOption(
                "Neovim",
                NeovimInstaller(self.runner, self.logger),
                "Install Neovim (latest release)"
            ),
            InstallOption(
                "btop",
                BTopInstaller(self.runner, self.logger),
                "Install btop system monitor"
            ),
            InstallOption(
                "nginx",
                NginxInstaller(self.runner, self.logger),
                "Install nginx web server"
            ),
            InstallOption(
                "Certbot",
                CertbotInstaller(self.runner, self.logger),
                "Install Certbot (Let's Encrypt)"
            ),
            InstallOption(
                "UFW",
                UFWInstaller(self.runner, self.logger),
                "Install and configure UFW firewall"
            ),
            InstallOption(
                "Fail2ban",
                Fail2banInstaller(self.runner, self.logger),
                "Install and configure Fail2ban"
            ),
            InstallOption(
                "Image Viewer",
                ImageViewerInstaller(self.runner, self.logger),
                "Install Advance Image Viewer"
            ),
            InstallOption(
                "curlpad",
                CurlpadInstaller(self.runner, self.logger),
                "Install curlpad"
            ),
            InstallOption(
                "Developer Tools",
                DevToolsInstaller(self.runner, self.logger),
                "Install developer tools (openssl, clangd, build-essential, etc.)"
            ),
            InstallOption(
                "SSH Key",
                SSHKeyInstaller(self.runner, self.logger),
                "Generate SSH key pair (RSA 4096-bit) and display public key"
            ),
            InstallOption(
                "fastfetch",
                FastfetchInstaller(self.runner, self.logger),
                "Install fastfetch system information tool"
            ),
            InstallOption(
                "podman",
                PodmanInstaller(self.runner, self.logger),
                "Install podman container engine"
            ),
            InstallOption(
                "zsh",
                ZshInstaller(self.runner, self.logger),
                "Install zsh and set it as default shell"
            ),
            InstallOption(
                "git",
                GitInstaller(self.runner, self.logger),
                "Install git version control system"
            ),
            InstallOption(
                "rkhunter",
                RkhunterInstaller(self.runner, self.logger),
                "Install rkhunter (Rootkit Hunter) security scanner"
            ),
            InstallOption(
                "chkrootkit",
                ChkrootkitInstaller(self.runner, self.logger),
                "Install chkrootkit security scanner"
            ),
            InstallOption(
                "vrms",
                VRMSInstaller(self.runner, self.logger),
                "Install vrms (Virtual Richard M. Stallman - lists non-free packages)"
            ),
        ]
    
    def show_welcome(self):
        """Display welcome message."""
        welcome_text = Text()
        
        # Title with emoji
        welcome_text.append("🚀 ", style="bold blue")
        welcome_text.append("rig", style="bold bright_white")
        welcome_text.append(" - Opinionated system setup tool", style="bold white")
        welcome_text.append(" v0.1.3", style="dim cyan")
        
        welcome_text.append("\n\n", style="white")
        
        # Description with better formatting
        welcome_text.append("✨ ", style="yellow")
        welcome_text.append(
            "Opinionated system setup tool with basic tools to get started with in any Linux distribution.\n",
            style="white"
        )
        welcome_text.append("📦 ", style="cyan")
        welcome_text.append("No custom configurations, just the essential tools needed to be installed.", style="white")
        
        welcome_text.append("\n\n", style="white")
        
        # Separator line
        welcome_text.append("─" * 50, style="dim")
        welcome_text.append("\n\n", style="white")
        
        # Copyright and license with better styling
        welcome_text.append("© ", style="dim")
        welcome_text.append("Copyright (C) 2025 ", style="dim")
        welcome_text.append("Akshat Kotpalliwar", style="bold dim cyan")
        welcome_text.append(" (alias ", style="dim")
        welcome_text.append("IntegerAlex", style="bold dim")
        welcome_text.append(")", style="dim")
        welcome_text.append("\n", style="white")
        welcome_text.append("📜 ", style="dim")
        welcome_text.append("License: ", style="dim")
        welcome_text.append("GPL-3.0-only", style="bold dim green")
        
        panel = Panel(
            welcome_text,
            border_style="bright_blue",
            padding=(1, 3),
            title="[bold bright_blue]✨ Welcome to rig ✨[/bold bright_blue]",
            title_align="center",
            expand=False
        )
        self.console.print(panel)
        self.console.print()
    
    def show_summary(self):
        """Show installation summary with enhanced formatting and statistics."""
        # Create enhanced table with better styling
        table = Table(
            title="📊 Installation Summary",
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            show_lines=True,
            box=None,
            padding=(0, 1)
        )
        table.add_column("🛠️ Tool", style="cyan bold", no_wrap=True, min_width=15)
        table.add_column("📈 Status", style="magenta", no_wrap=True, min_width=12)
        table.add_column("💬 Details", style="white", min_width=30)

        success_count = 0
        fail_count = 0
        skipped_count = 0

        for name, result in self.results:
            if result.success:
                if "already installed" in result.message.lower():
                    status = "[dim]⏭️ Skipped[/dim]"
                    skipped_count += 1
                else:
                    status = "[green]✅ Success[/green]"
                    success_count += 1
            else:
                status = "[red]❌ Failed[/red]"
                fail_count += 1

            message = result.message
            if result.error:
                # Truncate long error messages and add ellipsis
                if len(result.error) > 60:
                    message += f" ([red]{result.error[:57]}...[/red])"
                else:
                    message += f" ([red]{result.error}[/red])"

            table.add_row(name, status, message)

        self.console.print()
        self.console.print(table)
        self.console.print()

        # Enhanced summary statistics with icons and better formatting
        success_rate = (success_count / len(self.results) * 100) if self.results else 0

        summary_table = Table(show_header=False, box=None, padding=(0, 2))
        summary_table.add_column("Metric", style="white", no_wrap=True)
        summary_table.add_column("Value", style="bold cyan", justify="right")

        summary_table.add_row("✅ Successful", f"{success_count}")
        summary_table.add_row("❌ Failed", f"{fail_count}")
        summary_table.add_row("⏭️ Skipped", f"{skipped_count}")
        summary_table.add_row("📊 Total", f"{len(self.results)}")
        summary_table.add_row("🎯 Success Rate", f"{success_rate:.1f}%")

        # Calculate total execution time if available
        if hasattr(self, '_start_time'):
            end_time = time.time()
            duration = end_time - self._start_time
            summary_table.add_row("⏱️ Total Time", f"{duration:.1f}s")

        summary_panel = Panel(
            summary_table,
            title="📈 Statistics",
            border_style="green",
            padding=(1, 2)
        )

        self.console.print(summary_panel)
        self.console.print()
    
    def run(self):
        """Run the setup process."""
        self._start_time = time.time()
        self.show_welcome()
        
        # Bootstrap is always run first
        bootstrap = self.install_options[0]
        self.console.print(f"[bold]Running bootstrap...[/bold]")
        # Don't use spinner for bootstrap as it may need sudo password input
        result = bootstrap.installer.install()
        self.results.append((bootstrap.name, result))

        if not result.success:
            print("✖ Bootstrap failed:", result.message)
            print()
            print("⚠️  rig requires sudo access for system package installation.")
            print("💡 To use rig, run it in an interactive terminal: rig")
            print()
            print("Available tools include: GitHub CLI, uv, Node.js, Neovim, nginx, and more!")
            return
        else:
            self.console.print(f"[green]✓[/green] Bootstrap completed\n")

        # Ask for each option
        selected_options = []
        for option in self.install_options[1:]:  # Skip bootstrap
            # Check if already installed
            if hasattr(option.installer, 'is_installed'):
                with spinner_context(f"Checking {option.name}..."):
                    is_installed = option.installer.is_installed()
                if is_installed:
                    self.console.print(f"[dim]→ {option.name} is already installed, skipping[/dim]")
                    continue

            if Confirm.ask(f"[cyan]👉[/cyan] Install {option.name}?", default=False):
                selected_options.append(option)
        
        if not selected_options:
            self.console.print("[yellow]No tools selected for installation.[/yellow]")
            return
        
        # Install selected options
        self.console.print()
        self.console.print(f"[bold]Installing {len(selected_options)} tool(s)...[/bold]\n")
        
        for option in selected_options:
            self.console.print(f"[bold cyan]Installing {option.name}...[/bold cyan]")
            
            try:
                # Don't use spinner for installations as they may need sudo password
                # or show important output (similar to bootstrap)
                result = option.installer.install()
                
                if result.success:
                    self.console.print(f"[green]✓[/green] {result.message}")
                else:
                    self.console.print(f"[red]✖[/red] {result.message}")
                    if result.error:
                        self.console.print(f"[dim red]{result.error}[/dim red]")
                
                self.results.append((option.name, result))
            except KeyboardInterrupt:
                self.console.print("\n[yellow]⚠[/yellow] Installation interrupted by user")
                break
            except RigError as e:
                # Handle custom rig errors with suggestions
                error_result = InstallerResult(False, str(e), str(e))
                self.results.append((option.name, error_result))
                self.console.print(f"[red]✖[/red] {e.message}")
                if e.suggestion:
                    self.console.print(f"[cyan]💡[/cyan] {e.suggestion}")
                self.logger.log("error", f"Error installing {option.name}: {e}")
            except Exception as e:
                error_result = InstallerResult(False, f"Unexpected error: {str(e)}", str(e))
                self.results.append((option.name, error_result))
                self.console.print(f"[red]✖[/red] Unexpected error: {e}")
                self.logger.log("error", f"Unexpected error installing {option.name}: {e}")
        
        # Show summary
        self.show_summary()

        # Update shell configuration
        self.console.print()
        update_shell_config(".local/bin")

        # Final messages
        self.console.print()
        self.console.print(f"[green]✓[/green] Setup completed successfully 🎉")
        self.console.print(f"[dim]📄 Log file: {self.logger.log_file}[/dim]")


def main():
    """Main entry point."""
    try:
        manager = SetupManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"✖ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

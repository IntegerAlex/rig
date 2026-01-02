#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""
Beautiful system setup tool with rich UI and comprehensive error handling.
Migrated from new1.sh with enhanced features.
"""

import sys
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback

from utils import SetupLogger, CommandRunner, InstallerResult, InstallOption, BaseInstaller
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
        # welcome_text.append("🚀 ", style="bold blue")
        welcome_text.append("rig - Opinionated system setup tool", style="bold white")
        welcome_text.append(" v0.1.2", style="dim white")
        welcome_text.append("\n\n", style="white")
        welcome_text.append(
            "Opinionated system setup tool with basic tools to get started with in any Linux distribution.\n",
            style="dim"
        )
        welcome_text.append("No custom configurations, just the essential tools needed to be installed.", style="dim")
        welcome_text.append("\n\n", style="white")
        welcome_text.append("Copyright (C) 2025 ", style="dim")
        welcome_text.append("Akshat Kotpalliwar (alias IntegerAlex)", style="bold dim")
        welcome_text.append("\n", style="white")
        welcome_text.append("License: ", style="dim")
        welcome_text.append("GPL-3.0-only", style="bold dim")
        
        panel = Panel(
            welcome_text,
            border_style="blue",
            padding=(1, 2),
            title="Welcome",
            title_align="left"
        )
        self.console.print(panel)
        self.console.print()
    
    def show_summary(self):
        """Show installation summary."""
        table = Table(title="Installation Summary", show_header=True, header_style="bold blue")
        table.add_column("Tool", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Message", style="white")
        
        success_count = 0
        fail_count = 0
        
        for name, result in self.results:
            if result.success:
                status = "[green]✓ Success[/green]"
                success_count += 1
            else:
                status = "[red]✗ Failed[/red]"
                fail_count += 1
            
            message = result.message
            if result.error:
                message += f" ({result.error[:50]}...)" if len(result.error) > 50 else f" ({result.error})"
            
            table.add_row(name, status, message)
        
        self.console.print()
        self.console.print(table)
        self.console.print()
        
        # Summary stats
        summary_text = Text()
        summary_text.append(f"✓ Successful: ", style="green")
        summary_text.append(f"{success_count}", style="bold green")
        summary_text.append(f"  ✗ Failed: ", style="red")
        summary_text.append(f"{fail_count}", style="bold red")
        summary_text.append(f"  Total: ", style="white")
        summary_text.append(f"{len(self.results)}", style="bold white")
        
        self.console.print(Panel(summary_text, border_style="blue", padding=(1, 2)))
        self.console.print()
    
    def run(self):
        """Run the setup process."""
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
            if hasattr(option.installer, 'is_installed') and option.installer.is_installed():
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
            except Exception as e:
                error_result = InstallerResult(False, f"Unexpected error: {str(e)}", str(e))
                self.results.append((option.name, error_result))
                self.console.print(f"[red]✖[/red] Unexpected error: {e}")
                self.logger.log("error", f"Unexpected error installing {option.name}: {e}")
        
        # Show summary
        self.show_summary()
        
        # Final messages
        self.console.print()
        self.console.print(f"[green]✓[/green] Setup completed successfully 🎉")
        self.console.print(f"[dim]📄 Log file: {self.logger.log_file}[/dim]")
        self.console.print(f"[dim]🔁 Restart shell: source ~/.bashrc (or ~/.zshrc)[/dim]")


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

# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""SSH key generator installer."""

import os
from pathlib import Path

from utils.base import BaseInstaller
from utils.types import InstallerResult


class SSHKeyInstaller(BaseInstaller):
    """Generate SSH key pair."""
    
    def is_installed(self) -> bool:
        """Check if SSH key already exists."""
        ssh_dir = Path.home() / ".ssh"
        bot_key = ssh_dir / "bot"
        bot_pub = ssh_dir / "bot.pub"
        return bot_key.exists() and bot_pub.exists()
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Generating SSH key pair")
            
            ssh_dir = Path.home() / ".ssh"
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            
            bot_key = ssh_dir / "bot"
            bot_pub = ssh_dir / "bot.pub"
            
            # Check if key already exists
            if bot_key.exists() and bot_pub.exists():
                self.console.print("[yellow]⚠[/yellow] SSH key already exists, skipping generation")
                self._display_public_key(bot_pub)
                return InstallerResult(True, "SSH key already exists")
            
            # Generate SSH key (non-interactive, quiet mode)
            self.runner.run(
                ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", str(bot_key), "-N", "", "-q"],
                description="Generating SSH key pair"
            )
            
            # Set proper permissions
            bot_key.chmod(0o600)
            bot_pub.chmod(0o644)
            
            # Display public key
            self._display_public_key(bot_pub)
            
            return InstallerResult(True, "SSH key generated successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to generate SSH key", str(e))
    
    def _display_public_key(self, pub_key_path: Path):
        """Display the public key to the user."""
        try:
            if pub_key_path.exists():
                public_key = pub_key_path.read_text().strip()
                self.console.print()
                self.console.print("[bold cyan]Your SSH public key:[/bold cyan]")
                self.console.print(f"[dim]{public_key}[/dim]")
                self.console.print()
                self.console.print("[dim]Add this key to GitHub, GitLab, or your server's ~/.ssh/authorized_keys[/dim]")
        except Exception as e:
            self.console.print(f"[yellow]⚠[/yellow] Could not read public key: {e}")


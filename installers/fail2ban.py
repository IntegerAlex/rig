# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Fail2ban installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class Fail2banInstaller(BaseInstaller):
    """Install and configure Fail2ban."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("fail2ban-client"):
            return False
        
        try:
            result = self.runner.run(["fail2ban-client", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing Fail2ban")
            
            self.runner.run(
                ["apt", "install", "-y", "fail2ban"],
                sudo=True,
                description="Installing Fail2ban"
            )
            
            # Create jail.local configuration
            jail_config = """[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
backend = systemd

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
"""
            
            self.runner.run(
                ["bash", "-c", f"echo '{jail_config}' | sudo tee /etc/fail2ban/jail.local >/dev/null"],
                description="Configuring Fail2ban"
            )
            
            self.console.print(
                "[yellow]⚠[/yellow] Fail2ban installed but NOT started. Start manually with: sudo systemctl start fail2ban"
            )
            
            return InstallerResult(True, "Fail2ban installed and configured (not started)")
        except Exception as e:
            return InstallerResult(False, "Failed to install Fail2ban", str(e))


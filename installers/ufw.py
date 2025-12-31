# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""UFW firewall installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class UFWInstaller(BaseInstaller):
    """Install and configure UFW firewall."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("ufw"):
            return False
        
        try:
            result = self.runner.run(["ufw", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing UFW")
            
            self.runner.run(
                ["apt", "install", "-y", "ufw"],
                sudo=True,
                description="Installing UFW"
            )
            
            # Configure firewall rules
            self.runner.run(
                ["ufw", "default", "deny", "incoming"],
                sudo=True,
                description="Setting default deny incoming"
            )
            
            self.runner.run(
                ["ufw", "default", "allow", "outgoing"],
                sudo=True,
                description="Setting default allow outgoing"
            )
            
            self.runner.run(
                ["ufw", "allow", "22/tcp"],
                sudo=True,
                description="Allowing SSH"
            )
            
            self.runner.run(
                ["ufw", "allow", "80"],
                sudo=True,
                description="Allowing HTTP"
            )
            
            self.runner.run(
                ["ufw", "allow", "443"],
                sudo=True,
                description="Allowing HTTPS"
            )
            
            self.console.print(
                "[yellow]⚠[/yellow] UFW configured but NOT enabled. Enable manually with: sudo ufw enable"
            )
            
            return InstallerResult(True, "UFW installed and configured (not enabled)")
        except Exception as e:
            return InstallerResult(False, "Failed to install UFW", str(e))


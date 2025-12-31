# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Certbot installer."""

import os
import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class CertbotInstaller(BaseInstaller):
    """Install Certbot (Let's Encrypt)."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("certbot"):
            return False
        
        try:
            result = self.runner.run(["certbot", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing Certbot")
            
            # Install dependencies
            self.runner.run(
                ["apt", "install", "-y", "python3", "python3-dev", "python3-venv", 
                 "libaugeas-dev", "gcc"],
                sudo=True,
                description="Installing Certbot dependencies"
            )
            
            # Create certbot directory
            self.runner.run(["mkdir", "-p", "/opt/certbot"], sudo=True)
            
            # Create virtual environment if it doesn't exist
            certbot_venv = "/opt/certbot/bin/python"
            if not os.path.exists(certbot_venv):
                self.runner.run(
                    ["python3", "-m", "venv", "/opt/certbot"],
                    sudo=True,
                    description="Creating Certbot virtual environment"
                )
            
            # Install certbot
            self.runner.run(
                ["/opt/certbot/bin/pip", "install", "--upgrade", "pip"],
                sudo=True,
                description="Upgrading pip"
            )
            
            self.runner.run(
                ["/opt/certbot/bin/pip", "install", "certbot", "certbot-nginx"],
                sudo=True,
                description="Installing Certbot"
            )
            
            # Create symlink
            self.runner.run(
                ["ln", "-sf", "/opt/certbot/bin/certbot", "/usr/bin/certbot"],
                sudo=True,
                description="Creating certbot symlink"
            )
            
            return InstallerResult(True, "Certbot installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install Certbot", str(e))


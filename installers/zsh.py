# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Zsh installer."""

import subprocess
from pathlib import Path

from utils.base import BaseInstaller
from utils.types import InstallerResult


class ZshInstaller(BaseInstaller):
    """Install zsh and set it as default shell."""
    
    def is_installed(self) -> bool:
        try:
            result = self.runner.run(["zsh", "--version"], check=False, capture_output=True)
            if result.returncode != 0:
                return False
            
            # Check if zsh is already the default shell
            try:
                current_shell = Path("/etc/passwd").read_text()
                # Get current user's shell
                import os
                username = os.getenv("USER") or os.getenv("USERNAME")
                if username:
                    for line in current_shell.split('\n'):
                        if line.startswith(f"{username}:"):
                            shell = line.split(':')[-1]
                            return shell.endswith('/zsh')
            except:
                pass
            
            return True
        except:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing zsh")
            
            # Install zsh
            self.runner.run(
                ["apt", "install", "-y", "zsh"],
                sudo=True,
                description="Installing zsh"
            )
            
            # Find zsh path
            try:
                zsh_path = subprocess.check_output(["which", "zsh"], text=True).strip()
            except:
                zsh_path = "/usr/bin/zsh"
            
            # Set zsh as default shell (chsh doesn't need sudo for current user)
            self.console.print("[blue]ℹ[/blue] Setting zsh as default shell")
            self.runner.run(
                ["chsh", "-s", zsh_path],
                sudo=False,
                description="Setting zsh as default shell"
            )
            
            self.console.print(
                "[yellow]⚠[/yellow] Default shell changed to zsh. "
                "The change will take effect after you log out and log back in."
            )
            
            return InstallerResult(True, "zsh installed and set as default shell")
        except Exception as e:
            return InstallerResult(False, "Failed to install zsh", str(e))


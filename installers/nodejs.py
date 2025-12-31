# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Node.js installer via nvm."""

from pathlib import Path

from utils.base import BaseInstaller
from utils.types import InstallerResult


class NodeJSInstaller(BaseInstaller):
    """Install Node.js via nvm."""
    
    def is_installed(self) -> bool:
        nvm_dir = Path.home() / ".nvm"
        return (nvm_dir / "nvm.sh").exists()
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing Node.js via nvm")
            
            nvm_install_script = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"
            self.runner.run(
                ["bash", "-c", nvm_install_script],
                description="Installing nvm"
            )
            
            # Note: nvm needs to be sourced, which is tricky in non-interactive mode
            # The user will need to source ~/.bashrc or ~/.zshrc after installation
            self.console.print(
                "[yellow]⚠[/yellow] Please run: source ~/.bashrc (or ~/.zshrc) to use nvm",
                style="dim"
            )
            
            return InstallerResult(True, "Node.js (nvm) installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install Node.js", str(e))


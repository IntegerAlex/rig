# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""GitHub CLI installer."""

import subprocess

from utils.base import BaseInstaller
from utils.types import InstallerResult


class GitHubCLIInstaller(BaseInstaller):
    """Install GitHub CLI."""
    
    def is_installed(self) -> bool:
        try:
            result = self.runner.run(["gh", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing GitHub CLI")
            
            # Create keyrings directory
            self.runner.run(["mkdir", "-p", "/etc/apt/keyrings"], sudo=True)
            
            # Download and install keyring
            keyring_url = "https://cli.github.com/packages/githubcli-archive-keyring.gpg"
            self.runner.run(
                ["bash", "-c", f"wget -qO- {keyring_url} | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null"],
                description="Downloading GitHub CLI keyring"
            )
            
            self.runner.run(
                ["chmod", "go+r", "/etc/apt/keyrings/githubcli-archive-keyring.gpg"],
                sudo=True
            )
            
            # Add repository
            arch = subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip()
            repo_line = (
                f"deb [arch={arch} signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] "
                f"https://cli.github.com/packages stable main"
            )
            self.runner.run(
                ["bash", "-c", f"echo '{repo_line}' | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null"],
                description="Adding GitHub CLI repository"
            )
            
            self.runner.run(["apt", "update"], sudo=True)
            self.runner.run(["apt", "install", "-y", "gh"], sudo=True, description="Installing GitHub CLI")
            
            return InstallerResult(True, "GitHub CLI installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install GitHub CLI", str(e))


# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Git installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class GitInstaller(BaseInstaller):
    """Install git version control system."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("git"):
            return False
        
        try:
            result = self.runner.run(["git", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing git")
            
            self.runner.run(
                ["apt", "install", "-y", "git"],
                sudo=True,
                description="Installing git"
            )
            
            return InstallerResult(True, "git installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install git", str(e))


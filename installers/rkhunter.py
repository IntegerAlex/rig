# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Rkhunter installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class RkhunterInstaller(BaseInstaller):
    """Install rkhunter (Rootkit Hunter) security scanner."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("rkhunter"):
            return False
        
        try:
            result = self.runner.run(["rkhunter", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing rkhunter")
            
            self.runner.run(
                ["apt", "install", "-y", "rkhunter"],
                sudo=True,
                description="Installing rkhunter"
            )
            
            return InstallerResult(True, "rkhunter installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install rkhunter", str(e))


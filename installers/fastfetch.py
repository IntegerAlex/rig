# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Fastfetch installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class FastfetchInstaller(BaseInstaller):
    """Install fastfetch."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("fastfetch"):
            return False
        
        try:
            result = self.runner.run(["fastfetch", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing fastfetch")
            
            self.runner.run(
                ["apt", "install", "-y", "fastfetch"],
                sudo=True,
                description="Installing fastfetch"
            )
            
            return InstallerResult(True, "fastfetch installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install fastfetch", str(e))


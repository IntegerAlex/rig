# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Chkrootkit installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class ChkrootkitInstaller(BaseInstaller):
    """Install chkrootkit."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("chkrootkit"):
            return False
        
        try:
            result = self.runner.run(["chkrootkit", "-V"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing chkrootkit")
            
            self.runner.run(
                ["apt", "install", "-y", "chkrootkit"],
                sudo=True,
                description="Installing chkrootkit"
            )
            
            return InstallerResult(True, "chkrootkit installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install chkrootkit", str(e))


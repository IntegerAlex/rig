# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""btop installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class BTopInstaller(BaseInstaller):
    """Install btop."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("btop"):
            return False
        
        try:
            result = self.runner.run(["btop", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing btop")
            
            self.runner.run(
                ["apt", "install", "-y", "btop"],
                sudo=True,
                description="Installing btop"
            )
            
            return InstallerResult(True, "btop installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install btop", str(e))


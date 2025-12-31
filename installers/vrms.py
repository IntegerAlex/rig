# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""VRMS installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class VRMSInstaller(BaseInstaller):
    """Install vrms (Virtual Richard M. Stallman)."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("vrms"):
            return False
        
        try:
            result = self.runner.run(["vrms", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing vrms")
            
            self.runner.run(
                ["apt", "install", "-y", "vrms"],
                sudo=True,
                description="Installing vrms"
            )
            
            return InstallerResult(True, "vrms installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install vrms", str(e))


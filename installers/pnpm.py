# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""pnpm installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class PNPMInstaller(BaseInstaller):
    """Enable pnpm via corepack."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("pnpm"):
            return False
        
        try:
            result = self.runner.run(["pnpm", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Enabling pnpm")
            
            self.runner.run(
                ["corepack", "enable", "pnpm"],
                description="Enabling pnpm"
            )
            
            return InstallerResult(True, "pnpm enabled successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to enable pnpm", str(e))


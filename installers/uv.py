# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""uv (Astral Python manager) installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class UVInstaller(BaseInstaller):
    """Install uv (Astral Python manager)."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("uv"):
            return False
        
        try:
            result = self.runner.run(["uv", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing uv")
            
            install_script = "curl -LsSf https://astral.sh/uv/install.sh | sh"
            self.runner.run(
                ["bash", "-c", install_script],
                description="Installing uv"
            )
            
            return InstallerResult(True, "uv installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install uv", str(e))


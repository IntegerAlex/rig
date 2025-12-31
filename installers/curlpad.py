# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""curlpad installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class CurlpadInstaller(BaseInstaller):
    """Install curlpad."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("curlpad"):
            return False
        
        try:
            result = self.runner.run(["curlpad", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing curlpad")
            
            install_script = "curl -fsSL curlpad-installer.gossorg.in/install.sh | bash"
            self.runner.run(
                ["bash", "-c", install_script],
                description="Installing curlpad"
            )
            
            return InstallerResult(True, "curlpad installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install curlpad", str(e))


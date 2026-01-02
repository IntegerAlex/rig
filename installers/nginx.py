# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""nginx installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult
from utils.errors import PackageManagerError, InstallationError


class NginxInstaller(BaseInstaller):
    """Install nginx."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("nginx"):
            return False
        
        try:
            result = self.runner.run(["nginx", "-v"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing nginx")
            
            self.runner.run(
                ["apt", "install", "-y", "nginx"],
                sudo=True,
                description="Installing nginx"
            )
            
            self.runner.run(
                ["systemctl", "enable", "nginx"],
                sudo=True,
                description="Enabling nginx service"
            )
            
            return InstallerResult(True, "nginx installed successfully")
        except (PackageManagerError, InstallationError):
            # Re-raise custom errors as-is
            raise
        except Exception as e:
            # Convert other exceptions to installation errors with helpful suggestions
            raise InstallationError(
                "Failed to install nginx web server",
                "nginx",
                [
                    "Check your internet connection",
                    "Ensure you have sudo privileges",
                    "Try: sudo apt update && sudo apt install nginx"
                ]
            ) from e


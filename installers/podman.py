# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Podman installer."""

from utils.base import BaseInstaller
from utils.types import InstallerResult


class PodmanInstaller(BaseInstaller):
    """Install podman."""
    
    def is_installed(self) -> bool:
        try:
            result = self.runner.run(["podman", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing podman")
            
            self.runner.run(
                ["apt-get", "install", "-y", "podman"],
                sudo=True,
                description="Installing podman"
            )
            
            return InstallerResult(True, "podman installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install podman", str(e))


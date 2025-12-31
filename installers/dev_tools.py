# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Developer tools installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class DevToolsInstaller(BaseInstaller):
    """Install developer tools."""
    
    def is_installed(self) -> bool:
        # Check if key developer tools are installed
        # We check for a few key tools to determine if dev tools are installed
        key_tools = ["gcc", "make", "cmake", "pkg-config"]
        installed_count = sum(1 for tool in key_tools if shutil.which(tool))
        # If at least 3 out of 4 key tools are installed, consider dev tools installed
        return installed_count >= 3
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing developer tools")
            
            packages = [
                "openssl",
                "clangd",
                "build-essential",
                "pkg-config",
                "cmake",
                "git"
            ]
            
            self.runner.run(
                ["apt", "install", "-y"] + packages,
                sudo=True,
                description="Installing developer tools"
            )
            
            return InstallerResult(True, "Developer tools installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install developer tools", str(e))


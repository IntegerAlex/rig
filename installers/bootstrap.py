# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Bootstrap installer for system initialization."""

from utils.base import BaseInstaller
from utils.types import InstallerResult


class BootstrapInstaller(BaseInstaller):
    """Bootstrap system with essential packages."""
    
    def install(self) -> InstallerResult:
        try:
            print("ℹ Initializing system")

            self.runner.run(["apt", "update"], sudo=True, description="Updating package lists")
            self.runner.run(
                ["apt", "install", "-y", "ca-certificates", "curl", "wget", "gnupg", "lsb-release"],
                sudo=True,
                description="Installing essential packages"
            )

            return InstallerResult(True, "System initialized successfully")
        except Exception as e:
            print(f"DEBUG: Bootstrap exception: {e}")
            return InstallerResult(False, "Failed to initialize system", str(e))


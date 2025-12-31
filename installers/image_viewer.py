# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Advance Image Viewer installer."""

import shutil

from utils.base import BaseInstaller
from utils.types import InstallerResult


class ImageViewerInstaller(BaseInstaller):
    """Install Advance Image Viewer."""
    
    def is_installed(self) -> bool:
        # Check if command exists (common names for advance image viewer)
        if shutil.which("aiv") or shutil.which("advance-image-viewer"):
            return True
        # Check if installed via script location
        try:
            result = self.runner.run(["which", "aiv"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing Advance Image Viewer")
            
            install_script = "curl -fsSL https://advance-image-viewer.gossorg.in | bash"
            self.runner.run(
                ["bash", "-c", install_script],
                description="Installing Advance Image Viewer"
            )
            
            return InstallerResult(True, "Advance Image Viewer installed successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to install Advance Image Viewer", str(e))


# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Neovim installer."""

import os
import shutil
import tempfile

from utils.base import BaseInstaller
from utils.types import InstallerResult


class NeovimInstaller(BaseInstaller):
    """Install Neovim (latest release)."""
    
    def is_installed(self) -> bool:
        # Check if command exists first to avoid error logs
        if not shutil.which("nvim"):
            return False
        
        try:
            result = self.runner.run(["nvim", "--version"], check=False, capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def install(self) -> InstallerResult:
        try:
            self.console.print("[blue]ℹ[/blue] Installing Neovim")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz") as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz"
                self.runner.run(
                    ["curl", "-L", download_url, "-o", tmp_path],
                    description="Downloading Neovim"
                )
                
                self.runner.run(
                    ["rm", "-rf", "/opt/nvim-linux-x86_64"],
                    sudo=True
                )
                
                self.runner.run(
                    ["tar", "-C", "/opt", "-xzf", tmp_path],
                    sudo=True,
                    description="Extracting Neovim"
                )
                
                self.runner.run(
                    ["ln", "-sf", "/opt/nvim-linux-x86_64/bin/nvim", "/usr/local/bin/nvim"],
                    sudo=True,
                    description="Creating symlink"
                )
                
                return InstallerResult(True, "Neovim installed successfully")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
        except Exception as e:
            return InstallerResult(False, "Failed to install Neovim", str(e))


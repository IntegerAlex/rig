# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""pnpm installer."""

from __future__ import annotations

import shutil
from pathlib import Path

from utils.base import BaseInstaller
from utils.types import InstallerResult


class PNPMInstaller(BaseInstaller):
    """Enable pnpm via corepack."""

    _MIN_NODE_MAJOR_FOR_COREPACK = 24
    _DEFAULT_NODE_MAJOR = 24
    
    def _get_node_major(self) -> int | None:
        """Return installed node major version, or None if node missing/unknown."""
        if not shutil.which("node"):
            return None
        try:
            result = self.runner.run(["node", "--version"], check=False, capture_output=True)
            if result.returncode != 0 or not result.stdout:
                return None
            # node outputs like: v24.1.0
            v = result.stdout.strip()
            if v.startswith("v"):
                v = v[1:]
            major_str = v.split(".", 1)[0]
            return int(major_str)
        except Exception:
            return None
    
    def _has_nvm(self) -> bool:
        nvm_dir = Path.home() / ".nvm"
        return (nvm_dir / "nvm.sh").exists()
    
    def _enable_pnpm_via_nvm(self, node_major: int) -> None:
        """
        Use nvm to install/use a Node version, then enable pnpm with corepack.
        This must be done in a single shell so that `nvm use` affects `corepack`.
        """
        cmd = (
            'export NVM_DIR="$HOME/.nvm"; '
            '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; '
            f"nvm install {node_major}; "
            f"nvm use {node_major}; "
            "corepack enable pnpm; "
        )
        self.runner.run(["bash", "-lc", cmd], description=f"Installing/using Node {node_major} via nvm and enabling pnpm")
    
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
            node_major = self._get_node_major()
            corepack_available = shutil.which("corepack") is not None

            # If corepack isn't available (or Node is too old), prefer fixing via nvm if present.
            if (not corepack_available) or (node_major is None) or (node_major < self._MIN_NODE_MAJOR_FOR_COREPACK):
                if not self._has_nvm():
                    return InstallerResult(
                        False,
                        "Failed to enable pnpm (corepack requires Node 24+)",
                        "corepack/node not available and nvm not found. Install Node.js (via nvm) first, then rerun pnpm."
                    )
                self._enable_pnpm_via_nvm(self._DEFAULT_NODE_MAJOR)
            else:
                self.runner.run(
                    ["corepack", "enable", "pnpm"],
                    description="Enabling pnpm via corepack"
                )
            
            return InstallerResult(True, "pnpm enabled successfully")
        except Exception as e:
            return InstallerResult(False, "Failed to enable pnpm", str(e))


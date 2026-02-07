# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Zsh installer."""

import subprocess

from utils.types import InstallerResult

from .apt_package import AptPackageInstaller


class ZshInstaller(AptPackageInstaller):
    """Install zsh and set it as default shell."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="zsh",
            success_message="zsh installed and set as default shell",
        )

    def is_installed(self) -> bool:
        if not super().is_installed():
            return False
        # Check if zsh is already the default shell
        try:
            from pathlib import Path
            import os
            current_passwd = Path("/etc/passwd").read_text()
            username = os.getenv("USER") or os.getenv("USERNAME")
            if username:
                for line in current_passwd.split("\n"):
                    if line.startswith(f"{username}:"):
                        shell = line.split(":")[-1]
                        return shell.rstrip().endswith("/zsh")
        except Exception:
            pass
        return True

    def install(self) -> InstallerResult:
        result = super().install()
        if not result.success:
            return result
        try:
            self.console.print("[blue]ℹ[/blue] Setting zsh as default shell")
            try:
                zsh_path = subprocess.check_output(["which", "zsh"], text=True).strip()
            except Exception:
                zsh_path = "/usr/bin/zsh"
            self.runner.run(
                ["chsh", "-s", zsh_path],
                sudo=False,
                description="Setting zsh as default shell",
            )
            self.console.print(
                "[yellow]⚠[/yellow] Default shell changed to zsh. "
                "The change will take effect after you log out and log back in."
            )
        except Exception as e:
            return InstallerResult(False, "zsh installed but failed to set as default shell", str(e))
        return InstallerResult(True, "zsh installed and set as default shell")

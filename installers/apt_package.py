# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Base installer for single-package apt installs."""

import shutil
from typing import List, Optional

from utils.base import BaseInstaller
from utils.types import InstallerResult


class AptPackageInstaller(BaseInstaller):
    """Install a single package via apt. Subclass or use for simple which + version check and apt install -y."""

    def __init__(
        self,
        runner,
        logger,
        *,
        package_name: str,
        check_command: Optional[str] = None,
        version_args: Optional[List[str]] = None,
        display_name: Optional[str] = None,
        success_message: Optional[str] = None,
    ):
        super().__init__(runner, logger)
        self.package_name = package_name
        self.check_command = check_command if check_command is not None else package_name
        self.version_args = version_args if version_args is not None else ["--version"]
        self.display_name = display_name or package_name
        self.success_message = success_message or f"{self.display_name} installed successfully"

    def is_installed(self) -> bool:
        if not shutil.which(self.check_command):
            return False
        try:
            result = self.runner.run(
                [self.check_command] + self.version_args,
                check=False,
                capture_output=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def install(self) -> InstallerResult:
        try:
            self.console.print(f"[blue]ℹ[/blue] Installing {self.display_name}")
            self.runner.run(
                ["apt", "install", "-y", self.package_name],
                sudo=True,
                description=f"Installing {self.display_name}",
            )
            return InstallerResult(True, self.success_message)
        except Exception as e:
            return InstallerResult(
                False,
                f"Failed to install {self.display_name}",
                str(e),
            )

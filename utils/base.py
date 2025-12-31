# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Base installer class."""

from rich.console import Console

from .runner import CommandRunner
from .logger import SetupLogger
from .types import InstallerResult

console = Console()


class BaseInstaller:
    """Base class for all installers."""
    
    def __init__(self, runner: CommandRunner, logger: SetupLogger):
        self.runner = runner
        self.logger = logger
        self.console = console
    
    def install(self) -> InstallerResult:
        """Install the tool. Override in subclasses."""
        raise NotImplementedError
    
    def is_installed(self) -> bool:
        """Check if tool is already installed. Override in subclasses."""
        return False


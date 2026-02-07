# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Git installer."""

from .apt_package import AptPackageInstaller


class GitInstaller(AptPackageInstaller):
    """Install git version control system."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="git",
            success_message="git installed successfully",
        )

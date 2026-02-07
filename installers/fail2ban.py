# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Fail2ban installer."""

from .apt_package import AptPackageInstaller


class Fail2banInstaller(AptPackageInstaller):
    """Install and configure Fail2ban."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="fail2ban",
            check_command="fail2ban-client",
            success_message="Fail2ban installed successfully",
        )

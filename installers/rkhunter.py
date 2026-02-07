# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""rkhunter installer."""

from .apt_package import AptPackageInstaller


class RkhunterInstaller(AptPackageInstaller):
    """Install rkhunter (Rootkit Hunter) security scanner."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="rkhunter",
            success_message="rkhunter installed successfully",
        )

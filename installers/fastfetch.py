# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""fastfetch installer."""

from .apt_package import AptPackageInstaller


class FastfetchInstaller(AptPackageInstaller):
    """Install fastfetch system information tool."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="fastfetch",
            success_message="fastfetch installed successfully",
        )

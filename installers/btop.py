# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""btop installer."""

from .apt_package import AptPackageInstaller


class BTopInstaller(AptPackageInstaller):
    """Install btop."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="btop",
            success_message="btop installed successfully",
        )

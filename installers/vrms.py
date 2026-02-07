# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""vrms installer."""

from .apt_package import AptPackageInstaller


class VRMSInstaller(AptPackageInstaller):
    """Install vrms (Virtual Richard M. Stallman - lists non-free packages)."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="vrms",
            success_message="vrms installed successfully",
        )

# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Chkrootkit installer."""

from .apt_package import AptPackageInstaller


class ChkrootkitInstaller(AptPackageInstaller):
    """Install chkrootkit."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="chkrootkit",
            version_args=["-V"],
            success_message="chkrootkit installed successfully",
        )

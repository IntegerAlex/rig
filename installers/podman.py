# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Podman installer."""

from .apt_package import AptPackageInstaller


class PodmanInstaller(AptPackageInstaller):
    """Install podman."""

    def __init__(self, runner, logger):
        super().__init__(
            runner,
            logger,
            package_name="podman",
            success_message="podman installed successfully",
        )

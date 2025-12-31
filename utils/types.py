# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Type definitions for the setup tool."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class InstallerResult:
    """Result of an installation operation."""
    success: bool
    message: str
    error: Optional[str] = None


@dataclass
class InstallOption:
    """Represents an installation option."""
    name: str
    installer: "BaseInstaller"
    description: str


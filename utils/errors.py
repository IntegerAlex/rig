# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Custom exception classes for enhanced error handling."""


class RigError(Exception):
    """Base exception class for rig-related errors."""

    def __init__(self, message: str, suggestion: str = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)


class NetworkError(RigError):
    """Raised when network operations fail."""

    def __init__(self, message: str, url: str = None):
        super().__init__(
            message,
            f"Check your internet connection and try again. "
            f"{'URL: ' + url if url else ''}"
        )
        self.url = url


class PermissionError(RigError):
    """Raised when permission/authorization operations fail."""

    def __init__(self, message: str, command: str = None):
        suggestion = (
            "This operation requires administrator privileges. "
            f"{'Try running with sudo: sudo ' + command if command else 'Try running with sudo.'}"
        )
        super().__init__(message, suggestion)
        self.command = command


class PackageManagerError(RigError):
    """Raised when package manager operations fail."""

    def __init__(self, message: str, package: str = None):
        suggestion_parts = ["Try updating package lists: sudo apt update"]

        if package:
            suggestion_parts.extend([
                f"Check if package exists: apt search {package}",
                f"Try installing manually: sudo apt install {package}"
            ])

        suggestion_parts.append("Check for locked files: sudo killall apt apt-get")

        super().__init__(message, " | ".join(suggestion_parts))
        self.package = package


class CommandNotFoundError(RigError):
    """Raised when required commands are not found."""

    def __init__(self, command: str):
        message = f"Command not found: {command}"
        suggestion = f"Install {command} using your package manager (apt, yum, etc.)"
        super().__init__(message, suggestion)
        self.command = command


class InstallationError(RigError):
    """Raised when installation operations fail."""

    def __init__(self, message: str, tool: str = None, recovery_steps: list = None):
        if recovery_steps:
            suggestion = " | ".join(recovery_steps)
        elif tool:
            suggestion = (
                f"Try installing {tool} manually | "
                "Check system logs for more details | "
                "Ensure all dependencies are installed"
            )
        else:
            suggestion = "Check system logs for more details"

        super().__init__(message, suggestion)
        self.tool = tool
        self.recovery_steps = recovery_steps or []


class ValidationError(RigError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str = None):
        suggestion = f"Check the {field} value and try again" if field else "Check your input and try again"
        super().__init__(message, suggestion)
        self.field = field


class ConfigurationError(RigError):
    """Raised when configuration operations fail."""

    def __init__(self, message: str, config_file: str = None):
        suggestion = (
            f"Check permissions on {config_file}" if config_file
            else "Check configuration file permissions and content"
        )
        super().__init__(message, suggestion)
        self.config_file = config_file

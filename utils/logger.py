# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Logging utilities for the setup tool."""

import logging
import tempfile
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

# Initialize console
console = Console()

# Logging setup
LOG_FILE = Path("/var/log/setup.log")


class SetupLogger:
    """Centralized logging with both file and console output."""
    
    def __init__(self, log_file: Path = LOG_FILE):
        self.log_file = log_file
        self._setup_log_file()
        self.logger = self._setup_logger()
    
    def _setup_log_file(self):
        """Create log file with proper permissions."""
        try:
            if not self.log_file.exists():
                # Try to create log file (may require sudo)
                try:
                    self.log_file.parent.mkdir(parents=True, exist_ok=True)
                    self.log_file.touch()
                    self.log_file.chmod(0o644)
                except (PermissionError, OSError):
                    # Fallback to user's home directory
                    self.log_file = Path.home() / ".setup.log"
                    self.log_file.touch()
                    # Suppress the warning - it's not critical
                    pass
        except Exception as e:
            console.print(f"[red]✖[/red] Failed to setup log file: {e}")
            self.log_file = Path.home() / ".setup.log"
            self.log_file.touch()
    
    def _ensure_writable_log_file(self):
        """Ensure the log file is writable, fallback if not."""
        # Test if we can write to the current log file
        try:
            # Try to open in append mode to test write permissions
            with open(self.log_file, "a"):
                pass
        except (PermissionError, OSError):
            # Fallback to user's home directory
            fallback_log = Path.home() / ".setup.log"
            try:
                fallback_log.touch()
                self.log_file = fallback_log
                # Suppress warning - fallback is working fine
                pass
            except Exception as e:
                console.print(f"[red]✖[/red] Failed to create fallback log file: {e}")
                # Last resort: use a temp file
                self.log_file = Path(tempfile.gettempdir()) / "setup.log"
                self.log_file.touch()
                # Suppress warning - temporary log is working fine
                pass
    
    def _setup_logger(self) -> logging.Logger:
        """Configure logger with rich handler."""
        logger = logging.getLogger("setup")
        logger.setLevel(logging.DEBUG)
        
        # Ensure log file is writable
        self._ensure_writable_log_file()
        
        # File handler
        try:
            file_handler = logging.FileHandler(self.log_file, mode="a")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except (PermissionError, OSError) as e:
            # If we still can't create the handler, log a warning but continue
            console.print(f"[yellow]⚠[/yellow] Could not create file logger: {e}")
            console.print(f"[dim]Continuing without file logging...[/dim]")
        
        # Rich console handler (only for errors/warnings)
        console_handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            rich_tracebacks=True
        )
        console_handler.setLevel(logging.WARNING)
        logger.addHandler(console_handler)
        
        return logger
    
    def log(self, level: str, message: str):
        """Log a message at the specified level."""
        getattr(self.logger, level.lower())(message)


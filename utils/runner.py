# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Command execution utilities."""

import os
import subprocess
import sys
import threading
import time
from typing import List, Optional, Callable, Any
from functools import wraps

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from .logger import SetupLogger
from .errors import NetworkError, CommandNotFoundError, PermissionError, PackageManagerError

console = Console()


def retry_on_network_error(max_attempts: int = 3, backoff_factor: float = 1.0):
    """Decorator to retry network operations with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        backoff_factor: Base delay factor for exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (subprocess.CalledProcessError, NetworkError, OSError) as e:
                    last_exception = e

                    # Don't retry on permission errors or command not found
                    if isinstance(e, (CommandNotFoundError, PermissionError)):
                        raise

                    # Don't retry on the last attempt
                    if attempt == max_attempts - 1:
                        break

                    # Calculate backoff delay: 1s, 2s, 4s...
                    delay = backoff_factor * (2 ** attempt)
                    console.print(f"[yellow]⚠[/yellow] Network operation failed, retrying in {delay}s... ({attempt + 1}/{max_attempts})")

                    time.sleep(delay)

            # If we get here, all retries failed
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


class CommandRunner:
    """Handles command execution with proper error handling and logging."""
    
    def __init__(self, logger: SetupLogger):
        self.logger = logger
        self.console = console
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=True
        )
    
    def _check_sudo_available(self) -> bool:
        """Check if sudo is available and can be used."""
        try:
            result = subprocess.run(
                ["sudo", "-n", "true"],
                capture_output=True,
                timeout=2
            )
            # If -n (non-interactive) works, we have passwordless sudo
            if result.returncode == 0:
                return True
            # Otherwise, check if sudo exists
            subprocess.run(["which", "sudo"], check=True, capture_output=True, timeout=1)
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _is_network_command(self, command: List[str]) -> bool:
        """Check if command is network-related (should be retried)."""
        cmd_str = " ".join(command).lower()
        return any(network_indicator in cmd_str for network_indicator in [
            "curl", "wget", "apt update", "apt-get update"
        ])

    def _is_long_running_command(self, command: List[str]) -> bool:
        """Check if command is likely to take a long time (should show progress)."""
        cmd_str = " ".join(command).lower()
        return any(long_running in cmd_str for long_running in [
            "apt update", "apt install", "apt-get update", "apt-get install",
            "curl", "wget", "git clone"
        ])

    @retry_on_network_error(max_attempts=3, backoff_factor=1.0)
    def _run_with_retry(self,
                       command: List[str],
                       check: bool = True,
                       capture_output: bool = False,
                       text: bool = True,
                       stdin=None,
                       env=None) -> subprocess.CompletedProcess:
        """Run command with retry logic for network operations."""
        if capture_output:
            return subprocess.run(
                command,
                check=check,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=text,
                env=env
            )
        else:
            return subprocess.run(
                command,
                check=check,
                text=text,
                stdin=stdin,
                env=env
            )

    def run(
        self,
        command: List[str],
        check: bool = True,
        capture_output: bool = False,
        sudo: bool = False,
        description: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """
        Run a command with proper error handling.
        
        Args:
            command: Command to run as list of strings
            check: Raise exception on non-zero exit code
            capture_output: Capture stdout/stderr
            sudo: Prepend sudo to command
            description: Human-readable description for progress
            
        Returns:
            CompletedProcess object
            
        Raises:
            subprocess.CalledProcessError: If check=True and command fails
        """
        if sudo:
            # Check if sudo is available
            if not self._check_sudo_available():
                raise RuntimeError(
                    "sudo is required but not available or not configured. "
                    "Please ensure sudo is installed and you have the necessary permissions."
                )
            
            # Check if passwordless sudo is available
            sudo_check = subprocess.run(
                ["sudo", "-n", "true"],
                capture_output=True,
                timeout=2
            )
            
            if sudo_check.returncode != 0:
                # Sudo requires password - inform user
                self.console.print(
                    "[yellow]⚠[/yellow] [bold]sudo password required[/bold] - "
                    "You may be prompted for your password."
                )
                self.console.print("[dim]If the command appears stuck, enter your sudo password in the terminal.[/dim]")
            
            command = ["sudo"] + command
        
        # Add quiet flags for apt commands to reduce noise
        # Find apt command position (could be at index 0 or 1 if sudo was prepended)
        apt_idx = None
        if command[0] == "apt":
            apt_idx = 0
        elif len(command) > 1 and command[1] == "apt":
            apt_idx = 1
        
        is_apt_command = apt_idx is not None
        
        if is_apt_command:
            # Add -qq (very quiet) flag to apt commands to suppress verbose output
            # This suppresses "Reading package lists..." messages completely
            if "-q" not in command and "-qq" not in command and "-qqq" not in command:
                if "update" in command:
                    # Insert -qq after "apt" (at apt_idx + 1) for very quiet output
                    command.insert(apt_idx + 1, "-qq")
                elif "install" in command:
                    # Insert -qq after "install" for very quiet output
                    install_idx = command.index("install")
                    command.insert(install_idx + 1, "-qq")
            # Suppress apt CLI warnings by redirecting status messages
            # Add -o option to suppress the warning
            if "-o" not in command:
                # Find where to insert the option (after apt/apt-get)
                option_idx = apt_idx + 1
                # Insert after any existing flags
                while option_idx < len(command) and command[option_idx].startswith("-"):
                    option_idx += 1
                command.insert(option_idx, "-o")
                command.insert(option_idx + 1, "APT::Status-Fd=/dev/null")
        
        cmd_str = " ".join(command)
        self.logger.log("info", f"CMD: {cmd_str}")
        
        if description:
            self.console.print(f"[dim]→ {description}[/dim]")
        
        # Prepare environment for apt commands to suppress warnings
        env = os.environ.copy()
        if is_apt_command:
            env["DEBIAN_FRONTEND"] = "noninteractive"
            env["APT_LISTCHANGES_FRONTEND"] = "none"

        # Show progress bar for long-running commands
        show_progress = self._is_long_running_command(command) and not capture_output
        progress_task = None

        if show_progress:
            progress_description = description or f"Running: {command[0]}"
            progress_task = self.progress.add_task(progress_description, total=None)
            self.progress.start()

        try:
            # For sudo commands, handle output based on command type
            if sudo and not capture_output:
                # For apt commands, capture output for logging but suppress console output
                # The -qq flag suppresses most output, we'll only show errors
                if is_apt_command:
                    # Use Popen with real-time reading to prevent hanging
                    # Capture output for logging but suppress console output
                    # Redirect stderr to stdout and filter warnings
                    process = subprocess.Popen(
                        command,
                        text=True,
                        stdin=sys.stdin,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Merge stderr into stdout
                        bufsize=0,  # Unbuffered
                        env=env  # Use modified environment
                    )
                    
                    # Read output in real-time to prevent hanging
                    output_lines = []
                    error_lines = []
                    
                    def read_output():
                        for line in process.stdout:
                            line = line.rstrip()
                            if line:
                                # Filter out apt CLI interface warnings completely
                                if "apt does not have a stable CLI interface" in line.lower():
                                    continue
                                output_lines.append(line)
                                # Log to file immediately (warnings filtered out)
                                self.logger.log("info", line)
                                # Check if it's an error/warning for console display
                                line_lower = line.lower()
                                if any(word in line_lower for word in ["error", "failed", "warning", "cannot", "unable", "e:"]):
                                    # Skip the apt CLI warning
                                    if "apt does not have a stable CLI interface" not in line_lower:
                                        error_lines.append(line)
                    
                    # Read output in a thread to prevent blocking
                    output_thread = threading.Thread(target=read_output, daemon=True)
                    output_thread.start()
                    
                    # Wait for process to complete
                    returncode = process.wait()
                    output_thread.join(timeout=1)  # Wait for output reading to finish
                    
                    # Show errors/warnings on console
                    if error_lines:
                        for line in error_lines:
                            self.console.print(f"[dim red]{line}[/dim red]")
                    
                    # Create CompletedProcess-like result
                    result = subprocess.CompletedProcess(
                        command,
                        returncode,
                        '\n'.join(output_lines),
                        None
                    )
                    
                    if check and returncode != 0:
                        raise subprocess.CalledProcessError(returncode, command, result.stdout)
                else:
                    # For non-apt commands, show output normally
                    if self._is_network_command(command):
                        result = self._run_with_retry(
                            command,
                            check=check,
                            text=True,
                            stdin=sys.stdin,  # Ensure stdin is connected for password prompts
                            env=env
                        )
                    else:
                        result = subprocess.run(
                            command,
                            check=check,
                            text=True,
                            stdin=sys.stdin,  # Ensure stdin is connected for password prompts
                            env=env
                        )
            elif capture_output:
                # When capturing output, merge stderr into stdout
                if self._is_network_command(command):
                    result = self._run_with_retry(
                        command,
                        check=check,
                        capture_output=True,
                        env=env
                    )
                else:
                    result = subprocess.run(
                        command,
                        check=check,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        env=env
                    )
            else:
                if self._is_network_command(command):
                    result = self._run_with_retry(
                        command,
                        check=check,
                        text=True,
                        env=env
                    )
                else:
                    result = subprocess.run(
                        command,
                        check=check,
                        text=True,
                        env=env
                    )
            return result
        except subprocess.TimeoutExpired as e:
            if self._is_network_command(command):
                raise NetworkError(
                    f"Network request timed out: {cmd_str}",
                    url=next((arg for arg in command if arg.startswith(('http://', 'https://'))), None)
                ) from e
            else:
                error_msg = f"Command timed out: {cmd_str}"
                self.logger.log("error", error_msg)
                raise RuntimeError(error_msg) from e
        except subprocess.CalledProcessError as e:
            # Handle specific error cases
            if self._is_network_command(command):
                raise NetworkError(
                    f"Network request failed: {cmd_str} (exit code: {e.returncode})",
                    url=next((arg for arg in command if arg.startswith(('http://', 'https://'))), None)
                ) from e
            elif sudo and e.returncode == 1:
                # Likely a sudo permission issue
                raise PermissionError(
                    f"Permission denied running: {cmd_str}",
                    cmd_str
                ) from e
            elif "apt" in cmd_str.lower() and "lock" in str(e.stderr or "").lower():
                raise PackageManagerError(
                    f"Package manager is locked: {cmd_str}",
                    None
                ) from e
            else:
                error_msg = f"Command failed: {cmd_str}\nExit code: {e.returncode}"
                if e.stdout:
                    error_msg += f"\nOutput: {e.stdout}"
                if e.stderr:
                    error_msg += f"\nStderr: {e.stderr}"

                self.logger.log("error", error_msg)
                raise
        except FileNotFoundError as e:
            raise CommandNotFoundError(command[0]) from e
        except Exception as e:
            error_msg = f"Unexpected error running command: {cmd_str}\n{str(e)}"
            self.logger.log("error", error_msg)
            raise
        finally:
            # Stop progress bar if it was started
            if show_progress and progress_task is not None:
                self.progress.stop()


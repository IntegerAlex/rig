# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Command execution utilities."""

import os
import subprocess
import sys
import threading
from typing import List, Optional

from rich.console import Console

from .logger import SetupLogger

console = Console()


class CommandRunner:
    """Handles command execution with proper error handling and logging."""
    
    def __init__(self, logger: SetupLogger):
        self.logger = logger
        self.console = console
    
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
                    result = subprocess.run(
                        command,
                        check=check,
                        text=True,
                        stdin=sys.stdin,  # Ensure stdin is connected for password prompts
                        env=env
                    )
            elif capture_output:
                # When capturing output, merge stderr into stdout
                result = subprocess.run(
                    command,
                    check=check,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
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
            error_msg = f"Command timed out: {cmd_str}"
            self.logger.log("error", error_msg)
            raise RuntimeError(error_msg) from e
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {cmd_str}\nExit code: {e.returncode}"
            if e.stdout:
                error_msg += f"\nOutput: {e.stdout}"
            if e.stderr:
                error_msg += f"\nStderr: {e.stderr}"
            
            self.logger.log("error", error_msg)
            raise
        except FileNotFoundError as e:
            error_msg = f"Command not found: {command[0]}"
            self.logger.log("error", error_msg)
            raise RuntimeError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error running command: {cmd_str}\n{str(e)}"
            self.logger.log("error", error_msg)
            raise


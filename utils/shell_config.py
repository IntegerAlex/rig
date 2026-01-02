# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
"""Shell configuration utilities for automatic PATH setup."""

import os
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def detect_shell() -> str:
    """Detect the current user's shell.

    Returns:
        'bash' or 'zsh', or 'unknown' if cannot determine
    """
    # First, try to get from $SHELL environment variable
    shell_env = os.environ.get('SHELL', '').lower()
    if 'zsh' in shell_env:
        return 'zsh'
    elif 'bash' in shell_env:
        return 'bash'

    # Fallback: check /etc/passwd for current user
    try:
        import pwd
        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        shell_path = user_info.pw_shell.lower()

        if 'zsh' in shell_path:
            return 'zsh'
        elif 'bash' in shell_path:
            return 'bash'
    except (ImportError, KeyError, OSError):
        pass

    # If we can't determine, assume bash (most common)
    return 'bash'


def get_shell_config_file(shell: str) -> Optional[Path]:
    """Get the path to the shell configuration file.

    Args:
        shell: 'bash' or 'zsh'

    Returns:
        Path to .bashrc or .zshrc, or None if not found
    """
    home = Path.home()

    if shell == 'zsh':
        # Check for .zshrc first, then .zprofile, then .zshenv
        for config_file in ['.zshrc', '.zprofile', '.zshenv']:
            config_path = home / config_file
            if config_path.exists():
                return config_path
        # If none exist, use .zshrc
        return home / '.zshrc'
    elif shell == 'bash':
        # Check for .bashrc first, then .bash_profile, then .profile
        for config_file in ['.bashrc', '.bash_profile', '.profile']:
            config_path = home / config_file
            if config_path.exists():
                return config_path
        # If none exist, use .bashrc
        return home / '.bashrc'

    return None


def add_to_path(config_file: Path, path_to_add: str) -> bool:
    """Safely add a path to the shell configuration file.

    Args:
        config_file: Path to the shell config file (.bashrc or .zshrc)
        path_to_add: The path to add to PATH

    Returns:
        True if path was added, False if already present or error occurred
    """
    try:
        # Read current content
        if config_file.exists():
            content = config_file.read_text()
        else:
            content = ""

        # Check if PATH export already exists
        path_export = f'export PATH="{path_to_add}:$PATH"'
        if path_export in content:
            console.print(f"[dim]→ PATH entry already exists in {config_file.name}[/dim]")
            return False

        # Also check for alternative formats
        alt_formats = [
            f'export PATH="{path_to_add}:\\$PATH"',
            f'export PATH={path_to_add}:$PATH',
            f'export PATH={path_to_add}:\\$PATH',
            f'PATH="{path_to_add}:$PATH"',
            f'PATH={path_to_add}:$PATH'
        ]

        for alt_format in alt_formats:
            if alt_format in content:
                console.print(f"[dim]→ PATH entry already exists in {config_file.name}[/dim]")
                return False

        # Add the PATH export at the end of the file
        if content and not content.endswith('\n'):
            content += '\n'

        content += f'\n# Added by rig installer\n{path_export}\n'

        # Create parent directories if needed
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Write back to file
        config_file.write_text(content)

        console.print(f"[green]✓[/green] Added PATH entry to {config_file.name}")
        return True

    except (OSError, IOError) as e:
        console.print(f"[red]✖[/red] Failed to update {config_file.name}: {e}")
        return False


def update_shell_config(install_dir: str) -> bool:
    """Main function to detect shell and update shell configuration.

    Args:
        install_dir: Directory that should be added to PATH

    Returns:
        True if configuration was updated successfully
    """
    try:
        console.print("[blue]ℹ[/blue] Configuring shell...")

        # Detect shell
        shell = detect_shell()
        console.print(f"[dim]→ Detected shell: {shell}[/dim]")

        # Get config file
        config_file = get_shell_config_file(shell)
        if not config_file:
            console.print(f"[red]✖[/red] Could not determine config file for shell: {shell}")
            return False

        console.print(f"[dim]→ Config file: {config_file.name}[/dim]")

        # Add to PATH
        path_entry = f"$HOME/{install_dir}"
        success = add_to_path(config_file, path_entry)

        if success:
            console.print(f"[green]✓[/green] Shell configuration updated")
            console.print(f"[dim]→ Run: source ~/{config_file.name} to apply changes immediately[/dim]")

        return success

    except Exception as e:
        console.print(f"[red]✖[/red] Failed to configure shell: {e}")
        return False
